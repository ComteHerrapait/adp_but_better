from requests import Session

from adp_wrapper.constants import URL_DETAIL_USER, URL_REFERER, URL_SEARCH_USERS


def send_search_request(session: Session, query: str):
    params = (("q", query), ("searchType", "advance"))

    headers = {"Referer": URL_REFERER}

    response = session.get(
        URL_SEARCH_USERS,
        headers=headers,
        params=params,
    )

    return response.json()


def get_user_detail(session: Session, user_id: str):
    response = session.get(URL_DETAIL_USER + user_id)
    temp = response.json()
    return temp


def get_users_info(session: Session, query: str):
    json_response = send_search_request(session, query)
    users_raw = json_response["grouped"]["id_type"]["groups"][0]["doclist"]["docs"]
    users = []

    for u in users_raw:
        user_id = u["sr_sv_workerID"]
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

    return users
