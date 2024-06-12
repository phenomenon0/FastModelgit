
from openai import OpenAI
import json
import streamlit as st
import os
import base64
import PIL.Image

st.markdown('## A-IRIS: Vision Model ')
st.sidebar.markdown('Eye-ris ')


##############################################

client = OpenAI(api_key=st.secrets["open_ai"])
picture_upload = st.file_uploader("Upload a Picture", type=["jpg", "jpeg", "png"])
if picture_upload is not None:
    st.image(picture_upload, caption='Uploaded Image', use_column_width=True)
    picture = base64.b64encode(picture_upload.read()).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are basketball drawing meaningful insights from charts,explain in a few sentences the most important things on the chart/graph."},
            {"role": "user", "content": [
                {"type": "text", "text": "explain the key insight on this chart"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{picture}"}
                }
            ]}
        ],
        temperature=0.7,
    )
    st.write(response.choices[0].message.content)

    

    
 

