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

# Cookie（例：ブラウザから取得）
cookies = {
    # 必要なCookieを入れる
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

# URL一覧をファイルから読み込む
with open("failed_urls_request_nur2", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

request_failed_file = "failed_urls_request_nur3"
no_answer_file = "failed_urls_no_answer_nur3"

MAX_PAGE = 30  # 最大ページ数

def fetch_and_store(url):
    """指定URLからkamiyawarの回答を探し、見つかれば保存してTrueを返す"""
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        answers = soup.find_all("div", itemprop="text")
        for ans in answers:
            author_tag = ans.find_previous("p", itemprop="author")
            author = author_tag.get_text(strip=True) if author_tag else ""
            if author.startswith("kam") or author.startswith("神夜王") or author.startswith("深夜のネオン・ドクター"):
                answer_text = ans.get_text(separator="\n", strip=True)
                c.execute('INSERT INTO answers (url, answer) VALUES (?, ?)', (url, answer_text))
                conn.commit()
                return True
        return False

    except Exception as e:
        print(f"リクエスト失敗: {url} ({e})")
        with open(request_failed_file, "a") as f:
            f.write(url + "\n")
        return None

for base_url in urls:
    found = fetch_and_store(base_url)

    if found is None:
        # リクエスト自体が失敗した場合は次のURLへ
        continue

    if not found:
        # ページ番号を変えて再検索
        for page in range(2, MAX_PAGE + 1):
            page_url = f"{base_url}?sort=1&page={page}"
            found_page = fetch_and_store(page_url)
            if found_page:
                print(f"{page}ページ目で発見: {page_url}")
                break
            elif found_page is None:
                break  # 通信エラーなら中断
            time.sleep(1)
        else:
            # 全ページ試しても見つからなかった
            with open(no_answer_file, "a") as f:
                f.write(base_url + "\n")
            print(f"回答なし（全ページ）: {base_url}")

    time.sleep(1)

conn.close()
print("処理完了。")
