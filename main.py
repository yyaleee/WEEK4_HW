
import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)



def get_musicchart(date=''):
    client = MongoClient(host='localhost', port=27017)  # mongoDB는 27017 포트로 돌아갑니다.
    db = client.spartadb  # 'spartadb'라는 이름의 db를 만듭니다.

    # URL을 읽어서 HTML를 받아오고,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    default_url = 'https://www.genie.co.kr/chart/'
    data = requests.get(urljoin(default_url, 'top200?ditc=D&rtm=N&ymd=' + date),headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, tr들을 불러오기
    songs = soup.select('#body-content > div.newest-list > div.music-list-wrap > table > tbody > tr')

    # songs (tr들) 의 반복문을 돌리기
    rank = 1
    chart = []

    for song in songs:
        # song 안에 a 가 있으면,
        a_tag = song.select_one('.info .title.ellipsis')
        if a_tag is not None:
            title = a_tag.text.lstrip()
            artist = song.select_one('.info .artist.ellipsis').text
            doc = {
                'rank': rank,
                'title': title,
                'artist': artist
            }

            chart.append(doc)
            db.songs.insert_one(doc)

            rank += 1

    # print(chart)

if __name__ == '__main__':
    get_musicchart('20190908')
