import streamlit as st
import openai
import requests
from io import BytesIO

# Streamlit 시크릿으로부터 OpenAI API 키를 로드합니다.
openai.api_key = st.secrets["openai_api_key"]

# 페이지 레이아웃을 설정합니다.
st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

# 입력된 비밀번호가 올바른지 확인합니다.
if password == correct_password:
    st.title("당신의 타로 카드 만들기")
    st.header("학생 자기소개")

    # 사용자 입력
    name = st.text_input("이름을 입력하세요:")
    gender = st.radio("성별:", ('남자', '여자'))
    age = st.slider("나이:", 5, 18)
    likes_items = st.text_input("좋아하는 물건은 무엇인가요? (쉼표로 구분하여 최대 3개까지)")
    likes_people = st.text_input("존경하는 사람은 누구인가요? (쉼표로 구분하여 최대 3개까지)")
    aspiration = st.text_input("장래희망은 무엇인가요?")
    want_to_do = st.text_input("지금 하고 싶은 것은 무엇인가요?")
    favorite_food = st.text_input("가장 좋아하는 음식은 무엇인가요?")
    favorite_country = st.text_input("가장 좋아하는 나라는 어디인가요?")

    generate_button = st.button("타로 카드 생성")

    if generate_button:
        # 모든 필드가 채워졌는지 확인
        if not all([name, likes_items, likes_people, aspiration, want_to_do, favorite_food, favorite_country]):
            st.warning("모든 필드를 채워주세요!")
        else:
            # 이미지 생성 프롬프트를 생성합니다.
            prompt = f"타로 카드 디자인으로 중앙에는 {gender}아이의 일러스트레이션이 있고, 주변에는 그 아이가 좋아하는 물건({likes_items}), 존경하는 사람({likes_people}), 장래희망({aspiration}), 지금 해보고 싶은 것({want_to_do}), 좋아하는 음식({favorite_food}), 좋아하는 나라({favorite_country}) 등이 둘러싸고 있습니다. 카드 하단에는 학생의 이름 '{name}'이 크게 표시됩니다."

            try:
                # OpenAI API를 호출하여 이미지를 생성합니다.
                image_response = openai.Image.create(prompt=prompt, n=1, size="1024x1792")

                # 생성된 이미지를 표시합니다.
                generated_image_url = image_response['data'][0]['url']
                st.image(generated_image_url, caption=f"{name}의 개인화된 타로 카드")

                # 이미지 다운로드를 위한 준비
                response = requests.get(generated_image_url)
                image_bytes = BytesIO(response.content)

                # 이미지 다운로드 버튼
                st.download_button(label="이미지 다운로드",
                                   data=image_bytes,
                                   file_name=f"{name}_tarot_card.jpg",
                                   mime="image/jpeg")
                
            except openai.error.OpenAIError as e:
                st.error(f"API 요청 중 오류가 발생했습니다: {str(e)}")
else:
    st.warning("올바른 비밀번호를 입력해주세요.")
