#!/usr/bin/env python3
"""
Interactive calibration tool.

Run this first to verify coordinates and capture template images
before running main.py.

Commands (interactive menu):
  s  — take a screenshot and save it as calibration_screen.png
  c  — print the pixel color at a given coordinate
  t  — test-tap a coordinate
  q  — quit
"""

import sys
import time
import adb_controller as adb
import vision
import config
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO", format="{message}")


def take_screenshot() -> None:
    print("Taking screenshot...")
    screen = adb.screenshot()
    vision.save_debug_screenshot(screen, "calibration_screen.png")
    print(f"Saved calibration_screen.png  ({screen.shape[1]}×{screen.shape[0]} px)")
    return screen


def test_tap() -> None:
    x = int(input("  x: "))
    y = int(input("  y: "))
    print(f"Tapping ({x}, {y}) in 2 seconds...")
    time.sleep(2)
    adb.tap(x, y)
    print("Done.")


def test_template() -> None:
    name = input("  Template filename (e.g. red_dot.png): ").strip()
    print("Taking screenshot for matching...")
    screen = adb.screenshot()
    loc = vision.find_template(screen, name, threshold=0.7)
    if loc:
        print(f"  FOUND at {loc}")
    else:
        print("  NOT FOUND (lower threshold or add the template image)")


def rapid_tap_test() -> None:
    x = int(input("  x: "))
    y = int(input("  y: "))
    n = int(input("  count [default 55]: ") or "55")
    print(f"Rapid tapping ({x}, {y}) × {n} in 2 seconds...")
    time.sleep(2)
    adb.rapid_tap(x, y, count=n)
    print("Done.")


MENU = """
=== Stone Age Bot Calibration ===
  s  — screenshot → calibration_screen.png
  t  — test single tap
  r  — rapid tap test (golden backpack)
  m  — match a template against live screen
  q  — quit
> """

def main() -> None:
    try:
        model = adb.device_info()
        print(f"Connected: {model or 'unknown'}")
    except Exception as e:
        print(f"ADB error: {e}")
        sys.exit(1)

    while True:
        choice = input(MENU).strip().lower()
        if choice == "s":
            take_screenshot()
        elif choice == "t":
            test_tap()
        elif choice == "r":
            rapid_tap_test()
        elif choice == "m":
            test_template()
        elif choice == "q":
            print("Bye.")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
