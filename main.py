import requests
from bs4 import BeautifulSoup
import csv
import sys
import json

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36'
}

count=0
print('В РАБОТЕ')
print('СБОР ССЫЛОК')
url='https://www.joomil.ch/'
response=requests.get(url, headers=headers)
soup=BeautifulSoup(response.text, 'lxml')
categories=soup.find(id='navCategories').find_all('a')
links=[]
for cat in categories:
    response=requests.get(cat['href'])
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        under_categories = soup.find(id='navCategories').find_all('a')
        for category in under_categories:
            links.append(category['href'])
            count+=1
            print(f"Собрано ссылок на категории {count}")
    except:
        continue
links.append('https://www.joomil.ch/annonces-rencontres-romandie,28')

print()
print()
print('СБОР ДАННЫХ')
print()
print()

with open('phones.json', 'r', encoding='utf-8') as file: #открываю файл с сохраненными телефонами и присваиваю в переменную phones
    phones=json.load(file)

for url in links:
    response=requests.get(url=url, headers=headers)
    soup=BeautifulSoup(response.text,'lxml')
    try:
        try:
            pages=int(soup.find(id='navAdsPageNavigation').find_all('li')[-2].text.replace('\n','').strip())
        except:
            pages=1
        for page in range(1, pages+1):
            if page==1:
                link=url
            else:
                link=f"{url},p{page}"
            response=requests.get(link, headers=headers)
            soup=BeautifulSoup(response.text, 'lxml')
            ads=soup.find(id='navAdsUlList').find_all('div', class_='navAdsliBlock')
            for adv in ads:
                link=adv.find('a')['href']
                response=requests.get(link, headers=headers)
                soup=BeautifulSoup(response.text, 'lxml')
                try:
                    phone_num=soup.find('div', class_='divAnDetailContact').find_all('p')[-1].find_all('span')[5].text
                    print(phone_num)
                except:
                    continue
                try:
                    name=soup.find('div', class_='divAnDetailContact').find_all('p')[-1].find_all('span')[1].text
                except:
                    name='-'
                try:
                    adress=soup.find('div', class_='divAnDetailFeatures').find_all('span')[5].text
                except:
                    adress= '-'
                if phone_num not in phones:
                    phones[phone_num] = f"{name} {adress}"
                    with open('phones.json', 'w',
                              encoding='utf-8') as file:  # открываю файл с сохраненными телефонами и присваиваю в переменную phones
                        json.dump(phones, file, indent=4, ensure_ascii=False)
                    with open('phones.json', 'r',
                              encoding='utf-8') as file:  # открываю файл с сохраненными телефонами и присваиваю в переменную phones
                        phones = json.load(file)
                    with open('result.csv', 'a', newline='', encoding='utf-8-sig') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow([phone_num, name, adress])
    except:
        with open('fail.txt', 'w', encoding='utf-8') as file:
            file.write(str(sys.exc_info()))






