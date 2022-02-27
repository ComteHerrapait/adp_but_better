import requests

headers = {
    "authority": "legallais.slack.com",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryPBGcj8sy358Z0vNT",
    "accept": "*/*",
    "origin": "https://app.slack.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": 'G_ENABLED_IDPS=google; _ga=GA1.2.2047219621.1632749818; OptanonAlertBoxClosed=2021-09-27T13:37:18.973Z; b=.5fz85hdhi4yfmweanitmnmp2j; ssb_instance_id=f3b90820-f55f-41ad-8326-849e637fcf1c; shown_ssb_redirect_page=1; shown_download_ssb_modal=1; optimizelyEndUserId=oeu1632816282846r0.801269899888198; _ga=GA1.3.2047219621.1632749818; c={"digital_first_lightning_strike_custacq":1,"platform_beta_banner":1}; t={}; show_download_ssb_banner=1; no_download_ssb_banner=1; x=5fz85hdhi4yfmweanitmnmp2j.1645029975; documentation_banner_cookie=1; utm=%7B%22utm_source%22%3A%22in-prod%22%2C%22utm_medium%22%3A%22inprod-apps_link-slack_menu-cl%22%7D; d=bwuK6TWVu3NXOxLfEoYTjJpxy9YtdDW2F%2FIL2vielIN6soJCvicQ5BN%2FuQLOOz%2BYP0nXGkHwr0PxICcomAapxXIBWjsXy%2BetjcjAQpBVAASFarlLd8daJllBuPwkP2ECRD4EhEUPbL8ecRp5uCQpPTjHWxMrfKujF%2FqbrbxWzx1dCFsib%2Fmnsw%3D%3D; d-s=1645031177; lc=1645031177; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Feb+16+2022+18%3A06%3A17+GMT%2B0100+(heure+normale+d%E2%80%99Europe+centrale)&version=6.22.0&isIABGlobal=false&hosts=&consentId=d0e45b49-20df-41ff-a0f0-3c7e882cb7be&interactionCount=2&landingPath=NotLandingPage&groups=C0004%3A0%2CC0002%3A0%2CC0003%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=FR%3BNOR',
}

params = (
    ("_x_id", "cd75c561-1645031230.025"),
    ("_x_csid", "IClLW00C95g"),
    ("slack_route", "T02FXM1JC"),
    ("_x_version_ts", "1645027048"),
    ("_x_gantry", "true"),
    ("fp", "91"),
)

data = {
    "------WebKitFormBoundaryPBGcj8sy358Z0vNT\r\nContent-Disposition: form-data; name": '"profile"\r\n\r\n{"status_emoji":":tada:","status_expiration":1645052399,"status_text":"","status_text_canonical":""}\r\n------WebKitFormBoundaryPBGcj8sy358Z0vNT\r\nContent-Disposition: form-data; name="token"\r\n\r\nxoxc-2541715624-2536568458595-2560197464944-23a188852dc1e585a9b594b4facd7d96339fb1d45c592c67a2385fb02f3cd453\r\n------WebKitFormBoundaryPBGcj8sy358Z0vNT\r\nContent-Disposition: form-data; name="_x_reason"\r\n\r\nCustomStatusModal:handle_save\r\n------WebKitFormBoundaryPBGcj8sy358Z0vNT\r\nContent-Disposition: form-data; name="_x_mode"\r\n\r\nonline\r\n------WebKitFormBoundaryPBGcj8sy358Z0vNT\r\nContent-Disposition: form-data; name="_x_sonic"\r\n\r\ntrue\r\n------WebKitFormBoundaryPBGcj8sy358Z0vNT--'
}

response = requests.post(
    "https://legallais.slack.com/api/users.profile.set",
    headers=headers,
    params=params,
    data=data,
)

print(response.status_code)
print(response.text)
print(response.content)
