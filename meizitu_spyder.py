#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import requests
from bs4 import BeautifulSoup

headers = {

    'method': 'GET',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36'
}

home_url = 'https://qingbuyaohaixiu.com'

current_url = home_url
session = requests.session()


def get_image_url(html_url: str):
    time.sleep(1)
    response = session.get(html_url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'lxml').find('img').attrs['src']


def save_image(image_url: str):
    # get image name, it name is after the image url's last '/' end with jpg or png
    image_name = image_url.strip().split('/')[-1]
    image = session.get(image_url, headers=headers)
    if image.status_code == 200:
        time.sleep(3)
        print('%s founded, saving ' % image_name, end='\t')
        open('meizitu/' + image_name, 'wb').write(image.content)
        print('%s saved' % image_name)


def get_archives_lists(page_text: str):
    soup = BeautifulSoup(page_text, 'lxml')
    article_list = soup.findAll('article')
    lists = [article.find('a').attrs['href'] for article in article_list if article.h2 is not None]
    time.sleep(5)
    return lists


def next_page(current_page: str):
    global home_url
    global current_url
    soup = BeautifulSoup(current_page, 'lxml')
    next_page_number = soup.find('a', {'class': 'next page-numbers'})
    if next_page_number is None:
        return False
    print(next_page_number)
    current_url = next_page_number.attrs['href']
    return True


if __name__ == '__main__':
    if not os.path.exists('meizitu'):
        os.mkdir('meizitu')

    current_url = home_url + '/page/' + str(108)
    while True:
        response = session.get(current_url, headers=headers, verify=True)
        if response.status_code == 200:
            archives_lists = get_archives_lists(response.text)
            for archives in archives_lists:
                time.sleep(1)
                image_url = get_image_url(archives)
                save_image(image_url)
        if not next_page(response.text):
            break

