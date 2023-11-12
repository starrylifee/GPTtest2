import streamlit as st
import openai
import requests
from io import BytesIO

# OpenAI API 키를 Streamlit secrets에서 가져옵니다.
openai.api_key = st.secrets["api_key"]

st.set_page_config(layout="wide")

# 제목 및 헤더
st.title("미술작품 분석하기")
st.header("문제상황")

# 설명
text = '''
아래 드롭다운 메뉴에서 미술 작품을 선택하고 주제, 조형요소, 원리에 대해서 분석해보세요.
'''
st.write(text)

# 이미지 URL과 캡션을 딕셔너리로 정의
images = {
    'Composition II with Red Blue and Yellow': 'https://img.hani.co.kr/imgdb/resize/2012/0310/133125919362_20120310.JPG',
    '세한도': 'https://img1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/aXte/image/TkVLv4CxMI4Z8o0qN6B9O3eZFTI.png',
    '절규': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/The_Scream.jpg/1607px-The_Scream.jpg',
    '피레네의 성': 'https://www.greencurator.co.kr/data/item/GC17-A502-RM40MOT/GC17A502RM40MOT.jpg'
}

# 드롭다운 메뉴를 생성하고 사용자의 선택을 가져옵니다.
selected_caption = st.selectbox("미술 작품을 선택하세요:", options=list(images.keys()))

# 선택된 캡션에 해당하는 이미지를 표시합니다.
st.image(images[selected_caption], caption=selected_caption)

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

            # 번역된 텍스트를 숨겨진 상태로 표시
            with st.expander("번역된 텍스트 보기"):
                st.text(translated_text)
            
            # 이미지 생성 요청
            image_response = openai.Image.create(
                prompt=translated_text,
                n=1,
                size="1024x1024"
            )
            
            # 생성된 이미지의 URL을 가져옵니다.
            generated_image_url = image_response['data'][0]['url']
            
            # 이미지를 화면에 표시합니다.
            st.image(generated_image_url, caption='여러분이 본 그림이 이 그림이 맞나요?')
            st.write("조형요소:", f"점, 선, 면: {elements1}, 질감: {elements2}, 공간: {elements3}")
            st.write("조형원리:", f"균형, 대비, 강조, 리듬, 조화: {principles1}")
            st.write("소재:", f"그림의 주제: {subject1}, 공간별 내용: {subject2}")

            # 이미지 데이터를 다운로드하기
            response = requests.get(generated_image_url)
            image_bytes = BytesIO(response.content)

            # 다운로드 버튼 추가
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="generated_image.jpg",
                               mime="image/jpeg")
            
        except openai.error.OpenAIError as e:
            st.error(f"API 요청 중 오류가 발생했습니다: {str(e)}")
