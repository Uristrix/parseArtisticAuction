from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import xlsxwriter
import os
from dotenv import load_dotenv

load_dotenv()

data = {'data': []}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                        'AppleWebkit/537.36 '
                        '(KHTML, like Gecko) '
                        'Chrome/41.0.2228.0 '
                        'Safari/537.36'}


def parse(url, auction, page, num):
    for i in range(1, num + 1):
        html = requests.get(url + auction + page + str(i)).text

        soup = BeautifulSoup(html, 'html.parser')
        elems = soup.findAll('div', {"class": "item-wrap"})
        print(url + auction + page + str(i))

        for el in elems:
            temp = {}

            lot = el.find('a', {'class': 'btn-default'}, href=True)['href']
            _html = requests.get(url + lot)
            soup_lot = BeautifulSoup(_html.text, 'html.parser')

            temp['lot'] = soup_lot.find('strong').text if soup_lot.find('strong') is not None else ' '

            temp['description'] = soup_lot.find('h1', {'class': 'h2'}).text.replace(temp['lot'] + ' ', '').replace('\n',
                                                                                                                   '')

            temp['price'] = soup_lot.find('span', {'class': 'price_val'}).text if \
                soup_lot.find('span', {'class': 'price_val'}) is not None else ' '

            temp['info'] = list(
                filter(None, soup_lot.find('div', {'class': '-previewtext'}).find('p').text.split('\n')))

            temp['sales'] = soup_lot.find('div', {'class': 'sticker_recommend'}).text if \
                soup_lot.find('div', {'class': 'sticker_recommend'}) is not None else ' '

            img = soup_lot.find('ul', {'class': 'slides'}).findAll('a')
            for j in range(len(img)):
                img[j] = img[j]['href']
            temp['img'] = img

            data['data'].append(temp)
            print(temp)


if __name__ == '__main__':
    parse(os.getenv('URL'), os.getenv('AUCTION'), os.getenv('PAGE'), int(os.getenv('NUM')))

    workbook = xlsxwriter.Workbook('file.xlsx')
    worksheet = workbook.add_worksheet('Data')

    # Ширина колонок
    for i, el in enumerate([15, 50, 20, 50, 20]):
        worksheet.set_column(i, i, el)

    # Заголовок
    header = list(data['data'][0].keys())[:-1]
    print(header)
    for i, el in enumerate(header):
        worksheet.write(0, i, el)

    for i, el in enumerate(data['data']):
        for j, el2 in enumerate(el):
            if el2 == 'img':
                continue

            if el2 == 'info':
                worksheet.write(i + 1, j, ' '.join(el[el2]))
                continue

            worksheet.write(i + 1, j, el[el2])
    workbook.close()

    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

    if not os.path.exists('image'):
        os.makedirs('image')

    for i, el in enumerate(data['data']):
        try:
            if not os.path.exists('image/lot{}'.format(i + 1)):
                os.makedirs('image/lot{}'.format(i + 1))

            for j, el2 in enumerate(el['img']):
                try:
                    urllib.request.urlretrieve(os.getenv('URL') + el2, 'image/lot{}/{}.png'.format(i + 1, j + 1))
                    print('save {}_{}'.format(el['lot'], j + 1))
                except:
                    continue

        except:
            if not os.path.exists('image/lot{}'.format(i + 1)):
                os.makedirs('image/lot{}'.format(i + 1))

            for j, el2 in enumerate(el['img']):
                try:
                    urllib.request.urlretrieve(os.getenv('URL') + el2, 'image/lot{}/{}.png'.format(i + 1, j + 1))
                    print('save {}_{}'.format(el['lot'], j + 1))
                except:
                    continue
