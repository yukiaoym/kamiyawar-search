import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# 保存先DB
conn = sqlite3.connect("kamiyawar_answers.db")
c = conn.cursor()

# テーブル作成（存在しない場合）
c.execute('''
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    answer TEXT
)
''')
conn.commit()

# Cookieを辞書形式で用意（例: 手動でブラウザから取得）
cookies = {
    "_n": "cGqXa8MFQs3ITa7NVfN3SI_uPNOsj-OkAAq89Sw8WzB3djlqQuW7m01ihhrp0XJO0u_OLQqjkigRinWxxWlekRucvDp_3kxRLAx76WSSb3MRbLkApLgQlkzh_gYybygauH47Bm1dl0uXEbvrIJIsHXDGNXRw-Lw8FY1HTsdDxWr9I3slJhOR3X-zXZHQIiRHgTNuraOoTixM8a3pqyGRpUBH-flGgQ0g-HQYeMx2NxQVUtkq7wCt53Ou65SL8uIXO9CYaM4KgDuZtLjLRiOeuHKM44lJ79O7G7irLRF-9TPJLjgXTUIkV573Gk2cpQOY3F0ok_HI5u26mbpgn88iF-lucmsCBC0sK8Ves7LhTABgPZwlB05bsgmSjF20gDNQ6H9hWYbZwxT26Q_o1lntMsV3ZCaDkXIR-ptIGjgoY6u_wcBIEps5w1cAn5ONT7T9jS0uqxlHtIYruZEetLaiNiAU2sjAE4GFLwTDl3rTQfjNxR4FqkFjt6iXYZHAHJ2YZyQwwmErWPPZzTBnW-nX-8yDAnCTS9k_jeEW7VOsGsK7Yf9cUTHZesS8Yt9CoYhAUyTDAc6iQRw8RwvJj0eVSoBxz0zt36MxkguZK3JjlKZf1SY5nTGagaAfCg3v-KdQIOdYM0KEHeEUvNRDDuHRCKu9-ZGdMcuz_Lr6elBAyafRR0rMB0fsvWG5wG3tXmIe-ohbCcbyEvdkvIQLOQCAfCec9RM-4alj5XUYLn-rgs0bOXd5FkFrrqnXkHFUP3907KeodL0M_KTVuEn0cxZKPFxm-7c2VO5aWkPGF4yqtPgbwphdTKXCgukPtrFei4TsBhyjxTaRaZMCvFz3mao0mo_jbMYJZhudpm8AFl1ZMYbNpXm8hqYW0aqgLV75Exuify3lXKD4NiEaDhSultKnAC_QtriD7LMOpt7B4NLleyOxoKm_3hMM67RHeTA43-YSqXqpV8dinxqQt2kMpnjiudxAc6FcFhiRLWGPt1_qKWPLtHi_jk5Drd6IscG85A3Y-sxp6lQ1x139OWte-H-sVayJxLVQw3lPvpcjkIngxlWppDxM_JYW-ArkngHbvWtQ.3",      # 実際のYahoo! Cookie値
    "A": "7c6q18lk3qglh&t=1748845233&u=1755124648&sd=A&v=1&sc=off&d=C08MKWPROjfMIMhP/FpYbAQevBkyOO+UBZpSSXRG4OPfKqOMXMJotGet6P1u8313pp4LgZQmqQd1oHMDHIZEKN7I6Me1WgFia3EnRfj3L/ry0/CEdGfp/WW5WJq5zY+70nNyqyNE3UXzh/jL/0",
    "JV": "A74ugGgAAHmiXmgxTAko0WSSBKXhCh54xNKCdbNgx0126B3iOd2Dm3ggFePXqZHCoxSex0Wj2IyyX0t2zk-Q2gvFe7QEeTlSd6BuhY51UOot1Mhjyc_NJFlAFxhZrx4TtlhNolq6EE4HBj1VT96E0SRwbjJ9vFFk-nQVIrfFp9XlIEFIRgbDyIMcJ0VllYebfLWkjnljFvKnhR3JFdKH_sQPIld8Ur-Y1N0lJpAk0IdcHphC1y2SVZjwvJ2eYMOkIOOCxJubXtr0It422IBNEGKaL1QAJ0fXYTOvI7hRUSnuz9mm_RvhI5yI2F_QLIjDdFNk8rzQPYJrpbB9arZIv6EQUhWyp2Q0FiLx41sjqcknd5C_Rar3QvTGkf4k_DfJ9QdwZBoirNQhQB5DwT-hFqUPF6UQjwXgJ-Za-l3lrFnlxX37ds-eMdWiUDeZq--PaFWblaNPgvHvaCSbelm_tzDwAPsqmdVTIW4&v=2",
    "SSL": "1",
    "T": "aaca97d916d46d7cfcabe89523e1ca4fe0653663da3f16390c1473492b1eccbc",
    "XA": "7c6q18lk3qglh&t=1748845233&u=1755124648&sd=A&v=1&sc=off&d=C08MKWPROjfMIMhP/FpYbAQevBkyOO+UBZpSSXRG4OPfKqOMXMJotGet6P1u8313pp4LgZQmqQd1oHMDHIZEKN7I6Me1WgFia3EnRfj3L/ry0/CEdGfp/WW5WJq5zY+70nNyqyNE3UXzh/jL/0",
    "XB": "b08b78f0-3f79-11f0-8050-690332315c06&v=6&u=1748845233&s=vp",
    "Y": "v=2&l=f0083fba56e893daca1591ef3114236dfeae9b13177efab7c6e885e09fc315fc"# 他にも必要なCookieを全部入れる
}

# ヘッダーもブラウザっぽく
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

# URL一覧をファイルから読み込む
with open("url_list2", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# 失敗したURLを保存するファイル
request_failed_file = "failed_urls_request2"
no_answer_file = "failed_urls_no_answer2"

for url in urls:
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 回答ブロックをすべて取得
        answers = soup.find_all("div", itemprop="text")

        # kamiyawarさんの回答を抽出
        found = False
        for ans in answers:
            author_tag = ans.find_previous("p", itemprop="author")
            author = author_tag.get_text(strip=True) if author_tag else ""
            if author.startswith("kam"):
                answer_text = ans.get_text(separator="\n", strip=True)
                c.execute('INSERT INTO answers (url, answer) VALUES (?, ?)', (url, answer_text))
                conn.commit()
                found = True

        # 回答なしの場合
        if not found:
            with open(no_answer_file, "a") as f:
                f.write(url + "\n")
            print(f"回答なし: {url}")

        time.sleep(1)

    except Exception as e:
        print(f"リクエスト失敗: {url} ({e})")
        with open(request_failed_file, "a") as f:
            f.write(url + "\n")

conn.close()
print("処理完了。")
