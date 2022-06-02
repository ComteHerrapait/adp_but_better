import json
import logging
from datetime import datetime
from typing import Any

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
            "adp_name": item["timeOffPolicyCode"]["longName"],
            "my_name": None,
            "value": None,
            "unit": None,
        }
        balance = item["policyBalances"][0]

        policy_type: str = parsed_item.get("adp_name") or "invalid"
        if policy_type == "Débit crédit":
            parsed_item["my_name"] = "Débit Crédit"
            parsed_item["value"] = balance["totalTime"]["timeValue"]
            parsed_item["unit"] = balance["totalTime"]["nameCode"]["codeValue"]
        elif policy_type == "RTT Salarié":
            parsed_item["my_name"] = "RTT"
            parsed_item["value"] = balance["totalQuantity"]["quantityValue"]
            parsed_item["unit"] = balance["totalQuantity"]["unitTimeCode"]["codeValue"]
        elif policy_type == "CP écoulés":
            parsed_item["my_name"] = "Congés Payés"
            parsed_item["value"] = balance["totalQuantity"]["quantityValue"]
            parsed_item["unit"] = balance["totalQuantity"]["unitTimeCode"]["codeValue"]
        else:
            parsed_item["my_name"] = "ERR (" + policy_type + ")"
            parsed_item["value"] = "N/A"
            parsed_item["unit"] = "N/A"

        summary.append(parsed_item)
    log.info(f"successfully retrieved balances : {json.dumps(summary)}")

    return summary


def send_balances_request(session: Session) -> Any:
    """sends the request to get the balances from adp API

    Args:
        session (Session): browser session

    Returns:
        Any: response from API

    Raises:
        SessionTimeoutException
    """
    headers = {"Referer": URL_REFERER}
    today = datetime.strftime(datetime.now(), DATE_FORMAT)
    params = (("$filter", f"balanceAsOfDate eq '{today}'"),)
    url = URL_BALANCES.replace("<USER_ID>", get_setting("adp_username"))

    response = session.get(url, headers=headers, params=params)
    if "application/json" in response.headers.get("content-type", ""):
        return response.json()
    else:
        raise SessionTimeoutException()
