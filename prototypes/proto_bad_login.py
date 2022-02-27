import datetime
import json
from getpass import getpass

import requests

URL_LOGIN = "https://mon.adp.com/ipclogin/1/loginform.fcc"
URL_DATA = "https://mon.adp.com/v1_0/O/A/timeEntryDetails"
URL_PUNCH = "https://mon.adp.com/v1_0/O/A/timeEntry"


cookies = {
    "mlOqCpOrig": "rd1o00000000000000000000ffff0b81c0b4o1073",
}

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://mon.adp.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://mon.adp.com/static/redbox/login.html?TYPE=33554433&REALMOID=06-000e81a2-1e5a-10db-a395-e14c0b810000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-Uz3MmFlMtYXbbs4PyUg%2b8Qpa4qQTgAzkbzALwDsE1viMXj0fBx4BsHy3OVrQYonU&TARGET=-SM-HTTPS%3a%2f%2fmon%2eadp%2ecom%2fredbox%2flogin%2ehtml%3fREASON%3dERROR_TIMEOUT",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
}

data = {
    "user": "__REDACTED__",
    "password": "FAKE",
    "null": "on",
    "redirectUrl": "https://mon.adp.com/redbox/",
    "target": "https://mon.adp.com/redbox/",
    "qoSR5bIsEX-f": "A0dapMB-AQAAJ6HzDmYeUbugzNCncaS5s51YT_jcFLvRcU0pNGPLTDylHIF8AVugaa-uct61wH8AAOfvAAAAAA==",
    "qoSR5bIsEX-b": "u6qqn1",
    "qoSR5bIsEX-c": "AMDFosB-AQAAFghFVdD4oafo7MFSPl_XH-V57WWUPqaqcRGtzhqBR8LSpGOS",
    "qoSR5bIsEX-d": "AAaihIjBDKGNgUGASZAQhICS1WIagUfC0qRjkv_____Yki7PAGXAprI3m3cOn0MRzyz1H9I",
    "qoSR5bIsEX-z": "q",
    "qoSR5bIsEX-a": "wdjP0Bseo9hMt7y8czZhoqntqaXoCXYmTWsHiDyyKNi_IdsP3vyjZZ6SNoGO-H1Kot4L0lSaqhE0eHyfAGj1hehT5BM4UEn0ADLbM1Jk-FMJ-CeTYTaYnd_53qSFIxy5ylF_2iS_wsXw=lK41G15kDiS=vwP6u3YmWweRvg460UKf1FXPICS03cTqTPzOWgDUGewL9GckF-E=R4bM4VOT_pefyEE0h5el9JFF-2sDhbmqTo6tVWBp4KSk1NQ2Av6mQZKMjgectdLmz8aHkwNwKTDObDUJtuEW6VtFjkBKl_WXd=deTHCoXWD6mwhAYeORYck=kw3jlR_UXyizZqeONo-aIqqw6gY3lOZ4M_BPhKg7Bjn9IfQkSgVXQ06F3YS_4Oe2g9RXI0AIJHMQ7G0FgSetGBQTQ5oD7b7ZPZv3P4fRDsM3p2d0MWeAw_Z3TWK095y0NhFSpHbQ0wT5Bz9tqE8sdOU8S9GIL8GYXIVzuWFJJAMYk_slOOccwdnH=sfSuAhObXAMP0xU7EqtXdeosW0UVk389GSt3Jeu0nVRi=1ReEvw5x=3=Kiib27UCsY_O_CFs2D-9u3jkpecHoOdRkEqT69UtZMZBiMWDeQ27G1i_dJyXFE8zwg2bbVi0WwRuIZNLl614VjPDMDO-kRlI8-mMxL89XDfYuFt39wKnsp=RGA_kgT0Rs3x28yRKevBvkgZpPP1PBAP64gU-PpJpz4UdT-JHOMRudKpGwG8Y5ox-2YzBzSPpD-Y5Xq3asK4PGEKq0v_Bc6CfJ7L85iSkD0bKwZj-ktQmybwq6oRG9vZ82NTTsKjOjN2DGEjYaoAqCRqu3SonARudo7Dl-X-RNpizjFvR6e50lyyfKIbBMmHKFPXwfSaBJ9MVQO=EUHWbMMl5-si5P350Lg6tVx-kC-gn-OzhQAD-Tog8Jtx4nx53o3HPtcK9iTO6d4D-LLDNAIANGHO-Gs_9e9ZyVTzvgEHTH-FD2M5oAjzxWf0zOwsXfauYzNZW69lJCfQ7=8Lfs47VfQlF-3eclsby8IR8UhyWGVI=_eQYsXp3eejb-T4Utbz05d5NlGo7KdMPPwQbNg-=a3UgkjvKuKaoJyAtVBmidvvhoc4UuqzTAR6voh_lnBg7NY31995MUJUSmNRGKZsDV5U9FG77W8DhujORnkBQidHWq3Hx4_WHj06OEHGZTv60xK9vhICRG5hp067d_UAmOwFDkiDBvCjtSQfuNQqCjozlRlS539gz4JfVBMf7WsAksEVy523SRy2Jt=C0H1Hl3jo1K2E8GX_pRZv9CgN32lYpFb=KcVji0Tp=SHlQSeT5UjqkwVNio4uGOa4xoA4XYXWJQz5VYukEKcpH_Y094EulHS6Fy11dNsxbknyOveGKgYkj6tzfX2KU9HlW3sxmqPTo5fyJkez6B7mx_aenIP_xT3A11jJjeB2MwTS4oiZeddR91=3LWoe_da4=6bZyBvkWA8QvVyM5KURkMtvx45_mdcWXcOqT7D=2min4SeAHOsg0e2vCQ4O3AX2U9wPmDg6uexaKBf6JSHfBk8LoWC_=tFSbbER6yldzs9oKmF1fAQ8GA-zoLHfQJ9J3emA2tqO7OM5vFlMGIgtPpqnfsKZ8vNa79oOaRiH8F6-iWUnG1v1lsQV23aDqf0FSJyDpVH_j=wdlAk9_IQ8bIa7q26-1CfwtDcHhK47Tx8AodiYL3Z6_uMOEG4bADANjjdecK3X3UCB3oDKBPFzI_s95-RylWlUE10-t8vLaU522BVNWOM=ZjY6ssQPI6BMzNj15PeA621UCdBpbVXlLU4FMQYm=QVbED2o06Y7ZGNaz0YfD8nxeWHtk52YmlF9gEqXsMldzyyBJ7xq4uhcb=z1DfPwWuslYuKZgpuMwh-ICMb=DnwaUGog9-d0_fm6k_vMkb56N9ci7f0U=F0M9lXdvRZnF16qQ8mpT=F__3Ws6m7cBlN7whjPBM2gTGv3m3=kNh_aexYcq5GZbt33fk47pZWbat-D_suelDm2Aw_tJ6jZbmoAhMpEO9Qm__QljJo5stUYzQ-R6AjJcQxM0gHm1LwL1xnRtJsFYzhvpIKpF2c6sVbyKGddJcuc402ZSP85UN6xCbSpPFPO7qq4gJ5l9Pm=jMKplLIBiG=_iYnuY0PTOnz=pgjtYvRFSuyws9F=tzjfWcw_goUkGOqEi2-hRupIU_fzx173SyNH1Uk_S1l-DVSfgT_xlQta8VBv_=f6Iv2AP59sT08Kte62WtXTyN-BAkl9YYs3yO2cLK7EX=jPXA5o8LtH1E3zo==g11cBpgZnKXZCtC0O8Df8L3HfX1xZAWKyvW6g=SY0-0dHhj95_znVuYw7zpMRK4H5Ix8M7H0G4UEzqy04qjRJNVLzV7tEVtxyQCbzzlxlPszJBuQRj_w4PW6GBbcq=L9E2l-uxEJ0SNGMO7Nxpf36W4iWJ0=9_emwJfn5M7x6=mhTnqQIJVc0a=1xyf068y36UJPoAqhKtK5iSoAo7xi=y2acELq_7QgqxCnVFNymSUxh19xuFMv9PussW6Us_JQCkP3RHy8M7ZJ48ct5tmAa8oeRk8j5NGghBG3zOLJc40DoSH7gRSkhFszozo7Wq66A2-sc7aP57cDzdsdZekG3WVjhHQVIwP9wvwCmemAUOUqnNMSQcpqyvReW-_ClW7CBt_wkV1uE2_uDpo=N-CoH1WeLj6O0Q6FtDUof39sqPE5v1_U3Ld3g95eu2y_yxFbdefPFYEtfwjKyTekO52f0n5fKmAtHvX5fVlGm4lKbksEFCwRQmducutFe7oPJH2G541w9-Xi50pJMxwU8n_daIPOypP8QKQcc9M6bAY0uoRuwuf8uoUiCvlMoSxDqUCi7ZztnjDvIa2OJcdeUEu0TXG6SLLgy58C=wK77-4655CvS9QjmaQCultLD59ZoGJH4U9UsBglbIL=gEA8bbD9Efm5X8GhccfJL1Sh0QbLxDeHty4nXgNeeOYQBD-0UA578sxMeKVu6tlCQNLh2_C3RY=7zG8jvce8IJBy6MmoeGalGqggXLDQUsGJTURXthdU5dHHwdULOR=AvFfSUj1HTc2l9P_oZKRJgO=MMnK_caS1OqWXoWbsW7CkuwuiaE8nT_RZho04INYghxGQ_BMmX1LyovPXasP9DJkoRi3YIihuqJjvJ58K5ABiZVdv2swxZ2B6=dxoHWa6N=-iSSi5gccWk_BcoionNuxRkXu-F72TiGBx1kSmsPPRSxYhcS1vYY=ABnmXhSMa-Bp5ywlcLjv-_6RA7ZmywpBEZje_q6D5vm4bx9daaKvFsP16ROzXcNGSs9HWtt2ukvuOUf1iLyyy8qajUgyRgRa=h=yF1bynW8w-xPPydDGlDudxcBil9nRUOw9YkDykzg6sg1leipeL5BtDPVt77V46WPFQhOOFA4k6=tgefU9wYWEX96LYYNMcvaVcweuHsD7Pm6FmL6_TtJKgELaN_FSyJlI__s9xNEtNPYw7ubqG8Q-ki-xt=iUE9u5Pz6GieYs1wZXp==-pnclvtK8WdWeylpJc=RY0o5M3skEuCwum5JGgOJp=bUFRUbVhMczAe47C8mv0lEVTWHoEBmGEapa=MzyGhGwYEOxdlYY7Nf_unC1Z82dgYCMk6HtCzGtzJPCh=CgRW1Eli5-YoNgGv_MyjtfGis1I0As3ZLYZQDKF17msL5Mzw6GM9IcQz_J46ZVS22QQICIf5k_03UW3NMRCiexqYsYix29vSZDJhTkWzDz2-Gb7Qi3jcqCy=AdHxs1y1NptdxgjTIctvgavSlfJ4DvnQu3G5u=9abTY=RXlAzU8Ap-Ab0qlf_BtX1aC76BhOwjubWZiOp=k5jZNdHLdRYzVvioTfJCmN0ASTT69SYplsYlk=a_sVLVmNCv_z67tiEB7B7f7ipkvdaQ0jonW0RMVRSWR3WWJOo3eLiyMnttwUCDTIA5yBNyd3DXdBpMECDO83FMHIAvu0qmOulRF=p8JS02otdFXRZmCHAbqg1WivgNL7LndWVNwqlMTxC1PeTQQBT5osoqJ-hzwNtM04X_VwzYsisKwkkB=UybjLB7OaANtpqsQ6ZcjZ6QCsnGuXZfyXb7RhlVZXU-hetpDvH_w-UYnlQzS6upXxSLSyJfCL1n7Xs65k43FK6QX57tQhO=I-iQ7x6XIgYxuZdovAB465Czy=SCYUnfupUh=AuxLsnTdvGXZtt3F0SGyhWfqPtts2hfZUY8oPEUahD=4FeIwhIyYdeVT9j1B=XIadyg6Adn34yy1TKWyvUDGs=w7aW6hihouGPuViHiKidGX72ZWqb=BHfwH4hT4jzFemOqlJBzzcoqAzhInYVOx=5AA-E-_X4G5uMLRdkduVOd4dpEua26NJTPg5FHn1GD5_WlgRtHTpIASuKov9qGEyNmGBo2_hhpONC_1PGTNof22=YK2VwRy=Qyj-WwPWiY=m2yRTAgm0EIxpe6xzlqHyZbAMXD0gKl2eMtQv693uCk=nxQHPWleFXeP6gJQ6sTstt-OWuEEtz777mPnk45QlSIR9CRtPLudqDxKpLkMNnOkd8AZRAZxN0Wg9zIO0gSP=I5mdBDCOq84ssNoBHx0cZfj7QPWlQB1Bw05InayPAv6chAqPZb_-FDUFhvoxxHJk6a12FmRIpfu71WzOxn0pqUsA=TDlBVA9BVQYIp6XoCBtSbGlk_87T6fKH-nWpVfoUj89lmb8xjC6EE56cp6ywv9hWJUlu=YS-gy=vuzLj=WtmaRNvh89yvz7OXZmSHSCQJPd6Tx_XEDRKId=c8Aue47giVzL_CF1xGkj=j_2a43QS2VQtEncUFfx-7JNhSCvu4gmvXmNdZ=-wJDB91EKntPGl=8H64fUjKGW0eKxGwXJ4GtakYWMpnHMmjnFj62gYCxsIPfPpeYIp4EPsk4GCAixlBUtzSpj5Ue1uFJyGDXvwcWalCEhSYsF6Bx1qtCt0cxwlPddLxk3_GXMu1kk3SE1yqQW_PVjLekWi2gZQ3-IHAgikcgZZF3-IPQagudY7Nvu4xsp5Y7UlXs9l=w94L9aZhVbsfznIx8SDXRwcSUszlMz1UPIFhQXyPO7P1uUEG0JN_yNNLxjj9pAQlQhACjjcpamxlyOM13C99BCVJzbGzqeggWUIiwa5E4OqnYUpPfdxO3CujXm7uW6HpQxwYO=5FjTk980us-COZ3lMuVLmbGI-YbxqP5OPQ=ueyyaAT4MOQ-1Pf-XUYfa93q_3pokYadZpH9amAMncJv-IS",
}

session = requests.Session()
response_login = session.post(URL_LOGIN, headers=headers, cookies=cookies, data=data)

print(response_login.status_code)
print(json.dumps(dict(response_login.headers), indent=2))
print("URL :", response_login.url)
print("history")
for r in response_login.history:
    print(r.status_code)
    print(json.dumps(dict(r.headers), indent=2))
    print("URL :", r.url)
    print("\n")
