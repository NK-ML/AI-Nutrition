import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel(model_name='gemini-1.5-pro') 
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")

st.set_page_config(page_title="AI Nutritionist")
st.header("AI Nutritionist")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)
Submit = st.button("Tell me about the total calories")

input_prompt = """
    You are an expert nutritionist. Analyze the food items from the image 
    and calculate the total calories. Also, provide the details of each food item with calorie intake in the following format:

    1. Item 1 - Number of calories
    2. Item 2 - Number of calories
    ----
    ----
    Finally, mention whether the food is healthy or not. 
    Provide the approximate percentage breakdown of carbohydrates, fats, fibers, sugar, and other important nutrients.
"""

if Submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("The Response is")
        st.write(response)
    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"An error occurred: {e}")