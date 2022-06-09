import datetime
import json
import time

import requests

cookies = {
    'token': 'b701a148023548febaaec25977ad3f8f',
    '_ga': 'GA1.2.881351732.1654738310',
    '_gid': 'GA1.2.885428043.1654738310',
    '_gcl_au': '1.1.1114995989.1654738311',
    '_gat': '1',
    'amplitude_id_ee9e97f46fa77da052305bb94e327b88gangnamunni.com': 'eyJkZXZpY2VJZCI6ImYxNmVmN2Q3LTM5NzQtNDcwNi05ZTgxLWQzNmY5MTc0Y2U5YVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY1NDczODMxMDYyMCwibGFzdEV2ZW50VGltZSI6MTY1NDczODM3OTY5NSwiZXZlbnRJZCI6OSwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjl9',
    '_dd_s': 'rum=1&id=39f265f0-6ccd-4c9e-8a9b-8ab23c05c32c&created=1654738978123&expire=1654738978123',
}

headers = {
    'authority': 'www.gangnamunni.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR',
    'authorization': 'b701a148023548febaaec25977ad3f8f',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'token=b701a148023548febaaec25977ad3f8f; _ga=GA1.2.881351732.1654738310; _gid=GA1.2.885428043.1654738310; _gcl_au=1.1.1114995989.1654738311; _gat=1; amplitude_id_ee9e97f46fa77da052305bb94e327b88gangnamunni.com=eyJkZXZpY2VJZCI6ImYxNmVmN2Q3LTM5NzQtNDcwNi05ZTgxLWQzNmY5MTc0Y2U5YVIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY1NDczODMxMDYyMCwibGFzdEV2ZW50VGltZSI6MTY1NDczODM3OTY5NSwiZXZlbnRJZCI6OSwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjl9; _dd_s=rum=1&id=39f265f0-6ccd-4c9e-8a9b-8ab23c05c32c&created=1654738309632&expire=1654739293144',
    'referer': 'https://www.gangnamunni.com/reviews?eventId=2876',
    'review-token': '4784255c9480acf9159ca02b0a08f8f3:c86989783164e913fff6d22af35802d8bc9a321296a48a106d6aa7dd2b4682dc72c68f3187706fdad3a85c6c58d71768',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}



start = 0

while True:
    params = {
        'eventId': '2876',
        'start': f'{start}',
        'length': '20',
    }
    response = requests.get('https://www.gangnamunni.com/api/reviews', params=params, cookies=cookies, headers=headers)
    time.sleep(1)
    try:
        print(datetime.datetime.now())
        print(json.loads(response.text)['data'][0]['contents'])
        start += 20
    except:
        start = 0
