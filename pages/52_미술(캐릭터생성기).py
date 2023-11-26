import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

if password == correct_password:
    st.title("자신만의 캐릭터 만들기")
    st.header("캐릭터 정보")

    # 사용자 입력
    name = st.text_input("이름을 입력하세요:")
    gender = st.radio("성별:", ('남성', '여성'))
    age = st.slider("나이:", 5, 100)

    # 머리색, 눈 색상 및 캐릭터 스타일 선택
    hair_colors = ['검정', '갈색', '금발', '빨강', '회색', '흰색', '기타']
    eye_colors = ['검정', '갈색', '파랑', '초록', '회색', '호박색', '기타']
    character_styles = ['만화 스타일', '리얼리스틱 스타일', '수채화 스타일', '스케치 스타일', '픽셀 아트 스타일']

    hair_color = st.selectbox("머리 색상 선택:", hair_colors)
    eye_color = st.selectbox("눈 색상 선택:", eye_colors)
    character_style = st.selectbox("캐릭터 스타일 선택:", character_styles)

    favorite_activity = st.text_input("가장 좋아하는 활동은 무엇인가요?")
    animal = st.text_input("동물이라면 무엇이 되고 싶나요?")

    generate_button = st.button("캐릭터 생성")

    if generate_button:
        # 필수 필드가 모두 채워졌는지 확인
        if not all([name, gender, hair_color, eye_color, favorite_activity, animal]):
            st.warning("모든 필수 필드를 채워주세요!")
        else:
            prompt = f"{name}, {gender}로서 나이는 {age}, 머리 색상은 {hair_color} 및 눈 색상은 {eye_color}, {character_style}에서 {favorite_activity}을(를) 즐기는 모습. 그리고 같은 활동을 하는 {animal}의 이미지."

            try:
                # 컬러 이미지 생성
                color_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                color_image_url = color_image_response.data[0].url
                st.image(color_image_url, caption="캐릭터 이미지")

                # 이미지 다운로드 버튼
                response = requests.get(color_image_url)
                image_bytes = BytesIO(response.content)
                st.download_button(label="이미지 다운로드",
                                   data=image_bytes,
                                   file_name=f"character.jpg",
                                   mime="image/jpeg")
            except AttributeError as e:
                st.error("응답을 처리하는 중 오류 발생: " + str(e))
else:
    st.warning("정확한 비밀번호를 입력하세요.")
