"""
High-level game actions built on top of adb_controller + vision.

Each action follows the same pattern:
  1. Navigate to the right screen
  2. Detect the target element (template or fixed coords)
  3. Tap it
  4. Wait for animation / transition
  5. Return to the main screen
"""

import time
from loguru import logger
import adb_controller as adb
import vision
import config


_PAUSE = 0.8   # seconds to wait after a tap (animation settle)


# ── helpers ──────────────────────────────────────────────────────────────────

def _tap_template_or_coord(screen, template: str, fallback_key: str) -> bool:
    loc = vision.find_template(screen, template)
    if loc:
        adb.tap(*loc)
        return True
    coords = config.COORDS.get(fallback_key)
    if coords:
        logger.warning("Template '{}' not found, using fixed coords {}", template, coords)
        adb.tap(*coords)
        return True
    logger.error("Cannot tap '{}': no template and no fallback coord", template)
    return False


def _screenshot():
    return adb_controller_screenshot_with_retry()


def adb_controller_screenshot_with_retry(retries: int = 3) -> object:
    for attempt in range(retries):
        try:
            return adb.screenshot()
        except Exception as e:
            logger.warning("Screenshot attempt {} failed: {}", attempt + 1, e)
            time.sleep(1)
    raise RuntimeError("Screenshot failed after retries")


# ── actions ──────────────────────────────────────────────────────────────────

def claim_idle_rewards() -> None:
    """Open the idle-rewards pop-up and claim everything."""
    logger.info("Action: claim idle rewards")
    screen = _screenshot()

    # The claim pop-up might already be on screen, or we tap the reward icon
    if not vision.is_visible(screen, config.T_CLAIM_ALL):
        # Some versions show rewards automatically; otherwise tap the reward zone
        adb.tap(*config.COORDS["idle_claim_all"])
        time.sleep(_PAUSE)
        screen = _screenshot()

    loc = vision.find_template(screen, config.T_CLAIM_ALL)
    if loc:
        adb.tap(*loc)
        time.sleep(_PAUSE)

    # Dismiss OK / close dialog
    screen = _screenshot()
    ok_loc = vision.find_template(screen, config.T_OK_BUTTON)
    if ok_loc:
        adb.tap(*ok_loc)
        time.sleep(_PAUSE)

    logger.info("Idle rewards claimed")


def upgrade_main_unit() -> None:
    """Navigate to Characters, find the highest-DPS unit and level it up."""
    logger.info("Action: upgrade main unit")
    adb.tap(*config.COORDS["nav_characters"])
    time.sleep(_PAUSE * 2)

    screen = _screenshot()
    loc = vision.find_template(screen, config.T_LEVEL_UP)
    if loc:
        adb.tap(*loc)
        time.sleep(_PAUSE)
        logger.info("Level-up tapped")
    else:
        adb.tap(*config.COORDS["char_level_up"])
        time.sleep(_PAUSE)

    adb.press_back()
    time.sleep(_PAUSE)


def process_bag_notifications() -> None:
    """
    Open bag if there's a red-dot notification, then dismantle all excess gear.
    """
    logger.info("Action: process bag")
    screen = _screenshot()

    # Check if bag nav icon has a red dot
    red_dots = vision.find_all_templates(screen, config.T_RED_DOT)
    bag_icon_x, bag_icon_y = config.COORDS["nav_bag"]
    bag_has_notification = any(
        abs(x - bag_icon_x) < 80 and abs(y - bag_icon_y) < 80
        for x, y in red_dots
    )

    if not bag_has_notification:
        logger.info("No bag notification, skipping")
        return

    adb.tap(*config.COORDS["nav_bag"])
    time.sleep(_PAUSE * 2)

    # Switch to dismantle tab
    adb.tap(*config.COORDS["bag_dismantle_tab"])
    time.sleep(_PAUSE)

    screen = _screenshot()
    loc = vision.find_template(screen, config.T_DISMANTLE_ALL)
    if loc:
        adb.tap(*loc)
        time.sleep(_PAUSE)
    else:
        adb.tap(*config.COORDS["bag_dismantle_all"])
        time.sleep(_PAUSE)

    # Confirm dismantle
    screen = _screenshot()
    confirm = vision.find_template(screen, config.T_CONFIRM)
    if confirm:
        adb.tap(*confirm)
        time.sleep(_PAUSE)
    else:
        adb.tap(*config.COORDS["bag_confirm"])
        time.sleep(_PAUSE)

    adb.press_back()
    time.sleep(_PAUSE)
    logger.info("Bag processed")


def handle_golden_backpack(location: tuple[int, int] | None = None) -> None:
    """
    Rapid-tap the golden backpack event icon 50+ times before it disappears.
    `location` is the detected (x, y) from template matching, or None to use
    the fixed coord fallback.
    """
    logger.info("Action: golden backpack event!")
    if location:
        adb.rapid_tap(*location)
    else:
        adb.rapid_tap(*config.COORDS["golden_backpack"])
    logger.info("Golden backpack tapped {} times", config.GOLDEN_BACKPACK_TAP_COUNT)
