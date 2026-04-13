// ============================================================
// TASK 2 — Servidor Principal / Webhook Handler
// AgenteIAWhatsAppSV — Sofía (Claude AI Sales Agent)
//
// Flujo:
//   Manychat → POST /webhook → Claude API → respuesta a Manychat
//                                         → registro en Google Sheets
// ============================================================

require('dotenv').config();
const express = require('express');
const Anthropic = require('@anthropic-ai/sdk');

// Módulos propios del proyecto
const { getHistorial, agregarMensaje, limpiarHistorial, esPalabraDeReinicio } = require('./memory');
const { registrarInteraccion, inicializarHoja } = require('./sheets');
const SOFIA_SYSTEM_PROMPT = require('./sofia-prompt');

// ------------------------------------------------------------
// Configuración del servidor
// ------------------------------------------------------------
const app = express();
app.use(express.json());

// Puerto del servidor (Render y Railway lo asignan automáticamente)
const PUERTO = process.env.PORT || 3000;

// ------------------------------------------------------------
// Cliente de Claude API
// ← PONER TU API KEY: Crea una cuenta en https://console.anthropic.com
//   y agrega tu clave en el archivo .env como CLAUDE_API_KEY=sk-ant-...
// ------------------------------------------------------------
const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY,
});

// Modelo de Claude a usar
const MODELO_CLAUDE = 'claude-sonnet-4-6';

// Tokens máximos en la respuesta (controla el costo y el largo de los mensajes)
const MAX_TOKENS_RESPUESTA = 500;

// ------------------------------------------------------------
// Función auxiliar: detecta qué plan mencionó Sofía en su respuesta
// Esto se usa para registrar el interés del lead en Sheets
// ------------------------------------------------------------
function detectarPlanMencionado(texto) {
  const textoLower = texto.toLowerCase();
  if (textoLower.includes('premium') || textoLower.includes('179')) return 'Premium $179';
  if (textoLower.includes('profesional') || textoLower.includes('99')) return 'Profesional $99';
  if (textoLower.includes('básico') || textoLower.includes('basico') || textoLower.includes('49')) return 'Básico $49';
  return 'Ninguno';
}

// ------------------------------------------------------------
// Función auxiliar: detecta si el lead necesita escalación a humano
// ------------------------------------------------------------
function necesitaEscalacion(mensaje) {
  const frases = ['hablar con alguien', 'llamar', 'persona real', 'encargado', 'dueño', 'dueno', 'gerente', 'hablar con una persona'];
  const mensajeLower = mensaje.toLowerCase();
  return frases.some((frase) => mensajeLower.includes(frase));
}

