import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["api_key"])

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

# 비밀번호 확인
if password == correct_password:
    st.title("당신의 타로 카드 만들기")
    st.header("학생 자기소개")

    # 사용자 입력
    name = st.text_input("이름을 입력하세요:")
    gender = st.radio("성별:", ('남자', '여자'))
    age = st.slider("나이:", 5, 30)
    likes_items = st.text_input("좋아하는 물건을 입력하세요 (쉼표로 구분, 최대 3개):")
    likes_people = st.text_input("좋아하는 사람을 입력하세요 (쉼표로 구분, 최대 3개):")
    aspiration = st.text_input("장래 희망을 입력하세요:")
    want_to_do = st.text_input("지금 하고 싶은 것을 입력하세요:")
    favorite_food = st.text_input("가장 좋아하는 음식을 입력하세요:")
    favorite_country = st.text_input("가장 좋아하는 나라를 입력하세요:")

    generate_button = st.button("타로 카드 생성")

    if generate_button:
        # 모든 필드가 채워졌는지 확인
        if not all([name, likes_items, likes_people, aspiration, want_to_do, favorite_food, favorite_country]):
            st.warning("모든 필드를 채워주세요!")
        else:
            # 입력된 데이터를 영어로 번역하기 위한 ChatGPT API 호출
            translation_prompt = f"영어로 번역해주세요: '{name}은 {gender}입니다. 그들이 좋아하는 물건: {likes_items}, 좋아하는 사람: {likes_people}, 장래 희망: {aspiration}, 지금 하고 싶은 것: {want_to_do}, 좋아하는 음식: {favorite_food}, 좋아하는 나라: {favorite_country}'"
            try:
                translation_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": translation_prompt}
                    ]
                )
                translated_text = translation_response.choices[0].message.content

                # OpenAI API를 호출하여 이미지 생성
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=translated_text,
                    size="1024x1792",
                    quality="standard",
                    n=1
                )

                # 생성된 이미지 표시
                generated_image_url = image_response.data[0].url
                st.image(generated_image_url, caption=f"{name}의 개인화된 타로 카드")

                # 이미지 다운로드 준비
                response = requests.get(generated_image_url)
                image_bytes = BytesIO(response.content)

                # 이미지 다운로드 버튼
                st.download_button(label="이미지 다운로드",
                                   data=image_bytes,
                                   file_name=f"{name}_tarot_card.jpg",
                                   mime="image/jpeg")
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
