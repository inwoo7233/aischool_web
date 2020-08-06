import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import requests

URL = "https://movie.naver.com/movie/running/current.nhn"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

movie_data = []

movies = soup.select('dt.tit a')
for a_tag in movies: 
    title = a_tag.text

    link_split = a_tag['href'].split('=')
    code = link_split[1]
    movie_tile_code = {
        'title' : title,
        'code' : code
    } 
    movie_data.append(movie_tile_code)

for movie in movie_data:
    print()
    movie_code = movie['code']

    # headers : 클라이언트와 서버가 요청 또는 응답을 보낼 때 전송하는 부가적인 정보. 이것이 있어야 정상적 작동이 가능하다.
    headers = {
        'authority': 'movie.naver.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://movie.naver.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'NNB=6LMMGM5YOEBF6; notSupportBrowserAlert=true; NM_THUMB_PROMOTION_BLOCK=Y; nx_ssl=2; NV_WETR_LOCATION_RGN_M="MDkxNDAxMDQ="; NV_WETR_LAST_ACCESS_RGN_M="MDkxNDAxMDQ="; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NRTK=ag#20s_gr#1_ma#-1_si#-1_en#-1_sp#-1; BMR=s=1596698270468&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dsaypumpy%26logNo%3D221656755006%26categoryNo%3D83%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=UyXyWlp0YiRssk8lL+NssssstnR-016389; REFERER_DOMAIN="d3d3Lmdvb2dsZS5jb20="; csrf_token=a196b6a3-d8eb-4364-8c02-ca27f0fa18dc',
    }

    # params : 요청할 쿼리 내용
    params = (
        ('code', movie_code),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/basic.nhn', headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    lis = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_result > ul > li')
     
    for li in lis:
        star = int(li.select('div.star_score > em')[0].getText())
        p = li.select('div.score_reple > p')[0]
        a = p.select('a')
        print(f"[{movie['title']}] ", end='')
        print(f"{star}점")

        if (a != []):
            print(f"{a[0]['data-src']}\n")
        else:
            print(f"{p.text.strip()}\n")
    print("===========================================================")