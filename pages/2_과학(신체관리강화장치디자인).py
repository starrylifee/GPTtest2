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
    st.title("신체 관리 및 강화장치 이미지 생성기")

    # 장치 유형 선택
    device_type = st.selectbox("장치 유형 선택", ["관리장치", "강화장치"])

    # 관리장치 선택 시
    if device_type == "관리장치":
        organ = st.selectbox("어떤 기관을 관리하겠습니까?", ["심장", "폐", "피부", "눈", "코", "입", "배설기관"])
        effect1 = st.text_input("어떻게 관리하는지 설명을 문장으로 적어주세요 1")
        effect2 = st.text_input("어떻게 관리하는지 설명을 문장으로 적어주세요 2")
        effect3 = st.text_input("어떻게 관리하는지 설명을 문장으로 적어주세요 3")

    # 강화장치 선택 시
    elif device_type == "강화장치":
        organ = st.selectbox("어떤 기관을 강화하겠습니까?", ["근육", "뼈", "신경계", "뇌", "눈", "코", "입", "팔", "다리", "소화기관"])
        effect1 = st.text_input("강화된 기관으로 할 수 있는 일을 문장으로 적어주세요 1")
        effect2 = st.text_input("강화된 기관으로 할 수 있는 일을 문장으로 적어주세요 2")
        effect3 = st.text_input("강화된 기관으로 할 수 있는 일을 문장으로 적어주세요 3")

    generate_button = st.button("이미지 생성")

    if generate_button:
        prompt = f"{organ}을 위한 {device_type}. 변화: {effect1}, {effect2}, {effect3}."

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
            st.image(generated_image_url, caption="생성된 신체 관리 및 강화장치")

            # 이미지 다운로드 준비
            response = requests.get(generated_image_url)
            image_bytes = BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="body_device.jpg",
                               mime="image/jpeg")
        except AttributeError as e:
            st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
