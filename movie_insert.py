import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost", user="root", password="1019", db="final", charset="utf8")
try:
    curs = conn.cursor()
    sql = """insert into movie(code_movie, title, title_English, netizen_rate, audience_rate, review_count, playing_time,opening_date, image, enter_date)
             values (%s, %s, %s, %s, %s, %s, %s, %s , %s, now())"""

    insert_data = []
    count = 0

    code_movies = []  # 이곳에 movie_code.txt에 코드들을 넣는다. 그 후 실행하면 정상적 실행
    temp = set(code_movies)
    code_movies = list(temp)

    for code_movie in code_movies:
        url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code_movie}'

        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            #제목
            title = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a')

            if title is None:
                title = None
            else:
                title = title.text

            #제목(in English)
            title_English = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > strong')

            if title_English is None :
                title_English = None
            else:
                title_English = title_English.text

                index = title_English.find(',')
                title_English = title_English[0:index]

            #네티즌 평점

            netizen_rate = ""
            netizen_rates = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.star_score')

            if netizen_rates is None:
                netizen_rate = 0.00
            else:
                tmp = netizen_rates.find_all('em')

                if tmp is None:
                    netizen_rate = 0.00
                else:
                    for i in tmp:
                        tmp1 = i.text
                        netizen_rate += tmp1

            #관람객 평점

            audience_rate = ""
            audience_rates = soup.select_one('#actualPointPersentBasic > div')

            if audience_rates is None:
                audience_rate = 0.00
            else :
                tmp = audience_rates.find_all('em')
                if tmp is None:
                    audience_rate = 0.00
                else:
                    for i in tmp:
                        tmp1 = i.text
                        audience_rate += tmp1

            #리뷰 수
            review_count = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_total > strong > em')

            if review_count is None:
                review_count = 0
                review_count2 =soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(4) > div:nth-child(2) > div.score_total > strong > em')
                if review_count2 is None:
                    review_count = 0
                else:
                    review_count = review_count2.text.replace(',','').strip()
            else :
                review_count = review_count.text.replace(',','').strip()


            #상영시간
            playing_time = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)')

            if playing_time is None:
                playing_time = None
            else:
                if playing_time.text.find('분') == -1:
                    playing_time = None
                else:
                    playing_time = playing_time.text
                    playing_time = playing_time.replace('분','').strip()
                    playing_time = int(float(playing_time))



            #개봉날짜
            opening_year = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(1)')

            if opening_year is None:
                opening_year = None
            else:
                opening_year = opening_year.text.strip()

            opening_monthd = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(2)')

            if opening_monthd is None:
                opening_monthd = None
            else:
                opening_monthd =opening_monthd.text

            if opening_year is None and opening_monthd is None:
                opening_date = None
            else:
                opening_date = opening_year + opening_monthd

            #image
            image = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')

            if image is None:
                image = None
            else:
                image = image['src']


            insert_tmp = [int(code_movie), title, title_English, netizen_rate, audience_rate, int(float(review_count)), playing_time,opening_date, image]
            print(insert_tmp)
            print(count)
            count += 1
            insert_data.append(insert_tmp)

    curs.executemany(sql, insert_data)
    conn.commit()

finally:
    conn.close()