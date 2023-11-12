import streamlit as st
from openai import OpenAI

OpenAI.api_key = st.secrets["api_key"]

client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url