import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin

import time

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)


def create_db():
    client = MongoClient(host='localhost', port=27017)  # mongoDB는 27017 포트로 돌아갑니다.
    db = client.spartadb  # 'spartadb'라는 이름의 db를 만듭니다.
    coll_songs = db.songs


def get_songs():
    # URL을 읽어서 HTML를 받아오고,
    today_date = time.strftime('%Y%m%d')
    default_url = 'https://www.genie.co.kr/chart/'
    data = requests.get(urljoin(default_url, 'top200?ditc=D&rtm=N&ymd=' + '20190908'))

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')
    print(soup)

    # select를 이용해서, tr들을 불러오기
    songs = soup.select('#body_content > div.newest-list > div.music-list-wrap > table > tbody > tr')

    # songs (tr들) 의 반복문을 돌리기
    rank = 1
    for song in songs:
        # song 안에 a 가 있으면,
        a_tag = song.select_one('td.info > a.title')
        if a_tag is not None:
            title = a_tag.text
            artist = song.select_one('td.info > a.artist').text
            doc = {
                'rank': rank,
                'title': title,
                'artist': artist
            }
            db.songs.insert_one(doc)
            rank += 1


if __name__ == '__main__':
    create_db()
    get_songs()
