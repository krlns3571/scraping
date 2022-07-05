import requests

cookies = {
    'LENA-UID': '30e3ed15.5e10d837a3a3d',
    'SCOUTER': 'z6ile5iki7uq6e',
    'L-VISITOR': 'x18c4d9u8hkmgd',
    'JSESSIONID': 'D746CF60079B9454DB44305A12B78DD3.b98d5469542906361',
    'LOGNUM': '""',
    'LOGCATE': '""',
    'LOGSHOPCODE': '""',
    'LOGMODELNO': '""',
    'MYINFO': '"TMP_ID=20220610100358975"',
    '_gcl_au': '1.1.542642483.1654823041',
    '_ga': 'GA1.2.1873255587.1654823041',
    '_gid': 'GA1.2.960596589.1654823041',
    'MYTODAYGOODS': '"MODELNOS="',
    'MYSEARCHHISTORY2': '"SEARCHKEYWORD=S%3A%ED%82%A4%EB%B3%B4%EB%93%9C__06%EC%9B%9410%EC%9D%BC"',
    '_EXEN': '4',
    'AWSALB': 'bnbBy/6DvuwJ2Bo8XP47wMyf2UtBimm1suQtxyH8ZAotYpb7WwnbGJgXbdyjyB5Gnv38XY3wkGccKiyhVzTq6E3Yy/Q1/KoFTD7Y0dc2yOEffbJYZxCjIbIA+sVy',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'LENA-UID=30e3ed15.5e10d837a3a3d; SCOUTER=z6ile5iki7uq6e; L-VISITOR=x18c4d9u8hkmgd; JSESSIONID=D746CF60079B9454DB44305A12B78DD3.b98d5469542906361; LOGNUM=""; LOGCATE=""; LOGSHOPCODE=""; LOGMODELNO=""; MYINFO="TMP_ID=20220610100358975"; _gcl_au=1.1.542642483.1654823041; _ga=GA1.2.1873255587.1654823041; _gid=GA1.2.960596589.1654823041; MYTODAYGOODS="MODELNOS="; MYSEARCHHISTORY2="SEARCHKEYWORD=S%3A%ED%82%A4%EB%B3%B4%EB%93%9C__06%EC%9B%9410%EC%9D%BC"; _EXEN=4; AWSALB=bnbBy/6DvuwJ2Bo8XP47wMyf2UtBimm1suQtxyH8ZAotYpb7WwnbGJgXbdyjyB5Gnv38XY3wkGccKiyhVzTq6E3Yy/Q1/KoFTD7Y0dc2yOEffbJYZxCjIbIA+sVy',
    'Origin': 'http://www.enuri.com',
    'Referer': 'http://www.enuri.com/search.jsp?keyword=%ED%82%A4%EB%B3%B4%EB%93%9C',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {
    'from': 'search',
    'device': 'pc',
    'category': '',
    'tab': '1',
    'isDelivery': 'N',
    'isRental': 'Y',
    'pageNum': '1',
    'pageGap': '30',
    'sort': '2',
    'factory': '',
    'factory_code': '',
    'brand': '',
    'brand_code': '',
    'shopcode': '',
    'keyword': '%ED%82%A4%EB%B3%B4%EB%93%9C',
    'in_keyword': '',
    's_price': '0',
    'e_price': '0',
    'spec': '',
    'spec_name': '',
    'color': '',
    'isReSearch': 'N',
    'isTest': 'N',
    'prtmodelno': '',
    'isMakeshop': 'Y',
    'discount': '',
    'bbsscore': '',
}

response = requests.post('http://www.enuri.com/wide/api/listGoods.jsp', headers=headers, data=data, verify=False)