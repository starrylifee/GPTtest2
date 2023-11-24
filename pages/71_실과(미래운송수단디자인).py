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
    st.title("미래 교통 및 운송수단 만들기")

    # 사용자 입력
    transportation_type = st.selectbox("기본 교통수단 선택", ["자전거", "오토바이", "자동차(세단)", "자동차(SUV)", "자동차(버스)", "비행기", "킥보드", "배", "드론"])
    passenger_capacity = st.number_input("탑승 가능 인원", min_value=1, max_value=100, step=1)
    modification = st.text_input("변형할 물건 (예: 바퀴를 날개로 바꿉니다)")

    # 색상 선택 드롭다운
    color_options = {
        "빨간색": "#FF0000",
        "녹색": "#008000",
        "파란색": "#0000FF",
        "노란색": "#FFFF00",
        "주황색": "#FFA500",
        "보라색": "#800080",
        "분홍색": "#FFC0CB",
        "갈색": "#A52A2A",
        "회색": "#808080",
        "검정색": "#000000",
        "하늘색": "#87CEEB",
        "금색": "#FFD700",
        "은색": "#C0C0C0",
        "자홍색": "#FF00FF",
        "라임색": "#00FF00",
        "네이비색": "#000080",
        "올리브색": "#808000",
        "민트색": "#3EB489",
        "살구색": "#FBB982",
        "청록색": "#00FFFF"
    }
    color = st.selectbox("색상 선택", list(color_options.keys()))

    feature1 = st.text_input("특수 기능 1")
    feature2 = st.text_input("특수 기능 2")
    feature3 = st.text_input("특수 기능 3")

    generate_button = st.button("이미지 생성")

    if generate_button:
        prompt = f"미래의 {transportation_type}, 탑승 가능 인원: {passenger_capacity}, 변형: {modification}, 색상: {color_options[color]}, 특수 기능: {feature1}, {feature2}, {feature3}."

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
            st.image(generated_image_url, caption="미래 교통 및 운송수단")

            # 이미지 다운로드 준비
            response = requests.get(generated_image_url)
            image_bytes = BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="future_transport.jpg",
                               mime="image/jpeg")
        except AttributeError as e:
            st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
