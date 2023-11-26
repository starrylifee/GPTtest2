import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# Create an OpenAI object
client = OpenAI(api_key=st.secrets["api_key"])

# Set page layout
st.set_page_config(layout="wide")

# Enter the password
password = st.text_input("Enter your password:", type="password")
correct_password = st.secrets["password"]

if password == correct_password:
    st.title("Create Your Own Character")
    st.header("Character Information")

    # User inputs
    name = st.text_input("Enter your name:")
    gender = st.radio("Gender:", ('Male', 'Female'))
    age = st.slider("Age:", 5, 100)

    # Select hair color, eye color, and character style
    hair_colors = ['Black', 'Brown', 'Blonde', 'Red', 'Gray', 'White', 'Other']
    eye_colors = ['Black', 'Brown', 'Blue', 'Green', 'Gray', 'Hazel', 'Other']
    character_styles = ['Cartoon Style', 'Realistic Style', 'Watercolor Style', 'Sketch Style', 'Pixel Art Style']

    hair_color = st.selectbox("Select hair color:", hair_colors)
    eye_color = st.selectbox("Select eye color:", eye_colors)
    character_style = st.selectbox("Select character style:", character_styles)

    favorite_activity = st.text_input("What is your favorite activity?")
    animal = st.text_input("If you were an animal, what would you be?")

    generate_button = st.button("Generate Character")

    if generate_button:
        # Check if required fields are filled
        if not all([name, gender, hair_color, eye_color, favorite_activity, animal]):
            st.warning("Please fill in all required fields!")
        else:
            prompt = f"{name}, a {gender} at age {age}, with hair color {hair_color} and eye color {eye_color} in {character_style}, enjoying {favorite_activity}. And an image of an {animal} doing the same activity."

            try:
                # Generate a color image
                color_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                color_image_url = color_image_response.data[0].url
                st.image(color_image_url, caption="Character Image")

                # Download image button
                response = requests.get(color_image_url)
                image_bytes = BytesIO(response.content)
                st.download_button(label="Download Image",
                                   data=image_bytes,
                                   file_name=f"character.jpg",
                                   mime="image/jpeg")
            except AttributeError as e:
                st.error("Error accessing the response: " + str(e))
else:
    st.warning("Please enter the correct password.")
