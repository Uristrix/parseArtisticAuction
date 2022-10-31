from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import xlsxwriter
import os
import re
from dotenv import load_dotenv

load_dotenv()

data = {'data': []}

header_url = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                            'AppleWebkit/537.36 '
                            '(KHTML, like Gecko) '
                            'Chrome/41.0.2228.0 '
                            'Safari/537.36'}
classification = [
    {'class': '1.1', 'words': ['картина', 'картины', 'темпера', 'холст', 'акрил']},
    {'class': '1.2', 'words': ['рисунок', 'рисунки', 'акварель', 'гуашь', 'карандаш', 'картон', 'бумага']},
    {'class': '1.3', 'words': ['икона', 'иконы']},
    {'class': '1.4', 'words': ['печатная графика', 'печатные графики', 'шелкография', 'ксилография']},
    {'class': '1.5', 'words': ['плакат', 'плакаты']},
    {'class': '1.6', 'words': ['фотография', 'фотографии']},
    {'class': '2.1', 'words': ["фарфор", "стекло", "керамика", "фаянс"]},
    {'class': '2.2', 'words': ['бронза', 'бронзы']},
    {'class': '2.3', 'words': ["художественное литье", "металл", "оловянная утварь"]},
    {'class': '3.1', 'words': ['столовые приборы', 'лопаточки']},
    {'class': '3.2', 'words': ['тарелки', 'блюдо']},
    {'class': '3.3', 'words': ['посуда для питья', 'чашка', 'кружка']},
    {'class': '3.4', 'words': ['подсвечник', 'подсвечники']},
    {'class': '3.5', 'words': ['настольное украшение']},
    {'class': '3.6', 'words': ['мелочи']},
    {'class': '4.1', 'words': ['браслеты', "браслет"]},
    {'class': '4.2', 'words': ["кольца", "кольцо"]},
    {'class': '4.3', 'words': ["серьги", "серьга"]},
    {'class': '4.4', 'words': ["ожерелье", "ожерелья", 'подвеска', 'подвески']},
    {'class': '4.5', 'words': ["булавки", "заколки", 'броши', "булавка", "заколка", 'брошь']},
    {'class': '4.6', 'words': ["часы"]},
    {'class': '4.7', 'words': ["бижутерия", "бижутерии"]},
    {'class': '4.8', 'words': ["камни", "камень"]},
    {'class': '4.9', 'words': ["мужские украшения", "мужское украшение"]},
    {'class': '5.1', 'words': ["монета", "монеты"]},
    {'class': '5.2', 'words': ["деньги"]},
    {'class': '5.3', 'words': ["марки", "марка"]},
    {'class': '6', 'words': ["книги", "карты", "рукописи", "книга", "карта", "рукопись"]},
    {'class': '7.1', 'words': ["реклама", "открытки", "карточки", "рекламы", "бумаги", "открытка", "карточка"]},
    {'class': '7.2', 'words': ["автограф", "афиографы"]},
    {'class': '7.3', 'words': ["армия", "война"]},
    {'class': '7.3.1', 'words': ["награда", "награды"]},
    {'class': '7.3.2', 'words': ["оружие"]},
    {'class': '7.3.3', 'words': ["форма и аксессуары"]},
    {'class': '7.4', 'words': ["часы"]},
    {'class': '7.5', 'words': ["окаменелости", "минералы", "окаменелость", "минерал"]},
    {'class': '7.6', 'words': ["научные приборы", "музыкальные инструменты"]},
    {'class': '7.7', 'words': ["кутюр", "мода"]},
    {'class': '7.8', 'words': ["спорт", "рыбалка", "охота"]},
    {'class': '7.9', 'words': ["электронника"]},
    {'class': '7.10', 'words': ["исторические", "политические", "исторический", "политический"]},
    {'class': '8.1', 'words': ["стол", "столы"]},
    {'class': '8.2', 'words': ["стулья", "кресла", 'диваны', 'скамейки', "стул", "кресло", 'диван', 'скамейка']},
    {'class': '8.3', 'words': ["декор", "аксессуар", "зеркало", "зеркала", 'дерево', 'гипс']},
    {'class': '8.4', 'words': ["лампа", "лампы", "люстра", "люстры"]},
    {'class': '8.5', 'words': ["ковёр", "ковры", "коврик", "коврики"]},
    {'class': '8.6', 'words': ["кровать", "кровати"]},
]

