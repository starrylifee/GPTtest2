import streamlit as st
import openai

# OpenAI API 키를 Streamlit secrets에서 가져옵니다.
openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

# 제목 및 헤더
st.title("시에 맞는 이미지 만들기")
st.header("시를 입력하고 시에 어울리는 그림을 생성해보세요")

# 사용자 입력
poem = st.text_area("시를 여기에 입력하세요.")
subject = st.text_input("그림에 꼭 들어갔으면 하는 소재를 입력하세요.")
style = st.selectbox("그림의 스타일을 선택하세요.", ["몽환적인", "사실적인", "만화스타일", "추상적인", "임프레셔니즘"])

# 이미지 생성 버튼
generate_button = st.button('이미지 생성')

# 필수 입력 필드 검사
if generate_button:
    if not poem or not subject:
        st.warning("시와 소재를 모두 입력해주세요!")
    else:
        # 입력된 시, 소재, 스타일을 영어로 번역하는 로직
        try:
            translation_prompt = f"다음 시를 영어로 번역해주세요: {poem}\n\n그림에 꼭 들어갈 소재: {subject}\n\n선택한 그림 스타일: {style}"
            translation_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=translation_prompt,
                max_tokens=1024,
                temperature=0.3
            )
            
            # 번역된 영어 텍스트를 가져옵니다.
            translated_text = translation_response.choices[0].text.strip()
            
            # 이미지 생성 요청
            image_response = openai.Image.create(
                prompt=translated_text,
                n=1,
                size="1024x1024"
            )
            
            # 생성된 이미지의 URL을 가져옵니다.
            image_url = image_response['data'][0]['url']
            
            # 이미지를 화면에 표시합니다.
            st.image(image_url, caption='시, 소재, 스타일에 기반한 이미지')
            
        except openai.error.OpenAIError as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {str(e)}")