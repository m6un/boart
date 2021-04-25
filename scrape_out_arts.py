import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

url_for_type = "https://artsandculture.google.com/entity/abstract-expressionism/m012yb9?categoryid%5C%5Cu003dart-movement"
driver = webdriver.Chrome("C:/Users/Lasitha/Documents/chromedriver.exe")
driver.get(url_for_type)
parentElement = driver.find_element_by_class_name("s6J3Hd")
element = parentElement.find_elements_by_tag_name("div")[3]
element.click()
time.sleep(3)
url1 = driver.current_url
print(url1)
driver.quit()
# url1 = 'https://artsandculture.google.com/entity/abstract-expressionism/m012yb9?categoryid%5C%5Cu003dart-movement&date=1965'#driver.current_url

req1 = requests.get(url1)
soup1 = bs(req1.text, "lxml")
td1 = soup1.find_all("script")[3].contents[0]
le = td1.split(",")
d2, m = {}, []
for a in le:
    if a.startswith('"/asset') and a not in m:
        m.append(a)
        indx = le.index(a)
        d2[le[indx - 3]] = a[1:-1]
print(list(d2.keys()))
