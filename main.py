import re
import requests
import bs4

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

HEADERS = {
    'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-mobile': '?0'
}


def text_for_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def print_article(date, title, url):
    print(f"{date} - {title} - {url}")


def main():
    text = text_for_soup('https://habr.com/ru/all/')
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.findAll('article')
    for article in articles:
        title_element = article.find(class_='tm-article-snippet__title-link')
        title = title_element.find('span').text

        dt_element = article.find('time')
        date = dt_element['datetime'][:10]

        url = 'https://habr.com' + title_element['href']
        body = article.find(class_='article-formatted-body').text

        hubs = article.findAll(class_="tm-article-snippet__hubs-item-link")
        hubs = ' '.join(hub.find('span').text for hub in hubs)

        preview_text = title + body + hubs
        keywords_pattern = re.compile(f"{'|'.join(KEYWORDS)}", re.IGNORECASE)
        if keywords_pattern.search(preview_text):
            print_article(date, title, url)
        else:
            article_soup = bs4.BeautifulSoup(text_for_soup(url),
                                             features='html.parser')
            article_elem = article_soup.find(class_='article-formatted-body')
            article_text = article_elem.get_text()
            if keywords_pattern.search(article_text):
                print_article(date, title, url)


if __name__ == '__main__':
    main()
