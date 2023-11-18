import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

st.title("문제해결방법 논의하기")
st.header("문제상황")

# 문제 상황 텍스트
text = '''
해찬이네 가족이 도시로 이사 온 첫날, 해찬이는 높은 빌딩 숲 사이로 차가운 바람이 부는 것을 느꼈어요. 마을에서는 볼 수 없었던 빛나는 네온사인과 큰 차들의 소음이 가득했지만, 밤하늘에 별은 거의 보이지 않았어요.

"엄마, 여기 별이 왜 이렇게 적어요?" 해찬이가 물었어요.

"도시에는 불빛이 많아서 별빛이 잘 보이지 않는단다." 엄마가 조용히 대답했어요.

해찬이는 도시의 학교에서 많은 것을 배웠어요. 하지만 학교 뒤뜰에는 놀이터 대신 주차장이 있었고, 커다란 나무 대신 전신주와 광고판이 서 있었어요. 도시의 공원도 마을의 숲처럼 푸르지 않았어요. 사람들은 바쁘게 걸어 다니며, 때로는 서로 부딪히기도 했어요.

"할아버지, 도시에서는 나무가 별로 없어요. 왜 그런 거예요?"

"도시가 커지면서 사람들이 살 집과 큰 건물을 짓기 위해 나무를 많이 베어내고, 공장과 차들이 많아져서 공기도 안 좋아졌단다."

해찬이는 도시의 삶이 편리하긴 하지만, 마을의 싱그러운 자연과 밤하늘의 별, 그리고 사람들과의 따뜻한 인사가 그리웠어요. 그는 도시에서도 마을의 따스함을 느낄 수 있는 방법을 찾아야겠다고 생각했어요.
''' 
st.write(text)

# 사용자로부터 입력 받기
research = st.text_input("도시화를 해결할 수 있는 해결방안을 적고 엔터를 눌러주세요.")
st.divider()

@st.experimental_memo
def gptapi(persona, user):
     response = client.chat.completions.create(
         model="gpt-3.5-turbo",
         messages=[
             {"role": "system", "content": persona},
             {"role": "user", "content": user}
         ],
         max_tokens=1000,
         temperature=1
     )
     return response["choices"][0]["message"]["content"]

persona_prompt1 = '''
너는 사회선생님이야. 지금까지 우리 반은 도시화의 문제점(인구과밀, 환경오염, 사람이 적어지는 농촌)에 대해서 배웠어. 학생들은 도시화를 막는 방법에 대해서 고민했고, 학생들이 낸 해답을 너에게 제시할거야.
1단계: 학생이 생각한 내용을 간단히 요약하고, 구체적으로 칭찬해줘.
2단계: 학생이 제시한 해결책이 불러일으킬 수 있는 문제점을 1가지 짚고 문제 사례를 말해줘.
3단계: 다음의 항목으로 점수를 표현해줘. 총점 100점, 창의성 40점 만점, 현실성 30점, 논리성 30점
출력은 단계를 표현하지 않고 편지글처럼 선생님으로서의 대답만 글로 표현해줘.
'''

# 사용자 입력에 대한 응답 생성
if st.button("나의 해결방안 논의하기"):
     step1 = gptapi(persona_prompt1, research)
     st.write(step1)
