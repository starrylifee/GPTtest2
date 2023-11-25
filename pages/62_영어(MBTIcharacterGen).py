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

    # Select hair color and eye color
    hair_colors = ['Black', 'Brown', 'Blonde', 'Red', 'Gray', 'White', 'Other']
    eye_colors = ['Black', 'Brown', 'Blue', 'Green', 'Gray', 'Hazel', 'Other']
    hair_color = st.selectbox("Select hair color:", hair_colors)
    eye_color = st.selectbox("Select eye color:", eye_colors)

    favorite_activity = st.text_input("What is your favorite activity?")
    
    # Choose MBTI dimensions
    extroversion = st.radio("Focus of Attention - Direction of Energy:", [('Extraversion (E)', 'E'), ('Introversion (I)', 'I')])
    sensing = st.radio("Perceiving Function - How You Take in Information:", [('Sensing (S)', 'S'), ('Intuition (N)', 'N')])
    thinking = st.radio("Judging Function - Basis of Decision Making:", [('Feeling (F)', 'F'), ('Thinking (T)', 'T')])
    lifestyle = st.radio("Lifestyle Preference - How You Deal with the Outer World:", [('Judging (J)', 'J'), ('Perceiving (P)', 'P')])

    # Calculate MBTI type
    mbti_type = extroversion[1] + sensing[1] + thinking[1] + lifestyle[1]

    if all([extroversion, sensing, thinking, lifestyle]):
        st.write(f"Your MBTI type is {mbti_type}.")

    animal = st.text_input("If you were an animal, what would you be? (Optional)")

    st.caption("※ The 'If you were an animal' field is optional. You can leave it empty to generate a character image.")

    generate_button = st.button("Generate Character")

    if generate_button:
        # Check if required fields are filled
        if not all([name, gender, hair_color, eye_color, favorite_activity]):
            st.warning("Please fill in all required fields!")
        else:
            color_prompt = f"{name}, {gender} at age {age}, with hair color {hair_color} and eye color {eye_color}. With an MBTI type of {mbti_type}, enjoying {favorite_activity}."

            try:
                # Generate a color image
                color_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=color_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                color_image_url = color_image_response.data[0].url
                st.image(color_image_url, caption=f"{name}'s character")

                # Download image button
                response = requests.get(color_image_url)
                image_bytes = BytesIO(response.content)
                st.download_button(label="Download Image",
                                   data=image_bytes,
                                   file_name=f"{name}_character.jpg",
                                   mime="image/jpeg")
            except AttributeError as e:
                st.error("Error accessing the response: " + str(e))
else:
    st.warning("Please enter the correct password.")