// ============================================================
// RUTA PRINCIPAL — Webhook de Manychat
// ============================================================
// Manychat enviará un POST a esta URL cada vez que un usuario
// mande un mensaje en WhatsApp.
//
// ⚠️ ACCIÓN REQUERIDA: En Manychat, crea un "External Request"
// block y apunta la URL a: https://TU-SERVIDOR.com/webhook
// ------------------------------------------------------------
app.post('/webhook', async (req, res) => {
  // --- 1. Recibir y validar los datos de Manychat ---
  const {
    subscriber_id,
    name,
    phone,
    last_message,
    business_type, // campo opcional desde Manychat custom field
  } = req.body;

  // Validación básica — si no viene el mensaje, rechazar
  if (!subscriber_id || !last_message) {
    return res.status(400).json({ error: 'Faltan campos obligatorios: subscriber_id y last_message' });
  }

  console.log(`[Webhook] Mensaje recibido de ${name} (${subscriber_id}): "${last_message}"`);

  try {
    // --- 2. Verificar palabras de reinicio ---
    // Si el usuario quiere empezar de cero, limpiamos su historial
    if (esPalabraDeReinicio(last_message)) {
      limpiarHistorial(subscriber_id);
      const mensajeReinicio = '¡Claro que sí! Empecemos de nuevo. 😊 ¿En qué le puedo ayudar hoy?';

      // Retornar en formato Manychat Dynamic Block
      return res.json(formatearRespuestaManychat(mensajeReinicio));
    }

    // --- 3. Obtener historial de conversación ---
    const historial = getHistorial(subscriber_id);

    // Agregar el mensaje actual del usuario al historial
    historial.push({ role: 'user', content: last_message });

    // --- 4. Llamar a Claude API con el system prompt de Sofía ---
    const respuestaAPI = await anthropic.messages.create({
      model: MODELO_CLAUDE,
      max_tokens: MAX_TOKENS_RESPUESTA,
      system: SOFIA_SYSTEM_PROMPT,
      messages: historial,
    });

    const textoClaude = respuestaAPI.content[0].text;
    console.log(`[Claude] Respuesta para ${name}: "${textoClaude.substring(0, 80)}..."`);

    // --- 5. Guardar el intercambio en memoria ---
    agregarMensaje(subscriber_id, 'user', last_message);
    agregarMensaje(subscriber_id, 'assistant', textoClaude);

    // --- 6. Detectar información relevante para el CRM ---
    const planMencionado = detectarPlanMencionado(textoClaude);
    const requiereHumano = necesitaEscalacion(last_message);

    let estadoLead = 'Activo';
    if (requiereHumano) estadoLead = 'Requiere Humano';
    if (planMencionado !== 'Ninguno') estadoLead = 'Interesado';

    // --- 7. Registrar interacción en Google Sheets (en paralelo, no bloquea) ---
    registrarInteraccion({
      fecha: new Date().toLocaleString('es-SV', { timeZone: 'America/El_Salvador' }),
      subscriberId: subscriber_id,
      nombre: name || 'Desconocido',
      telefono: phone || 'No disponible',
      tipoNegocio: business_type || 'No especificado',
      mensaje: last_message,
      respuestaClaude: textoClaude,
      planMencionado,
      estado: estadoLead,
    }).catch((err) => console.error('[Sheets] Error al registrar (no crítico):', err.message));

    // --- 8. Retornar respuesta en formato Manychat Dynamic Block ---
    // Manychat leerá este JSON y enviará el mensaje al usuario en WhatsApp
    return res.json(formatearRespuestaManychat(textoClaude));

  } catch (error) {
    console.error('[Error] Fallo en el webhook:', error.message);

    // Si Claude falla, enviar mensaje de error amigable al usuario
    const mensajeError = 'Disculpe, tuve un problema técnico. ¿Puede intentarlo de nuevo en un momento? 🙏';
    return res.status(500).json(formatearRespuestaManychat(mensajeError));
  }
});

// ============================================================
// Formatea la respuesta en el formato que Manychat espera
// (Dynamic Block / External Request Response)
// ============================================================
function formatearRespuestaManychat(texto) {
  return {
    version: 'v2',
    content: {
      messages: [
        {
          type: 'text',
          text: texto,
        },
      ],
      actions: [],
      quick_replies: [],
    },
  };
}

// ============================================================
// RUTA DE SALUD — Para verificar que el servidor está corriendo
// Visita: https://TU-SERVIDOR.com/health
// ============================================================
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    agente: 'Sofía — AgenteIAWhatsAppSV',
    timestamp: new Date().toISOString(),
  });
});

// ============================================================
// Iniciar el servidor
// ============================================================
app.listen(PUERTO, async () => {
  console.log(`✅ Servidor de Sofía corriendo en puerto ${PUERTO}`);
  console.log(`   → Webhook: POST http://localhost:${PUERTO}/webhook`);
  console.log(`   → Health:  GET  http://localhost:${PUERTO}/health`);

  // Intentar inicializar la hoja de Google Sheets al arrancar
  try {
    await inicializarHoja();
    console.log('✅ Google Sheets conectado correctamente');
  } catch (error) {
    console.warn('⚠️  Google Sheets no disponible al iniciar (verificar credenciales):', error.message);
  }
});
