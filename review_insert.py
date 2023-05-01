import pymysql
import requests
from bs4 import BeautifulSoup

# code_num = [171539]

insert_data = []


conn = pymysql.connect(host="localhost", user="root", password="1019", db="final", charset="utf8")
count = 0
try:
    curs = conn.cursor()
    sql = """insert into review(code_movie, review_title, review_text, review_uname, review_date, review_good)
             values (%s, %s, %s, %s, %s, %s)"""

    insert_data = []
    code_movies = []  # 이곳에 movie_code.txt에 코드들을 넣는다. 그 후 실행하면 정상적 실행
    temp = set(code_movies)
    code_movies = list(temp)

    for code_movie in code_movies:
         url = f'https://movie.naver.com/movie/bi/mi/review.naver?code={code_movie}'
         response = requests.get(url)

         final = []
         if response.status_code == 200:
              html = response.text
              soup = BeautifulSoup(html, 'html.parser')

              for i in range(1, 4):
                   title = soup.select_one(
                        f'#reviewTab > div > div > ul > li:nth-child({i}) > a > strong')
                   text_ = soup.select_one(
                        f'#reviewTab > div > div > ul > li:nth-child({i}) > p > a')
                   uname = soup.select_one(
                        f' #reviewTab > div > div > ul > li:nth-child({i}) > span > a ')
                   date = soup.select_one(
                        f' #reviewTab > div > div > ul > li:nth-child({i}) > span > em:nth-child(2) ')
                   good = soup.select_one(
                        f' #reviewTab > div > div > ul > li:nth-child({i}) > span > em:nth-child(3) ')

                   if uname == None:
                        uname = None
                   else:
                        uname = uname.text

                   if date == None:
                        date = None
                   else:
                        date = date.text

                   if good == None:
                        good = None
                   else:
                        good = good.text

                   if title == None:
                        title = None
                   else:
                        title = title.text

                   if text_ == None:
                        text_ = None
                   else:
                        text_ = text_.text

                   # insert_tmp = [title.get_text(),, text.get_text(), uname.get_text(), date.get_text(), good.text()]
                   insert_tmp = [int(code_movie), title, text_, uname, date, good]

                   print(insert_tmp)
                   insert_data.append(insert_tmp)

    curs.executemany(sql, insert_data)
    conn.commit()
finally:
    conn.close()
