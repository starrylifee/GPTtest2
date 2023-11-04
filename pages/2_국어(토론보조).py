import streamlit as st
import openai

openai.api_key = st.secrets

st.set_page_config(layout="wide")

st.title("주장과 근거 점검하기")

st.divider()

