from pprint import pprint

import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from urllib.parse import urljoin


from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

def launch_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('windows-size=1920x1080')
    options.add_argument('disable-gpu')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    driver.get('https://select.ridibooks.com/book/510000165')

    print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # soup.....
    driver.quit()

def search_karaoke(title):

    # url 변환하기
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    default_url = 'http://www.ikaraoke.kr/isong/'
    query_url = 'search_musictitle.asp?sch_txt=' + convert_hangeul(title)
    # print(default_url+query_url)
    # data = requests.get(urljoin(default_url, query_url),headers=headers)

    # 셀레니움 사용해서 url 열기
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('windows-size=1920x1080')
    options.add_argument('disable-gpu')
    driver = webdriver.Chrome('/users/yalejeong/Downloads/chromedriver')
    driver.get(default_url+query_url)
    time.sleep(5)  # Let the user actually see something!

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    # soup = BeautifulSoup(data.text, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()

    # select를 이용해서, tr들을 불러오기
    songs = soup.select('#contentcolumn > div.tbl_board > table > tbody > tr')
    songs_2 = soup.select('#contentcolumn > div.tbl_board > table')
    # print(songs)

    # songs (tr들) 의 반복문을 돌리기
    i = 1
    searched_songs = []
    searched_titles = []

    for song in songs:
        # song 안에 a 가 있으면,
        a_tag = song.select_one('.pl8')
        if a_tag is not None:
            title = a_tag.text.strip()
            artist = song.select_one('.tit.pl8').text.strip()
            kara_num = song.select_one('.ac').text.strip()
            doc = {
                'title': title,
                'artist': artist,
                'kara_num' : kara_num
            }

            searched_songs.append(doc)
            # db.songs.insert_one(doc)
            searched_titles.append(title)


    print("최신곡 20개만 노출됩니다.")
    pprint(searched_songs)


def convert_hangeul(word):
    euc_data = str(word.encode('euc-kr'))
    trim_data = euc_data[2:-1]
    mod_data = trim_data.replace("\\x",'%').upper()
    return  mod_data
    # 인코딩 알아내기
    # print(chardet.detect(euc_data))


def test():

    driver = webdriver.Chrome('/users/yalejeong/Downloads/chromedriver')  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/');
    time.sleep(5)  # Let the user actually see something!
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5)  # Let the user actually see something!
    driver.quit()

if __name__ == '__main__':
    # test()
    search_karaoke("기적")
    # print("%")
    # convert_hangeul("배일호")

#     %B9%E8%C0%CF%C8%A3
