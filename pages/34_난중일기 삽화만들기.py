import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 객체 생성 및 API 키 제공
client = OpenAI(api_key=st.secrets["api_key"])

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("Enter your password:", type="password")
correct_password = st.secrets["password"]

# 입력된 비밀번호가 정확한지 확인
if password == correct_password:
    st.title("임진왜란 관련 이미지 생성")

    # 사용자 입력
    character = st.selectbox("등장 인물 선택", ["선조", "신하", "백성", "군인", "장군", "이순신 장군", "왜군", "명나라 병사, 의병"])
    emotion = st.text_input("예상되는 마음")

    generate_button = st.button("이미지 생성")

    if generate_button:
        # 프롬프트 구성
        prompt = f"조선 임진왜란 시, {character}의 입장에서 {emotion}을 느끼는 장면. 이순신 장군과의 전투, 왜군의 침략, 백성들의 고통, 명나라 병사의 지원 등을 상상하여 그림으로 표현."

        try:
            # OpenAI API를 호출하여 이미지 생성
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",
                quality="standard",
                n=1
            )

            # 생성된 이미지 표시
            generated_image_url = image_response.data[0].url
            st.image(generated_image_url, caption="생성된 이미지")

            # 이미지 다운로드 준비
            response = requests.get(generated_image_url)
            image_bytes = BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="historical_imagination.jpg",
                               mime="image/jpeg")
            
        except AttributeError as e:
            st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
