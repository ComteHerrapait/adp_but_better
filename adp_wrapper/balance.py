import json
import logging
from datetime import datetime

from requests import Session

from adp_wrapper.auth import SessionTimeoutException
from adp_wrapper.constants import DATE_FORMAT, URL_BALANCES, URL_REFERER, get_setting

log = logging.getLogger(__name__)


def get_balances(session: Session) -> list[dict]:
    """gets the balances of a user, such as the amount of time off and overtime
    Args:
        session (Session): session object
    Returns:
        list[dict]: list of balances
    """
    raw_balances = send_balances_request(session)
    summary = []

    if not raw_balances:
        return []

    raw_balances = raw_balances["timeOffBalances"][0]["timeOffPolicyBalances"]

    for item in raw_balances:
        parsed_item = {
            "name": item["timeOffPolicyCode"]["longName"],
            "description": None,
            "value": None,
            "unit": None,
        }
        balance = item["policyBalances"][0]

        match parsed_item.get("name"):
            case "Débit crédit":
                parsed_item["description"] = balance["balanceTypeCode"]["shortName"]
                parsed_item["value"] = balance["totalTime"]["timeValue"]
                parsed_item["unit"] = balance["totalTime"]["nameCode"]["codeValue"]
            case "RTT Salarié":
                parsed_item["description"] = balance["balanceTypeCode"]["shortName"]
                parsed_item["value"] = balance["totalQuantity"]["quantityValue"]
                parsed_item["unit"] = balance["totalQuantity"]["unitTimeCode"][
                    "codeValue"
                ]

        summary.append(parsed_item)
    log.info(f"successfully retrieved balances : {json.dumps(summary)}")

    return summary


def send_balances_request(session: Session) -> dict:
    """sends the request to get the balances from adp API

    Args:
        session (Session): browser session

    Returns:
        dict: response from API

    Raises:
        SessionTimeoutException
    """
    headers = {"Referer": URL_REFERER}
    today = datetime.strftime(datetime.now(), DATE_FORMAT)
    params = (("$filter", f"balanceAsOfDate eq '{today}'"),)
    url = URL_BALANCES.replace("<USER_ID>", get_setting("adp_username"))

    response = session.get(url, headers=headers, params=params)
    if "application/json" in response.headers.get("content-type"):
        return response.json()
    else:
        raise SessionTimeoutException()
