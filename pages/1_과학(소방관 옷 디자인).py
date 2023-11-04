import streamlit as st
import openai

openai.api_key = st.secrets

st.set_page_config(layout="wide")

st.title("소방관 옷 디자인하기")

st.divider()
