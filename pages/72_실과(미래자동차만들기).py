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
    st.title("미래 자동차 디자인 생성")

    # 자동차 유형 선택
    car_type = st.selectbox("자동차 유형 선택", ["전기차", "하이브리드", "태양열 자동차", "자율 주행 차량"])

    # 디자인 스타일
    design_style = st.selectbox("디자인 스타일", ["미래적", "클래식", "스포티"])

    # 차량 크기
    car_size = st.slider("차량 크기 선택", min_value=1, max_value=10)

    # 휠 디자인
    wheel_design = st.selectbox("휠 디자인", ["전통적", "현대적", "미래적"])

    # 색상 선택
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

    # 날개 유무 선택
    has_wings = st.selectbox("날개 유무", ["있음", "없음"])

    # 특수 기능 입력
    feature1 = st.text_input("특수 기능 1 (예: 고속 충전)")
    feature2 = st.text_input("특수 기능 2 (예: AI 보조 운전)")
    feature3 = st.text_input("특수 기능 3 (예: 확장형 인터랙티브 대시보드)")

    # 이미지 생성 버튼
    generate_button = st.button("이미지 생성")

    if generate_button:
        # DALL-E에 전달할 프롬프트 구성
        prompt = f"미래의 자동차를 그려줘. 자동차의 타입은 {car_type}, 디자인 스타일: {design_style}, 크기: {car_size}, 휠 디자인: {wheel_design}, 색상: {color_options[color]}, 날개: {has_wings}, 특수 기능: {feature1}, {feature2}, {feature3}."

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
            st.image(generated_image_url, caption="미래 자동차 디자인")

            # 이미지 다운로드 준비
            response = requests.get(generated_image_url)
            image_bytes = BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="future_car_design.jpg",
                               mime="image/jpeg")
        except AttributeError as e:
            st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
