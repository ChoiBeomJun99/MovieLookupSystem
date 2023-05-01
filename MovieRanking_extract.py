import csv
import time
import pymysql
import requests
from bs4 import BeautifulSoup

# 상위 2000 영화 div 추출

k = []
code_num = []

for page in range(1, 41):
    urls = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220604&page={page}'
    for j in range(2, 51):

        html = requests.get(urls)

        soup = BeautifulSoup(html.content, 'html.parser')

        title_url = soup.select_one(
            f'#old_content > table > tbody > tr:nth-child({j}) > td.title  ')
        if title_url == None:
            continue
        else:
            k.append(title_url)
            print(title_url)

# 상위 2000개 영화 코드 번호 추출

num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

for i in range(0, len(k)):

    a = list(str(k[i]))

    for j in range(0, len(a) - 3):

        if a[j] == "c" and a[j + 1] == "o" and a[j + 2] == "d" and a[j + 3] == "e":
            if a[j + 11] == " ":
                code_num.append(int("".join(a[j + 5:j + 10])))
                break
            else:
                code_num.append(int("".join(a[j + 5:j + 11])))
                break

print(code_num)


