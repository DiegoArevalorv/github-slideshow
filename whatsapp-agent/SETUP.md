# AgenteIAWhatsAppSV — Guía de Setup y Costos

## Archivos del proyecto

```
whatsapp-agent/
├── server.js          ← Servidor principal (webhook handler)
├── sofia-prompt.js    ← System prompt de Sofía (Task 1)
├── memory.js          ← Memoria de conversaciones (Task 3)
├── sheets.js          ← Integración Google Sheets
├── package.json       ← Dependencias de Node.js
├── .env.example       ← Plantilla de variables de entorno
└── SETUP.md           ← Esta guía
```

---

## TASK 4 — Calculadora de Costos Claude API

> Basado en precios de **claude-sonnet-4-6**: ~$3/M tokens entrada, ~$15/M tokens salida.
> Verificar precios actuales en: https://www.anthropic.com/pricing

### Supuestos por mensaje
| Componente               | Tokens estimados |
|--------------------------|-----------------|
| System prompt (Sofía)    | ~500 tokens     |
| Historial (10 mensajes)  | ~750 tokens     |
| Mensaje del usuario      | ~50 tokens      |
| **Total entrada**        | **~1,300 tokens** |
| Respuesta de Sofía       | ~150 tokens     |

**Costo por mensaje:**
- Entrada: 1,300 × $0.000003 = **$0.0039**
- Salida: 150 × $0.000015 = **$0.0023**
- **Total por mensaje: ~$0.006**

---

### Escenario 1 — 50 clientes activos / 20 mensajes día

| Concepto                   | Valor        |
|----------------------------|-------------|
| Mensajes al mes            | 30,000      |
| Costo API Claude/mes       | **~$182**   |
| Ingreso (todos en Básico $49) | $2,450   |
| Ingreso (todos en Pro $99)  | $4,950     |
| Ingreso (todos en Premium $179) | $8,950 |
| **Margen neto (Plan Básico)** | **$2,268 (93%)** |
| **Margen neto (Plan Pro)**  | **$4,768 (96%)** |
| **Margen neto (Plan Premium)** | **$8,768 (98%)** |

---

### Escenario 2 — 100 clientes activos / 20 mensajes día

| Concepto                   | Valor        |
|----------------------------|-------------|
| Mensajes al mes            | 60,000      |
| Costo API Claude/mes       | **~$364**   |
| Ingreso (todos en Básico $49) | $4,900   |
| Ingreso (todos en Pro $99)  | $9,900     |
| Ingreso (todos en Premium $179) | $17,900 |
| **Margen neto (Plan Básico)** | **$4,536 (93%)** |
| **Margen neto (Plan Pro)**  | **$9,536 (96%)** |
| **Margen neto (Plan Premium)** | **$17,536 (98%)** |

---

### Escenario 3 — 200 clientes activos / 20 mensajes día

| Concepto                   | Valor        |
|----------------------------|-------------|
| Mensajes al mes            | 120,000     |
| Costo API Claude/mes       | **~$729**   |
| Ingreso (todos en Básico $49) | $9,800   |
| Ingreso (todos en Pro $99)  | $19,800    |
| Ingreso (todos en Premium $179) | $35,800 |
| **Margen neto (Plan Básico)** | **$9,071 (93%)** |
| **Margen neto (Plan Pro)**  | **$19,071 (96%)** |
| **Margen neto (Plan Premium)** | **$35,071 (98%)** |

> 💡 **Consejo:** Activa **Prompt Caching** en Claude API para reducir el costo
> del system prompt hasta un 90%. Esto puede bajar tu costo total ~35%.
> Ver: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

---

## TASK 5 — Checklist de Setup (paso a paso)

### PASO 1 — Obtener tu Claude API Key
⚠️ ACCIÓN REQUERIDA

1. Ve a: https://console.anthropic.com/settings/keys
2. Crea una cuenta o inicia sesión
3. Haz clic en **"Create Key"**
4. Copia la clave (empieza con `sk-ant-...`)
5. Pégala en tu archivo `.env` como `CLAUDE_API_KEY=sk-ant-...`

> 💳 Requiere tarjeta de crédito. Carga mínima: $5 USD.

---

### PASO 2 — Configurar el Webhook en Manychat
⚠️ ACCIÓN REQUERIDA

1. Ve a: https://manychat.com → tu bot de WhatsApp
2. Crea un nuevo **Flow** (o edita uno existente)
3. Agrega un bloque **"External Request"**
4. Configura:
   - **Method:** POST
   - **URL:** `https://TU-SERVIDOR.com/webhook` ← (del Paso 3)
   - **Headers:** `Content-Type: application/json`
   - **Body (JSON):**
     ```json
     {
       "subscriber_id": "{{subscriber.id}}",
       "name": "{{subscriber.first_name}} {{subscriber.last_name}}",
       "phone": "{{subscriber.phone}}",
       "last_message": "{{last_text_input}}",
       "business_type": "{{custom.tipo_negocio}}"
     }
     ```
5. En **"Response"**, selecciona **"Use Response as Bot Reply"**

---

### PASO 3 — Desplegar el servidor (GRATIS con Render)
⚠️ ACCIÓN REQUERIDA

