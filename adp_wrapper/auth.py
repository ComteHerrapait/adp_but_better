import logging
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

log = logging.getLogger(__name__)


class NoPasswordFoundException(Exception):
    """no password found in keyring"""

    def __init__(self, username: str) -> None:
        self.username = username
        self.message = f"No password stored in keyring for '{username}'"
        log.error("NoPasswordFoundException : " + self.message)
        super().__init__(self.message)


class UnableToLoginException(Exception):
    """Login to adp was not successful"""

    def __init__(self, username: str) -> None:
        self.username = username
        self.message = f"login failed for '{username}'"
        log.error("UnableToLoginException : " + self.message)
        super().__init__(self.message)


class AccountErrorException(Exception):
    """ADP account has problems"""

    def __init__(self, username: str) -> None:
        self.username = username
        self.message = f"problems with ADP account '{username}'"
        log.error("AccountErrorException : " + self.message)
        super().__init__(self.message)


class SessionTimeoutException(Exception):
    """Session timed out"""

    def __init__(self, *args: object) -> None:
        log.warning("SessionTimeoutException : browser session timed out")
        super().__init__(*args)


def adp_login() -> requests.Session:
    """logs in to adp, by asking for username and password through command line
    interface

    Returns:
        requests.Session: session created by login in
    """
    session = requests.Session()
    logged_in = False
    while not logged_in:
        try:
            log.info("Logging in")
            username = get_username()
            password = get_password(username)
            send_login_request(session, username, password)
            logged_in = True
            log.info(f"Logged in as '{username}'")
        except UnableToLoginException:
            print("Please try again, check your credentials")
            set_setting("skip_password_prompt", False)
        except AccountErrorException:
            print("Your ADP account has errors")
            print("please use the web interface : https://mon.adp.com/")
            set_setting("skip_password_prompt", False)
            log.warning("closing application because ADP account has errors")
            exit(GOODBYE_MESSAGE)
        except NoPasswordFoundException:
            print("Please provide a password")
            set_setting("skip_password_prompt", False)
        except KeyboardInterrupt:
            log.warning("application interrupted by user (^C) during login")
            exit(GOODBYE_MESSAGE)
    # save username if login successful
    set_setting("adp_username", username)
    return session


def send_login_request(session: requests.Session, username: str, password: str) -> None:
    """send the login request (POST)

    Args:
        session (requests.Session)
        username (str)
        password (str)

    Raises:
        UnableToLoginException
    """
    data = {
        "user": username,
        "password": password,
        "target": "https://mon.adp.com/redbox/",
    }

    response_login = session.post(URL_LOGIN, data=data)

    bad_login = response_login.url.endswith("?REASON=BADLOGIN")
    account_error = response_login.url.endswith("pwdservice/accountError")

    if not response_login.ok or bad_login:
        raise UnableToLoginException(username)
    if account_error:
        raise AccountErrorException(username)


def get_username() -> str:
    """get username, from command line or from config file

    Returns:
        str: username
    """

    config_value = get_setting("adp_username")
    if not config_value:
        term_value = input(USERNAME_PROMPT) or None
        while term_value is None:
            term_value = input(USERNAME_PROMPT + "(again)") or None
        return_value = term_value
    else:
        return_value = config_value
        print(USERNAME_PROMPT + return_value + " -config-")

    return return_value


def get_password(username: str) -> str:
    """get password, from command line or from keyring

    Args:
        username (str): username for which to get password

    Raises:
        NoPasswordFoundException

    Returns:
        str: password
    """
    skip_password = get_setting("skip_password_prompt")
    if skip_password or ((term_value := getpass(PASSWORD_PROMPT)) == ""):
        # password prompt skipped through config or empty response
        keyring_value = keyring.get_password(APP_NAME, username)
        if keyring_value is None:
            raise NoPasswordFoundException(username)
        else:
            if skip_password:
                print(PASSWORD_PROMPT + " -keyring- (auto)")
            else:
                log.info(f"keyring : found password for '{username}'")
                # erase the prompt line to print a message
                print("\033[1A" + PASSWORD_PROMPT + " -keyring- " + "\033[K")
            return_value = keyring_value
    else:
        # settings set to not skip password and non null value entered
        keyring.set_password(APP_NAME, username, term_value)
        log.info(f"keyring : stored new password for '{username}'")
        return_value = term_value
    return return_value
