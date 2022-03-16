import json
import logging
import logging.config

import inquirer
from requests import Session

from adp_wrapper.auth import SessionTimeoutException, adp_login
from adp_wrapper.CLI_utils import display_punch_times, print_header
from adp_wrapper.constants import GOODBYE_MESSAGE, LOGGING_SETTINGS_FILE
from adp_wrapper.punch import get_punch_times
from adp_wrapper.user_commands import COMMAND_LIST, cmd_exit


def main_loop(session: Session) -> bool:
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do now ?",
            choices=COMMAND_LIST.keys(),
            carousel=True,
        ),
    ]
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    if answers is not None:
        answer = answers.get("action", "Exit")
    else:
        answer = "Exit"

    user_command = COMMAND_LIST.get(answer)
    if user_command is not None:
        return user_command(session)
    else:
        return cmd_exit(session)


def setup_logging() -> None:
    """
    Setup logging from config file or with basic config if not found
    """
    if LOGGING_SETTINGS_FILE.exists():
        with LOGGING_SETTINGS_FILE.open("r") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

    log = logging.getLogger(__name__)
    log.debug("logger initialized")


if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger(__name__)
    log.info("starting app")

    # Welcome message
    print_header(True)

    # login
    session = adp_login()

    # display today's punch times
    timestamps = get_punch_times(session)
    display_punch_times(timestamps)

    running = True
    while running:
        try:
            running = main_loop(session)
        except SessionTimeoutException:
            print_header(True)
            print("Session timed out. Logging in again...")
            session = adp_login()
            timestamps = get_punch_times(session)
            display_punch_times(timestamps)
        except KeyboardInterrupt:
            log.warning("application interrupted by user (ˆC)")
            running = False
        except AssertionError as ae:
            log.critical(ae)
            print(ae)
            running = False

    log.info("quitting app")
    exit(GOODBYE_MESSAGE)
