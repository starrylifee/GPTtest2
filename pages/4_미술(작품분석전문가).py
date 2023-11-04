import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

st.title("미술작품 분석하기")

st.header("문제상황")

text = '''
아래의 미술 작품을 보고 주제, 조형요소, 원리에 대해서 분석해보세요.
'''
st.write(text)

elements1 = st.text_input("점, 선, 면에 대해서 적어보세요.")
elements2 = st.text_input("그림의 질감에 대해서 적어보세요")
elements3 = st.text_input("그림의 공간에 대해서 적어보세요")

st.divider()

principles1 = st.text_input("그림의 균형, 대비, 강조, 리듬, 조화에 대해서 적어보세요.")

st.divider()

subject1 = st.text_input("그림에 그려진 것들에 대해서 적어보세요.")
subject2 = st.text_input("그림각 공간에 드려진 것들에 대해서 적어보세요.")

generate_button = st.button('그림을 만들어봐요.')

if generate_button and elements1 and elements2 and elements3 and principles1 and subject1 and subject2:
    # 한국어 프롬프트를 영어로 번역합니다.
    translation_prompt = f"{elements1}, {elements2}, {elements3}, {principles1}, {subject1}, {subject2} - 이 설명을 영어로 번역해주세요."
    @st.cache_data
    translation_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=translation_prompt,
        max_tokens=60,
        temperature=0.5
    )
    
    # 번역된 영어 텍스트를 가져옵니다.
    translated_text = translation_response.choices[0].text.strip()
    
    # 번역된 텍스트를 사용하여 이미지를 생성합니다.
    image_response = openai.Image.create(
        prompt=translated_text,
        n=1,
        size="1024x1024"
    )
    
    # 생성된 이미지의 URL을 가져옵니다.
    image_url = image_response['data'][0]['url']
    
    # 이미지를 화면에 표시합니다.
    st.image(image_url, caption='여러분이 본 그림이 이 그림이 맞나요?')