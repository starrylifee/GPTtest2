import streamlit as st
import openai

openai.api_key = st.secrets

st.set_page_config(layout="wide")

st.title("문제해결방법 논의하기")

st.divider()

