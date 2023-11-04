import streamlit as st
import openai

openai.api_key = st.secrets

st.set_page_config(layout="wide")

st.title("초등학교 인공지능 도구 모음")

st.divider()

st.header("왼쪽의 페이지에서 원하는 도구를 선택하세요.")

st.write("starrylife")


#팁
#powershell 말고 cmd에서 실행
#conda env list 가상환경 이름 잊었을 때 설정한 가상환경 리스트 확인
#streamlit run home.py
#ctrl C하면 빠져나옴
#screts.tomi 는 그냥 복사해서 씀
#commit 실수했을때는 복구해보기
