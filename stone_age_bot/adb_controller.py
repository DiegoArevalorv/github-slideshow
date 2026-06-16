"""
Device controller — supports three backends auto-detected at startup:

  1. rish   (Shizuku) — best for Termux on same device, no root/PC needed
  2. adb    (ADB)     — PC with USB/WiFi, or same device with ADB connected
  3. termux — fallback screenshot via termux-screenshot (Termux:API)

Backend priority: rish > adb > error

Shizuku setup (Samsung / non-rooted, no PC):
  1. Install "Shizuku" from Play Store
  2. Open Shizuku → "Start via wireless debugging" → follow steps
  3. Shizuku app → scroll down → enable "Use Shizuku in terminal apps"
  4. In Termux: rish -c "echo ok"   ← should print "ok"

ADB setup (PC):
  adb devices   # verify device is listed
"""

import subprocess
import time
import io
import os
import tempfile
import numpy as np
from PIL import Image
from loguru import logger
import config


# ── backend detection ────────────────────────────────────────────────────────

def _detect_backend() -> str:
    # 1. Try rish (Shizuku)
    r = subprocess.run(["rish", "-c", "echo ok"],
                       capture_output=True, timeout=5)
    if r.returncode == 0 and b"ok" in r.stdout:
        logger.info("Backend: rish (Shizuku)")
        return "rish"

    # 2. Try adb
    r = subprocess.run(["adb", "shell", "echo", "ok"],
                       capture_output=True, timeout=5)
    if r.returncode == 0 and b"ok" in r.stdout:
        logger.info("Backend: adb")
        return "adb"

    raise RuntimeError(
        "No working backend found.\n"
        "Option A (recommended): Install Shizuku from Play Store,\n"
        "  start it via Wireless Debugging, then enable terminal access.\n"
        "Option B: Connect ADB from a PC: adb connect <device-ip>:PORT"
    )


_BACKEND: str | None = None


def _backend() -> str:
    global _BACKEND
    if _BACKEND is None:
        _BACKEND = _detect_backend()
    return _BACKEND


def _shell(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command via the active backend."""
    b = _backend()
    if b == "rish":
        full = ["rish", "-c", cmd]
    else:
        base = ["adb"]
        if config.ADB_DEVICE:
            base += ["-s", config.ADB_DEVICE]
        full = base + ["shell", cmd]
    logger.debug("{}: {}", b.upper(), cmd)
    return subprocess.run(full, capture_output=True, check=check)


# ── public API ────────────────────────────────────────────────────────────────

def screenshot() -> np.ndarray:
    """Return current screen as an RGB numpy array."""
    b = _backend()
    if b == "adb":
        base = ["adb"]
        if config.ADB_DEVICE:
            base += ["-s", config.ADB_DEVICE]
        result = subprocess.run(
            base + ["exec-out", "screencap", "-p"],
            capture_output=True, check=True
        )
        img = Image.open(io.BytesIO(result.stdout)).convert("RGB")
        return np.array(img)

    # rish backend — save screencap to a temp file readable by Termux
    tmp = "/data/local/tmp/_bot_screen.png"
    _shell(f"screencap -p {tmp}")
    # copy out via rish cat
    result = subprocess.run(
        ["rish", "-c", f"cat {tmp}"],
        capture_output=True, check=True
    )
    img = Image.open(io.BytesIO(result.stdout)).convert("RGB")
    return np.array(img)


def tap(x: int, y: int) -> None:
    sx = int(x * config.SCALE_X)
    sy = int(y * config.SCALE_Y)
    _shell(f"input tap {sx} {sy}")


def rapid_tap(x: int, y: int,
              count: int = config.GOLDEN_BACKPACK_TAP_COUNT,
              delay: float = config.GOLDEN_BACKPACK_TAP_DELAY_S) -> None:
    """Fire `count` taps as fast as possible — used for golden backpack event."""
    sx = int(x * config.SCALE_X)
    sy = int(y * config.SCALE_Y)
    logger.info("Rapid tap ({},{}) × {}", sx, sy, count)

    # Build one shell command that loops on-device — much faster than
    # one subprocess call per tap because it avoids the rish/adb round-trip.
    cmd = f"for i in $(seq 1 {count}); do input tap {sx} {sy}; done"
    _shell(cmd, check=False)


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
    sx1, sy1 = int(x1 * config.SCALE_X), int(y1 * config.SCALE_Y)
    sx2, sy2 = int(x2 * config.SCALE_X), int(y2 * config.SCALE_Y)
    _shell(f"input swipe {sx1} {sy1} {sx2} {sy2} {duration_ms}")


def press_back() -> None:
    _shell("input keyevent 4")


def device_info() -> str:
    result = _shell("getprop ro.product.model", check=False)
    return result.stdout.decode().strip()
