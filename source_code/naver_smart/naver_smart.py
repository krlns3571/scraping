# import requests
#
# # cookies = {
# #     'NNB': 'PAQF2L7C6DFWA',
# #     'AD_SHP_BID': '9',
# #     'ASID': '36b4314a0000017aa8b13d1800005d61',
# #     'MM_NEW': '1',
# #     'NFS': '2',
# #     'NDARK': 'Y',
# #     'autocomplete': 'use',
# #     '_ga_1BVHGNLQKG': 'GS1.1.1649754168.4.0.1649754196.0',
# #     'NV_WETR_LAST_ACCESS_RGN_M': '"MTQxMTA2MzA="',
# #     'NV_WETR_LOCATION_RGN_M': '"MTQxMTA2MzA="',
# #     'nid_inf': '1764228022',
# #     'NID_AUT': 'nA5vPlUxT/q10CWr843fmjLqVCMWoC4sod9BAogmDQpPKiJCfhmkPru+hihZMMqt',
# #     'NID_JKL': 'viT11G2dDPUH7lXr1sbyCvZTa6lGIya977Nqbkh/Ino=',
# #     '_ga': 'GA1.2.1439908789.1623999453',
# #     '_ga_7VKFYR6RV1': 'GS1.1.1651198031.81.1.1651198039.52',
# #     'nx_ssl': '2',
# #     'page_uid': 'hFGQXdp0JXosscfX43VssssstlV-347157',
# #     'BMR': 's=1652661592780&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dlsm_origin%26logNo%3D120210926900&r2=https%3A%2F%2Fwww.google.com%2F',
# #     'sus_val': 'L1IYHqJdITRh7jwh+2+YL0OW',
# #     'NID_SES': 'AAABoDtcStuc8EZYrUiXlv6ByoUBeuGqUUKamy+wnWZ3bTW6fYFLUR2PtFYdyY3QYIdY9kVyKHrf3Pkpjid7BO3fulxFtEB8wD4KNfUrMEOxTsvHlzpeJJYWdg7ioz64fRLYbWmGuDgLidiR5yjzeR+BV0+BycpVu2+YIPS3EEe7JapheGJ8o/FR0VEeSX7CfigQolHTEqZgI7FRqlCFNgaZqB6aEY9HmVAqQQCub73m9RWB4Q3YlkgOpPuU3/m3lW3RkFOrAkOwGR3Fa8kVo02v0pLF/ywBZz91T4JE0+4gSCK5SXQ/2jPvIOxWd7miFnaKy2dlq9I2RfmDpYjSdE5MqwCBpnWXOq0p0ihTYc0WWnwd9vwhviG8leI9RLkqlaBI0tbKY8P9DUWZ6jwBezqu+rwGy6o6zXvSS8iRidOi1L9cAt1ZpNK04Fn9RLVDB4zWKJYPVjLlW6v8ezSPN5J7vWt/BMJA7pNxct1Ra+ElExQ9ChR9Xz7Hb2gUKZny8QAZWC0UxRickzMqhJmvbrBKUC5wrihUDEk6+PAJpgURdeCF',
# #     'spage_uid': 'hFGQXdp0JXosscfX43VssssstlV-347157',
# # }
#
# headers = {
#     'authority': 'search.shopping.naver.com',
#     'accept': 'application/json, text/plain, */*',
#     'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
#     # Requests sorts cookies= alphabetically
#     # 'cookie': 'NNB=PAQF2L7C6DFWA; AD_SHP_BID=9; ASID=36b4314a0000017aa8b13d1800005d61; MM_NEW=1; NFS=2; NDARK=Y; autocomplete=use; _ga_1BVHGNLQKG=GS1.1.1649754168.4.0.1649754196.0; NV_WETR_LAST_ACCESS_RGN_M="MTQxMTA2MzA="; NV_WETR_LOCATION_RGN_M="MTQxMTA2MzA="; nid_inf=1764228022; NID_AUT=nA5vPlUxT/q10CWr843fmjLqVCMWoC4sod9BAogmDQpPKiJCfhmkPru+hihZMMqt; NID_JKL=viT11G2dDPUH7lXr1sbyCvZTa6lGIya977Nqbkh/Ino=; _ga=GA1.2.1439908789.1623999453; _ga_7VKFYR6RV1=GS1.1.1651198031.81.1.1651198039.52; nx_ssl=2; page_uid=hFGQXdp0JXosscfX43VssssstlV-347157; BMR=s=1652661592780&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dlsm_origin%26logNo%3D120210926900&r2=https%3A%2F%2Fwww.google.com%2F; sus_val=L1IYHqJdITRh7jwh+2+YL0OW; NID_SES=AAABoDtcStuc8EZYrUiXlv6ByoUBeuGqUUKamy+wnWZ3bTW6fYFLUR2PtFYdyY3QYIdY9kVyKHrf3Pkpjid7BO3fulxFtEB8wD4KNfUrMEOxTsvHlzpeJJYWdg7ioz64fRLYbWmGuDgLidiR5yjzeR+BV0+BycpVu2+YIPS3EEe7JapheGJ8o/FR0VEeSX7CfigQolHTEqZgI7FRqlCFNgaZqB6aEY9HmVAqQQCub73m9RWB4Q3YlkgOpPuU3/m3lW3RkFOrAkOwGR3Fa8kVo02v0pLF/ywBZz91T4JE0+4gSCK5SXQ/2jPvIOxWd7miFnaKy2dlq9I2RfmDpYjSdE5MqwCBpnWXOq0p0ihTYc0WWnwd9vwhviG8leI9RLkqlaBI0tbKY8P9DUWZ6jwBezqu+rwGy6o6zXvSS8iRidOi1L9cAt1ZpNK04Fn9RLVDB4zWKJYPVjLlW6v8ezSPN5J7vWt/BMJA7pNxct1Ra+ElExQ9ChR9Xz7Hb2gUKZny8QAZWC0UxRickzMqhJmvbrBKUC5wrihUDEk6+PAJpgURdeCF; spage_uid=hFGQXdp0JXosscfX43VssssstlV-347157',
#     'referer': 'https://search.shopping.naver.com/allmall',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
# }
#
# params = {
#     'page': '26',
#     'sortingOrder': 'prodClk',
# }
#
# response = requests.get('https://search.shopping.naver.com/allmall/api/allmall', params=params, headers=headers)

