from tqdm import tqdm
import requests, re
from bs4 import BeautifulSoup
import json


def loaddata(session, page, url):
    url = url + '&page=%d' % (page)
    request = session.get(url)
    response = BeautifulSoup(request.text, 'html.parser')
    return response


def workfile(soup, page, users):
    with open('./page_%d.html' % (page), 'w', encoding="utf-8") as htmlfile:
        htmlfile.write(soup.text)
    with open('dataset.json', 'a') as f:
        dataset = json.dumps('"Nik";"status";"data";"info"' + '\n', indent=4)

    Nikdict = []

    for i in range(users):
        # Ник будем использовать за уникальное поле
        Nik = soup.find_all('h3')[i].get_text()
        data = soup.find_all(class_='posted_info desc lighter ipsType_small')[i].get_text()
        data = data.replace("		  			  Отправлено ", "")
        # tet = soup.find("div", itemprop="commentText", class_="post entry-content ")
        # Пробуем получить статус, инфо(город и пол), ccылки
        try:
            ad_url = re.sub(r'"', '', [i.xpath(ID + '/div/div[2]/div[3]/a[2]')[0].text for i in ID])
        except:
            ad_url = ''
        # Получаем доступные ссылки
        try:
            info = re.sub(r'"', '', [i.xpath(ID + '/div/div[1]/div/ul[2]')[0].text for i in ID])
        except:
            info = ''
        try:
            status = re.sub(r'"', '', [i.xpath(ID + '/div/div[1]/div/li[1]/li[2]/p')[0].text for i in ID])
        except:
            status = ''

        # Если объявление с таким номером уже есть, не добавляем его
        if Nik in Nikdict:
            # with open('dataset.json','a') as f:
            dataset = json.dumps('"\n"+'"'+data+'"';'"'+ad_h1+'"'+"\n"', indent=4)
            # f.write('"'+Nik+'";"'+status+'";"'+data+'";"'+tet+'";"'+info+'"'+'\n')
        else:
            dataset = json.dumps('"\n"+'"'+Nik+'"';'"'+status+'"';'"'+data+'"';'"'+info+'"'+"\n"', indent=4)
            Nik = Nik.rstrip().strip()
            Nik = Nik.split('#')
            Nik = list(filter(None, Nik))
            Nikdict.append(Nik)

            # Очищаем строку от ненужных символов
    print(Nikdict)

    f.close()
    htmlfile.close()


def main():
    s = requests.Session()
    s.headers.update({
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
    # Количество страниц в теме, количество пользователей на странице и url темы
    pages = 3
    users = 25
    url = 'http://forum.reutov.ru/index.php?showtopic=12836'
    for page in tqdm(range(pages)):
        request = loaddata(s, page, url)
        workfile(request, page, users)


if __name__ == "__main__":
    main()
