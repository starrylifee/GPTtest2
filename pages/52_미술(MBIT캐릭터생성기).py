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
    hair_color = st.selectbox("머리 색상을 선택하세요:", ['검정색', '갈색', '금발', '빨간색', '회색', '흰색', '기타'])
    eye_color = st.selectbox("눈 색상을 선택하세요:", ['검정색', '갈색', '파란색', '초록색', '회색', '호박색', '기타'])
    favorite_activity = st.text_input("가장 좋아하는 활동은 무엇인가요?")
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
            # 동물 관련 정보가 있는 경우 추가
            animal_info = f", 닮은 동물: {animal}" if animal else ""
            # 컬러 캐릭터 이미지 생성 프롬프트
            color_prompt = f"{gender} 아이, 나이 {age}, 머리 색상 {hair_color}, 눈 색상 {eye_color}. 좋아하는 활동 {favorite_activity}을 하는 모습{animal_info}. MBTI 유형 '{mbti_type}'의 성격 특성을 반영한 캐릭터. 캐릭터의 이름 '{name}'이 하단에 표시됩니다."

            # 컬러링 북 스타일 흑백 캐릭터 이미지 생성 프롬프트
            bw_prompt = color_prompt + " 이미지는 컬러링 북 스타일로, 굵은 검은색 윤곽선과 흰색 공간이 있는 형태로 제작됩니다."

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
                st.image(color_image_url, caption=f"{name}의 캐릭터 - 컬러")

                # 흑백 이미지 생성
                bw_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=bw_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                bw_image_url = bw_image_response.data[0].url
                st.image(bw_image_url, caption=f"{name}의 캐릭터 - 컬러링 북 스타일")

                # 이미지 다운로드 버튼
                for image_url, image_name in [(color_image_url, "color"), (bw_image_url, "black_white")]:
                    response = requests.get(image_url)
                    image_bytes = BytesIO(response.content)
                    st.download_button(label=f"{image_name.title()} 이미지 다운로드",
                                       data=image_bytes,
                                       file_name=f"{name}_character_{image_name}.jpg",
                                       mime="image/jpeg")
            except AttributeError as e:
                st.error("응답 접근 중 오류 발생: " + str(e))
else:
    st.warning("올바른 비밀번호를 입력하세요.")