**Opción A: Render.com (recomendada — gratis)**

1. Ve a: https://render.com → crea cuenta gratis
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Root Directory:** `whatsapp-agent`
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
   - **Plan:** Free
5. En **"Environment Variables"**, agrega:
   - `CLAUDE_API_KEY` = tu clave de Claude
   - `GOOGLE_SHEETS_ID` = ID de tu hoja
   - `GOOGLE_SERVICE_ACCOUNT_JSON` = contenido del JSON de cuenta de servicio
6. Haz clic en **"Create Web Service"**
7. Copia la URL que te da Render (ej: `https://sofia-agent.onrender.com`)
8. Esa URL es la que usas en el Paso 2 de Manychat

> ⏱️ El plan gratis de Render "duerme" el servidor después de 15 min sin actividad.
> El primer mensaje puede tardar ~30 segundos. Para evitar esto: actualiza a $7/mes.

**Opción B: Railway.app ($5/mes, más rápido)**
1. Ve a: https://railway.app
2. New Project → Deploy from GitHub
3. Agrega las mismas variables de entorno

---

### PASO 4 — Conectar Google Sheets API
⚠️ ACCIÓN REQUERIDA

**Parte A: Crear el proyecto y cuenta de servicio**
1. Ve a: https://console.cloud.google.com
2. Crea un nuevo proyecto (ej: "AgenteIAWhatsApp")
3. En el menú, ve a **APIs y Servicios** → **Biblioteca**
4. Busca **"Google Sheets API"** → Activar
5. Ve a **APIs y Servicios** → **Credenciales**
6. Haz clic en **"Crear credenciales"** → **"Cuenta de servicio"**
7. Nombre: `sofia-agent` → Crear
8. En la cuenta creada, ve a la pestaña **"Claves"**
9. Haz clic en **"Agregar clave"** → **"JSON"** → Descargar el archivo
10. Copia TODO el contenido del archivo JSON descargado

**Parte B: Crear y compartir la Google Sheet**
1. Ve a: https://sheets.google.com → Crea una nueva hoja
2. Nómbrala: **AgenteIAWhatsAppSV - Leads**
3. Crea una pestaña llamada **"Leads"**
4. Haz clic en **"Compartir"**
5. Agrega el email de tu cuenta de servicio (está en el JSON, campo `client_email`)
   - Ejemplo: `sofia-agent@tu-proyecto.iam.gserviceaccount.com`
6. Dale permisos de **Editor**
7. Copia el ID de la hoja desde la URL (el código largo entre `/d/` y `/edit`)

**Parte C: Agregar a tus variables de entorno**
- `GOOGLE_SHEETS_ID` = el ID del paso 7
- `GOOGLE_SERVICE_ACCOUNT_JSON` = TODO el contenido del archivo JSON (en una sola línea)

---

### PASO 5 — Probar el flujo completo
⚠️ ACCIÓN REQUERIDA

**Prueba local (antes de subir a Render):**
```bash
# En la carpeta whatsapp-agent/
npm install
cp .env.example .env
# Edita .env con tus credenciales reales
npm run dev

# En otra terminal, prueba con curl:
curl -X POST http://localhost:3000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "subscriber_id": "test-123",
    "name": "María García",
    "phone": "+50378901234",
    "last_message": "hola me interesa el servicio para mi restaurante"
  }'
```

**Prueba en producción:**
1. Envía un mensaje de WhatsApp al número de tu Manychat
2. Activa el Flow que creaste en el Paso 2
3. Verifica que:
   - [ ] Sofía responde en WhatsApp
   - [ ] La interacción aparece en tu Google Sheet
   - [ ] Los logs en Render muestran el mensaje recibido

**Verificar que el servidor está vivo:**
```
GET https://TU-SERVIDOR.onrender.com/health
```
Debe responder: `{"status":"ok","agente":"Sofía — AgenteIAWhatsAppSV"}`

---

## Diagrama del flujo completo

```
Lead en WhatsApp
      │
      ▼
   Manychat
(recibe mensaje)
      │
      ▼
 POST /webhook
(tu servidor en Render)
      │
      ├──► memory.js     (recupera historial)
      │
      ▼
  Claude API
 claude-sonnet-4-6
 "Sofía" genera respuesta
      │
      ├──► memory.js     (guarda intercambio)
      ├──► sheets.js     (registra en Sheets)
      │
      ▼
Respuesta JSON
(formato Manychat)
      │
      ▼
   Manychat
(envía al usuario)
      │
      ▼
 Lead en WhatsApp
 recibe respuesta
```

---

## Preguntas frecuentes

**¿Qué pasa si Claude no responde?**
El servidor envía un mensaje de error amigable al usuario y registra el error en los logs.

**¿Puedo cambiar la personalidad de Sofía?**
Sí — edita el archivo `sofia-prompt.js`. No necesitas tocar el resto del código.

**¿Cómo agrego un nuevo plan o cambio precios?**
Edita la sección "Planes disponibles" en `sofia-prompt.js`.

**¿El servidor puede manejar muchos usuarios a la vez?**
Sí — Node.js maneja concurrencia bien. El plan gratis de Render maneja hasta ~100 req/min.
