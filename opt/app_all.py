from bs4 import BeautifulSoup
import requests
import pandas as pd

csv_list = []

# 中学社会ページから、一問一答ページのURLリストを取得する
link_url = 'https://jyosiki.com/C_S.html'
link_r = requests.get(link_url)
l_soup = BeautifulSoup(link_r.content, 'html.parser')
sub_list = l_soup.find(id="main2")
sub_a = sub_list.find_all("a")

urls = []
for a in sub_a:
    urls.append(a.get('href'))

sla = link_url.rfind('/')
url_list = []
for url_data in urls:
    url_list.append(link_url[:sla+1] + url_data)

# 一問一答ページから、問題・回答を取得し、配列に格納する
for url in url_list:
    answers = []
    questions = []
    tmp_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    elems = soup.find_all(class_="mainmondai")

    if len(elems) > 0:
        # 回答リスト
        dd_list = elems[0].find_all('dd')
        answers = []
        for dd in dd_list:
            answers.append(dd.find('span').text)

        # 問題リスト
            dt_list = elems[0].find_all('dt')
            questions = []
            for dt in dt_list:
                tt = dt.text.replace('\xa0\xa0\t','')
                idx = tt.find('.')
                questions.append(tt[idx+1:])

        # 問題リスト＋回答リストの配列
        tmp_list = []
        i = 0
        for question in questions:
            tmp_list.append([question, answers[i]])
            i+=1

        csv_list.extend(tmp_list)

# CSV出力
df = pd.DataFrame(csv_list)
df.to_csv('../結果_all.csv')