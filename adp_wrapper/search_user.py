import logging
from typing import Any

from requests import Session

from adp_wrapper.auth import SessionTimeoutException
from adp_wrapper.CLI_utils import Spinner
from adp_wrapper.constants import URL_DETAIL_USER, URL_REFERER, URL_SEARCH_USERS

log = logging.getLogger(__name__)


def send_search_request(session: Session, query: str) -> Any:
    params = (("q", query), ("searchType", "advance"))

    headers = {"Referer": URL_REFERER}

    response = session.get(
        URL_SEARCH_USERS,
        headers=headers,
        params=params,
    )

    return response.json()


def get_user_detail(session: Session, user_id: str) -> Any:
    """gets details of a user from adp, using its id

    Args:
        session (Session): browser session
        user_id (str): user id

    Raises:
        SessionTimeoutException: the browser session timed out

    Returns:
        Any: user details
    """
    response = session.get(URL_DETAIL_USER + user_id)
    if "application/json" in response.headers.get("content-type", ""):
        return response.json()
    else:
        raise SessionTimeoutException()


def get_users_info(session: Session, query: str, display: bool = True) -> list[dict]:
    """returns a list of user matching the query

    Args:
        session (Session): browser session
        query (str): query
        display (bool, optional): display waiting spinner to console. Defaults to True.

    Returns:
        list[dict]: users matching the query
    """
    if display:
        spinner = Spinner(True)

    json_response = send_search_request(session, query)

    if display:
        print("\b:", end="")

    users_raw = json_response["grouped"]["id_type"]["groups"][0]["doclist"]["docs"]
    users = []
    for u in users_raw:
        user_detail_url = u.get("r_sv_uri")
        if not user_detail_url:
            continue
        user_id = user_detail_url.split("/")[-1]
        details = get_user_detail(session, user_id)
        users.append(
            {
                "id": user_id,
                "name": u["sr_sv_workerLegalFullName"],
                "email": u["r_mv_workerBusinessEmail"],
                "phone": u["r_mv_workerBusinessLandline"],
                "details": details,
            }
        )

    if display:
        spinner.stop()

    log.info(f"searched for '{query}' in users, got {len(users)} results")
    return users
