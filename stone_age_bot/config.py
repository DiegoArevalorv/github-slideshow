"""
Configuration for Stone Age: Idle Adventure bot.

All coordinates are for a 1080x1920 resolution (standard FHD portrait).
If your emulator or device uses a different resolution, scale them with
the SCALE_X / SCALE_Y factors below.
"""

# --- Device / emulator connection ----------------------------------------
ADB_DEVICE = None          # None = auto-detect first device; or "emulator-5554"
DEVICE_WIDTH = 1080
DEVICE_HEIGHT = 1920
SCALE_X = 1.0              # Set to actual_width  / 1080 if your res differs
SCALE_Y = 1.0              # Set to actual_height / 1920 if your res differs

# --- Scheduler -----------------------------------------------------------
CYCLE_INTERVAL_HOURS = 4   # How often the full routine runs
SCREENSHOT_INTERVAL_S = 1  # Polling rate during event watch (seconds)
EVENT_WATCH_DURATION_S = 30 # How long to watch for pop-up events after routine

# --- Template matching ---------------------------------------------------
TEMPLATE_DIR = "templates"
MATCH_THRESHOLD = 0.80     # 0–1; lower = more permissive

# Template filenames (place PNG images in stone_age_bot/templates/)
T_RED_DOT          = "red_dot.png"
T_GOLDEN_BACKPACK  = "golden_backpack.png"
T_CLAIM_ALL        = "claim_all_btn.png"
T_LEVEL_UP         = "level_up_btn.png"
T_OK_BUTTON        = "ok_button.png"
T_DISMANTLE_ALL    = "dismantle_all_btn.png"
T_CONFIRM          = "confirm_btn.png"

# --- UI regions (x, y, w, h) to limit template search scope  -----------
# Leaving these as None searches the full screen.
REGION_BOTTOM_NAV  = (0, 1600, 1080, 320)   # Bottom navigation bar
REGION_FULL        = None

# --- Fixed button coordinates (fallback when template not found) --------
# These are approximate for 1080x1920; calibrate with your device.
COORDS = {
    # Main menu icons (bottom navigation)
    "nav_characters":  (108, 1750),
    "nav_bag":         (324, 1750),
    "nav_summon":      (540, 1750),
    "nav_shop":        (756, 1750),
    "nav_dungeon":     (972, 1750),

    # Inside Bag / Inventory screen
    "bag_dismantle_tab":  (810, 300),
    "bag_dismantle_all":  (540, 1650),
    "bag_confirm":        (660, 1100),

    # Inside Characters / Upgrade screen
    "char_level_up":      (810, 1500),

    # Idle rewards pop-up
    "idle_claim_all":     (540, 1300),
    "idle_ok":            (540, 1450),

    # Golden Backpack event (center of bag icon when it appears)
    "golden_backpack":    (540, 960),
}

# --- Golden Backpack rapid-tap settings ----------------------------------
GOLDEN_BACKPACK_TAP_COUNT   = 55   # Slightly more than 50 to be safe
GOLDEN_BACKPACK_TAP_DELAY_S = 0.02 # 20 ms between taps ≈ 50 taps/sec
