from datetime import datetime

import art

from adp_wrapper.auth import adp_login
from adp_wrapper.CLI_utils import display_punch_times
from adp_wrapper.punch import get_punch_times, punch

if __name__ == "__main__":
    # Welcome message
    print("\033[H\033[J", end="")
    art.tprint("ADP but better\n", font="tarty1")

    # login
    session = adp_login()

    # display today's punch times
    timestamps = get_punch_times(session)
    display_punch_times(timestamps)

    # let you punch in or out with the terminal
    if input("Punch ? (y/n)") == "y":
        # get the punch time through terminal interaction
        punch_time = datetime.now()
        hour = int(input("Hour : ") or punch_time.hour)
        minutes = int(input("Minutes : ") or punch_time.minute)
        punch_time = punch_time.replace(hour=hour, minute=minutes)
        punch_time_str = punch_time.strftime("%A(%d) %H:%M")

        # let the user validate the punch time
        if input(f"Punching at {punch_time_str} (y/n)") == "y":
            if punch(session, punch_time):
                print("Punch successfully sent")
                timestamps = get_punch_times(session)
                display_punch_times(timestamps)
            else:
                print("Punch failed")
        else:
            print("Punch cancelled")
