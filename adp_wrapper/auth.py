from getpass import getpass

import keyring
import requests

from adp_wrapper.constants import (
    APP_NAME,
    GOODBYE_MESSAGE,
    PASSWORD_PROMPT,
    URL_LOGIN,
    USERNAME_PROMPT,
    get_setting,
    set_setting,
)


class NoPasswordFoundException(Exception):
    pass


class UnableToLoginException(Exception):
    pass


def adp_login() -> requests.Session:
    session = requests.Session()
    logged_in = False
    while not logged_in:
        try:
            username = get_username()
            password = get_password(username)
            send_login_request(session, username, password)
            logged_in = True
        except UnableToLoginException as e:
            print(e)
            print("Please try again, check your credentials")
        except NoPasswordFoundException as e:
            print(e)
            print("Please provide a password")
        except KeyboardInterrupt:
            exit(GOODBYE_MESSAGE)
    # save username if login successful
    set_setting("adp_username", username)
    return session


def send_login_request(session: requests.Session, username: str, password: str) -> None:
    data = {
        "user": username,
        "password": password,
        "target": "https://mon.adp.com/redbox/",
    }

    response_login = session.post(URL_LOGIN, data=data)
    if not response_login.reason == "OK":
        raise UnableToLoginException(f"Unable to login to '{username}'")


def get_username() -> str:
    config_value = get_setting("adp_username")
    if not config_value:
        term_value = input(USERNAME_PROMPT) or None
        while term_value is None:
            term_value = input(USERNAME_PROMPT + "(again)") or None
        return_value = term_value
    else:
        return_value = config_value
        print(USERNAME_PROMPT + return_value + " (from config)")

    return return_value


def get_password(username: str) -> str:
    if (term_value := getpass(PASSWORD_PROMPT)) == "":
        keyring_value = keyring.get_password(APP_NAME, username)
        if keyring_value is None:
            raise NoPasswordFoundException("No password provided or stored in keyring")
        else:
            # erase the prompt line to print a message
            print("\033[1A" + PASSWORD_PROMPT + " -keyring- " + "\033[K")
            return_value = keyring_value
    else:
        keyring.set_password(APP_NAME, username, term_value)
        return_value = term_value
    return return_value
