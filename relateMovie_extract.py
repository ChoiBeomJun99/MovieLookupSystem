import requests
from bs4 import BeautifulSoup

k = []
code_movies = []  # 이곳에 movie_code.txt에 코드들을 넣는다. 그 후 실행하면 정상적 실행

f = open("C:/db/db.txt", 'w')
count = 0
for i in range(len(code_movies)-50,0,-1):
    urls = f'https://movie.naver.com/movie/bi/mi/basic.naver?code={code_movies[i]}'
    for j in range(1, 6):
        print(count)
        count+=1
        html = requests.get(urls)
        soup = BeautifulSoup(html.content, 'html.parser')
        title_url = soup.select_one( f' #content > div.article > div:nth-child(7) > div:nth-child({j}) ')
        if title_url == None:
            continue
        else:
            a = list(str(title_url))
            for j in range(0, len(a)-3):

                if a[j] == "c" and a[j+1] == "o" and a[j+2] == "d" and a[j+3] == "e":
                    if a[j+11] == " " or a[j+11] == "#" or a[j+11] == "&":
                        f.write("".join(a[j+5:j+10]))
                        f.write(",")
                        code_movies.append(int("".join(a[j+5:j+10])))
                        break
                    elif a[j+9] == " " or a[j+9] == "#" or a[j+9] == "&":
                        f.write("".join(a[j+5:j+8]))
                        f.write(",")
                        code_movies.append(int("".join(a[j+5:j+8])))
                        break
                    elif a[j+10] == " " or a[j+10] == "#" or a[j+10] == "&":
                        f.write("".join(a[j+5:j+9]))
                        f.write(",")
                        code_movies.append(int("".join(a[j+5:j+9])))
                        break
                    else:
                        f.write("".join(a[j+5:j+11]))
                        f.write(",")
                        code_movies.append(int("".join(a[j+5:j+11])))
                        break