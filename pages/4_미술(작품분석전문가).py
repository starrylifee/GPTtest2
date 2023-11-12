import streamlit as st
import openai
import requests
from io import BytesIO

# OpenAI API 키를 Streamlit secrets에서 가져옵니다.
openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

# 제목 및 헤더
st.title("미술작품 분석하기")
st.header("문제상황")

# 설명
text = '''
아래 드롭다운 메뉴에서 미술 작품을 선택하고 주제, 조형요소, 원리에 대해서 분석해보세요.
'''
st.write(text)

# 이미지 URL과 캡션을 딕셔너리로 정의
images = {
    'Composition II with Red Blue and Yellow': 'https://img.hani.co.kr/imgdb/resize/2012/0310/133125919362_20120310.JPG',
    '세한도': 'https://img1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/aXte/image/TkVLv4CxMI4Z8o0qN6B9O3eZFTI.png',
    '절규': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/1607px-The_Scream.jpg',
    '피레네의 성': 'https://www.greencurator.co.kr/data/item/GC17-A502-RM40MOT/GC17A502RM40MOT.jpg'
}

# 드롭다운 메뉴를 생성하고 사용자의 선택을 가져옵니다.
selected_caption = st.selectbox("미술 작품을 선택하세요:", options=list(images.keys()))

# 선택된 캡션에 해당하는 이미지를 표시합니다.
st.image(images[selected_caption], caption=selected_caption)

# 사용자 입력
elements1 = st.text_input("점, 선, 면에 대해서 적어보세요.")
elements2 = st.text_input("그림의 질감에 대해서 적어보세요")
elements3 = st.text_input("그림의 공간에 대해서 적어보세요")
principles1 = st.text_input("그림의 균형, 대비, 강조, 리듬, 조화에 대해서 적어보세요.")
subject1 = st.text_input("그림에 그려진 것들에 대해서 적어보세요.")
subject2 = st.text_input("그림의 각 공간에 그려진 것들에 대해서 적어보세요.")

