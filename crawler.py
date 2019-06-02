from tqdm import tqdm
import datetime
import requests
from bs4 import BeautifulSoup as bs
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from menus.models import CustomMenu

def getMenu(num):
    r = requests.get('http://www.hanyang.ac.kr/web/www/re'+ str(num)).text
    r_html = bs(r, 'html.parser')
    location = r_html.find('title').text.split('-')[0][:-1]
    date = r_html.find('div', {'class' : 'day-selc'}).find('strong').text
    menus = r_html.findAll('li', {'class' : 'span3'})

    datas = []
    i = 0
    for menu in menus:
        i += 1
        data = {}
        name = list(menu.find('h3'))
        title = name[0].replace('\n', '').replace('\r', '').replace('\t', '')
        if title[0] == ' ':
            title = title[1:]
        price_temp = menu.find('p', {'class' : 'price'}).text
        if price_temp != '-':
            price = ''
            for s in price_temp:
                if s.isdigit():
                    price += s
            price = int(price)
        else:
            price = 0

        photo = menu.find('img')['src']
        if photo == '/html-repositories/images/custom/food/no-img.jpg':
            photo = 'http://www.hanyang.ac.kr/html-repositories/images/custom/food/no-img.jpg'
        data['title'] = title
        data['res'] = str(num)
        data['id'] = str(i)
        data['location'] = location
        data['photo'] = photo
        data['price'] = price
        datas.append(data)
    if len(datas) > 0:
        print(datas[0]['location'] + ' done!')

    return datas

def getAllMenu():
    data_list = []

    for i in range(1, 9):
        data_list += getMenu(i)
        
    return data_list

def main():
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')

    data_list = getAllMenu()
    print('Crawling Done')
    if len(CustomMenu.objects.filter(mid__startswith=nowDate)) == 0:
        print('updating new menus')
    for data in data_list:
        mid = nowDate+data['res']+data['id']
        
        try:
            CustomMenu.objects.get(mid=mid)
        except CustomMenu.DoesNotExist:
            print(mid + ' menu update!')
            CustomMenu(
                mid = mid,
                title=data['title'],
                location=data['location'],
                price=data['price'],
                photo=data['photo']
                ).save()
        else:
            if CustomMenu.objects.get(mid=mid).photo != data['photo']:
                print(mid + ' photo update!')
                updatePhoto = CustomMenu.objects.get(mid=mid)
                updatePhoto.photo = data['photo']
                updatePhoto.save()
            else:
                pass
    print('Update DB Done')