def parse(url, auction, page, num):
    l = 0
    for i in range(1, num + 1):
        html = requests.get(url + auction + page + str(i)).text

        soup = BeautifulSoup(html, 'html.parser')
        elems = soup.findAll('div', {"class": "item-wrap"})
        print(url + auction + page + str(i))

        for el in elems:
            temp = {}
            lot = el.find('div', {'class': 'title'}).find('a', href=True)['href']
            _html = requests.get(url + lot)
            soup_lot = BeautifulSoup(_html.text, 'html.parser')

            l += 1
            temp['lot'] = soup_lot.find('strong').text if soup_lot.find('strong') is not None else "Лот №{}".format(l)

            temp['description'] = soup_lot.find('h1', {'class': 'h2'}).text.replace(temp['lot'] + ' ', '').replace('\n','') if soup_lot.find('h1', {'class': 'h2'}) is not None else ' '

            temp['price'] = soup_lot.find('span', {'class': 'price_val'}).text if \
                soup_lot.find('span', {'class': 'price_val'}) is not None else ' '

            temp['info'] = list(
                filter(None, soup_lot.find('div', {'class': '-previewtext'}).find('p').text.split('\n')))

            temp['sales'] = soup_lot.find('div', {'class': 'sticker_recommend'}).text if \
                soup_lot.find('div', {'class': 'sticker_recommend'}) is not None else ' '

            temp['article'] = el.find('span', {'class': 'article'}).find('span').text \
                if el.find('span', {'class': 'article'}) is not None \
                else list(filter(None, soup_lot.find('div', {'class': '-previewtext'}).text.split('\n')))[-1] \
                if len(list(filter(None, soup_lot.find('div', {'class': '-previewtext'}).text.split('\n')))[-1]) < 15 \
                else temp['lot']

            img = soup_lot.find('ul', {'class': 'slides'}).findAll('a')
            img_temp = []
            for j in range(len(img)):
                img_temp.append({'url': img[j]['href'], 'article': temp['article'] if len(img) == 1 else temp['article'] + '-' + chr(ord('а') + j)})

            temp['img'] = img_temp

            data['data'].append(temp)
            print(temp)

def create_xlsx():
    workbook = xlsxwriter.Workbook('file.xlsx')
    worksheet = workbook.add_worksheet('Data')
    style1 = workbook.add_format({
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '00AEFF',
        "font_color": "white"
    })

    style2 = workbook.add_format({
        'bold': 1,
        'border': 2,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': 'F0FFFF',
        'text_wrap': 1
    })

    # Ширина колонок
    for i, el in enumerate([15 for i in range(8)] + [50, 15, 20, 20, 50]):
        worksheet.set_column(i, i, el)

    # Заголовок
    header = ['лот', 'класс/подкласс', 'автор', 'регион', 'наимнование', 'год', 'цена', 'TTX', 'описание', 'фото', 'проданные лоты', 'ключевые слова', 'доп...']

    for i, el in enumerate(header):
        worksheet.write(0, i, el, style1)

    for i, el in enumerate(data['data']):
        descr = el['description'].split('.')
        descr = list(filter(None, descr))
        while ' (?)' in descr:
            descr.remove(' (?)')

        # Лот
        worksheet.write(i + 1, 0, el['lot'], style2)

        # Автор
        worksheet.write(i + 1, 2, descr[0], style2)

        # Год
        worksheet.write(i + 1, 5, descr[len(descr) - 1], style2)

        descr = descr[1:-1]

        # Регион
        if len(descr) >= 2:
            worksheet.write(i + 1, 3, descr[0], style2)
            descr = descr[1:]
        else:
            worksheet.write(i + 1, 3, '', style2)

        # Наименование
        worksheet.write(i + 1, 4, ''.join(descr), style2)

        # Цена
        worksheet.write(i + 1, 6, el['price'].replace(' ₽', ''), style2)

        # ттх
        ttx = re.sub(r'\.\s$|\.$', '', el['info'][0])
        worksheet.write(i + 1, 7, ttx, style2)

        # Класс
        class_ = []
        info_ = ttx.lower()
        for t1 in classification:
            for t2 in t1['words']:
                if info_.find(t2) != -1:
                    class_.append(t1['class'])
                    break

        worksheet.write(i + 1, 1, '\n'.join(class_), style2)

        # Описание
        info = '\n'.join(el['info'])
        info = info.replace(el['info'][0], '')
        if len(el['img']) != 0:
            art = el['img'][0]['article']
            art = re.sub(r'-[а-я]$', '', art)
            info = info.replace(art, '')

        worksheet.write(i + 1, 8, info, style2)

        # фото
        lst = []
        for x in range(len(el['img'])):
            lst.append(el['img'][x]['article'].replace('/', '-'))

        worksheet.write(i + 1, 9, '\n'.join(lst), style2)

        # Проданные лоты
        worksheet.write(i + 1, 10, el['sales'].replace(' ₽', ''), style2)

        # Ключевые слова
        worksheet.write(i + 1, 11, el['info'][0].split('.')[0], style2)

        # description
        worksheet.write(i + 1, 12, el['description'], style2)

    workbook.close()


def create_json():
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def create_image():
    if not os.path.exists('image'):
        os.makedirs('image')

    for i, el in enumerate(data['data']):
        try:
            for j, el2 in enumerate(el['img']):
                try:
                    name = el2['article'].replace('/', '-')
                    if os.path.exists('image/{}.png'.format(name)):
                        name += " " + el['lot']

                    urllib.request.urlretrieve(os.getenv('URL') + el2['url'], 'image/{}.png'.format(name))
                    print('save {}_{} image/{}.png'.format(el['lot'], j + 1, name))
                except:
                    continue

        except:
            for j, el2 in enumerate(el['img']):
                try:
                    name = el2['article'].replace('/', '-')
                    if os.path.exists('image/{}.png'.format(name)):
                        name += " " + el['lot']

                    urllib.request.urlretrieve(os.getenv('URL') + el2['url'], 'image/{}.png'.format(name))
                    print('save {}_{}'.format(el['lot'], j + 1))
                except:
                    continue


if __name__ == '__main__':
    parse(os.getenv('URL'), os.getenv('AUCTION'), os.getenv('PAGE'), int(os.getenv('NUM')))
    create_json()
    create_xlsx()
    create_image()
