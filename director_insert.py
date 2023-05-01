import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost", user="root", password="1019", db="final", charset="utf8")

try:
    curs = conn.cursor()
    sql = """insert into director(director_code, code_movie, name_korean, name_English, work_name, enter_date)
             values (%s, %s , %s, %s, %s, now())"""

    movie_codes = []
    insert_data = []
    code_directors = []
    director_code = [] #이 List에 direct_code를 넣은 후 실행

    # url = 'https://movie.naver.com/movie/bi/pi/basic.naver?code=180101'

    for director in director_code:

        url = f'https://movie.naver.com/movie/bi/pi/basic.naver?code={director}'

        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            name_korean = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a')

            if name_korean is None:
                name_korean = None
            else:
                name_korean = name_korean.text.strip()

            name_english = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > strong')

            if name_english is None:
                name_english = None
            else:
                name_english = name_english.text.strip()

            works = soup.select('#content > div.article > div.section_group.section_group_frst > div > div > ul > li')

            if works is None:
                works_tmp = None
            else:
                for work in works:
                    tmp = work.select_one('div > strong > a')
                    if tmp is None:
                        works_tmp = None
                        works_code_tmp = None
                        # director_code, movie_code, name_korean, name_english, work
                        insert_tmp = [director, works_code_tmp, name_korean, name_english, works_tmp]
                        insert_data.append(insert_tmp)
                        print(insert_tmp)
                    else:
                        works_tmp = tmp.text.strip()

                        works_code_tmp = tmp['href']
                        index = works_code_tmp.find('=')
                        works_code_tmp = works_code_tmp[index + 1:]

                        insert_tmp = [director, works_code_tmp, name_korean, name_english, works_tmp]
                        insert_data.append(insert_tmp)
                        print(insert_tmp)
                        # insert_tmp = [name_korean, name_english, works_tmp, works_code_tmp]

                        # print(name_korean)
                        # print(name_english)
                        # print(works_tmp)
                        # print(works_code_tmp)

    curs.executemany(sql, insert_data)
    conn.commit()

finally:
    conn.close()