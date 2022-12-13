import json

import requests


headers = {
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.coursera.org',
    'Referer': 'https://www.coursera.org/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# data = json.loads(
#     '{"requests":[{"indexName":"DO_NOT_DELETE_PLACEHOLDER_INDEX_NAME","params":"query=free&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="},{"indexName":"prod_all_launched_products_term_optimization","params":"query=free&hitsPerPage=12&maxValuesPerFacet=1000&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&ruleContexts=%5B%22ko%22%5D&facets=%5B%22topic%22%2C%22skills%22%2C%22productDifficultyLevel%22%2C%22productDurationEnum%22%2C%22entityTypeDescription%22%2C%22partners%22%2C%22allLanguages%22%5D&tagFilters="},{"indexName":"test_suggestions","params":"query=free&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="},{"indexName":"prod_degrees","params":"query=free&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="}]}')
# page = 0
# params = f"query=free&hitsPerPage=12&maxValuesPerFacet=1000&page={page}&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&ruleContexts=%5B%22ko%22%5D&facets=%5B%22topic%22%2C%22skills%22%2C%22productDifficultyLevel%22%2C%22productDurationEnum%22%2C%22entityTypeDescription%22%2C%22partners%22%2C%22allLanguages%22%5D&tagFilters="
# data['requests'][1]['params'] = params
# data = json.dumps(data)
page = 0
topic = "Social%20Sciences"
while True:
    data = json.loads(
        '{"requests":[{"indexName":"DO_NOT_DELETE_PLACEHOLDER_INDEX_NAME","params":"query=free&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="},{"indexName":"prod_all_launched_products_term_optimization","params":"query=free&hitsPerPage=12&maxValuesPerFacet=1000&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&ruleContexts=%5B%22ko%22%5D&facets=%5B%22topic%22%2C%22skills%22%2C%22productDifficultyLevel%22%2C%22productDurationEnum%22%2C%22entityTypeDescription%22%2C%22partners%22%2C%22allLanguages%22%5D&tagFilters="},{"indexName":"test_suggestions","params":"query=free&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="},{"indexName":"prod_degrees","params":"query=free&page=0&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&facets=%5B%5D&tagFilters="}]}')

    params = f"""query=free&hitsPerPage=1000&maxValuesPerFacet=1000&page={page}&highlightPreTag=<ais-highlight-0000000000>&highlightPostTag=</ais-highlight-0000000000>&clickAnalytics=true&facets=["isCreditEligible","topic","skills","productDifficultyLevel","productDurationEnum","entityTypeDescription","partners","allLanguages"]&tagFilters=&facetFilters=[["topic:{topic}"]]"""
    data['requests'][1]['params'] = params
    data = json.dumps(data)
    response = requests.post(
        'https://lua9b20g37-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.30.0%3Breact-instantsearch%205.2.3%3BJS%20Helper%202.26.1&x-algolia-application-id=LUA9B20G37&x-algolia-api-key=dcc55281ffd7ba6f24c3a9b18288499b',
        headers=headers,
        data=data,
    )
    # [print('https://www.coursera.org' + x['objectUrl']) for x in json.loads(response.text)['results'][1]['hits']]
    if json.loads(response.text)['results'][1]['hits']:
        with open('links2.txt', 'a', encoding='utf8') as f:
            for x in json.loads(response.text)['results'][1]['hits']:
                f.write('https://www.coursera.org' + x['objectUrl']+"\n")
    else:
        print(page)
        break
    page += 1
    # print(page)
