"""
Continuous event monitor that runs between main routine cycles.

Watches for pop-up events (golden backpack, dialogs) at a high polling rate
so the bot reacts within SCREENSHOT_INTERVAL_S seconds.
"""

import time
from loguru import logger
import adb_controller as adb
import vision
import bot_actions
import config


def watch_for_events(duration_s: float = config.EVENT_WATCH_DURATION_S) -> None:
    """
    Poll the screen for `duration_s` seconds looking for:
      - Golden Backpack pop-up  → rapid-tap immediately
      - Any stray OK / confirm dialogs → dismiss them
    """
    logger.info("Event watch started ({} s)", duration_s)
    deadline = time.time() + duration_s

    while time.time() < deadline:
        try:
            screen = adb.screenshot()
        except Exception as e:
            logger.warning("Screenshot error during event watch: {}", e)
            time.sleep(config.SCREENSHOT_INTERVAL_S)
            continue

        # ── Golden Backpack ──────────────────────────────────────────────
        backpack_loc = vision.find_template(
            screen,
            config.T_GOLDEN_BACKPACK,
            threshold=0.75,   # slightly lower threshold for fast detection
        )
        if backpack_loc:
            bot_actions.handle_golden_backpack(backpack_loc)
            # After tapping, extend watch slightly to catch the close animation
            deadline = max(deadline, time.time() + 5)

        # ── Stray OK / confirm dialogs ───────────────────────────────────
        ok_loc = vision.find_template(screen, config.T_OK_BUTTON, threshold=0.85)
        if ok_loc:
            logger.info("Dismissing stray OK dialog at {}", ok_loc)
            adb.tap(*ok_loc)
            time.sleep(0.5)

        time.sleep(config.SCREENSHOT_INTERVAL_S)

    logger.info("Event watch finished")
