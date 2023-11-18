import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 객체 생성 시 API 키를 직접 제공
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

# 이미지 생성 요청
response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

# 응답에서 이미지 URL 추출 (API 업데이트에 따라 달라질 수 있음)
image_url = response.data[0].url  # 예시로, 실제 응답 구조에 맞춰야 함

# 이미지 URL 출력
st.image(image_url)
