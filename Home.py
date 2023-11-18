import streamlit as st
import openai

openai.api_key = st.secrets

st.set_page_config(layout="wide")

st.title("초등학교 인공지능 도구 모음")

st.divider()

st.header("왼쪽의 페이지에서 원하는 도구를 선택하세요.")

st.write("비밀번호가 걸려있습니다.")


#팁
#powershell 말고 cmd에서 실행
#conda env list 가상환경 이름 잊었을 때 설정한 가상환경 리스트 확인
#streamlit run home.py
#ctrl C하면 빠져나옴
#screts.tomi 는 그냥 복사해서 씀
#commit 실수했을때는 복구해보기

#github에 뉴repository만들기
#…or push an existing repository from the command line 복사
#터미널 git bash 실행
#git init
#git add .
#git commit -m one
#복사한거 붙여넣기 엔터
#github 새로고침 - 올라가있음
#원격저장소 에러시 참고 https://chat.openai.com/c/dc510df8-e93f-42e5-8b66-314d19694b3e
#share.streamlit.io 이동 정보이동
#advanced setting - api key 그대로 입력
