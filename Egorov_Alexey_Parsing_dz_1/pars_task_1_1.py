# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint
import json


user = 'AlxEgory'
responce = requests.get(f'https://api.github.com/users/{user}/repos')
repo_list = responce.json()
print(f'Список репозиториев для пользователя: {user}')
for repo in repo_list:
    print(repo['name'])

with open ('repos_list.json', 'w', encoding='utf-8') as f:
    json.dump(repo_list, f)
print('Файл json создан')