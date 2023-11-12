import openai
import streamlit as st

# API 키 설정
openai.api_key = st.secrets["api_key"]

# DALL-E 이미지 생성 요청
response = openai.Image.create(
    model="dall-e-3",
    prompt="a white siamese cat",
    n=1,
    size="1024x1024"
)

# 이미지 URL 가져오기
image_url = response.data[0].url
