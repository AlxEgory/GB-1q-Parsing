# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH и/или Superjob.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.



from bs4 import BeautifulSoup as BS
import requests
from pprint import pprint

page = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
site = 'https://hh.ru'
url = site + '/search/vacancy'
vacancy_list = []
while True:
    params = {'text': 'Phyton',
              'page': page}
    response = requests.get(url, params=params, headers=headers)
    if response.ok:
        dom = BS(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': "vacancy-serp-item"})
        for vacancy in vacancies:
            vacancy_data = {}
            name_link = vacancy.find('a')
            name = name_link.text
            link = name_link.get('href')
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['site'] = site
            try:
                sallary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"}).text.replace('\u202f', '').split(' ')
                if sallary[0] == 'от':
                    vacancy_data['sallary_min'] = round(float(sallary[1]), 2)
                    vacancy_data['sallary_max'] = None
                    vacancy_data['sallary_cur'] = sallary[2]
                elif sallary[0] == 'до':
                    vacancy_data['sallary_min'] = None
                    vacancy_data['sallary_max'] = round(float(sallary[1]), 2)
                    vacancy_data['sallary_cur'] = sallary[2]
                else:
                    vacancy_data['sallary_min'] = round(float(sallary[0]), 2)
                    vacancy_data['sallary_max'] = round(float(sallary[2]), 2)
                    vacancy_data['sallary_cur'] = sallary[3]
            except:
                vacancy_data['sallary_min'] = None
                vacancy_data['sallary_max'] = None
                vacancy_data['sallary_cur'] = None
            vacancy_list.append(vacancy_data)
        next_page = dom.find('a', {'data-qa': "pager-next"})
        if not next_page:
            break
        page += 1

pprint(vacancy_list)
