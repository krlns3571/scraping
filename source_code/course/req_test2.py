import requests

cookies = {
    'CSRF3-Token': '1671346882.Z9LIW83SZZTVgJh9',
    '__204u': '7356721977-1670482882418',
    '__204r': '',
    'IR_gbd': 'coursera.org',
    'usprivacy': '1---',
    '_gcl_au': '1.1.1221592879.1670482899',
    '_rdt_uuid': '1670482899126.ec90a9c3-5097-4bab-bbe8-fc0e10d28c3f',
    'FPID': 'FPID2.2.BuquahRDNaVepq0PUztvHX8wQMH1ePi30C1WWf33FBM%3D.1670482899',
    'OneTrustWPCCPAGoogleOptOut': 'false',
    '_hjSessionUser_469298': 'eyJpZCI6ImYyZTI0MDI5LWYyNWQtNTM2MS1hMTY4LTRkM2EzNWRhMTNmOSIsImNyZWF0ZWQiOjE2NzA0ODI5NDExMjgsImV4aXN0aW5nIjp0cnVlfQ==',
    '_gid': 'GA1.2.1935763441.1670896898',
    'FPLC': 'K3g9RYMONMh6cFS7ikau%2FLkHHjvYyxoKSqJFLYoI%2FBOY5dRCTcPYX%2B7irdOmA1HRssHJqxls0o2GFHdA1KyAu3IfsVt4PT1RVGJx4uTPvQ%2ByBXDO5Tc19JfCdi%2FgTw%3D%3D',
    'g_state': '{"i_p":1671502345277,"i_l":3}',
    '_hjIncludedInSessionSample': '0',
    'IR_14726': '1670912631836%7C0%7C1670912631836%7C%7C',
    'OptanonConsent': 'isIABGlobal=false&datestamp=Tue+Dec+13+2022+15%3A23%3A51+GMT%2B0900+(%ED%95%9C%EA%B5%AD+%ED%91%9C%EC%A4%80%EC%8B%9C)&version=6.10.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=KR%3B11',
    'OptanonAlertBoxClosed': '2022-12-13T06:23:51.888Z',
    '_uetsid': '145655607a8a11ed925d63414734a893',
    '_uetvid': '297e28d076c611eda8ee2d4bc807bc52',
    '_ga': 'GA1.1.1724731528.1670482899',
    '_tq_id.TV-63455409-1.39ed': '6b35eecb3eb4a995.1670482900.0.1670912633..',
    '_ga_7GZ59JSFWQ': 'GS1.1.1670907803.5.1.1670913354.0.0.0',
    '__400v': 'bfaff60e-1794-4473-def7-88f38599afbd',
    '__400vt': '1670915019086',
}

headers = {
    'authority': 'www.coursera.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'CSRF3-Token=1671346882.Z9LIW83SZZTVgJh9; __204u=7356721977-1670482882418; __204r=; IR_gbd=coursera.org; usprivacy=1---; _gcl_au=1.1.1221592879.1670482899; _rdt_uuid=1670482899126.ec90a9c3-5097-4bab-bbe8-fc0e10d28c3f; FPID=FPID2.2.BuquahRDNaVepq0PUztvHX8wQMH1ePi30C1WWf33FBM%3D.1670482899; OneTrustWPCCPAGoogleOptOut=false; _hjSessionUser_469298=eyJpZCI6ImYyZTI0MDI5LWYyNWQtNTM2MS1hMTY4LTRkM2EzNWRhMTNmOSIsImNyZWF0ZWQiOjE2NzA0ODI5NDExMjgsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1935763441.1670896898; FPLC=K3g9RYMONMh6cFS7ikau%2FLkHHjvYyxoKSqJFLYoI%2FBOY5dRCTcPYX%2B7irdOmA1HRssHJqxls0o2GFHdA1KyAu3IfsVt4PT1RVGJx4uTPvQ%2ByBXDO5Tc19JfCdi%2FgTw%3D%3D; g_state={"i_p":1671502345277,"i_l":3}; _hjIncludedInSessionSample=0; IR_14726=1670912631836%7C0%7C1670912631836%7C%7C; OptanonConsent=isIABGlobal=false&datestamp=Tue+Dec+13+2022+15%3A23%3A51+GMT%2B0900+(%ED%95%9C%EA%B5%AD+%ED%91%9C%EC%A4%80%EC%8B%9C)&version=6.10.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=KR%3B11; OptanonAlertBoxClosed=2022-12-13T06:23:51.888Z; _uetsid=145655607a8a11ed925d63414734a893; _uetvid=297e28d076c611eda8ee2d4bc807bc52; _ga=GA1.1.1724731528.1670482899; _tq_id.TV-63455409-1.39ed=6b35eecb3eb4a995.1670482900.0.1670912633..; _ga_7GZ59JSFWQ=GS1.1.1670907803.5.1.1670913354.0.0.0; __400v=bfaff60e-1794-4473-def7-88f38599afbd; __400vt=1670915019086',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

response = requests.get('https://www.coursera.org/learn/game-theory-1', cookies=cookies, headers=headers)