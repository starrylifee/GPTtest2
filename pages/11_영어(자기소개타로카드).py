import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# Create an OpenAI object by providing the API key directly
client = OpenAI(api_key=st.secrets["api_key"])

# Set the page layout
st.set_page_config(layout="wide")

# Password input
password = st.text_input("Enter your password:", type="password")
correct_password = st.secrets["password"]

# Check if the entered password is correct
if password == correct_password:
    st.title("Create Your Tarot Card")
    st.header("Student Introduction")

    # User input
    name = st.text_input("Enter your name:")
    gender = st.radio("Gender:", ('Male', 'Female'))
    age = st.slider("Age:", 5, 30)
    likes_items = st.text_input("What items do you like? (Separate with commas, up to 3)")
    likes_people = st.text_input("Who are the people you like? (Separate with commas, up to 3)")
    aspiration = st.text_input("What is your aspiration?")
    want_to_do = st.text_input("What do you want to do right now?")
    favorite_food = st.text_input("What is your favorite food?")
    favorite_country = st.text_input("What is your favorite country?")

    generate_button = st.button("Generate Tarot Card")

    if generate_button:
        # Check if all fields are filled
        if not all([name, likes_items, likes_people, aspiration, want_to_do, favorite_food, favorite_country]):
            st.warning("Please fill in all fields!")
        else:
            # Generate the image creation prompt
            prompt = f"A tarot card design with a central illustration of a {gender.lower()} child, surrounded by items they like ({likes_items}), people they like ({likes_people}), their aspiration ({aspiration}), what they want to do right now ({want_to_do}), their favorite food ({favorite_food}), and their favorite country ({favorite_country}). The student's name '{name}' is prominently displayed at the bottom of the card."

            try:
                # Call the OpenAI API to generate the image
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1792",
                    quality="standard",
                    n=1
                )

                # Display the generated image
                generated_image_url = image_response.data[0].url
                st.image(generated_image_url, caption=f"{name}'s Personalized Tarot Card")

                # Prepare for image download
                response = requests.get(generated_image_url)
                image_bytes = BytesIO(response.content)

                # Image download button
                st.download_button(label="Download Image",
                                   data=image_bytes,
                                   file_name=f"{name}_tarot_card.jpg",
                                   mime="image/jpeg")
                
            except AttributeError as e:
                st.error("An error occurred while accessing the response: " + str(e))
else:
    st.warning("Please enter the correct password.")
