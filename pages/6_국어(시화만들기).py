import streamlit as st
import openai

# OpenAI API 키를 Streamlit secrets에서 가져옵니다.
openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

# 제목 및 헤더
st.title("시에 맞는 이미지 만들기")
st.header("시를 입력하고 연관된 이미지를 생성해보세요")

# 사용자 입력
poem = st.text_area("시를 여기에 입력하세요.")
