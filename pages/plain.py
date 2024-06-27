
from openai import OpenAI
import json
import streamlit as st
import os 

st.title(' A Plain Jane ')
 

     
    
     
 

################ PAGE STARTS HERE ############################## 

 
#team_voice = st.text_input("Team scout- sample report ")
client = OpenAI(api_key=st.secrets["open_ai"])

# Define the function to get the scouting report
@st.cache_data()
def get_scouting_report(_llm, model, player, temperature,seed):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
        messages=[
            {
                    "role": "system",
                    "content": """ 
Create an engaging, brief summary of a basketball player's performance using the following guidelines:

Overall Impact (1 sentence):
Summarize the player's role and primary contribution to the team.
Example: "Max Rice is a sharpshooting guard who spreads the floor and punishes defenses from beyond the arc."
Standout Statistic (1 sentence):
Highlight the player's most impressive or unique statistical achievement.
Example: "His 83.9% free throw accuracy puts him in the elite 87th percentile of shooters from the charity stripe."
Offensive Toolkit (1-2 sentences):
Describe the player's most effective offensive moves or situations.
Example: "Rice thrives in spot-up situations, boasting a 53.5% adjusted field goal percentage and 1.042 points per possession in these scenarios."
Areas for Improvement (1 sentence):
Briefly mention one or two aspects of the player's game that need work.
Example: "Improving his 37.2% overall field goal percentage could elevate his game to the next level."
Intriguing Fact (1 sentence):
Include an interesting statistic or fact that adds color to the player's profile.
Example: "Despite his guard status, Rice contributes a solid 3.7 rebounds per game, showcasing his all-around effort on the court."

Combine these elements into a cohesive paragraph of 5-6 sentences, ensuring the summary is informative, engaging, and captures the essence of the player's performance in a concise manner.   """
            },
            {
                "role": "user",
                "content": player_boxscore  
            },
            
        ],
    )

    return chat_completion.choices[0].message.content

#openai strategy is to tweak either temperature or top_p to get the desired output not both 
seed_value = st.radio("Seed Values", [111, 2652, 230, 4432],horizontal=True)
temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=1.0, value=0.7, step=0.1)


#if st.button("Generate Scouting Report from input"):
 #   scouting_report = get_scouting_report(client,  "gpt-4o", player_boxscore,temperature, seed_value)
  #  st.write(scouting_report)
    

# Sample data
import json
with open("players.json", "r") as f:
    data = json.load(f)
sample_data = list(data)

def generate_scouting_report(data):
    
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature,  seed_value)
    st.write(scouting_report)
    

if st.button("Scout A  Player", type='primary'):
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    else:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    player_boxscore = str(sample_data[st.session_state.current_index])
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature,  seed_value)
    st.write(scouting_report)
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    
    
