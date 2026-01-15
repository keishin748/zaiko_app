import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# -------------------------
# DB初期化
# -------------------------
def init_db():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------
# DB接続
# -------------------------
def get_db():
    return sqlite3.connect("inventory.db")

# -------------------------
# タイトル
# -------------------------
st.title("在庫管理システム")

# -------------------------
# メニュー
# -------------------------
menu = st.sidebar.selectbox(
    "メニューを選択",
    ["商品登録", "一覧表示", "商品検索", "在庫更新", "商品削除"]
)

# -------------------------
# 商品登録
# -------------------------
if menu == "商品登録":
    st.subheader("商品登録")

    name = st.text_input("商品名")
    quantity = st.number_input("在庫数", min_value=0, step=1)
    price = st.number_input("価格", min_value=0, step=100)

    if st.button("登録"):
        if name == "":
            st.error("商品名を入力してください")
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO inventory (name, quantity, price, created_at) VALUES (?, ?, ?, ?)",
                (name, quantity, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()
            st.success("商品を登録しました")

# -------------------------
# 一覧表示
# -------------------------
elif menu == "一覧表示":
    st.subheader("在庫一覧")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    items = cur.fetchall()
    conn.close()

    if items:
        df = pd.DataFrame(
            items,
            columns=["ID", "商品名", "在庫数", "価格", "登録日時"]
        )
        st.dataframe(df)
    else:
        st.info("在庫がありません")

# -------------------------
# 商品検索
# -------------------------
elif menu == "商品検索":
    st.subheader("商品検索")

    keyword = st.text_input("検索する商品名")

    if st.button("検索"):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM inventory WHERE name LIKE ?",
            ("%" + keyword + "%",)
        )
        items = cur.fetchall()
        conn.close()

        if items:
            df = pd.DataFrame(
                items,
                columns=["ID", "商品名", "在庫数", "価格", "登録日時"]
            )
            st.dataframe(df)
        else:
            st.warning("該当する商品がありません")

# -------------------------
# 在庫更新
# -------------------------
elif menu == "在庫更新":
    st.subheader("在庫更新")

    item_id = st.number_input("商品ID", min_value=1, step=1)
    new_quantity = st.number_input("新しい在庫数", min_value=0, step=1)

    if st.button("更新"):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
        if cur.fetchone() is None:
            st.error("指定した商品IDは存在しません")
        else:
            cur.execute(
                "UPDATE inventory SET quantity = ? WHERE id = ?",
                (new_quantity, item_id)
            )
            conn.commit()
            st.success("在庫数を更新しました")
        conn.close()

# -------------------------
# 商品削除
# -------------------------
elif menu == "商品削除":
    st.subheader("商品削除")

    item_id = st.number_input("削除する商品ID", min_value=1, step=1)

    if st.button("削除"):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
        if cur.fetchone() is None:
            st.error("指定した商品IDは存在しません")
        else:
            cur.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            conn.commit()
            st.success("商品を削除しました")
        conn.close()
