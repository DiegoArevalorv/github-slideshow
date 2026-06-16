"""
Computer vision helpers using OpenCV template matching.

Usage:
  screen = adb_controller.screenshot()
  loc = find_template(screen, "red_dot.png")
  if loc:
      adb_controller.tap(*loc)
"""

import os
import cv2
import numpy as np
from loguru import logger
import config


def _load_template(filename: str) -> np.ndarray | None:
    path = os.path.join(os.path.dirname(__file__), config.TEMPLATE_DIR, filename)
    if not os.path.exists(path):
        logger.warning("Template not found: {}", path)
        return None
    return cv2.imread(path, cv2.IMREAD_COLOR)


def find_template(
    screen: np.ndarray,
    template_filename: str,
    threshold: float = config.MATCH_THRESHOLD,
    region: tuple | None = None,
) -> tuple[int, int] | None:
    """
    Search for template_filename inside screen (or a sub-region).
    Returns (center_x, center_y) in full-screen coordinates, or None.
    """
    template = _load_template(template_filename)
    if template is None:
        return None

    search_img = screen
    offset_x, offset_y = 0, 0
    if region:
        rx, ry, rw, rh = region
        search_img = screen[ry:ry + rh, rx:rx + rw]
        offset_x, offset_y = rx, ry

    # Convert both to BGR for OpenCV
    haystack = cv2.cvtColor(search_img, cv2.COLOR_RGB2BGR)
    needle   = cv2.cvtColor(template,   cv2.COLOR_BGR2BGR)  # already BGR

    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        logger.debug("Template '{}' not found (best={:.2f})", template_filename, max_val)
        return None

    th, tw = needle.shape[:2]
    cx = offset_x + max_loc[0] + tw // 2
    cy = offset_y + max_loc[1] + th // 2
    logger.debug("Template '{}' found at ({}, {}) conf={:.2f}",
                 template_filename, cx, cy, max_val)
    return (cx, cy)


def find_all_templates(
    screen: np.ndarray,
    template_filename: str,
    threshold: float = config.MATCH_THRESHOLD,
) -> list[tuple[int, int]]:
    """Return ALL non-overlapping matches (useful for multiple red dots)."""
    template = _load_template(template_filename)
    if template is None:
        return []

    haystack = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    needle   = template

    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    th, tw = needle.shape[:2]
    points = []
    for pt in zip(*locations[::-1]):   # (x, y) pairs
        cx, cy = pt[0] + tw // 2, pt[1] + th // 2
        # Suppress duplicates within 20px
        if all(abs(cx - px) > 20 or abs(cy - py) > 20 for px, py in points):
            points.append((cx, cy))

    logger.debug("Template '{}' found {} times", template_filename, len(points))
    return points


def is_visible(screen: np.ndarray, template_filename: str,
               threshold: float = config.MATCH_THRESHOLD) -> bool:
    return find_template(screen, template_filename, threshold) is not None


def save_debug_screenshot(screen: np.ndarray, name: str = "debug.png") -> None:
    path = os.path.join(os.path.dirname(__file__), name)
    cv2.imwrite(path, cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
    logger.debug("Debug screenshot saved: {}", path)
