import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
import pandas as pd

# OpenAI 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 데이터프레임 생성 및 표시
image_options_df = pd.DataFrame(image_options_summary)
st.table(image_options_df)

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

if password == correct_password:

# 이미지 선택 옵션을 표로 정리
    image_options_summary = {
        "옵션 카테고리": [
            "일반적인 배경", 
            "한국 특정 장소 배경", 
            "스타일", 
            "색상 구성", 
            "시대/문화", 
            "분위기", 
            "구도", 
            "이미지 사이즈"
        ],
        "선택 가능한 옵션": [
            "산, 바다, 해변, 강, 계곡, 하늘, 들판, 도시, 시골, 숲, 사막, 눈 덮인 산, 호수, 강변, 정원, 공원, 야생, 동굴, 폭포",
            "한강, 제주도, 경복궁, 남산타워, 부산 해운대, 설악산, 한옥 마을, 전주 한옥 마을, 동대문 디자인 플라자, 인사동, 북한산, 춘천, 양양 서핑 비치, 대구, 광주, 울산, 천안, 안동 하회마을",
            "사실적인 묘사, 인상주의, 고전주의, 전통 한국화, 모더니즘, 초현실주의, 팝 아트, 수채화, 디지털 아트, 픽셀 아트, 세피아 톤",
            "파스텔, 밝은 톤, 어두운 톤, 흑백, 모노크롬, 고채도, 저채도, 온색, 냉색, 자연색, 가을 색상, 봄 색상, 여름 색상, 겨울 색상, 전통 한국색상, 현대적 색상, 미래적 색상, 빈티지 색상, 고급스러운 색상, 생동감 있는 색상",
            "삼국시대, 고려시대, 조선시대, 대한제국, 일제 강점기, 한국 전쟁, 1960년대 한국, 1980년대 한국, 2000년대 한국, 현대 한국, 미래 한국, 조선시대 궁중, 고려시대 불교 사찰, 삼국시대 고분, 전통 한옥, 현대 서울, 전통 시장, 한국의 농촌, 한국의 도시화, 한국의 기술 발전",
            "평화로운, 몽환적인, 다이내믹한, 우울한, 행복한, 긴장된, 로맨틱한, 신비로운, 재미있는, 고요한, 전통적인, 현대적인, 미래적인, 역사적인, 민속적인, 도시적인, 자연적인, 산업적인, 활기찬, 고즈넉한",
            "Top View, Eye Level, Low Angle, High Angle, Bird's Eye View, Worm's Eye View, Close-up, Wide Shot, Panoramic View, Symmetrical",
            "1:1 (1024x1024), 9:16 (576x1024), 16:9 (1024x576)"
        ]
    }

    st.title("이미지를 만들어 보세요.")
    st.header("이미지 옵션")

    # 사용자 입력
    theme = st.text_input("이미지 주제 입력:")
    additional_text = st.text_input("추가적인 설명 입력 (선택사항):")

    # 옵션 선택
    background_option1 = ["없음", "산", "바다", "해변", "강", "계곡", "하늘", "들판", "도시", "시골", "숲", "사막", "눈 덮인 산", "호수", "강변", "정원", "공원", "야생", "동굴", "폭포"]
    background_option2 = ["없음", "한강", "제주도", "경복궁", "남산타워", "부산 해운대", "설악산", "한옥 마을", "전주 한옥 마을", "동대문 디자인 플라자", "인사동", "북한산", "춘천", "양양 서핑 비치", "대구", "광주", "울산", "천안", "안동 하회마을"]
    style_options = ["없음", "사실적인 묘사", "인상주의", "고전주의", "전통 한국화", "모더니즘", "초현실주의", "팝 아트", "수채화", "디지털 아트", "픽셀 아트", "세피아 톤"]
    color_scheme_options = ["없음", "파스텔", "밝은 톤", "어두운 톤", "흑백", "모노크롬", "고채도", "저채도", "온색", "냉색", "자연색", "가을 색상", "봄 색상", "여름 색상", "겨울 색상", "전통 한국색상", "현대적 색상", "미래적 색상", "빈티지 색상", "고급스러운 색상", "생동감 있는 색상"]
    era_culture_options = ["없음", "삼국시대", "고려시대", "조선시대", "대한제국", "일제 강점기", "한국 전쟁", "1960년대 한국", "1980년대 한국", "2000년대 한국", "현대 한국", "미래 한국", "조선시대 궁중", "고려시대 불교 사찰", "삼국시대 고분", "전통 한옥", "현대 서울", "전통 시장", "한국의 농촌", "한국의 도시화", "한국의 기술 발전"]
    mood_options = ["없음", "평화로운", "몽환적인", "다이내믹한", "우울한", "행복한", "긴장된", "로맨틱한", "신비로운", "재미있는", "고요한", "전통적인", "현대적인", "미래적인", "역사적인", "민속적인", "도시적인", "자연적인", "산업적인", "활기찬", "고즈넉한"]
    composition_options = ["없음", "Top View", "Eye Level", "Low Angle", "High Angle", "Bird's Eye View", "Worm's Eye View", "Close-up", "Wide Shot", "Panoramic View", "Symmetrical"]
    size_options = ["1:1 (1024x1024)", "9:16 (576x1024)", "16:9 (1024x576)"]

    # 셀렉트박스
    background1 = st.selectbox("일반적인 배경 선택:", background_option1)
    background2 = st.selectbox("한국 특정 장소 배경 선택:", background_option2)
    style = st.selectbox("스타일 선택:", style_options)
    color_scheme = st.selectbox("색상 구성 선택:", color_scheme_options)
    era_culture = st.selectbox("시대/문화 선택:", era_culture_options)
    mood = st.selectbox("분위기 선택:", mood_options)
    composition = st.selectbox("구도 선택:", composition_options)
    size = st.selectbox("이미지 사이즈 선택:", size_options)

    generate_button = st.button("이미지 생성")

    if generate_button:
        # 프롬프트 생성
        prompt_parts = [theme]
        if additional_text:
            prompt_parts.append(additional_text)
        if background1 != "없음":
            prompt_parts.append(f"{background1} 배경")
        if background2 != "없음":
            prompt_parts.append(f"{background2} 배경")
        if style != "없음":
            prompt_parts.append(f"{style} 스타일")
        if color_scheme != "없음":
            prompt_parts.append(f"{color_scheme} 색상")
        if era_culture != "없음":
            prompt_parts.append(f"{era_culture} 시대/문화")
        if mood != "없음":
            prompt_parts.append(f"{mood} 분위기")
        if composition != "없음":
            prompt_parts.append(f"{composition} 구도")

        # 최종 프롬프트 생성 및 출력
        final_prompt = ', '.join(prompt_parts)
        st.write("생성될 이미지의 프롬프트:", final_prompt)

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
                prompt=final_prompt,
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