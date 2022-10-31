import hashlib
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime as dt
import re

def task_parse(taskid,item,marketplace,status):
    try:
        item['url'] = re.search(r'(.+)\?',item['url'])[1]
    except:
        pass
    task_doc = {
        'task_id':taskid,
        'id':hashlib.sha256(item['url'].encode('utf-8')).hexdigest(),
        'product_name':item['name'],
        'marketplace':marketplace,
        'url':item['url'],
        'isDownloaded':None,
        'isParsed':None,
        'isUploaded':None,
        'status':status
    }
    try:
        task_doc['list_url'] = item['list_url'] # Disini ada yang berubah
    except:
        pass

    return task_doc

def bukalapak_parse(detail,id_product,product_name):
    attraction = {
        'id_product':id_product or None,
        'product_name':product_name,
        'category':detail['category']['name'].lower() or None,
        'price':detail['price'] or None,
        'crawled':dt.today(),
        'description': detail['description'],
        'url': detail['url'],
        'images': {
            'full' : detail['images']['large_urls'],
        },
        'discount':detail['discount_percentage'] or 0,
        'stats': {
            'rating':detail['rating']['average_rate'] or 0,
            'item_count':detail['stock'],
            'sold_count':detail['stats']['sold_count'],
            'view_count':detail['stats']['view_count'],
            # 'favorited_count': 0,
        },
        'favorited_count':0,
        'processing_time':'',
        'item_condition':detail['condition'].lower() or None,
        'keywords':detail['category']['name'].lower() or None,
        'manufacturer':None,
        'stores': {
            'url': detail['store']['url'],
            'name': detail['store']['name'],
        },
        'marketplace':'Bukalapak',
        'created_at':dt.today(),
        'updated_at':dt.today(),
    }
    return attraction

def tokopedia_parse(detail,id_product,product_name):
    try:
        for index in detail['components']:
            if index['name'] == 'product_detail':
                detail_data = index['data']
                for index in detail_data[0]['content']:
                    if index['title'] == 'Kondisi':
                        kondisi = index['subtitle']
                    if index['title'] == 'Kategori':
                        keyword = index['subtitle']
                    if index['title'] == 'Deskripsi':
                        deskripsi = index['subtitle']
                        break
                break
    except Exception as e:
            print(e)

    try:
        for index in detail['components']:
            if index['name'] == 'product_media':
                detail_data = index['data']
                images = []
                for index in detail_data[0]['media']:
                    images.append(index['urlOriginal'])
                break
    except Exception as e:
            print(e)

    try:
        for index in detail['components']:
            if index['name'] == 'product_content':
                detail_data = index['data']
                for index in detail_data:
                    discount = index['campaign']['percentageAmount'] or 0
                    price = index['price']['value'] or 0
                    stock = index['stock']['value'] or 0
                break
    except Exception as e:
            print(e)

    try:
        category = []
        for index in detail['basicInfo']['category']['detail']:
            category.append(index['name'])
    except Exception as e:
            print(e)
            
    attraction = {
        'product_id':id_product or None,
        'product_name':product_name,
        'category':', '.join(category) or None,
        'price':price or None,
        'crawled':dt.today(),
        'description': deskripsi.replace('\n', ' '),
        'url':detail['basicInfo']['url'],
        'images': {
            'full' : images,
        },
        'stats': {
            'rating': detail['basicInfo']['stats']['rating'] or None,
            'item_count': int(stock),
            'sold_count': int(detail['basicInfo']['txStats']['countSold']),
            'view_count': int(detail['basicInfo']['stats']['countView']),
            # 'favorited_count': 0,
        },
        'discount':discount or None,
        'favorited_count':0,
        'processing_time':'',
        'item_condition':kondisi.lower() or None,
        'keywords':keyword.lower() or None,
        'manufacturer':None,
        'stores': {
            'url': re.search(r"(.+/.+)/",detail['basicInfo']['url'])[1],
            'name': detail['basicInfo']['shopName'],
            'location': detail['basicInfo']['shopMultilocation']['cityName'],
        },
        'marketplace':'Tokopedia',
        'created_at':dt.today(),
        'updated_at':dt.today()
    }

    return attraction

def lazada_parse(detail,id_product,product_name):
    detail['url'] = f"https:{detail['detailUrl']}"
    url_product = requests.get(detail['url'])
    soup = BeautifulSoup(url_product.text,'lxml')
    # Disini ada yang berubah
    shop_url = soup.find('a',class_ = 'pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name')['href']
    pics_links = []
    pics = soup.find_all('img', class_ = 'pdp-mod-common-image item-gallery__thumbnail-image')
    for pic in pics:
        pics_links.append(pic['src'])
    
    category = []
    for index in detail['categories']:
        category.append(index)
        
    try:
        discount = detail['discount']
    except Exception as e:
        discount = 0
        
    attraction = {
        'product_id':id_product or None,
        'product_name':product_name,
        'category':category or None,
        'price':detail['price'] or None,
        'crawled':dt.today(),
        'description': None ,
        'url':detail['url'],
        'images': {
            'full' : pics_links,
        },
        'stats': {
            'rating': detail['ratingScore'] or None,
            'item_count': None,
            'sold_count': None,
            'view_count': None,
            # 'favorited_count': 0,
        },
        'discount':discount,
        'favorited_count':0,
        'processing_time':'',
        'item_condition':None,
        'keywords':None,
        'manufacturer':None,
        'stores': {
            'url': re.search(r'(.+)\?',shop_url)[1],
            'name': detail['sellerName'],
            'location': detail['location'],
        },
        'marketplace':'Lazada',
        'created_at':dt.today(),
        'updated_at':dt.today()
    }
    return attraction