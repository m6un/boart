# pure selenium trial for scrape_out_arts
# not a necessary code
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

url = "https://artsandculture.google.com/entity/abstract-expressionism/m012yb9?categoryid%5C%5Cu003dart-movement"
driver = webdriver.Chrome("C:/Users/Lasitha/Documents/chromedriver.exe")
driver.get(url)
parentElement = driver.find_element_by_class_name("s6J3Hd")
element = parentElement.find_elements_by_tag_name("div")[3]
element.click()
time.sleep(3)
url1 = driver.current_url
print(url1)
driver.quit()
