// ============================================================
// TASK 3 — Sistema de Memoria de Conversaciones
// Almacena el historial por subscriber_id (hasta 10 mensajes)
// Limpia conversaciones inactivas después de 24 horas
// ============================================================

// Objeto en memoria que guarda el historial de cada usuario
// Estructura: { "subscriber_id": { messages: [...], lastActivity: Date } }
// ⚠️ NOTA: Este almacenamiento es temporal — se borra si el servidor se reinicia.
//    Para producción con múltiples usuarios, considera usar Redis o una base de datos.
const conversaciones = {};

// Máximo de mensajes por conversación (controla el costo de tokens en Claude)
const MAX_MENSAJES = 10;

// Tiempo máximo de inactividad antes de borrar el historial (24 horas en milisegundos)
const LIMITE_INACTIVIDAD_MS = 24 * 60 * 60 * 1000;

// ------------------------------------------------------------
// Obtiene el historial de mensajes de un usuario
// Retorna un array de { role: "user"|"assistant", content: "..." }
// ------------------------------------------------------------
function getHistorial(subscriberId) {
  if (!conversaciones[subscriberId]) {
    return [];
  }
  return conversaciones[subscriberId].messages;
}

// ------------------------------------------------------------
// Agrega un mensaje al historial de un usuario
// Si el historial supera MAX_MENSAJES, elimina los más antiguos
// ------------------------------------------------------------
function agregarMensaje(subscriberId, role, content) {
  // Crear entrada si no existe
  if (!conversaciones[subscriberId]) {
    conversaciones[subscriberId] = {
      messages: [],
      lastActivity: new Date(),
    };
  }

  // Agregar el nuevo mensaje
  conversaciones[subscriberId].messages.push({ role, content });

  // Actualizar la marca de tiempo de última actividad
  conversaciones[subscriberId].lastActivity = new Date();

  // Mantener solo los últimos MAX_MENSAJES para controlar costos de tokens
  if (conversaciones[subscriberId].messages.length > MAX_MENSAJES) {
    // Eliminar los mensajes más antiguos, conservar los más recientes
    conversaciones[subscriberId].messages = conversaciones[subscriberId].messages.slice(-MAX_MENSAJES);
  }
}

// ------------------------------------------------------------
// Limpia el historial de un usuario (reinicio de conversación)
// Se activa cuando el usuario escribe "reiniciar" o "empezar de nuevo"
// ------------------------------------------------------------
function limpiarHistorial(subscriberId) {
  delete conversaciones[subscriberId];
  console.log(`[Memoria] Historial eliminado para subscriber: ${subscriberId}`);
}

// ------------------------------------------------------------
// Revisa y elimina conversaciones que llevan más de 24 horas inactivas
// Esta función se ejecuta automáticamente cada hora
// ------------------------------------------------------------
function limpiarInactivos() {
  const ahora = new Date();
  let eliminados = 0;

  for (const subscriberId in conversaciones) {
    const ultimaActividad = conversaciones[subscriberId].lastActivity;
    const tiempoInactivo = ahora - ultimaActividad;

    if (tiempoInactivo > LIMITE_INACTIVIDAD_MS) {
      delete conversaciones[subscriberId];
      eliminados++;
    }
  }

  if (eliminados > 0) {
    console.log(`[Memoria] Limpieza automática: ${eliminados} conversación(es) inactiva(s) eliminada(s)`);
  }
}

// Ejecutar limpieza automática cada hora (3,600,000 milisegundos)
setInterval(limpiarInactivos, 60 * 60 * 1000);

// ------------------------------------------------------------
// Detecta si el mensaje del usuario es una palabra de reinicio
// ------------------------------------------------------------
function esPalabraDeReinicio(mensaje) {
  const palabrasDeReinicio = ['reiniciar', 'empezar de nuevo', 'reset', 'comenzar de nuevo', 'borrar historial'];
  const mensajeLower = mensaje.toLowerCase().trim();
  return palabrasDeReinicio.some((palabra) => mensajeLower.includes(palabra));
}

module.exports = {
  getHistorial,
  agregarMensaje,
  limpiarHistorial,
  esPalabraDeReinicio,
};
