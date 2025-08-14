import streamlit as st
import sqlite3

# ページ上部アンカー
st.markdown('<a name="top"></a>', unsafe_allow_html=True)

st.title("📚 kamiyawarさんの回答検索")

# Font Awesome CDN 読み込み
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# 検索タイプ
search_type = st.radio("検索タイプを選択してください", ("AND検索", "OR検索"))
keywords_input = st.text_input("検索キーワード（スペース区切り）")

if keywords_input:
    keywords = keywords_input.strip().split()
    
    conn = sqlite3.connect("kamiyawar_answers.db")
    c = conn.cursor()

    if search_type == "AND検索":
        where_clause = " AND ".join(["answer LIKE ?" for _ in keywords])
    else:
        where_clause = " OR ".join(["answer LIKE ?" for _ in keywords])
    
    params = ['%' + kw + '%' for kw in keywords]
    query = f"SELECT url, answer FROM answers WHERE {where_clause}"
    
    c.execute(query, params)
    results = c.fetchall()
    conn.close()

    if results:
        st.write(f"検索結果: {len(results)} 件")
        for url, answer in results:
            st.write("**URL:**", url)
            st.write("**Answer:**", answer)
            st.write("---")
    else:
        st.write("該当する回答はありません。")

# Font Awesome ボタン
st.markdown("""
<style>
#scroll-top-button {
    position: fixed;
    bottom: 40px;
    right: 40px;
    background: rgba(76, 175, 80, 0.9);
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    text-align: center;
    line-height: 50px;
    font-size: 24px;
    font-family: 'Font Awesome 5 Free';
    font-weight: 900;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: all 0.2s ease-in-out;
    z-index: 100;
}
#scroll-top-button:hover {
    background: rgba(76, 175, 80, 1);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    transform: translateY(-2px);
}
#scroll-top-button::before {
    content: '\\f062'; /* Font Awesome 上矢印 */
}
</style>
<a href="#top" id="scroll-top-button"></a>
""", unsafe_allow_html=True)
