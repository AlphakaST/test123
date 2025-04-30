# .streamlit/secrets.toml 예시:

# [dashboard]
# password = "YOUR_DASHBOARD_PASSWORD"

import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# 설정 로드
mysql_conf = st.secrets["mysql"]
dashboard_pw = st.secrets["dashboard"]["password"]

# 페이지 설정
st.set_page_config(page_title="교사용 대시보드", layout="wide")
st.title("🔒 교사용 대시보드")

# 비밀번호 입력
pw_input = st.text_input("대시보드 비밀번호를 입력하세요", type="password")
if pw_input != dashboard_pw:
    if pw_input:
        st.error("비밀번호가 올바르지 않습니다.")
    st.stop()

# 데이터베이스 연결 및 조회
try:
    conn = mysql.connector.connect(
        host=mysql_conf["host"],
        user=mysql_conf["user"],
        password=mysql_conf["password"],
        database=mysql_conf["database"],
        port=mysql_conf.get("port", 3306)
    )
    cursor = conn.cursor()
    query = (
        "SELECT student_id, answer1, answer2, answer3, answer4, answer5,"
        " feedback1, feedback2, feedback3, feedback4, feedback5, submitted_at"
        " FROM test1"
        " ORDER BY submitted_at DESC"
    )
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["학번", "답안1", "답안2", "답안3", "답안4", "답안5",
               "피드백1", "피드백2", "피드백3", "피드백4", "피드백5", "제출시각"]
    df = pd.DataFrame(rows, columns=columns)
    st.dataframe(df)

except Error as e:
    st.error(f"데이터 조회 오류: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
