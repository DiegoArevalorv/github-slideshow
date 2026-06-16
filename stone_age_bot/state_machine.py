"""
Bot state machine for Stone Age: Idle Adventure.

States
------
IDLE        → waiting for the scheduler to fire
RUNNING     → executing the main routine step by step
WATCHING    → polling for pop-up events between routine cycles
ERROR       → something went wrong; will retry next cycle
"""

from enum import Enum, auto
from loguru import logger
import bot_actions
import event_handler
import config


class State(Enum):
    IDLE     = auto()
    RUNNING  = auto()
    WATCHING = auto()
    ERROR    = auto()


class BotStateMachine:
    def __init__(self):
        self.state = State.IDLE
        self.cycle_count = 0

    # ── public API ────────────────────────────────────────────────────────

    def run_cycle(self) -> None:
        """Execute one complete routine cycle."""
        self._transition(State.RUNNING)
        try:
            self._execute_routine()
            self._transition(State.WATCHING)
            self._watch()
        except Exception as e:
            logger.exception("Cycle {} failed: {}", self.cycle_count, e)
            self._transition(State.ERROR)
        finally:
            self._transition(State.IDLE)

    # ── private ───────────────────────────────────────────────────────────

    def _execute_routine(self) -> None:
        self.cycle_count += 1
        logger.info("=== Cycle {} start ===", self.cycle_count)

        # Step 1: Claim accumulated idle rewards
        bot_actions.claim_idle_rewards()

        # Step 2: Level up the main DPS unit
        bot_actions.upgrade_main_unit()

        # Step 3: Clear inventory notifications (dismantle junk gear)
        bot_actions.process_bag_notifications()

        logger.info("=== Cycle {} complete ===", self.cycle_count)

    def _watch(self) -> None:
        event_handler.watch_for_events(config.EVENT_WATCH_DURATION_S)

    def _transition(self, new_state: State) -> None:
        logger.debug("State: {} → {}", self.state.name, new_state.name)
        self.state = new_state
