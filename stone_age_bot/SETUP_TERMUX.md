# Configuración en Termux (Android, sin PC)

Este bot corre **directamente en tu teléfono** usando Termux.
No necesitas una computadora.

---

## Requisitos

- Android 11 o superior (para ADB inalámbrico local)
- App **Termux** (desde F-Droid, no la versión desactualizada de Play Store)
- App **Termux:API** (desde F-Droid, mismo autor)

---

## Paso 1 — Activar las Opciones de Desarrollador

1. Ve a **Ajustes → Acerca del teléfono**
2. Toca **Número de compilación** 7 veces
3. Regresa a **Ajustes → Sistema → Opciones de desarrollador**
4. Activa **Depuración inalámbrica** (Wireless debugging)

---

## Paso 2 — Instalar dependencias en Termux

```bash
# Actualizar paquetes
pkg update && pkg upgrade -y

# Instalar Python, ADB y compiladores necesarios para OpenCV
pkg install -y python android-tools clang libpng libjpeg-turbo

# Instalar dependencias Python
pip install opencv-python numpy Pillow schedule loguru
```

> **Nota**: `opencv-python` puede tardar varios minutos en compilar.
> Si falla, prueba con `pip install opencv-python-headless`.

---

## Paso 3 — Conectar ADB al mismo dispositivo

Abre **Depuración inalámbrica** en Ajustes. Verás dos opciones:

### 3a. Emparejar dispositivo (solo la primera vez)

1. Toca **Vincular dispositivo con código**
2. Anota el **Puerto** y el **Código de vinculación**
3. En Termux:
   ```bash
   adb pair 127.0.0.1:PUERTO_DE_VINCULACION CODIGO
   ```

### 3b. Conectar

1. En la pantalla de Depuración inalámbrica anota el **Puerto** principal
2. En Termux:
   ```bash
   adb connect 127.0.0.1:PUERTO_PRINCIPAL
   ```
3. Verifica:
   ```bash
   adb devices
   # Debe mostrar: 127.0.0.1:PUERTO  device
   ```

---

## Paso 4 — Clonar el bot y configurar

```bash
# Clonar el repositorio
pkg install -y git
git clone https://github.com/diegoarevalorv/github-slideshow.git
cd github-slideshow/stone_age_bot
```

Edita `config.py` si tu teléfono no es resolución 1080×1920:

```python
DEVICE_WIDTH  = 1080   # cambia al ancho real de tu pantalla
DEVICE_HEIGHT = 1920   # cambia al alto real de tu pantalla
SCALE_X = real_width  / 1080
SCALE_Y = real_height / 1920
```

---

## Paso 5 — Calibrar coordenadas

```bash
python calibrate.py
```

- Usa la opción `s` para tomar una captura de pantalla
- Abre `calibration_screen.png`, mide las coordenadas de cada botón
- Actualiza el diccionario `COORDS` en `config.py`
- Usa la opción `t` para probar que los toques llegan al lugar correcto

---

## Paso 6 — Capturar imágenes de plantilla

1. Abre **Stone Age: Idle Adventure**
2. En Termux (otra sesión), ejecuta `python calibrate.py` → `s`
3. Con cualquier editor de imágenes (en la galería o usando `convert` de ImageMagick), recorta cada elemento:
   - El punto rojo de notificación
   - El ícono de la mochila dorada
   - Los botones "Reclamar Todo", "Subir Nivel", "Desmantelar"
4. Guarda los recortes en `stone_age_bot/templates/` con los nombres indicados en `templates/README.md`

---

## Paso 7 — Ejecutar el bot

```bash
# Prueba de un solo ciclo (recomendado para verificar primero)
python main.py --once --debug

# Ejecución continua (ciclo cada 4 horas)
python main.py

# Mantener corriendo aunque cierres Termux (usa tmux o nohup)
pkg install tmux
tmux new -s bot
python main.py
# Ctrl+B luego D para desconectar de tmux sin matar el proceso
```

---

## Solución de problemas

| Error | Solución |
|---|---|
| `adb: command not found` | `pkg install android-tools` |
| `error: no devices` | Repite el paso 3b; el puerto cambia cada vez que reinicias Wireless Debugging |
| `import cv2` falla | `pip install opencv-python-headless` |
| Template no encontrado | Recaptura la plantilla; ajusta `MATCH_THRESHOLD` a 0.70 en `config.py` |
| El toque llega al lugar equivocado | Ajusta `SCALE_X`/`SCALE_Y` o recalibra las coordenadas |

---

## Notas de seguridad

- Este bot automatiza **solo tu propia cuenta**
- Úsalo con moderación para no arriesgarte a bans por comportamiento inusual
- El juego es idle — intervalos de 4h son más que suficientes y difíciles de detectar
