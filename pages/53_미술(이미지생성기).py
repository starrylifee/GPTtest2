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
    st.title("임의의 이미지 생성")
    st.header("이미지 옵션")

    # 사용자 입력
    theme = st.text_input("이미지 주제 입력:")
    additional_text = st.text_input("추가적인 설명 입력 (선택사항):")

    # 각각의 프롬프트 선택 옵션 (None 추가)
    background_options = ["없음", "해변", "산", "도시", "숲", "사막", "우주", "고대 유적", "미래 도시", "가상 세계", "마법의 성"]
    style_options = ["없음", "인상주의", "고전주의", "전통 동양", "모더니즘", "초현실주의", "팝 아트", "만화 스타일", "픽셀 아트", "수채화", "디지털 아트"]
    color_scheme_options = ["없음", "파스텔", "밝은 톤", "어두운 톤", "흑백", "모노크롬", "고채도", "저채도", "온색", "냉색", "자연색"]
    era_culture_options = ["없음", "빅토리아 시대", "고대 이집트", "중세 유럽", "에도 시대 일본", "미래 사회", "로마 제국", "아즈텍 문명", "르네상스", "현대 도시", "가상 세계"]
    mood_options = ["없음", "평화로운", "몽환적인", "다이내믹한", "우울한", "행복한", "긴장된", "로맨틱한", "신비로운", "재미있는", "고요한"]
    fantasy_scifi_options = ["없음", "드래곤", "외계인", "마법사", "사이버펑크", "로봇", "마법의 세계", "우주선", "시간 여행", "고대 신화", "미래 도시"]
    size_options = ["1:1 (1024x1024)", "9:16 (576x1024)", "16:9 (1024x576)"]

    # 셀렉트박스
    background = st.selectbox("배경 선택:", background_options)
    style = st.selectbox("스타일 선택:", style_options)
    color_scheme = st.selectbox("색상 구성 선택:", color_scheme_options)
    era_culture = st.selectbox("시대/문화 선택:", era_culture_options)
    mood = st.selectbox("분위기 선택:", mood_options)
    fantasy_scifi = st.selectbox("판타지/과학공상 요소 선택:", fantasy_scifi_options)
    size = st.selectbox("이미지 사이즈 선택:", size_options)

    generate_button = st.button("이미지 생성")

    if generate_button:
        # 프롬프트 생성
        prompt_parts = [theme]
        if additional_text:
            prompt_parts.append(additional_text)
        if background != "없음":
            prompt_parts.append(f"{background} 배경")
        if style != "없음":
            prompt_parts.append(f"{style} 스타일")
        if color_scheme != "없음":
            prompt_parts.append(f"{color_scheme} 색상")
        if era_culture != "없음":
            prompt_parts.append(f"{era_culture} 시대/문화")
        if mood != "없음":
            prompt_parts.append(f"{mood} 분위기")
        if fantasy_scifi != "없음":
            prompt_parts.append(f"{fantasy_scifi} 요소 포함")
        prompt = ', '.join(prompt_parts)

        # 사이즈 설정
        if size == "1:1 (1024x1024)":
            selected_size = "1024x1024"
        elif size == "9:16 (576x1024)":
            selected_size = "576x1024"
        else:
            selected_size = "1024x576"

        try:
            # 이미지 생성
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=selected_size,
                quality="standard",
                n=1
            )
            image_url = image_response.data[0].url
            st.image(image_url, caption="생성된 이미지")

            # 이미지 다운로드 버튼
            response = requests.get(image_url)
            image_bytes = BytesIO(response.content)
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="generated_image.jpg",
                               mime="image/jpeg")
        except AttributeError as e:
            st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력하세요.")
