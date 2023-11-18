import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# OpenAI 클라이언트 객체 생성
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password"]

# 입력된 비밀번호가 올바른지 확인합니다.
if password == correct_password:

    st.title("소방관 옷 디자인하기")

    st.divider()

    st.header("도전과제")

    text = '''
    미래의 소방관은 어떤 방화복을 입을까요?
    화재를 진압하는 미래의 방화복을 디자인 해보고 주요 기능을 요약해서 적어봅시다.

    힌트 ! 연소의 3조건을 생각해 봅시다.
    1. 발화점 이상의 온도
    2. 탈 물질
    3. 산소

    아래의 3개 빈칸을 모두 적지 않으면 도움을 드릴 수 없습니다.
    '''
    st.write(text)

    function1 = st.text_input("방화복의 첫번째 주요 기능을 적고 엔터를 눌러주세요.")
    function2 = st.text_input("방화복의 두번째 주요 기능을 적고 엔터를 눌러주세요.")
    function3 = st.text_input("방화복의 세번째 주요 기능을 적고 엔터를 눌러주세요.")

    st.divider()

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

    persona_prompt1 = '''
    너는 과학생님이야. 지금까지 우리 반은 연소의 3가지 조건(탈물질, 발화점이상의 온도, 산소)에 대해서 배웠어.
    학생들은 연소의 3가지 조건을 반대로 이용해서 불을 끌수 있는 소방관의 방화복을 디자인하려고 해.
    학생들이 적어놓은 방화복의 기능을 확인하고 다음을 실행해줘.

    1단계: 학생이 생각한 내용을 간단히 요약하고, 구체적으로 칭찬해줘.

    2단계: 학생의 방화복에 불을 끌 수 있는 능력이 없으면 방화복에 불을 끄는 기능을 추가하라고 말해줘. 만일 연소의 3가지 조건중 1가지를 이용한 소화기능을 넣었다면, 다른 연소 조건으로도 기능을 추가하라고 해줘.
    
    3단계: 다음의 항목으로 학생이 디자인한 방화복의 점수를 표현해줘. 총점 100점, 창의성 30점, 기능성 40점, 현실성 30점이야.
    예를들어 무게가 너무 무겁거나, 불에 너무 잘타는 방화복은 기능성에서 10점 정도를 주도록 해. 기본적인 방화복의 성능은 '불에 안타야 하고', '활동성'이 있어야 하고, '불을 끄는 기능'이 있으면 좋아.
    
    모든 단계별 출력은 개조식으로 간단히 출력해줘.

    만일 학생이 집어넣은 방화복의 기능이 초등학생에게 어울리지 않는 입력(범죄에 악용되거나 너무 잔인하다면)이라면 "올바른 방화복의 기능을 넣어주세요"라고만 출력해줘.
    '''

    if function1 and function2 and function3:  # 입력이 모두 존재할 때만 실행
        multifunction = f"{function1}, {function2}, {function3}"

        if st.button("나의 방화복 어때요?"): 
            evaluation = gptapi(persona_prompt1, multifunction)
            st.write(evaluation)

        # 이미지 생성 버튼
        if st.button("이미지 생성"):
            # 이미지 생성 요청
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=f"Firefighter's futuristic suit based on: {multifunction}",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # 응답에서 이미지 URL 추출
            try:
                image_url = image_response.data[0].url
                st.image(image_url, caption="소방관의 미래 방화복")

                # 이미지 다운로드
                response = requests.get(image_url)
                image_bytes = BytesIO(response.content)
                st.download_button(
                    label="이미지 다운로드",
                    data=image_bytes,
                    file_name="firefighter_suit.jpg",
                    mime="image/jpeg"
                )
            except AttributeError as e:
                st.error("이미지 생성 중 오류가 발생했습니다: " + str(e))

else:
    st.warning("올바른 비밀번호를 입력해주세요.")
