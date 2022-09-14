from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import time
category = [
    'books',
    'coins',
    'painting',
    'decorativeart',
    'antiquearm',
    'autographs',
    'bonds',
    'medals',
    'marks',
    'stamps'
]

data = {'data': []}
URL = 'https://artistic-auction.ru'
Auction = '/auctions/proshedshie-auktsiony/auktsion-russkogo-i-zapadnoevropeyskogo-iskusstva-23-07-2022'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT '
                        '6.1) AppleWebkit/537.36 ('
                        'KHTML, like Gecko) '
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
    parse(URL+Auction, '/?PAGEN_1=', 13)

    for j, el in enumerate(data['data']):
        time.sleep(0.3)
        urllib.request.urlretrieve(URL+el['imgUrl'], 'image/Лот №{}.png'.format(j+1))
        print('save {}'.format(el['lot']))

    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
