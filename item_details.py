import requests
from bs4 import BeautifulSoup as bs

url2 = "https://artsandculture.google.com/asset/anne-in-a-striped-dress-fairfield-porter/TAHUTWNOPxdkYA"
req2 = requests.get(url2)
soup2 = bs(req2.text, "lxml")
im = "https:" + soup2.find_all("img", class_="pmK5Xc")[0]["src"]  # img_link
td1 = soup2.find("section", class_="rw8Th QwmCXd")
td3 = td1.find_all("li")
# print(td3)
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

print(d3)
# d3['Date created']=td3[2].contents[1]
# d3['Location']=td3[3].contents[1]
# d3['Medium']=td3[7].find_all('a')[0].text
f7 = open("/Users/Lasitha/Documents/art_tweets/scraped_data/current_tweet.txt", "w+")
for i in d3:
    f7.write(i + ":" + d3[i] + "\n")
f7.close()
response = requests.get(im)
if response.status_code == 200:
    with open(
        "/Users/Lasitha/Documents/art_tweets/scraped_data/imgs/current.jpg", "wb"
    ) as f:
        f.write(response.content)
print(d3)
