import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

# 입력된 비밀번호가 올바른지 확인합니다.
if password == correct_password:

    st.title("토론 수업용 인공지능 도우미")

    st.divider()

    st.header("도전과제")

    text = '''
    학생 여러분, 오늘의 토론 주제는 무엇일까요? 여러분이 선택한 주제에 대한 주장을 준비했나요?
    주장과 함께 그 주장을 뒷받침하는 근거를 제시해 보세요. 인공지능이 여러분의 근거를 평가하고, 예상되는 반론을 제시해 드릴 거예요.

    아래의 3개 빈칸에 주장과 근거를 적어 주세요. 모든 칸을 채우지 않으면 도움을 드릴 수 없습니다.
    '''
    st.write(text)

    argument = st.text_input("여러분의 주장을 적어주세요.")
    evidence1 = st.text_input("첫 번째 근거를 적어주세요.")
    evidence2 = st.text_input("두 번째 근거를 적어주세요.")
    evidence3 = st.text_input("세 번째 근거를 적어주세요.")

    st.divider()

    # gptapi 함수 정의
    @st.experimental_memo
    def gptapi(prompt, user_input):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000,
            temperature=1
        )
        return response.choices[0].message.content

    persona_prompt = '''
    인공지능 교사로서, 토론 수업에 참여하는 학생들의 주장과 근거를 평가해야 합니다. 
    학생들이 제시한 주장과 근거를 바탕으로 다음 작업을 수행해주세요.

    1단계: 학생이 제시한 주장과 근거를 간략히 요약해주세요.

    2단계: 제시된 근거의 타당성을 평가하고, 주장을 강화할 수 있는 추가적인 근거나 정보를 제안해주세요.

    3단계: 예상되는 반론을 제시하여, 학생이 토론 준비를 보다 효과적으로 할 수 있도록 도와주세요.
    
    모든 단계별 출력은 개조식으로 간단히 출력해주세요.

    만약 학생이 제시한 주장이나 근거가 부적절하거나 수업 주제와 맞지 않는 경우, "주제에 맞는 적절한 주장과 근거를 제시해주세요"라고 안내해주세요.
    '''

    if argument and evidence1 and evidence2 and evidence3:  # 입력이 모두 존재할 때만 실행
        argument_evidence = f"{argument}, {evidence1}, {evidence2}, {evidence3}"
        st.write(argument_evidence)

        st.divider()

        if st.button("주장과 근거 평가받기"): 
            evaluation = gptapi(persona_prompt, argument_evidence)
            st.write(evaluation)

else:
    st.warning("올바른 비밀번호를 입력해주세요.")
