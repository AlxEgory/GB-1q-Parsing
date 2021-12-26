from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['mvideo_database']
goods_db = db.goods


def mvideo_parser(collection):
    driver = webdriver.Chrome('/Users/alexeyegorov/PycharmProjects/pythonProject/MyPars/Egorov_Alexey_Parsing_dz_5/chromedriver')
    driver.get('https://www.mvideo.ru/')
    driver.implicitly_wait(10)
    actions = ActionChains(driver)
    in_trend_elem = driver.find_element(By.TAG_NAME, 'mvid-shelf-group')
    actions.move_to_element(in_trend_elem)
    actions.perform()
    in_trend_btn = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]/../..")
    in_trend_btn.click()
    forward_btn = driver.find_element(By.XPATH, "//mvid-shelf-group/mvid-carousel//button[contains(@class, 'btn forward')]")
    while forward_btn.is_displayed():
        try:
            forward_btn.click()
        except:
            break
    names_el = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel//div[contains(@class, 'product-mini-card__name')]")
    prices_el = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel//span[contains(@class, 'price__main-value')]")
    names = []
    prices = []
    for name_el in names_el:
        names.append(name_el.text)
    for price_el in prices_el:
        prices.append(float(price_el.text.replace(' ', '')))
    for name, price in zip(names, prices):
        good = {}
        good['name'] = name
        good['price'] = price
        if not collection.find_one(good):
            collection.insert_one(good)
    driver.close()


mvideo_parser(goods_db)
print(goods_db.count_documents({}))
for good in goods_db.find({}):
    pprint(good)