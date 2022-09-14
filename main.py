from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

data = {'data': []}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                        'AppleWebkit/537.36 '
                        '(KHTML, like Gecko) '
                        'Chrome/41.0.2228.0 '
                        'Safari/537.36'}


def parse(url, page, num):
    for i in range(1, num + 1):
        html = requests.get(url + page + str(i)).text

        soup = BeautifulSoup(html, 'html.parser')
        elems = soup.findAll('div', {"class": "item-wrap"})

        print(url + page + str(i))

        for el in elems:
            temp = {}

            temp['lot'] = el.find('strong').text if el.find('strong') is not None else "none"

            temp['price'] = el.find('span', {'class': 'price_val'}).text if el.find('span', {
                'class': 'price_val'}) is not None else 'none'

            temp['description'] = el.find('img', {'class': 'img-responsive'})['alt'] if \
                el.find('img', {'class': 'img-responsive'})['alt'] is not None else 'none '

            temp['imgUrl'] = el.find('img', {'class': 'img-responsive'})['src'] if \
                el.find('img', {'class': 'img-responsive'})['src'] is not None else 'none'

            art = el.find('span', {'class': 'article'})
            temp['№'] = art.find('span').text if art is not None else 'none'

            data['data'].append(temp)
            print(temp)


if __name__ == '__main__':
    if not os.path.exists('image'):
        os.makedirs('image')

    parse(os.getenv('URL') + os.getenv('AUCTION'), os.getenv('PAGE'), 13)

    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

    for j, el in enumerate(data['data']):
        try:
            time.sleep(0.3)
            urllib.request.urlretrieve(os.getenv('URL') + el['imgUrl'], 'image/Лот №{}.png'.format(j + 1))
            print('save {}'.format(el['lot']))
        except:
            time.sleep(0.3)
            urllib.request.urlretrieve(os.getenv('URL') + el['imgUrl'], 'image/Лот №{}.png'.format(j + 1))
            print('save {}'.format(el['lot']))
