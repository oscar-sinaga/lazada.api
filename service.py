from service.crawler import Tokopedia
from service.crawler import Bukalapak
from service.crawler import Lazada
from service.parsing import task_parse, bukalapak_parse, tokopedia_parse, lazada_parse
from service.elasticserv import Elastic
from service.bigquery import search_elastic, load_files
from service.config import configBigQuery
from datetime import datetime as dt

def post_task(taskid,query,marketplace,maxitem):
    elastic = Elastic()
    status = 1
    result = 0

    if marketplace == 'tokopedia':
        tokopedia = Tokopedia()
        for i in range(1,maxitem,50):
            res = tokopedia.getItems(query,i)
            for item in res['data']['products']:
                parsed_data = task_parse(taskid, item, marketplace, status)
                res = elastic.saving(parsed_data, parsed_data['id'], index = 'dev_marcella_tasks')
                result += res['created']    

    if marketplace == 'bukalapak':
        bukalapak = Bukalapak()
        maxpage = int(maxitem / 50)
        for i in range(1,maxpage+1):
            res = bukalapak.getItems(query, i)
            for item in res['data']:
                parsed_data = task_parse(taskid, item, marketplace, status)
                res = elastic.saving(parsed_data, parsed_data['id'], index = 'dev_marcella_tasks')
                result += res['created']

    #Untuk Lazada
    if marketplace == 'lazada':
        lazada = Lazada()
        maxpage = int(maxitem/40)
        for i in range(1,maxpage+1):
            res = lazada.getItems(query,i)
            for item in res:
                parsed_data = task_parse(taskid, item, marketplace, status)
                res = elastic.saving(parsed_data, parsed_data['id'], index = 'dev_marcella_tasks')
                result += res['created'] 
                
    return result

def update_task(taskid,query):
    elastic = Elastic()
    if query == 'activate':
        updated_data = {'status':"1"}
        elastic.update(updated_data, taskid, index = 'dev_marcella_tasks',type='tasks')
    if query == 'deactivate':
        updated_data = {'status':"0"}
        elastic.update(updated_data, taskid, index = 'dev_marcella_tasks',type='tasks')
    else:
        return 'query not found'
    return 'update tasks success'

def do_task():
    elastic = Elastic()
    tasks = elastic.search('status', 1, index = 'dev_marcella_tasks')

    for task in tasks['hits']:
        # try:
        task = task['_source']
        if task['marketplace'] == 'tokopedia':
            tokopedia = Tokopedia()
            detailed_data = tokopedia.getDetail(task['url'])
            downloaded = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            parsed_data = tokopedia_parse(detailed_data, task['id'], task['product_name'])
            parsed = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            elastic.saving(parsed_data, task['id'], index='dev_marcella_datas')
            uploaded = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            data = {"isDownloaded":downloaded,"isParsed":parsed,"isUploaded":uploaded}
            elastic.update(data, task['id'],index = 'dev_marcella_tasks',type='data')
        if task['marketplace'] == 'bukalapak':
            bukalapak = Bukalapak()
            detailed_data = bukalapak.getDetail(task['url'])
            downloaded = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            parsed_data = bukalapak_parse(detailed_data, task['id'], task['product_name'])
            parsed = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            elastic.saving(parsed_data,task['id'],index='dev_marcella_datas')
            uploaded = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            data = {"isDownloaded":downloaded,"isParsed":parsed,"isUploaded":uploaded}
            elastic.update(data, task['id'],index = 'dev_marcella_tasks',type='data')
        if task['marketplace'] == 'lazada':
            lazada = Lazada()
            detailed_data_list = lazada.getDetail(task['list_url'])# Disini ada yang berubah
            downloaded = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            for detailed_data in detailed_data_list:# Disini ada yang berubah
              if detailed_data['name'] == task['name']:# Disini ada yang berubah
                parsed_data = lazada_parse(detailed_data, task['id'], task['product_name'])# Disini ada yang berubah
            parsed = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            elastic.saving(parsed_data,task['id'],index='dev_marcella_datas')
            uploaded = dt.today().strftime('%Y-%m-%d %H:%M:%S')
            data = {"isDownloaded":downloaded,"isParsed":parsed,"isUploaded":uploaded}
            elastic.update(data, task['id'],index = 'dev_marcella_tasks',type='data')


def toBigQuery():
    file_names = []
    search_elastic('dev_marcella_datas', file_names)
    load_files('dev_marcella_datas', configBigQuery.TABLE_PROJECT, configBigQuery.TABLE_DATASET, configBigQuery.TABLE_NAME)

# if __name__ == "__main__":
#     # post_task("1-tp", "tp-link", "tokopedia", 100)
#     # post_task("1-bl","tp-link","bukalapak",1000)
#     do_task()
#     # # update_task("1",'deactivate')
#     # # update_task("2",'deactivate')

#     # Kalau mau coba
#     # post_task(ID(BEBAS), query(BEBAS), marketplace(BARU TOKOPEDIA/BUKALAPAK), max jumlah(bebas))
#     # => Dipakai buat nambah tasks baru
#     # do_task()
#     # => dipakai untuk menjalankan crawler getDetail dari tasks yang ada didatabase
#     # update_task(ID, activate/deactivate) (Ini masih ngebug sih, dari elasticnya)
#     # => activate buat ganti status = 1, deactivate buat ganti status task = 0. 1 akan dijakanlan
#     #    pas crawler getDetail Jalan, 0 bakal diskip