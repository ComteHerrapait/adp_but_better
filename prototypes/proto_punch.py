import requests

cookies = {
    "mlOqCpOrig": "rd1o00000000000000000000ffff0b81c0b6o1073",
    "9NsIAD8oR9": "ANW8T8B-AQAAmcOXZ72Y5bj2U1XMz7TgopIwBB5ftyBK2nhqGS-W9HyJpVO-|1|1|4ba998918a3664d48ff2402937eb91aa6d487053",
    "FRANCE-PORTAL": "rd1o00000000000000000000ffff0b81c303o8080",
    "ADPEHCRELEASE": "----S-6-----------------------a---1-----------------------------4------12----2-------------------------------------------1",
    "disconnecturl": "https://hr-services.fr.adp.com/portal-main/postconnect.jsp",
    "EMEASMSESSION": "FNiMbq5A3zCQCV6FXUXlEUv+cXFKm8KzHkoGmzFweFBsg6jiG+Q4sowodZUmQXyF2XiwPDyHT3oA2uEViHWbTItFzZv27WggOyuygFScpWH4EZYVJ7asUh784WTHtUcU0hKPUCRhL1U0/MVE4/Gkl0qKQ4hi4COCQmZuRzXEqF2ER0oiny+SSWkaC8KkT658MpqFi3Mk1FxgBbmLTzyGjbrJGePIhaIH4KG1yvj6fhiL1ooigKL65AMFkyYkFGjciG5AZErBJHFuuUdoYaUomOYib3091i+k3oP3mTscTvOGX6jhDYoPCY/GJNI/utZrBEiQbBWc3NVKxQJRayDtpeVLKosZRAgp9bpkoHjmY3FW0N4WELqcE924+LWpg5pDz8bcIp2mlkp+zi5bfRsMPoRVhPZGoDBkZr4ONnlaBptghDQ1TS9v/9uXXNvP5DQalyztM3j0Mw8lrrE0K9kF2odkCDTGTiT5/RdoRmRyaIBx9SW5gkDxORtenc8tkcTQJkbCfL2BO/pULnRZEVcNZ7cCSW3WfnngVOPFnKDT6kvfUGmRgoSrYDb9GJXUQA/ntJLSWswM8Lx7YFf+bahNOTYJeZ6ATsK/t3nRiw9wGj7UhpD0F2494TqU/pbqxQCMhOHq/le6aHsMyK8Wwcg1eg2ofvE5j2qWZcCfj9JHVZsVtC8lAPqJHb/p9RyqBkJzJM4vDF+NUY3M71c55h16wPlUX6wr7pYl7bO8SidSKUbXscHeIwy9x6ui4/VN1Sh8D49rG0cnIWPrCqqDPuxPmkjN6vo4uZN/Np8pxOVXdYE8lSKnVG7CgCanV+SkJzhKv/HIIgzVqYlGRhaTkD/HsX7Cdcg8nxycTl5rMfIxrurbHFTGFmyCK05h9xh2MkaXC4yvtk6WSIKJdZpGoLDfj7pwHDN8V+XRMYLjXVjLU5eYL8CIVK+TdQrv6SeT/LHp0bQNPr13Wgd0bHMPUhA3iUst4FJ9fMVne0kPg6Pr0Hvum6kFgiM3N7wbq6qxWFWC1n5y58zAwA0zsM0z1wNZxvNpKAqPF8k9054SA1bDF34JftcTjkU8Ch9yug/G6vTqwmpQesHGuKpnIdvqh5y7TO28Pw6JBXZ6wEfzzo49PyU7UfbuW+Rxl31rHRDnv/Ag",
}

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://mon.adp.com",
    "Referer": "https://mon.adp.com/redbox/3.10.1.2/",
}
temp = "2022-02-03T17:55:29"
data = (
    '{"timeEntry":{"metadeviceDateTime":"'
    + temp
    + '+01:00","positionID":{"id":"__REDACTED__","schemeName":"PFID","schemeAgencyName":"ADP Registry"},"clockEntry":{"entryDateTime":"'
    + temp
    + '+01:00","actionCode":"punch"}}}'
)

response = requests.post(
    "https://mon.adp.com/v1_0/O/A/timeEntry",
    headers=headers,
    cookies=cookies,
    data=data,
)
print(response.status_code)
print(response.text)