import requests

cookies = {
    'NNB': 'PK7DSCRLYOMWE',
    'NDARK': 'Y',
    'nx_ssl': '2',
    'nid_inf': '1832816580',
    'NID_AUT': 'yYwXtW3vNwipOkQWIFWAAB4mJu2vGvfm5H4RaAyBedYCoGjC4kcRIszcsl+xRT5/',
    'NID_JKL': '3EwaVKjrI/WbCsA6BWvp1aSKEuxf54od17O/b7oYAZA=',
    'ncpa': '752773|l4djy7zc|d9b94ada8b618bdfd54f50eb928a0d77c7163595|s_33fb081ad95f|dca1bdfbf9174ec3f0ce4b11a2161391feeafc36',
    '_ga': 'GA1.2.1316686313.1654849442',
    '_gid': 'GA1.2.799388018.1655348399',
    '_ga_7VKFYR6RV1': 'GS1.1.1655348399.7.1.1655348430.29',
    'BMR': '',
    'sus_val': 'fr4aqF9d1pP0mhUT6O0YfNDT',
    'autocomplete': 'use',
    'AD_SHP_BID': '18',
    '_naver_usersession_': 'cB1v/+iDEPOL3v9JpybC78W+',
    'NID_SES': 'AAABo15VQTzJ9PYHh5uiUZ0ZQ2sR9vN6OhtqUjHmK022cCNwzaYpPfH/JVay5yKq24sKFGhN/O31bo/mx6W8KPbFVyYRSziIEvvU1A57nU+j4hjpJ5P3C0shnI9T3th0VAIl6aTnx6zNxrts0KG5bhzb1cf0oPFuYBase1NQpms5DQOxBwZ5miJFKtiuuc7nX8Ux6xtjvLv8MTvV6KeKFZPgUZiUDAjENJ20IDfsGzfk4o3scFM4A8AdzVH43UJV8ncQiHVpQ0F6npT2xGvtij3TzAFoLiNEDIz5zSE3FM/WAitnWWALfSaXzxoTFE4HkEXAWEhnw6/6C66NAKNio9NQ8XqwsEO9CC1kZ0VHKCNbJYhgfeEwy+XVLQO5AA6wDJ276m4WT+/+m+o6jA7DAqx5dZ6OwMB6M8+UY6ZBjrtRorxObxUhgGxDjqW+f4/P1qkU2jh+3KH37l7Cq3LuDVHjci0SgUTMLkOeonApfPzwXesMMGlqN7BW5dkER2bdp9EfGA0xYGXdGm6c5LXn5Ycj5t+RlqNQlCgpwBn7GC3Ko9cJZWbBbu2XJOrsvaRnmv7/iw==',
    'page_uid': 'hqrNudprvTVssl+x2j0ssssssBK-228726',
    'spage_uid': 'hqrNudprvTVssl%2Bx2j0ssssssBK-228726',
}

headers = {
    'isSmartStore': 'Y',
    'page': '44',
    'sortingOrder': 'prodClk',
}


response = requests.get('https://search.shopping.naver.com/allmall/api/allmall', params=params, cookies=cookies, headers=headers)