import json
import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://quotes.toscrape.com'


def get_urls():
    session = requests.Session()
    base_url = BASE_URL
    all_urls = [base_url]

    while True:
        response = session.get(base_url)
        if response.status_code != 200:
            print(f"Failed to retrieve {base_url}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('ul[class=pager] li[class=next] a')

        if not content:
            break

        base_url = urljoin(BASE_URL, content[0]['href'])
        all_urls.append(base_url)

    return all_urls


def spider_quote(url):
    result = []
    author_urls = set()

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=quote]')

        for quote in content:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = quote.find('div', class_='tags').meta['content'].split(',')

            span_tag = quote.find('span', class_=None)

            author_url = urljoin(BASE_URL, span_tag.find('a')['href'])
            author_urls.add(author_url)

            result.append({
                "tags": tags,
                "author": author,
                "quote": text,
            })
    return result, author_urls


def spider_author(url):
    result = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=author-details]')

        for quote in content:
            author = quote.find('h3', class_='author-title').text  # автор
            born_date = quote.find('span', class_='author-born-date').text
            born_location = quote.find('span', class_='author-born-location').text
            description = quote.find('div', class_='author-description').text.strip()

            result.append({
                "fullname": author,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            })
    return result


def main():
    data_quotes = []
    data_authors = []
    author_urls = set()
    for url in get_urls():
        data, urls = spider_quote(url)
        data_quotes.extend(data)
        author_urls.update(urls)

    for url in author_urls:
        data_authors.extend(spider_author(url))

    with open(os.path.abspath('data_json/quotes.json'), 'w', encoding='utf-8') as fd:
        json.dump(data_quotes, fd, ensure_ascii=False, indent=2)
    with open(os.path.abspath('data_json/authors.json'), 'w', encoding='utf-8') as fd:
        json.dump(data_authors, fd, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
