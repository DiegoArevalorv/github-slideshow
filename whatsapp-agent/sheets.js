// ============================================================
// Módulo de Google Sheets — Registro de interacciones
// Columnas: Fecha | Subscriber ID | Nombre | Teléfono |
//           Tipo de Negocio | Mensaje | Respuesta Claude |
//           Plan Mencionado | Estado
// ============================================================

const { google } = require('googleapis');

// ← PONER TU ID DE GOOGLE SHEET aquí (es el código largo en la URL de tu hoja)
// Ejemplo: https://docs.google.com/spreadsheets/d/ESTE_ES_EL_ID/edit
const SPREADSHEET_ID = process.env.GOOGLE_SHEETS_ID;

// Nombre de la hoja/pestaña dentro del documento
const NOMBRE_HOJA = 'Leads';

// ------------------------------------------------------------
// Crea el cliente autenticado de Google Sheets usando una cuenta de servicio.
// La cuenta de servicio permite que tu servidor acceda sin login manual.
// ⚠️ ACCIÓN REQUERIDA: Ver SETUP.md para crear tu cuenta de servicio.
// ------------------------------------------------------------
function crearClienteSheets() {
  // Las credenciales se leen desde la variable de entorno GOOGLE_SERVICE_ACCOUNT_JSON
  // ← PONER TU API KEY: Pega el contenido del archivo JSON de tu cuenta de servicio
  //    en la variable de entorno GOOGLE_SERVICE_ACCOUNT_JSON
  const credenciales = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT_JSON);

  const auth = new google.auth.GoogleAuth({
    credentials: credenciales,
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
  });

  return google.sheets({ version: 'v4', auth });
}

// ------------------------------------------------------------
// Registra una interacción completa en Google Sheets
// Se llama después de cada respuesta de Claude
// ------------------------------------------------------------
async function registrarInteraccion(datos) {
  const {
    fecha,
    subscriberId,
    nombre,
    telefono,
    tipoNegocio,
    mensaje,
    respuestaClaude,
    planMencionado,
    estado,
  } = datos;

  try {
    const sheets = crearClienteSheets();

    // Fila de datos en el mismo orden que los encabezados
    const fila = [
      fecha,           // Fecha y hora del mensaje
      subscriberId,    // ID del suscriptor en Manychat
      nombre,          // Nombre del prospecto
      telefono,        // Teléfono del prospecto
      tipoNegocio,     // Tipo de negocio (restaurante, tienda, etc.)
      mensaje,         // Mensaje que envió el usuario
      respuestaClaude, // Respuesta generada por Sofía (Claude)
      planMencionado,  // Qué plan se mencionó en la conversación
      estado,          // Estado del lead (Nuevo, Interesado, Cerrado, etc.)
    ];

    await sheets.spreadsheets.values.append({
      spreadsheetId: SPREADSHEET_ID,
      range: `${NOMBRE_HOJA}!A:I`, // Columnas A hasta I
      valueInputOption: 'USER_ENTERED',
      requestBody: {
        values: [fila],
      },
    });

    console.log(`[Sheets] Interacción registrada para: ${nombre} (${subscriberId})`);
  } catch (error) {
    // El error en Sheets no debe detener la respuesta al usuario
    console.error('[Sheets] Error al registrar interacción:', error.message);
  }
}

// ------------------------------------------------------------
// Crea los encabezados en la hoja si está vacía
// Ejecutar una sola vez al iniciar el servidor por primera vez
// ------------------------------------------------------------
async function inicializarHoja() {
  try {
    const sheets = crearClienteSheets();

    // Verificar si ya tiene encabezados
    const respuesta = await sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET_ID,
      range: `${NOMBRE_HOJA}!A1:I1`,
    });

    const filas = respuesta.data.values;

    // Si la primera fila está vacía, agregar los encabezados
    if (!filas || filas.length === 0) {
      await sheets.spreadsheets.values.update({
        spreadsheetId: SPREADSHEET_ID,
        range: `${NOMBRE_HOJA}!A1:I1`,
        valueInputOption: 'USER_ENTERED',
        requestBody: {
          values: [
            [
              'Fecha',
              'Subscriber ID',
              'Nombre',
              'Teléfono',
              'Tipo de Negocio',
              'Mensaje',
              'Respuesta Claude',
              'Plan Mencionado',
              'Estado',
            ],
          ],
        },
      });
      console.log('[Sheets] Encabezados creados en la hoja:', NOMBRE_HOJA);
    }
  } catch (error) {
    console.error('[Sheets] Error al inicializar hoja:', error.message);
  }
}

module.exports = { registrarInteraccion, inicializarHoja };
