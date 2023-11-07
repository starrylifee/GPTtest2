import streamlit as st
from openai import OpenAI
client = OpenAI()


# OpenAI API 키를 Streamlit secrets에서 가져옵니다.
openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

# 제목 및 헤더
st.title("미술작품 분석하기")
st.header("문제상황")

# 설명
text = '''
아래의 미술 작품을 보고 주제, 조형요소, 원리에 대해서 분석해보세요.
'''
st.write(text)

image_url = 'https://img.hani.co.kr/imgdb/resize/2012/0310/133125919362_20120310.JPG'

# Display the image using the st.image function
st.image(image_url, caption='Composition II with Red Blue and Yellow')

# 사용자 입력
elements1 = st.text_input("점, 선, 면에 대해서 적어보세요.")
elements2 = st.text_input("그림의 질감에 대해서 적어보세요")
elements3 = st.text_input("그림의 공간에 대해서 적어보세요")
principles1 = st.text_input("그림의 균형, 대비, 강조, 리듬, 조화에 대해서 적어보세요.")
subject1 = st.text_input("그림에 그려진 것들에 대해서 적어보세요.")
subject2 = st.text_input("그림의 각 공간에 그려진 것들에 대해서 적어보세요.")

# 이미지 생성 버튼
generate_button = st.button('그림을 만들어봐요.')

# 필수 입력 필드 검사
if generate_button:
    if not (elements1 and elements2 and elements3 and principles1 and subject1 and subject2):
        st.warning("모든 필드를 채워주세요!")
    else:
        # 입력이 모두 채워졌을 때의 처리 로직
        # 번역할 텍스트를 한국어에서 영어로 번역하는 로직
        try:
            translation_prompt = f"점, 선, 면: {elements1}, 질감: {elements2}, 공간: {elements3}, 균형/대비/강조/리듬/조화: {principles1}, 주제: {subject1}, 공간별 내용: {subject2} - 이 설명을 영어로 번역해주세요."
            translation_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=translation_prompt,
                max_tokens=1024,
                temperature=0.3
            )
            
            # 번역된 영어 텍스트를 가져옵니다.
            translated_text = translation_response.choices[0].text.strip()
            
            # 이미지 생성 요청
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=translated_text,
                n=1,
                size="1024x1024"
            )
            
            # 생성된 이미지의 URL을 가져옵니다.
            image_url = image_response['data'][0]['url']
            
            # 이미지를 화면에 표시합니다.
            st.image(image_url, caption='여러분이 본 그림이 이 그림이 맞나요?')
            # 사용자가 입력한 내용을 화면에 표시합니다.
            st.write("## 여러분이 입력한 분석 내용")
            st.write(f"점, 선, 면: {elements1}")
            st.write(f"질감: {elements2}")
            st.write(f"공간: {elements3}")
            st.write(f"균형/대비/강조/리듬/조화: {principles1}")
            st.write(f"주제: {subject1}")
            st.write(f"공간별 내용: {subject2}")
            
        except openai.error.OpenAIError as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {str(e)}")
