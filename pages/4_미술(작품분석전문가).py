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

@st.cache_data
def gptapi(persona, user):
     response = openai.ChatCompletion.create(
     model="gpt-3.5-turbo",
     messages=[
         {"role": "system", "content" : persona},
         {"role": "user", "content": user}
     ],
     max_tokens = 1000,
     temperature = 1
     )
     return response["choices"][0]["message"]["content"]

persona_prompt1 = '''
너는 사회선생님이야. 지금까지 우리 반은 도시화의 문제점(인구과밀, 환경오염, 사람이 적어지는 농촌)에 대해서 배웠어. 학생들은 도시화를 막는 방법에 대해서 고민했고, 학생들이 낸 해답을 너에게 제시할거야.
1단계: 학생이 생각한 내용을 간단히 요약하고, 구체적으로 칭찬해줘.
2단계: 학생이 제시한 해결책이 불러일으킬 수 있는 문제점을 1가지 짚고 문제 사례를 말해줘.
3단계: 다음의 항목으로 점수를 표현해줘. 총점 100점, 창의성 40점 만점, 현실성 30점, 논리성 30점
출력은 단계를 표현하지 않고 편지글처럼 선생님으로서의 대답만 글로 표현해줘.
'''

# persona_prompt2 = '''
#     너는 역사선생님이야. 학생들이 조사해온 자료를 요악한 내용을 보고, 문제를 만들어줘
#     '''

# #클릭해야 실행되도록 버튼 만들기
if st.button("나의 해결방안 논의하기"): 
#     #복잡한 단계는 나누어 진행하기
     step1 = gptapi(persona_prompt1, research)
     st.write(step1)

#     step2 = gptapi(persona_prompt2, step1)
#     st.write(step2)