from pymongo import MongoClient
from pprint import pprint
from bs4 import BeautifulSoup as BS
import requests
import time

start = time.perf_counter()
client = MongoClient('localhost', 27017)
db = client['vacancy_database']
vacancies_db = db.vacancies

def hh_parser(collection):
    page = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    site = 'https://hh.ru'
    url = site + '/search/vacancy'

    while True:
        params = {'text': 'Python',
                  'page': page,
                  'items_on_page': 20}
        response = requests.get(url, params=params, headers=headers)
        dom = BS(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': "vacancy-serp-item"})
        if response.ok and vacancies:
            for vacancy in vacancies:
                vacancy_data = {}
                name_link = vacancy.find('a')
                name = name_link.text
                link = name_link.get('href')
                vacancy_data['name'] = name
                vacancy_data['link'] = link
                vacancy_data['site'] = site
                try:
                    salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).text.replace(
                        '\u202f', '').split(' ')
                    if salary[0] == 'от':
                        vacancy_data['salary_min'] = round(float(salary[1]), 2)
                        vacancy_data['salary_max'] = None
                        vacancy_data['salary_cur'] = salary[2]
                    elif salary[0] == 'до':
                        vacancy_data['salary_min'] = None
                        vacancy_data['salary_max'] = round(float(salary[1]), 2)
                        vacancy_data['salary_cur'] = salary[2]
                    else:
                        vacancy_data['salary_min'] = round(float(salary[0]), 2)
                        vacancy_data['salary_max'] = round(float(salary[2]), 2)
                        vacancy_data['salary_cur'] = salary[3]
                except:
                    vacancy_data['salary_min'] = None
                    vacancy_data['salary_max'] = None
                    vacancy_data['salary_cur'] = None
                if not collection.find_one(vacancy_data):
                    collection.insert_one(vacancy_data)
                # vacancy_list.append(vacancy_data)
            page += 1
        else:
            break


hh_parser(vacancies_db)
print(vacancies_db.count_documents({}), time.perf_counter()-start)
req_salary = float(input('Введите зарплату: '))
for vacancy in vacancies_db.find({'$or': [{'salary_min': {'$gt': req_salary}},
                                         {'salary_max': {'$gt': req_salary}}]}):
    pprint(vacancy)

