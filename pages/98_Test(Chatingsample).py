import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

# 입력된 비밀번호가 올바른지 확인합니다.
if password == correct_password:

    st.title("간단한 GPT-3.5 테스트")

    # 사용자 입력 받기
    user_input = st.text_input("질문을 입력하세요:")

    # 버튼이 클릭되면 응답 생성
    if st.button("응답 생성"):
        try:
            # GPT-3.5 API 호출
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )
            # 응답 데이터 구조 확인
            st.write("Response object:", response)
            # 응답 표시
            st.write("Generated response:", response.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.warning("올바른 비밀번호를 입력해주세요.")