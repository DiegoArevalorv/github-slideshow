#!/usr/bin/env python3
"""
Stone Age: Idle Adventure — AFK Bot
====================================
Runs the full routine every CYCLE_INTERVAL_HOURS hours and watches for
golden backpack / other pop-up events between cycles.

Usage (Termux on-device):
  python main.py

Usage (PC with device connected via USB or WiFi ADB):
  python main.py --device emulator-5554

Flags:
  --once        Run one cycle now and exit (useful for testing)
  --device ID   Override ADB_DEVICE in config.py
  --debug       Save a debug screenshot before each cycle
"""

import argparse
import time
import sys
import schedule
from loguru import logger
import adb_controller as adb
import config
from state_machine import BotStateMachine


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Stone Age: Idle Adventure bot")
    p.add_argument("--once",   action="store_true", help="Run one cycle and exit")
    p.add_argument("--device", default=None,        help="ADB device serial")
    p.add_argument("--debug",  action="store_true", help="Save debug screenshots")
    return p.parse_args()


def setup_logging(debug: bool) -> None:
    logger.remove()
    level = "DEBUG" if debug else "INFO"
    logger.add(sys.stderr, level=level,
               format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | {message}")
    logger.add("bot.log", rotation="10 MB", retention="7 days", level="DEBUG")


def verify_adb_connection() -> None:
    try:
        model = adb.device_info()
        logger.info("Connected to: {}", model or "unknown device")
    except Exception as e:
        logger.error("ADB connection failed: {}", e)
        logger.error("Make sure ADB is running:")
        logger.error("  Termux: pkg install android-tools")
        logger.error("          adb pair 127.0.0.1:<PAIR_PORT> <CODE>")
        logger.error("          adb connect 127.0.0.1:<DEBUG_PORT>")
        logger.error("  PC:     adb devices")
        sys.exit(1)


def main() -> None:
    args = parse_args()
    setup_logging(args.debug)

    if args.device:
        config.ADB_DEVICE = args.device

    logger.info("Stone Age Bot starting up")
    verify_adb_connection()

    bot = BotStateMachine()

    if args.once:
        logger.info("--once flag: running single cycle")
        bot.run_cycle()
        return

    # Schedule recurring cycles
    interval_h = config.CYCLE_INTERVAL_HOURS
    logger.info("Scheduled to run every {} hours", interval_h)

    # Run immediately on start, then on schedule
    bot.run_cycle()
    schedule.every(interval_h).hours.do(bot.run_cycle)

    logger.info("Bot running. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")


if __name__ == "__main__":
    main()
