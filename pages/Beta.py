
from openai import OpenAI
import json
import streamlit as st
import os
st.markdown('## Beta')
st.sidebar.markdown('This is the Beta page, ')





################ PAGE STARTS HERE ############################## 

st.title("A-eye: freewill version -- beta No sample report")
#team_voice = st.text_input("Team scout- sample report ")
player_boxscore = st.text_input("Player box scores")
client = OpenAI(api_key=st.secrets["open_ai"])

# Define the function to get the scouting report
@st.cache_data()
def get_scouting_report(_llm, model, player, temperature, p,seed):
    chat_completion = _llm.chat.completions.create(
        model=model,
   
        messages=[
            {
                    "role": "system",
                    "content": """You are an expert basketball scout analyzing players using box scores and SYNERGY stats preparing your team to play against them. 
                    write on how they attack and defensive strategy . use markdown and emoji to emphasize key points. 
                    Use basketball lingo and terminology to sound like a real scout. Take a deep breath and work on this problem step-by-step.
                    """
            },
            {
                "role": "user",
                "content": player_boxscore + "analyze player coach."
            },
            
        ],
    )

    return chat_completion.choices[0].message.content
#openai strategy is to tweak either temperature or top_p to get the desired output not both 
seed_value = st.radio("Seed Values", [111, 22, 23, 4])
temperature = st.slider("Temperature", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=0.9, step=0.1)

if st.button("Generate Scouting Report"):
    scouting_report = get_scouting_report(client,  "gpt-3.5-turbo", player_boxscore,temperature, top_p, seed_value)
    st.write(scouting_report)
    
