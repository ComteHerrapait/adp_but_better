import dataclasses
import os
import threading
from datetime import date, datetime, timedelta
from enum import Enum
from json import JSONEncoder, dumps
from time import sleep, time
from typing import Any

import art
import inquirer

"""
These functions serve to display and interact with the user through the terminal.
"""


class EnhancedJSONEncoder(JSONEncoder):
    """Enhances the JSONEncoder class to handle dataclasses, datetime and Enum."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.value
        return super().default(o)


def print_json(obj: Any, **kwargs) -> None:
    """Prints a JSON representation of the given object.

    Args:
        obj (Any): object to print
        **kwargs: additional arguments passed to json.dumps
    """
    print(dumps(obj, cls=EnhancedJSONEncoder, **kwargs))


def print_header(clear: bool = True) -> None:
    """prints the app header to the terminal, using art library

    Args:
        clear (bool, optional): clear the console. Defaults to True.
    """
    if clear:
        print("\033[H\033[J", end="")
    width = os.get_terminal_size().columns
    # adapt text size to terminal width
    if width > 101:
        art.tprint("ADP but better\n", font="tarty1")
    else:
        art.tprint("ADP but better\n", font="tarty2")


def format_timedelta(timedelta: timedelta) -> str:
    """Convert a timedelta to a string.

    Args:
        timedelta (timedelta)

    Returns:
        str: formatted timedelta
    """
    return str(abs(timedelta))[:-3]


def user_validation_punch(punch_time: datetime) -> bool:
    """ask user to validate the punch time.

    Args:
        punch_time (datetime): punch date and time

    Returns:
        bool: user validated
    """
    punch_time_str = punch_time.strftime("%A(%d) %H:%M")
    return inquirer.confirm(f"Punching at {punch_time_str}")


class Spinner:
    busy = False
    delay = 0.1
    message = "Waiting"
    start_time = 0
    waiting_char = "."

    def __init__(self, start_now=False) -> None:
        if start_now:
            self.start()

    def task(self):
        print(self.message, end=" ")
        while self.busy:
            sleep(self.delay)
            print(self.waiting_char, end="", flush=True)
        elapsed = time() - self.start_time
        print(f" done ({elapsed:.2f}s)")

    def start(self):
        self.busy = True
        self.start_time = time()
        threading.Thread(target=self.task, name="SpinnerThread").start()

    def stop(self):
        self.busy = False
        sleep(2 * self.delay)
