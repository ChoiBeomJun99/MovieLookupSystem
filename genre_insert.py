import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost", user="root", password="1019", db="final", charset="utf8")
count = 0
try:
    curs = conn.cursor()
    sql = """insert into genre(code_movie, genre, enter_date)
             values (%s, %s, now())"""



    insert_data = []
    code_movies = []  # 이곳에 movie_code.txt에 코드들을 넣는다. 그 후 실행하면 정상적 실행
    temp = set(code_movies) #중복 제거
    code_movies = list(temp)

    for code_movie in code_movies:
        url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code_movie}'

        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            #장르
            genres = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1)')

            if genres is None:
                genre = None
                insert_tmp = [code_movie, genre]
                insert_data.append(insert_tmp)

            else:
                tmp = genres.find_all('a')

                if tmp is None:
                    genre = None
                    insert_tmp = [code_movie, genre]
                    insert_data.append(insert_tmp)
                else:
                    for i in tmp:
                        genre = i.text
                        # print(code_movie)
                        # print(genre)
                        insert_tmp = [code_movie, genre]
                        insert_data.append(insert_tmp)

            print(count)
            print(insert_tmp)
            count += 1

    curs.executemany(sql, insert_data)
    conn.commit()

finally:
    conn.close()


