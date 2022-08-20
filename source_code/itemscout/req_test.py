import datetime
import json
import os
import time

import pandas as pd
import numpy as np
import requests

from tqdm import tqdm

file_datetime = datetime.datetime.now().strftime('%y%m%d_%H%M')
os.mkdir(f'./{file_datetime}')

excel_file = 'input.xlsx'

excel_dir = os.path.join(excel_file)

df_from_excel = pd.read_excel(excel_dir)
df_from_excel = df_from_excel.replace({np.nan: None})


def print_xlsx(list_, path, header, header_size):
    df = pd.DataFrame(list_, )
    writer = pd.ExcelWriter(f"{path}.xlsx", engine='xlsxwriter', )
    df.to_excel(writer, header=header, index=False)
    for column, column_length in zip(df, header_size):
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)
    writer.close()


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': '_tmp_vid=aad538c56543cb; ch-veil-id=09f6c9c3-d803-4a93-9bee-6001d5af468b; ch-session-18876=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiIxODg3Ni02MjU0YzRjOGNkMWI1NTYzYjRjZCIsImlhdCI6MTY1Mjg1NDQzMSwiZXhwIjoxNjU1NDQ2NDMxfQ.EVVh10_ZYr59068ALL96Sj3deTOPEBb0uflu-MAnIXY; _ga=GA1.2.1562557702.1652854423; _gid=GA1.2.542208610.1652854435; amp_752e71=CJi5TJWuwWv4EmFMj7hguh...1g3aspve0.1g3au33p4.5.0.5; _ga_PHL0WGSFWB=GS1.1.1652854423.1.1.1652855771.0',
    'Origin': 'https://itemscout.io',
    'Referer': 'https://itemscout.io/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

keyword = []
seaover = []
top40_sales = []
top40_count = []
top80_sales = []
top80_count = []

try:
    for idx, key in enumerate(tqdm(df_from_excel['키워드'], '키워드')):
        data = {
            'keyword': key,
        }

        data_id = json.loads(requests.post('https://api.itemscout.io/api/keyword', headers=headers, data=data).text)[
            'data']
        result = requests.get(f'https://api.itemscout.io/api/v2/keyword/stats/{data_id}', headers=headers).text
        seaover.append(json.loads(result)['data']['overseaProductPercent'])
        top40_sales.append(json.loads(result)['data']['statsFromNPay']['sales'])
        top40_count.append(json.loads(result)['data']['statsFromNPay']['saleCount'])
        top80_sales.append(json.loads(result)['data']['statsFromNPay']['salesFrom80'])
        top80_count.append(json.loads(result)['data']['statsFromNPay']['saleCountFrom80'])
        keyword.append(key)
        df_from_excel['키워드'].pop(idx)
        time.sleep(3)
except:
    pass

print_xlsx(pd.DataFrame([keyword, seaover,top40_sales,top40_count,top80_sales,top80_count]).T, f'./{file_datetime}/result',
           ['키워드', '해외상품비율', 'top40 매출', 'top40 판매량', 'top80 매출', 'top80 판매량'], [20, 20, 20, 20, 20, 20])
print_xlsx(pd.DataFrame(df_from_excel['키워드']),'./input',['키워드'],[20])

print(f'총 {len(seaover)}개의 수집이 완료되었습니다. 해당 창은 종료하셔도 좋습니다.')
time.sleep(3000)
