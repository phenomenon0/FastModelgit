
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
                    "content": """Prompt:

Given a JSON file containing synergy stats and box score data for a basketball player, your task is to generate a narrative summary of the player's performance across various play types. The output should highlight key statistics and provide insights in a readable, narrative format without first listing all the stats. Here is an example of the desired output format:

Example Output:

Highly efficient on cuts with an impressive 63.6% shooting and zero turnovers. 🔥🎯

Hand-offs aren't his strong suit, with a low shooting percentage of 17.4% and modest points per possession. 🚫🏀

Kyle struggles in isolation plays, failing to score with a FG% of 0% and a high turnover rate. 😓🔄

Similarly, other plays labeled as miscellaneous show poor shooting and a high turnover rate. 📉⛔

Kyle capitalizes well on offensive rebounds, showing a solid FG% 46.7% and efficient scoring. 🏀💪

Off-screen plays exhibit moderate efficiency with a reasonable FG percentage (FG%: 31.6%). 📏🏹

Kyle excels significantly as a ball handler in pick and roll situations without sacrificing shot accuracy (FG%: 54.2% 🌟). 🔄🏆

Consistent as a roll man in PnR with decent shooting percentage and low turnovers, scoring the second most points here. 📊🎯

A proficient spot-up shooter with a solid FG% and good overall efficiency. 🎯🏀

Effective in transition with high PPP and a solid shooting percentage. 🚀🔥

Kyle Rode is a competent scorer averaging 14.2 points per game, shooting 38.8% from three-point range, and contributing with 4.9 rebounds and 2.5 assists. ⭐🏀

Instructions:

Parse the JSON data: Extract the synergy and box score statistics.
Analyze the data: Identify key performance indicators such as shooting percentages, turnovers, points per possession (PPP), and other relevant stats.
Generate the line by line  summary:Mention only play types with more than 7% of his play  For each play type, write a one-liner that highlights the key stats, focusing on strengths and weaknesses 
Avoid listing raw stats upfront. Instead, embed the statistics within short concise  sentences.
Requirements:

The summary should be coherent and provide a clear picture of the player's performance.
Highlight impressive stats as well as areas needing improvement.
Use percentages, points per possession (PPP), and other relevant metrics to support your statements.
Make the narrative engaging by using varied sentence structures and appropriate adjectives.
                    
                """
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
    
    
