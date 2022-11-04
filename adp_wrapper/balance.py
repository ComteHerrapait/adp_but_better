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
            "longName": item["timeOffPolicyCode"]["longName"],
            "shortName": item["timeOffPolicyCode"]["shortName"],
            "values": [],
        }

        item_values = item.get("policyBalances")
        for value in item_values:
            parsed_item["values"].append(parse_balance_value(value))

        summary.append(parsed_item)
    log.info(f"successfully retrieved balances : {json.dumps(summary)}")

    return summary


def parse_balance_value(input_value: dict) -> dict:
    output = {"type": "N/A", "value": 0, "unit": "N/A", "name": "N/A"}
    if input_value.get("totalTime") is not None:
        # Time mode
        output["type"] = "time"
        output["unit"] = input_value["totalTime"]["nameCode"]["codeValue"]
        output["value"] = input_value["totalTime"]["timeValue"]
        output["name"] = input_value["balanceTypeCode"]["shortName"]
    elif input_value.get("totalQuantity") is not None:
        # Quantity mode
        output["type"] = "quantity"
        output["unit"] = input_value["totalQuantity"]["unitTimeCode"]["codeValue"]
        output["value"] = input_value["totalQuantity"]["quantityValue"]
        output["name"] = input_value["balanceTypeCode"]["shortName"]

    else:
        # Error mode
        output["type"] = "error"

    return output


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
