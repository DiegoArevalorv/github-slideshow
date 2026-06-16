"""
ADB wrapper — works both from a PC and from Termux on the same device.

On-device Termux setup (Android 11+, no PC needed):
  pkg install android-tools
  # Enable Developer Options → Wireless Debugging → Pair device
  adb pair 127.0.0.1:<PAIR_PORT> <PAIR_CODE>
  adb connect 127.0.0.1:<DEBUG_PORT>

PC setup:
  adb devices   # verify device is listed
"""

import subprocess
import time
import io
import numpy as np
from PIL import Image
from loguru import logger
import config


def _run(cmd: list[str], check=True) -> subprocess.CompletedProcess:
    base = ["adb"]
    if config.ADB_DEVICE:
        base += ["-s", config.ADB_DEVICE]
    full_cmd = base + cmd
    logger.debug("ADB: {}", " ".join(full_cmd))
    return subprocess.run(full_cmd, capture_output=True, check=check)


def screenshot() -> np.ndarray:
    """Return current screen as an RGB numpy array."""
    result = _run(["exec-out", "screencap", "-p"])
    img = Image.open(io.BytesIO(result.stdout)).convert("RGB")
    return np.array(img)


def tap(x: int, y: int) -> None:
    """Single tap at (x, y), scaled to device resolution."""
    sx = int(x * config.SCALE_X)
    sy = int(y * config.SCALE_Y)
    _run(["shell", "input", "tap", str(sx), str(sy)])


def rapid_tap(x: int, y: int,
              count: int = config.GOLDEN_BACKPACK_TAP_COUNT,
              delay: float = config.GOLDEN_BACKPACK_TAP_DELAY_S) -> None:
    """Fire `count` taps as fast as possible — used for golden backpack event."""
    sx = int(x * config.SCALE_X)
    sy = int(y * config.SCALE_Y)
    logger.info("Rapid tap x={} y={} × {}", sx, sy, count)
    for _ in range(count):
        _run(["shell", "input", "tap", str(sx), str(sy)], check=False)
        time.sleep(delay)


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
    sx1, sy1 = int(x1 * config.SCALE_X), int(y1 * config.SCALE_Y)
    sx2, sy2 = int(x2 * config.SCALE_X), int(y2 * config.SCALE_Y)
    _run(["shell", "input", "swipe",
          str(sx1), str(sy1), str(sx2), str(sy2), str(duration_ms)])


def press_back() -> None:
    _run(["shell", "input", "keyevent", "4"])


def device_info() -> str:
    result = _run(["shell", "getprop", "ro.product.model"], check=False)
    return result.stdout.decode().strip()
