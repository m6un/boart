import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from random import choice
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


def initial_scrape():
    try:
        l1, l2 = [], []
        URL = "https://artsandculture.google.com/category/art-movement?tab=pop&date=1000"
        req = requests.get(URL)
        soup = bs(req.text, "lxml")
        td = soup.find_all("script")[3].contents[0][336:]
        l = td.split(",")  # l1:art movement type name,l2:art movement type link
        for r in l:
            if r == "null":
                l.remove(r)
            if r.startswith('"//'):
                l.remove(r)
            if r == "[]":
                l.remove(r)
            if r.endswith('items"'):
                l.remove(r)

        for j in range(len(l)):
            if '"' in l[j]:
                result = l[j].index('"', 0, -1)
                if l[j][result + 1].isupper() == True:
                    index1, index2 = l[j].index('"', 0, -1), -1
                    l1.append(l[j][index1 + 1 : index2])
        l1, indl = l1[55:218], []
        for y in range(len(l1)):
            if len(l1[y]) == 1:
                indl.append(l1[y])
                indl.append(l1[y + 1])
        for t in indl:
            if t in l1:
                l1.remove(t)
        d1 = {}
        for q in l1:
            search = q.lower()
            search = search.replace(" ", "-")
            search = search.replace("'", "-")
            for g in l:
                if search in g:
                    l2.append(g)
        temp = []
        for x in l2:
            if x not in temp and x.startswith('"/entity'):
                temp.append(x)
        l2 = temp
        for q in l1:
            search = q.lower()
            search = search.replace(" ", "-")
            search = search.replace("'", "-")
            for g in l2:
                if search in g:
                    d1[q] = g
        del d1["Romanesque art"]
        del d1["Bronze Age"]
        del d1["Early Christian art and architecture"]
        print(d1)
        types = list(d1.keys())
        length1 = len(types)
        n = random.randint(0, length1)
        typ = types[n]
        url_for_type = d1[typ]
        return [typ, url_for_type]
    except Exception as e:
        pass


def scrape_out_arts():
    try:
        a = initial_scrape()
        typ = a[0]
        url_for_type = "https://artsandculture.google.com" + a[1][1:-1]
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.delete_all_cookies()
        driver.maximize_window()
        driver.get(url_for_type)
        wait = WebDriverWait(driver, 100)
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "s6J3Hd")))
        parentElement = driver.find_element_by_class_name("s6J3Hd")
        element = parentElement.find_elements_by_tag_name("div")[3]
        print(element)
        driver.execute_script("arguments[0].click();", element)
        element.click()
        if not element.click():
            pass
        driver.set_page_load_timeout(30)
        time.sleep(3)
        url1 = driver.current_url
        print(url1)
        driver.quit()
        req1 = requests.get(url1)
        soup1 = bs(req1.text, "lxml")
        td1 = soup1.find_all("script")[3].contents[0]
        le = td1.split(",")
        print('le',le)
        d2, m = {}, []
        for a in le:
            if a.startswith('"/asset') and a not in m:
                m.append(a)
                indx = le.index(a)
                d2[le[indx - 3]] = a[1:-1]
        art = list(d2.keys())
        length2 = len(art)
        f1 = open("scraped_data/tweeted.txt", "r")
        lines = f1.readlines()
        for line in lines:
            if typ in line:
                oldline = line
                line1 = line
        ge1, ge2 = line1.index(":"), line1.index("\n")
        if ge2 - ge1 == 1:
            choiceindex = []
        else:
            choiceindex = line1[ge1 + 1 : ge2].split(" ")
            for i in range(0, len(choiceindex)):
                choiceindex[i] = int(choiceindex[i])

        i = choice([i for i in range(0, length2) if i not in choiceindex])
        url_for_art = d2[art[i]]
        line1 = line1[:-1] + " " + str(i) + "\n"
        new_lines = ""
        for line in lines:
            if oldline in line:
                new_lines += line1
            else:
                new_lines += line
        f1.close()
        fe = open("scraped_data/tweeted.txt", "w")
        fe.write(new_lines)
        fe.close()
        return [i, url_for_art, typ]
    except Exception as e:
        pass


def art_details():
    b = scrape_out_arts()
    try:
        print(b)
        url_for_art = "https://artsandculture.google.com" + b[1] + "?hl=en"
        print(url_for_art)
        req4 = requests.get(url_for_art)
        soup4 = bs(req4.text, "lxml")
        im = soup4.find_all("img")[0]["src"]  # img_link
        print(im)
        td1 = soup4.find("section", class_="rw8Th QwmCXd")
        td3 = td1.find_all("li")
        d3 = {}
        for i in range(len(td3)):
            if "Title" in td3[i].find_all("span")[0].text:
                ind = td3[i].text.index(": ")
                k = td3[i].text[ind + 1 :][1:]
                d3["Title"] = k
            if "Creator" in td3[i].find_all("span")[0].text:
                ind = td3[i].text.index(": ")
                k = td3[i].text[ind + 1 :][1:]
                d3["Creator"] = k
            if "Date" in td3[i].find_all("span")[0].text:
                ind = td3[i].text.index(": ")
                k = td3[i].text[ind + 1 :][1:]
                d3["Date"] = k
            if "Location" in td3[i].find_all("span")[0].text:
                ind = td3[i].text.index(": ")
                k = td3[i].text[ind + 1 :][1:]
                d3["Location"] = k
            if "Medium" in td3[i].find_all("span")[0].text:
                ind = td3[i].text.index(": ")
                k = td3[i].text[ind + 1 :][1:]
                d3["Medium"] = k
            if "External Link" in td3[i].find_all("span")[0].text:
                a = td3[i].find_all("a")
                d3["External Link"] = a[0]["href"]
        d3["Type"] = b[2]

        f7 = open(
            "scraped_data/current_tweet.txt", "w+"
        )
        for i in d3:
            f7.write(i + ":" + d3[i] + "\n")
        f7.close()

        response = requests.get("http:" + im)
        if response.status_code == 200:
            with open(
                "scraped_data/imgs/current.jpg", "wb"
            ) as f:
                f.write(response.content)
    except Exception as e:
        pass


