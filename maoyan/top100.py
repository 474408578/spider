import json
import time
import requests
import re

from requests import RequestException

'''
top100电影的排名，图片，标题，演员，上映时间，评分
排名：'<dd>.*?board-index.*?>(.*?)</i>'
图片：'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"'
标题：'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?title="(.*?)"'
演员：'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?title="(.*?)".*?"star.*?>(.*?)<'
上映时间：'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?title="(.*?)".*?"star.*?>(.*?)<.*?releasetime.*?>(.*?)</p>'
评分：'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?title="(.*?)".*?"star.*?>(.*?)<.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)\..*?fraction.*?>(.*?)</i>.*?</dd>'
'''


def get_one_page(url):
    try:
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
    


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?title="(.*?)".*?"star.*?>(.*?)<.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)\..*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + '.' + item[6].strip(),
        }


# def write_to_file(content):
#     with open('result.txt', 'a') as f:
#         print(type(json.dumps(content)))
#         f.write(json.dumps(content, ensure_ascii=False).encode('utf-8'))
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    for i in range(0, 100, 10):
        main(i)
        time.sleep(1)
