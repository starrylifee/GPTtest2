import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
import wikipedia

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
    historical_event = st.text_input("역사적 사건")

    generate_button = st.button("역사적 정보 검색 및 이미지 생성")

    if generate_button and historical_event:
        # 위키백과에서 역사적 사건 정보 검색
        try:
            event_summary = wikipedia.summary(historical_event)
            st.text_area("역사적 사실", event_summary, height=250)
        except Exception as e:
            st.error(f"Error retrieving information: {e}")

        prompt = f"{era}의 {location}에서 역사적 사건 '{historical_event}'에 관련된 장면. 배경 설명: {event_summary}"

        # OpenAI API를 호출하여 이미지 생성
        try:
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
