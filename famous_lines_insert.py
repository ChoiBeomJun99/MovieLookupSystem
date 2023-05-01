import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost", user="root", password="1019", db="final", charset="utf8")
try:
    curs = conn.cursor()
    sql = """insert into famous_lines(code_movie, famous_line, enter_date)
             values (%s, %s, now())"""

    insert_data = []
    code_movies = []  # 이곳에 movie_code.txt에 코드들을 넣는다. 그 후 실행하면 정상적 실행

    temp = set(code_movies)
    code_movies = list(temp)

    count = 0
    for code_movie in code_movies:
        url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code_movie}'

        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            #Famous_lines 명대사

            famous_lines = soup.select('#content > div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li')

            if famous_lines is None:
                famous_lines = None
                insert_tmp = [code_movie, famous_lines]
                insert_data.append(insert_tmp)
            else:
                for line in famous_lines:
                    tmp = line.select_one('div > div > strong')

                    if tmp is None :
                        famous_lines = None;
                        insert_tmp = [code_movie, famous_lines]
                        insert_data.append(insert_tmp)
                    else:
                        famous_lines = tmp.text.strip()
                        insert_tmp = [code_movie, famous_lines]
                        insert_data.append(insert_tmp)
                        print(insert_tmp)

            print(count)
            count += 1
            # insert_tmp = [code_movie, genre]
            # insert_data.append(insert_tmp)

    curs.executemany(sql, insert_data)
    conn.commit()

finally:
    conn.close()


