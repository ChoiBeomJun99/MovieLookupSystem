import pymysql
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost", user="root", password="1019", db="final", charset="utf8")

try:
     count =0
     curs = conn.cursor()
     sql = """insert into actor(code_movie, actor_code, actor_name, role, casting_name, enter_date)
             values (%s, %s ,%s, %s, %s, now())"""

     code_movies = [] #이곳에 movie_code.txt에 코드들을 넣는다. 그 후 실행하면 정상적 실행
     temp = set(code_movies)
     code_movies = list(temp)

     insert_data = []

     for code_movie in code_movies:
          url = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code_movie}'

          response = requests.get(url)
          if response.status_code == 200:
               html = response.text
               soup = BeautifulSoup(html, 'html.parser')
               i =0

               actors = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > ul > li')

               for actor in actors:

                    if i == 0 :
                         i += 1

                    else:

                         actor_code = actor.select_one('a.tx_people')
                         if actor_code is None:
                              actor_code = None
                         else :
                              actor_code = actor_code['href']
                              index = actor_code.find('=')

                              actor_code = int(float(actor_code[index+1:]))

                         actor_name = actor.select_one('a.tx_people')

                         if actor_name is None:
                              actor_name = None
                         else:
                              actor_name = actor_name.text.strip()


                         role = actor.select_one('dl > dt')

                         if role is None:
                              role = None
                         else:
                              role = role.text.strip()

                         casting_name = actor.select_one('dl > dd')

                         if casting_name is None:
                              casting_name = None
                         else:
                              casting_name = casting_name.text.replace('역','').strip()

                         # print("영화 코드 : %s" % code_movie)
                         # print("배우 코드 : %s" %  actor_code)
                         # print("배우 이름 : %s" % actor_name)
                         # print("역할 : %s " % role)
                         # print("배역 이름 : %s " % casting_name)
                         # print("------------------------------------------------")

                         insert_tmp = [code_movie, actor_code, actor_name, role, casting_name]
                         print(insert_tmp)
                         print(count)
                         count+=1
                         insert_data.append(insert_tmp)

     curs.executemany(sql, insert_data)
     conn.commit()

finally:
     conn.close()

