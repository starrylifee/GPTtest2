import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

# MBTI 유형별 형용사 매핑
mbti_traits = {
    'INTJ': ['전략적', '창의적', '독립적'],
    'INTP': ['분석적', '호기심이 많은', '객관적인'],
    'ENTJ': ['당당한', '효율적', '솔직한'],
    'ENTP': ['발명적', '통찰력 있는', '독창적'],
    'INFJ': ['통찰력 있는', '자비로운', '이상적인'],
    'INFP': ['공감 능력이 뛰어난', '창의적', '이타적인'],
    'ENFJ': ['카리스마 있는', '영감을 주는', '공감 능력이 뛰어난'],
    'ENFP': ['열정적', '창의적', '사교적'],
    'ISTJ': ['조직적', '신뢰할 수 있는', '실용적'],
    'ISFJ': ['보살피는', '세심한', '충성스러운'],
    'ESTJ': ['결단력 있는', '책임감 있는', '논리적'],
    'ESFJ': ['돌보는', '사회적', '지지적인'],
    'ISTP': ['실용적', '관찰력 있는', '즉흥적'],
    'ISFP': ['예술적', '모험적', '쉽게 대하는'],
    'ESTP': ['활동적', '대담한', '현실적'],
    'ESFP': ['즉흥적', '재미있는', '친근한']
}

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
    age = st.slider("나이:", 5, 70)

    # 머리 색상 및 눈 색상 선택
    hair_colors = ['검정색', '갈색', '금발', '빨간색', '회색', '흰색', '기타']
    eye_colors = ['검정색', '갈색', '파란색', '초록색', '회색', '호박색', '기타']
    hair_color = st.selectbox("머리 색상을 선택하세요:", hair_colors)
    eye_color = st.selectbox("눈 색상을 선택하세요:", eye_colors)

    favorite_activity = st.text_input("가장 좋아하는 활동은 무엇인가요?")
    
    # MBTI 유형 선택
    mbti_type = st.selectbox("MBTI 유형을 선택하세요:", 
                             ('INTJ', 'INTP', 'ENTJ', 'ENTP', 
                              'INFJ', 'INFP', 'ENFJ', 'ENFP', 
                              'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 
                              'ISTP', 'ISFP', 'ESTP', 'ESFP'))

    animal = st.text_input("나를 닮은 동물이 있다면 무엇인가요? (선택사항)")

    st.caption("※ '나를 닮은 동물' 항목은 선택사항입니다. 비워두어도 캐릭터 이미지를 생성할 수 있습니다.")

    generate_button = st.button("캐릭터 생성하기")

    if generate_button:
        # 필수 필드가 채워졌는지 확인
        if not all([name, gender, hair_color, eye_color, favorite_activity, mbti_type]):
            st.warning("필수 항목을 모두 채워주세요!")
        else:
            # 동물이 있는 경우 동물 캐릭터 프롬프트 생성
            if animal:
                color_prompt = f"{animal}이(가) {mbti_type} 성격으로 {favorite_activity}을(를) 하는 모습. 캐릭터의 이름 '{name}'이 하단에 표시됩니다."
            else:
                color_prompt = f"{gender} 아이, 나이 {age}, 머리 색상 {hair_color}, 눈 색상 {eye_color}. {mbti_type} 유형의 성격으로 {favorite_activity}을(를) 하는 모습. 캐릭터의 이름 '{name}'이 하단에 표시됩니다."

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
