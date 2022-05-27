import json
import re
from datetime import datetime

from pytz import timezone

import requests
from bs4 import BeautifulSoup


def parse_review(j) -> list:
    # data_dict = copy.deepcopy(data_column_dict)
    # data_dict.update({
    #     "platform_name": 'googleplay',
    #     "platform_form": 'app',
    #     "platform_id": self.app_id,
    #     "keyword_id": self.keyword_id,
    #     "platform_title": self.app_dict['platform_title'],
    #     "article_title": self.app_dict['article_title'],
    # })
    review_list = []

    '''review'''
    try:
        review_id = j[0]
        username = j[9][1]
        user_photo = j[9][3][0][3][2]
        published_date = datetime.fromtimestamp(j[5][0])
        content = j[4]
        rate = j[2]
        like = j[6]
        url = 'https://play.google.com/store/apps/details?id={appid}&reviewId={reviewid}' \
            .format(appid="com.kakao.talk", reviewid=review_id)
    except KeyError as e:
        pass
        # log.error("Can't parse 'review' json format")
        # log.debug(e.__str__())

    else:
        # review_dict = copy.deepcopy(data_dict)
        aa = {
            "article_form": 'body',
            "article_id": review_id,
            "article_nickname": username,
            "article_order": 0,
            "article_url": url,
            "article_date": published_date,
            "article_data": content,
            "reply_url": url,
            "article_profileurl": user_photo,
            "etc": json.dumps({'rate': rate, 'like': like}),
        }
        # review_list.append(review_dict)
        review_list.append(aa)
        '''reply of review(from dev team)'''
        try:
            dev_name = j[7][0]
            dev_content = j[7][1]
            dev_published_date = datetime.fromtimestamp(j[7][2][0])

        except TypeError:
            '''no reply from dev team'''
            pass

        else:
            # reply_dict = copy.deepcopy(data_dict)
            aa = {
                "article_form": 'reply',
                "article_order": 0,
                "article_id": dev_name,
                "article_nickname": dev_name,
                "article_parent": username,
                "article_url": url,
                "article_date": dev_published_date,
                "article_data": dev_content,
                "reply_url": url,
                # "article_profileurl": app_dict["article_profileurl"],
            }
            review_list.append(aa)
            # review_list[0]['article_order'] += 1
            # review_list.insert(0, reply_dict)

    return review_list

def str_to_datetime(date_from_mysql):
    obj_datetime = datetime.combine(date_from_mysql, datetime.min.time())
    return replace_tz(obj_datetime)


def replace_tz(obj_datetme):
    return obj_datetme.replace(tzinfo=timezone('Asia/Seoul'))

def get_r_args(page_token=None):
    sort = {
        'NEWEST': 2,
        'RATING': 3,
        'HELPFULNESS': 1
    }

    if page_token is None:
        page_token = 'null'
    else:
        page_token = r'\"' + page_token + r'\"'

    args = {
        'url': 'https://play.google.com/_/PlayStoreUi/data/batchexecute',

        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        'params': {
            'f.sid': '-697906427155521722',
            'bl': 'boq_playuiserver_20190903.08_p0',
            'hl': 'ko',
            'gl': 'kr',
            'soc-app': '121',
            'soc-platform': '1',
            'soc-device': '1',
            '_reqid': '1065213',
            'rpcids': 'qnKhOb'
        },
        'data': {
            'f.req': r'[[["UsvDTd","[null,null,[2,{sort},'
                     r'[{numOfReviewsPerRequest},null,{token}],null,[]],'
                     r'[\"{appid}\",7]]",null,"generic"]]]'
                     r''.format(sort=sort['NEWEST'],
                                numOfReviewsPerRequest=100,
                                token=page_token,
                                appid="com.kakao.talk",
                                )
        },
        'allow_redirects': True,
    }

    return args


def strip_text_from_tag(soup_tag, default=None):
    try:
        stripped = soup_tag.text.strip()
    except AttributeError:
        stripped = default
    return stripped

def get_etc(soup):
    etc = []
    star_class, media_class, img_class, video_class = 'BHMmbe', 'SgoUSc', 'Q4vdJd', 'MSLVtf'

    etc.append({
        'rate': strip_text_from_tag(
            soup.find('div', attrs={'class': star_class}),
            default=''
        )
    })

def get_json(res):

    emoji_escape = r'\\\\'
    string_double_quote = r'\\\"'
    double_quote = r'\"'
    tmp_str_d_quote = r'***str_d_q***'
    tmp_d_quote = r'***d_q***'

    context = re.search(r'"(\[\[.*\]\])"', res.text).group(1)
    no_emoji_escape = context.replace(emoji_escape, '')
    tmp_context = no_emoji_escape.replace(string_double_quote, tmp_str_d_quote).replace(double_quote, tmp_d_quote)
    no_escape = tmp_context.replace('\\n', '').replace('\\', '')
    result = no_escape.replace(tmp_str_d_quote, r'\"').replace(tmp_d_quote, r'"')

    try:
        return json.loads(result)
    except ValueError as e:
        try:
            r_gdict = re.search(r'char\s(?P<error_index>\d+)\)', e.__str__()).groupdict()
            err_index = int(r_gdict['error_index'])
            err_context = result[err_index - 100: err_index + 100]

            # log.error('json parsing error')
            # log.debug('error context : ' + err_context)

        except KeyError as e:
            pass
        # log.debug(e.__repr__())

        return None

url = "https://play.google.com/store/apps/details?id=com.kakao.talk"
res = requests.get(url, headers={'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6'})


soup = BeautifulSoup(res.text, 'lxml')
app_name_class, description_class, app_img_class = 'AHFaub', 'sngebd', 'xSyT2c'

app_name = strip_text_from_tag(soup.find('h1', attrs={'class': app_name_class}), default=None)
description = strip_text_from_tag(soup.find('div', attrs={'jsname': description_class}), default=None)
etc = get_etc(soup)
url = "https://play.google.com/store/apps/details?id=" + "com.kakao.talk"
try:
    app_img = soup.find('div', attrs={'class': app_img_class}).img['src']
except (AttributeError, KeyError, TypeError):
    app_img = None

# app_dict = copy.deepcopy(data_column_dict)
aa = {
    "article_form": 'body',
    # "platform_id": self.app_id,
    # "keyword_id": self.keyword_id,
    # "article_id": self.app_id,
    "article_url": url,
    "article_nickname": app_name,
    "article_data": description,
    "platform_title": app_name,
    "article_profileurl": app_img,
    "article_title": app_name,
    "etc": etc,
    "article_date": None,  # set after review crawling
    "article_order": None,  # set after review crawling
}
page = 1


page_token = None
while True:
    args = get_r_args(page_token)
    res = requests.post(**args)

    s_date = datetime.strptime('2022-05-01','%Y-%m-%d')
    e_date = datetime.strptime('2022-05-25','%Y-%m-%d')

    j = get_json(res)

    if j is not None:

        for review in j[0]:
            published_time = replace_tz(datetime.fromtimestamp(review[5][0]))
            parsed_review = parse_review(review)
            # if s_date <= published_time <= e_date:
            #     parsed_review = parse_review(review)
            #     # review_list.extendleft(parsed_review)
            # elif published_time < s_date:
            #     working = False
            #     break
            # elif e_date < published_time:
            #     continue
            print(parsed_review)
        page_token = j[1][1]
        page += 1

        # log.info('page %d, total reviews %d', page, len(review_list))
