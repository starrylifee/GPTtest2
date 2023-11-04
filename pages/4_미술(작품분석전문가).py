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
       prompt_text = elements1 + "하고" + elements2 + "하고" + elements3 + "하고" + principles1 + "하고" + subject1 + "하고" + subject2 + "한 그림을 그려줘"
    response = openai.Image.create(
        prompt=prompt_text,
        n=1,
        size="256x256"
    )
    
    image_url = response['data'][0]['url']
    
    st.image(image_url, caption='Generated Image')