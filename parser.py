from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


def load_data(session, page, url):
    url = url + '&page=%d' % page
    request = session.get(url)
    response = BeautifulSoup(request.text, 'html.parser')
    return response


def work_file(soup, page, users):
    with open('./page_%d.html' % page, 'w', encoding="utf-8") as htmlfile:
        htmlfile.write(soup.text)

    dates_nicknames = []

    for i in range(users):
        nickname = soup.find_all('h3')[i].get_text()
        data = soup.find_all(class_='posted_info desc lighter ipsType_small')[i].get_text()
        data = data.replace("\n\t\t\t\t\tОтправлено ", "").replace("\n", "")

        if nickname not in dates_nicknames:
            nickname = nickname.strip().replace("\t", "").replace("\n", "")
            dates_nicknames.append({data: nickname})

    print(dates_nicknames)


def main():
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    })
    # Количество страниц в теме, количество пользователей на странице и url темы
    pages = 3
    users = 25
    url = 'http://forum.reutov.ru/index.php?showtopic=12836'
    for page in tqdm(range(pages)):
        request = load_data(s, page, url)
        work_file(request, page, users)


if __name__ == "__main__":
    main()
