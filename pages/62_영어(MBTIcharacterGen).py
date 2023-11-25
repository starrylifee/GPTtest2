import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# Create an OpenAI object
client = OpenAI(api_key=st.secrets["api_key"])

# Set page layout
st.set_page_config(layout="wide")

# Password input
password = st.text_input("Enter your password:", type="password")
correct_password = st.secrets["password"]

if password == correct_password:
    st.title("Create Your Own Character")
    st.header("Character Information")

    # User input
    name = st.text_input("Enter your name:")
    gender = st.radio("Gender:", ('Male', 'Female'))
    age = st.slider("Age:", 5, 100)

    # Hair color and eye color selection
    hair_colors = ['Black', 'Brown', 'Blonde', 'Red', 'Grey', 'White', 'Other']
    eye_colors = ['Black', 'Brown', 'Blue', 'Green', 'Grey', 'Hazel', 'Other']
    hair_color = st.selectbox("Select your hair color:", hair_colors)
    eye_color = st.selectbox("Select your eye color:", eye_colors)

    favorite_activity = st.text_input("What is your favorite activity?")
    mbti_type = st.selectbox("Select your MBTI type:", 
                             ('INTJ', 'INTP', 'ENTJ', 'ENTP', 
                              'INFJ', 'INFP', 'ENFJ', 'ENFP', 
                              'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 
                              'ISTP', 'ISFP', 'ESTP', 'ESFP'))
    animal = st.text_input("Do you resemble an animal? (Optional)")

    st.caption("※ The 'Do you resemble an animal?' field is optional. You can still create a character image without it.")

    generate_button = st.button("Generate Character")

    if generate_button:
        # Check if all required fields are filled
        if not all([name, gender, hair_color, eye_color, favorite_activity, mbti_type]):
            st.warning("Please fill in all required fields!")
        else:
            # Add animal information if provided
            animal_info = f", resembling an animal: {animal}" if animal else ""
            # Color character image prompt
            color_prompt = f"A character that resembles a {gender.lower()} person, age {age}, with {hair_color} hair and {eye_color} eyes. They are doing their favorite activity: {favorite_activity}{animal_info}. The character reflects the personality traits of the MBTI type '{mbti_type}'. The character's name '{name}' is shown at the bottom."

            # Coloring book style black and white character image prompt
            bw_prompt = color_prompt + " The image should be in the style of a coloring book, with bold black outlines and white spaces, without any shades of grey."

            try:
                # Generate color image
                color_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=color_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                color_image_url = color_image_response.data[0].url
                st.image(color_image_url, caption=f"{name}'s Character - Color")

                # Generate black and white image
                bw_image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=bw_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                bw_image_url = bw_image_response.data[0].url
                st.image(bw_image_url, caption=f"{name}'s Character - Coloring Book Style")

                # Image download button
                for image_url, image_name in [(color_image_url, "color"), (bw_image_url, "black_white")]:
                    response = requests.get(image_url)
                    image_bytes = BytesIO(response.content)
                    st.download_button(label=f"Download {image_name.title()} Image",
                                       data=image_bytes,
                                       file_name=f"{name}_character_{image_name}.jpg",
                                       mime="image/jpeg")
            except AttributeError as e:
                st.error("An error occurred while accessing the response: " + str(e))
else:
    st.warning("Please enter the correct password.")
