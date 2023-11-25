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
    st.title("Create Your Character")
    st.header("Character Information")

    # User input
    name = st.text_input("Enter your name:")
    gender = st.radio("Gender:", ('Male', 'Female'))
    age = st.slider("Age:", 5, 100)
    hair_color = st.text_input("What is your hair color?")
    eye_color = st.text_input("What is your eye color?")
    favorite_activity = st.text_input("What is your favorite activity?")
    mbti_type = st.selectbox("Select your MBTI type:", 
                             ('INTJ', 'INTP', 'ENTJ', 'ENTP', 
                              'INFJ', 'INFP', 'ENFJ', 'ENFP', 
                              'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 
                              'ISTP', 'ISFP', 'ESTP', 'ESFP'))

    # MBTI traits mapping
    mbti_traits = {
        'INTJ': ['strategic', 'innovative', 'independent'],
        'INTP': ['analytical', 'curious', 'objective'],
        'ENTJ': ['assertive', 'efficient', 'outspoken'],
        'ENTP': ['inventive', 'insightful', 'original'],
        'INFJ': ['insightful', 'compassionate', 'idealistic'],
        'INFP': ['empathetic', 'creative', 'altruistic'],
        'ENFJ': ['charismatic', 'inspiring', 'empathetic'],
        'ENFP': ['enthusiastic', 'creative', 'sociable'],
        'ISTJ': ['organized', 'reliable', 'practical'],
        'ISFJ': ['nurturing', 'detail-oriented', 'loyal'],
        'ESTJ': ['decisive', 'responsible', 'logical'],
        'ESFJ': ['caring', 'social', 'supportive'],
        'ISTP': ['practical', 'observant', 'spontaneous'],
        'ISFP': ['artistic', 'adventurous', 'easygoing'],
        'ESTP': ['energetic', 'bold', 'realistic'],
        'ESFP': ['spontaneous', 'entertaining', 'friendly']
    }

    animal = st.text_input("Do you resemble an animal? (Optional)")

    st.caption("※ The 'Do you resemble an animal?' field is optional. You can still create a character image without it.")

    generate_button = st.button("Generate Character")

    if generate_button:
        # Check if all required fields are filled
        if not all([name, gender, hair_color, eye_color, favorite_activity, mbti_type]):
            st.warning("Please fill in all fields!")
        else:
            mbti_adjectives = ", ".join(mbti_traits[mbti_type])
            # Generate prompt based on animal input
            if animal:
                color_prompt = f"An animal that resembles a {animal} with {mbti_adjectives} MBTI personality traits, doing the activity: {favorite_activity}. The character's name '{name}' is shown at the bottom."
            else:
                color_prompt = f"A character that is a {gender.lower()} person, age {age}, with {hair_color} hair and {eye_color} eyes. They are doing their favorite activity: {favorite_activity}. The character reflects the {mbti_adjectives} personality traits of the MBTI type '{mbti_type}'. The character's name '{name}' is shown at the bottom."

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
                st.image(color_image_url, caption=f"{name}'s Character")

                # Image download button
                response = requests.get(color_image_url)
                image_bytes = BytesIO(response.content)
                st.download_button(label="Download Image",
                                   data=image_bytes,
                                   file_name=f"{name}_character.jpg",
                                   mime="image/jpeg")
            except AttributeError as e:
                st.error("An error occurred while accessing the response: " + str(e))
else:
    st.warning("Please enter the correct password.")
