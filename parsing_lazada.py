import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime as dt
import re
url = "https://www.lazada.co.id/catalog/?_keyori=ss&ajax=true&from=input&isFirstRequest=true&page=1&q=lenovo"
payload={}
headers = {
  'authority': 'www.lazada.co.id',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '__wpkreporterwid_=98884795-cebb-4cd4-2729-9290266a6194; hng=ID|id-ID|IDR|360; hng.sig=dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ; lzd_cid=899e648d-6ba2-4a82-a3a4-c2dd4271313a; t_uid=899e648d-6ba2-4a82-a3a4-c2dd4271313a; _bl_uid=IUlI39ndk85lay4vn76R0jmlUapb; t_fv=1666483278536; cna=T3LbG+vYlhMCAbTyaSu9zrDz; _gcl_au=1.1.1640065967.1666918330; _fbp=fb.2.1666918338766.587895684; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C19294%7CvVersion%7C5.2.0%7CMCMID%7C80275101829536896263017449610910177661%7CMCAAMLH-1667525551%7C3%7CMCAAMB-1667525551%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1666927951s%7CNONE; sgcookie=E100%2BatxSEkTE%2BOd6CuD24yemzV3c%2B0ljSBn5drQGd%2FdMuUMEP6NmBydNVmbZJeGOjEed0m4Dr7x7AjGoR3igtV0uz4luBeb5zTesjsNCr9FJK0%3D; t_sid=19Vm7XTUOc44J3c1xjYL2WgUOEsAXKob; utm_origin=https://www.google.com/; utm_channel=SEO; _gcl_aw=GCL.1667033846.Cj0KCQjwnvOaBhDTARIsAJf8eVMYEO4BEjSd0DvIUPYpS0ZdzXanvnLg2AKvb319xEjYfCzJLliGBxoaAkl2EALw_wcB; lzd_sid=1887a2de6c7ad2c221bf42edf6b3d182; _m_h5_tk=4a9e3eb21b31be94a380ccd5162d0732_1667042126693; _m_h5_tk_enc=e2cd36a307c9a490ccd145eb98213583; _tb_token_=58eb68f56bea3; _uetsid=b9e3be90576711eda601d1bf5efa8301; _uetvid=c5c0b310565a11eda22f7136b4c07b0f; cto_bundle=YvY2LF9Xd2pqaFFHd050dGRXU1pxSWZWRER6VjNvTXYyOEZ4M00ydnZPRWo4OFl5emdjWXhETUNzUHRoSnpCQUNCWXloUFBWdkUwNk1PQW1MVzI3ODgzYjZ2dHRISWpVUHMxMkszNE0wSiUyQnNucmglMkJUSHNSbFQzc2pIZnFLdHlDV1R1NjdLNElHVnZibzB0UWxjS2U5ZU1LaCUyQlElM0QlM0Q; xlly_s=1; tfstk=cHlFBdfXpBdeEykhg5FrgUzXNaVdZuGoGpU8K3DCpb4hIPehiHj8SKxiv07NqJf..; l=eBO9PgPcTiQ7lsEFBOfZlurza77OSIRY6uPzaNbMiOCPOs1p5SjAW6ydrM89C3MNhsa6R3rp2umHBeYBqIDjLbHEAjH5SNDmn; isg=BIyMWkQKA4MJehf3EnBkmgh3Xeq-xTBvI-EQP-ZNmDfacSx7DtUA_4LHEWHJZmjH; hng=ID|id-ID|IDR|360; hng.sig=dJwrVwSueShOlZz95EBCvlH9FLAVtzGZ3msUnc25HIQ',
  'referer': 'https://www.lazada.co.id/catalog/?q=xiaomi&_keyori=ss&from=input&spm=a2o4j.home.search.go.41f753e0T41uYl',
  'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  'x-csrf-token': '58eb68f56bea3',
  'x-requested-with': 'XMLHttpRequest'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()

listItems = data['mods']['listItems']

f=[]
for item in listItems :
    
    item['url'] = f"https:{item['itemUrl']}"
    url_product = requests.get(item['url'])
    soup = BeautifulSoup(url_product.text,'lxml')
    
    shop_url = soup.find('a',class_ = 'pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name')['href']
    pics_links = []
    pics = soup.find_all('img', class_ = 'pdp-mod-common-image item-gallery__thumbnail-image')
    for pic in pics:
        pics_links.append(pic['src'])
    
    category = []
    for index in item['categories']:
        category.append(index)
        
    try:
        discount = item['discount']
    except Exception as e:
        discount = 0
        print(e)
    
    
    
    attraction = {
        'product_id':item['itemId'] or None,
        'product_name':item['name'],
        'category':category or None,
        'price':item['price'] or None,
        'crawled':dt.today(),
        'description': None ,
        'url':item['url'],
        'images': {
            'full' : pics_links,
        },
        'stats': {
            'rating': item['ratingScore'] or None,
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
            'name': item['sellerName'],
            'location': item['location'],
        },
        'marketplace':'Lazada',
        'created_at':dt.today(),
        'updated_at':dt.today()
    }
    f.append(attraction)


f[4]