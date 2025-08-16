from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import time

# DB接続
conn = sqlite3.connect("kamiyawar_answers.db")
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    answer TEXT
)
''')
conn.commit()

# URL一覧を読み込む
with open("failed_urls_no_answer_nur2", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# 失敗ファイル
request_failed_file = "failed_urls_request_nur4"
no_answer_file = "failed_urls_no_answer_nur4"

# Selenium設定
options = Options()
# options.add_argument("--headless")  # ヘッドレスにする場合
driver = webdriver.Chrome(options=options)

# 手動でYahooにログインしてEnter押す
input("Yahoo!にログインしてページを開いたらEnterキーを押してください…")

for url in urls:
    try:
        driver.get(url)
        time.sleep(3)  # JS読み込み待ち

        soup = BeautifulSoup(driver.page_source, "html.parser")

        answers = soup.find_all("div", itemprop="text")
        found = False
        for ans in answers:
            author_tag = ans.find_previous("p", itemprop="author")
            author = author_tag.get_text(strip=True) if author_tag else ""
            if author.startswith("kam") or author.startswith("神夜王") or author.startswith("深夜のネオン・ドクター"):
                answer_text = ans.get_text(separator="\n", strip=True)
                c.execute('INSERT INTO answers (url, answer) VALUES (?, ?)', (url, answer_text))
                conn.commit()
                found = True

        if not found:
            with open(no_answer_file, "a") as f:
                f.write(url + "\n")
            print(f"回答なし: {url}")

        time.sleep(1)

    except Exception as e:
        print(f"リクエスト失敗: {url} ({e})")
        with open(request_failed_file, "a") as f:
            f.write(url + "\n")

driver.quit()
conn.close()
print("処理完了。DBに保存、HTTP失敗URLと回答なしURLは別ファイルに記録しました。")
