import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

# 제목 및 헤더
st.title("시에 맞는 이미지 만들기")
st.header("시를 입력하고 시에 어울리는 그림을 생성해보세요")

# 사용자 입력
poem = st.text_area("시를 여기에 입력하세요.")
subject = st.text_input("그림에 꼭 들어갔으면 하는 소재를 입력하세요.")

# 스타일 옵션
style_options = {
    "몽환적인": "dreamy",
    "사실적인": "realistic",
    "만화스타일": "cartoon",
    "추상적인": "abstract",
    "임프레셔니즘": "impressionistic"
}

# 사용자에게 스타일을 한글로 선택하게 함
selected_style_korean = st.selectbox("그림의 스타일을 선택하세요.", list(style_options.keys()))

# 이미지 생성 버튼
generate_button = st.button('이미지 생성')

# 필수 입력 필드 검사
if generate_button:
    if not poem or not subject:
        st.warning("시와 소재를 모두 입력해주세요!")
    else:
        # 입력된 시, 소재, 스타일로 이미지 생성 프롬프트 생성
        image_prompt = f"시: '{poem}'\n소재: '{subject}'\n스타일: '{style_options[selected_style_korean]}'"
        
        try:
            # 이미지 생성 요청
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=3
            )
                                   
            # 각 이미지에 대한 처리
            image_url = image_response.data[0].url  # 응답 구조에 따라 적절히 추출
            st.image(image_url, caption='생성된 이미지')

            # 이미지 다운로드 준비
            response = requests.get(image_url)
            image_bytes = BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                            data=image_bytes,
                            file_name="downloaded_image.jpg",
                            mime="image/jpeg")
            
        except Exception as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {str(e)}")