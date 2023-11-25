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
    st.title("나만의 캐릭터 만들기")
    st.header("캐릭터 정보 입력")

    # 사용자 입력
    name = st.text_input("이름을 입력하세요:")
    gender = st.radio("성별:", ('남자', '여자'))
    age = st.slider("나이:", 5, 100)

    # 머리 색상 및 눈 색상 선택
    hair_colors = ['검정색', '갈색', '금발', '빨간색', '회색', '흰색', '기타']
    eye_colors = ['검정색', '갈색', '파란색', '초록색', '회색', '호박색', '기타']
    hair_color = st.selectbox("머리 색상을 선택하세요:", hair_colors)
    eye_color = st.selectbox("눈 색상을 선택하세요:", eye_colors)

    favorite_activity = st.text_input("가장 좋아하는 활동은 무엇인가요?")
    
    # MBTI 차원 선택
    extroversion = st.radio("주의초점 - 에너지의 방향:", [('외향 (E)', 'E'), ('내향 (I)', 'I')])
    sensing = st.radio("인식기능 - 사람이나 사물을 인식하는 방식:", [('감각 (S)', 'S'), ('직관 (N)', 'N')])
    thinking = st.radio("판단기능 - 판단의 근거:", [('감정 (F)', 'F'), ('사고 (T)', 'T')])
    lifestyle = st.radio("생활양식 - 선호하는 삶의 패턴:", [('판단 (J)', 'J'), ('인식 (P)', 'P')])

    # MBTI 유형 계산
    mbti_type = extroversion[1] + sensing[1] + thinking[1] + lifestyle[1]

    if all([extroversion, sensing, thinking, lifestyle]):
        st.write(f"당신은 {mbti_type}입니다.")

    animal = st.text_input("나를 닮은 동물이 있다면 무엇인가요? (선택사항)")

    st.caption("※ '나를 닮은 동물' 항목은 선택사항입니다. 비워두어도 캐릭터 이미지를 생성할 수 있습니다.")

    generate_button = st.button("캐릭터 생성하기")

    if generate_button:
        # 필수 필드가 채워졌는지 확인
        if not all([name, gender, hair_color, eye_color, favorite_activity]):
            st.warning("필수 항목을 모두 채워주세요!")
        else:
            color_prompt = f"{name}, {gender} 아이, 나이 {age}, 머리 색상 {hair_color}, 눈 색상 {eye_color}. {mbti_type} 유형의 성격으로 {favorite_activity}을(를) 하는 모습."

            try:
                # 컬러 이미지 생성
                color_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=color_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                color_image_url = color_image_response.data[0].url
                st.image(color_image_url, caption=f"{name}의 캐릭터")

                # 이미지 다운로드 버튼
                response = requests.get(color_image_url)
                image_bytes = BytesIO(response.content)
                st.download_button(label="이미지 다운로드",
                                   data=image_bytes,
                                   file_name=f"{name}_character.jpg",
                                   mime="image/jpeg")
            except AttributeError as e:
                st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력하세요.")
