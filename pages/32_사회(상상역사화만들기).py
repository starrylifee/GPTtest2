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
    st.title("상상속의 역사화 만들기")

    # 사용자 입력
    era = st.selectbox("시대 선택", ["선사시대", "삼국시대", "고려시대", "조선시대", "일제강점기", "현대"])
    location = st.text_input("장소")
    character1 = st.text_input("등장 인물 1")
    character2 = st.text_input("등장 인물 2")
    character3 = st.text_input("등장 인물 3")
    background = st.text_area("배경 묘사")
    historical_fact = st.text_area("역사적 사실")

    generate_button = st.button("이미지 생성")

    if generate_button:
        # 입력된 캐릭터를 기반으로 프롬프트 구성
        characters = [character1, character2, character3]
        characters = [character for character in characters if character]  # 빈 문자열 제외
        characters_str = ", ".join(characters) if characters else "인물 없음"

        prompt = f"{era}의 {location}에서 {characters_str}가 있는 장면. 배경: {background}. 역사적 사실: {historical_fact}."

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
            st.image(generated_image_url, caption="생성된 역사화")

            # 이미지 다운로드 준비
            response = requests.get(generated_image_url)
            image_bytes = BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="custom_historical_painting.jpg",
                               mime="image/jpeg")
            
        except AttributeError as e:
            st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
