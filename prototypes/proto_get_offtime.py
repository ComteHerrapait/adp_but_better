import json

import requests

cookies = {
    "mlOqCpOrig": "rd1o00000000000000000000ffff0b81c0b4o1073",
    "EMEASMSESSION": "WVxdi7rJEUL03muD8xuTlGOlEl3cybcdWd2/ZmJdebHYbwsy+RVUrcFbGcb3xF13Zdn5mFL20C53o9fCznswfW9bW3wj+RDbxDmGFy10JBJhKm7KudcfTD9NpJRC/Y1FgRzabeRFW+rlBZHLrnt+iWsIkRzxvqciFXd5eFNsE3Edyi/89nqKcS3ouNtcZrk2d2n2rH37GEBfK7fNLZ1s/gMQahZ6y8bK/wuYSGFC0Asm5p+Fl4A2Hpe/9kPmmLjTQ2AAxfhxjVDS0vi50Ob3CMidOHzMdEXUOrG2fLQ91WvZ8YyH0TNMq2pT42Swu3l69QGLFjDo6VFuIgToCSRgK8h+MmYPkVoX2A4VYRXqIP/EIDTQcV/JBQEvugzdGYjLXq8dYewtd5sGOGgRBAZ+8oliBBRQ/2kGpwMwLCETrU2k6kRc+NiqiiJwFGaIjuSjIxVxFsObFyKQfxQ9I8mN/oRyfigNyaR7VoGbTnfn69/LAWEjt2Tm80OMPU4UA+SD8x2XdFSp1q2hyDA+oFi2JZks51YAKPcRZC4yPS7vSpUsAgAFiawZInEWC83E7Gb1gdAyxtyGgTkDlUZL3sDrJmuSfHZ7UMRrFyf/SRn7Y5/sWIpvCiuJryyGgIPrKyiuo49dPfxbsEgDAwYp7fxPUFx/rIaZL7yF6j2exAGoL0xlFqgNXzGkuf1usifxEwU+cqR1q6+qoNeyFJTjWQCkvBDCqV63YXUFhGFFaZ+NZ03vttk0Vx64Mz0nx+S4LpEGkGqqTFCmPTfLK+dAH9v3MJQ0kol3C5lyAHOe+386R9c5hor2fcMn1fEgBef5U5a0b0/ZMObBcLzJPRAllwq1soxRI7DbO6sP4xboStbj5TNGAveUR9oUWz/P9pbxjjYEidlGi9/k0gfkQ5xAu4h3kPAA6/K5wptn8bqkyoI3GxR+QRxhF2olSUtwKi5bW9ZMzFdRg5eT6fembkZZVe5z2Ilf/h1lX+qnbQTZ4ZpgqkdWVTN9QFES9ASTTNOn5JEZap6HfRVsyJnwPai4hUAF5SAE1M7Wb0Rx0Fv0X3sbmXv3NcmE+H5su+ltaKf7JCnLl2hyNqR20wkNTnmm6gLyNBHgtF42ZkgKZ86PhEH+nn0Z8s5GFRlG91pNEOwkAj7R",
    "9NsIAD8oR9": "AA8e6tB-AQAAS84IavMOwZ4lVfykRESYltARHIME8qZldoOr0urKqrizcBfv|1|1|881218f557f038efeacc0a5a11caa69b4014827f",
    "FRANCE-PORTAL": "rd1o00000000000000000000ffff0b81c303o8080",
    "disconnecturl": "https://hr-services.fr.adp.com/portal-main/postconnect.jsp",
}

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "Accept-Language": "fr-FR",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "rolecode": "employee",
    "Accept": "application/json, text/plain, */*",
    "consumerappoid": "RDBX:3.10",
    "sec-ch-ua-platform": '"macOS"',
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://mon.adp.com/redbox/3.10.1.2/",
}

params = (("$filter", "balanceAsOfDate eq '2022-02-06'"),)

response = requests.get(
    "https://mon.adp.com/time/v3/workers/__REDACTED__/time-off-balances",
    headers=headers,
    params=params,
    cookies=cookies,
)

json_response = response.json()
time_balance = json_response["timeOffBalances"][0]["timeOffPolicyBalances"][0][
    "policyBalances"
][0]["totalTime"]
print(time_balance)
print(json.dumps(response.json(), indent=2))
