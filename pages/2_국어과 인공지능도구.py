import streamlit as st
import openai

#openai api key
openai.api_key = st.secrets["api_key"]

#페이지 레이아웃 설정
st.set_page_config(layout="wide")

#페이지의 메인 이름
st.title("국어 6학년 인공지능 토론도우미")

# #가로 줄
st.divider()

# #헤더 
st.header("토론주제")

# #텍스트 출력하기
text = '''
지난 주말, 유나는 가족과 함께 동물원을 방문했습니다. 그녀는 다양한 동물들을 가까이에서 볼 수 있어서 매우 흥분되었지만, 동시에 몇몇 동물들이 좁은 우리 안에서 불안해 보이는 것을 보고 마음이 무거워졌습니다. 특히, 큰 호랑이가 작은 우리 안을 불안하게 왔다 갔다 하는 모습이 인상 깊었습니다. 유나는 호랑이가 자연에서는 넓은 영역을 돌아다니며 살아가는 동물이라는 것을 알고 있었기 때문에, 이러한 모습이 동물에게 과연 옳은 것인지 의문을 가졌습니다.

학교에 돌아온 유나는 선생님과 친구들에게 동물원 방문 경험을 나누며, 동물원과 수족관이 동물의 권리를 침해한다고 느꼈다고 말했습니다. 그녀는 동물들이 자연 상태에서와 같은 환경에서 살아갈 권리가 있다고 생각했습니다. 그러나 유나의 친구 중 일부는 동물원과 수족관이 오히려 동물들을 보호하고, 사람들에게 교육적인 경험을 제공한다고 반박했습니다.
 '''
st.write(text)
# # st.write("~~~") 의 형태로도 출력 가능

# #링크 넣기
# st.markdown("[위키피디아 링크](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%A2%85)")

# #학생들이 텍스트 입력하는 곳 만들기
# #조사한 자료를 research에 저장
option = st.selectbox(
    '당신의 주장은 무엇인가요?',
    ('동물원과 수족관을 없애야 한다.', '동물원과 수족관은 필요한 시설이다.'))

st.write('You selected:', option)
st.write = "왜냐하면"
research = st.text_input("주장에 대한 근거를 적고 엔터를 누르세요.")

# st.write(research)

st.divider()

# #ChatGPT API 활용하기 response를 불러오는 함수 만들기
@st.cache_data #반복 수행을 막아줌
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

# #prompt 설정하기
persona_prompt1 = '''
너는 초등학교 6학년 국어선생님이야. 아이들은 동물원과 수족관은 동물의 권리를 침해하기 때문에 폐쇄되어야 한다. 라는 문장을 토론 주제로 찬성과 반대 의견을 제시하고 있어.
학생이 올린 찬성 및 반대의 주장과 근거를 듣고 다음을 말해줘.
첫번째 문단은 학생이 적은 주장과 의견을 한번더 말해줘
두번째 문단은 학생이 적은 의견에 대한 예상되는 반론을 말해줘
세번째 문단은 학생이 적은 주장과 근거를 평가해줘. 총점은 100점으로 근거의 주제 관련성 30점, 근거의 창의성 30점, 주장과 근거의 명료성 40점이야.
'''

# persona_prompt2 = '''
#     너는 역사선생님이야. 학생들이 조사해온 자료를 요악한 내용을 보고, 문제를 만들어줘
#     '''

# #클릭해야 실행되도록 버튼 만들기
if st.button("나의 주장과 근거는 몇점일까?"): 
#     #복잡한 단계는 나누어 진행하기
     step1 = gptapi(persona_prompt1, research)
     st.write(step1)

#     step2 = gptapi(persona_prompt2, step1)
#     st.write(step2)