import logging
from typing import Any, Tuple

from requests import Session

from adp_wrapper.auth import SessionTimeoutException
from adp_wrapper.CLI_utils import Spinner
from adp_wrapper.constants import (
    URL_DETAIL_USER_ASSOCIATE,
    URL_DETAIL_USER_WORKER,
    URL_REFERER,
    URL_SEARCH_USERS,
    USER_INFO_CUSTOM_FIELD_TRANSLATIONS,
)

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


def get_associate_info(session: Session, user_id: str) -> Any:
    headers = {"Referer": URL_REFERER}

    response = session.get(URL_DETAIL_USER_ASSOCIATE + user_id, headers=headers)
    if "application/json" in response.headers.get("content-type", ""):
        return response.json()
    else:
        raise SessionTimeoutException()


def get_worker_info(session: Session, user_id: str) -> Any:
    headers = {"Referer": URL_REFERER}

    response = session.get(URL_DETAIL_USER_WORKER + user_id, headers=headers)
    if "application/json" in response.headers.get("content-type", ""):
        return response.json()
    else:
        raise SessionTimeoutException()


def get_user_detail(session: Session, user_id: str) -> dict:
    associate = get_associate_info(session, user_id)
    workers = get_worker_info(session, user_id).get("workers", [])
    result = {}
    result["associate"] = associate
    if len(workers) > 0:
        result["worker"] = workers[0]
    else:
        result["workers"] = workers
    return result


def print_user_details(user_dict: dict) -> None:
    print(f"id\t: {user_dict['associate']['associateoid']}")
    print(f"name\t: {user_dict['associate']['name']['formatted']}")
    start_date = user_dict["worker"]["workerStatus"]["effectiveDate"]
    start_date_original = user_dict["worker"]["workerDates"]["originalHireDate"]
    print(f"hired\t: {start_date} ({start_date_original})")

    # e-mail addresses
    for mail in user_dict["worker"]["businessCommunication"]["emails"]:
        mail_name = mail["nameCode"]["longName"]
        mail_uri = mail["emailUri"]
        print(f"mail\t: '{mail_name}' {mail_uri}")

    # jobs
    for job in user_dict["worker"]["workAssignments"]:
        print(f"job\t: {job['jobTitle']}")
        print(f" > start\t: {job['expectedStartDate']}")
        for manager in job["reportsTo"]:
            f_name = manager["reportsToWorkerName"]["givenName"]
            l_name = manager["reportsToWorkerName"]["familyName1"]
            print(f" > manager\t: {f_name} {l_name})({manager['associateOID']})")
        for department in job["assignedOrganizationalUnits"]:
            print(f" > {department['itemID']} : {department['nameCode']['longName']}")

        for address in job["assignedWorkLocations"]:
            print(f" > address\t: {address['nameCode']['longName']}")
            print(
                f"\t{address['address']['postalCode']} {address['address']['cityName']}"
            )
            print(f"\t{address['address']['lineOne']} {address['address']['lineTwo']}")

        # misc fields (codes)
        for field in job["customFieldGroup"]["codeFields"]:
            field_name = field["itemID"]
            if field_name in USER_INFO_CUSTOM_FIELD_TRANSLATIONS:
                field_name = USER_INFO_CUSTOM_FIELD_TRANSLATIONS[field_name]

            field_value = f"{field.get('longName', 'N/A')} ({field['codeValue']})"
            print(f"{field_name}\t: {field_value}")

        # misc fields (numbers)
        for field in job["customFieldGroup"]["numberFields"]:
            field_name = field["itemID"]
            if field_name in USER_INFO_CUSTOM_FIELD_TRANSLATIONS:
                field_name = USER_INFO_CUSTOM_FIELD_TRANSLATIONS[field_name]
            print(f"{field_name}\t: {field['numberValue']}")

    print(f"status\t: {user_dict['worker']['workerStatus']['statusCode']['codeValue']}")


def get_users_id(
    session: Session, query: str, display: bool = True
) -> list[Tuple[str, str]]:
    """returns a list of user matching the query

    Args:
        session (Session): browser session
        query (str): query
        display (bool, optional): display waiting spinner to console. Defaults to True.

    Returns:
        list[Tuple[str, str]]: users matching the query
    """
    if display:
        spinner = Spinner(True)

    json_response = send_search_request(session, query)

    if display:
        print("\b:", end="")

    try:
        users_raw = json_response["grouped"]["id_type"]["groups"][0]["doclist"]["docs"]
    except KeyError:
        users_raw = []

    users = []
    for u in users_raw:
        user_detail_url = u.get("r_sv_uri")
        if not user_detail_url:
            continue
        user_id = user_detail_url.split("/")[-1]
        users.append((u["sr_sv_workerLegalFullName"], user_id))

    if display:
        spinner.stop()

    log.info(f"searched for '{query}' in users, got {len(users)} results")
    return users
