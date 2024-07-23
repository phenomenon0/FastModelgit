from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# PAT and JEFFERSON 🕵️🕵️‍♂️")


####################



st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha"])

################ PAGE STARTS HERE ############################## 
 

client = OpenAI(api_key=st.secrets["open_ai"])




# Define the function to get the scouting report
def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
     seed= 111,
        messages=[
            {
                    "role": "system",
                    "content":"""You are an expert basketball scout analyzing players using box scores and synergy stats. Create a concise scouting report following these strict guidelines:

FORMAT:
• Use ONLY bullet points, no subheadings or paragraphs.
• Each bullet point should start with "•".
• Follow the exact structure provided for each bullet point.
• Avoid use of "_" in stats 


## Player Breakdown

• [adjective] usage [POSITION] ([USG%] ) who plays [adjective] minutes ([MPG] mpg) scoring [PPG] PPG ([PPG] percentile) on [adjective] [TS%] TS% ([TS%] percentile)

• More likely to shoot from the [outside/inside] ([2P-R or 3P-R]% [2P-R or 3P-R]) where he/she shoots a [adjective] [2P% or 3P%] [2P% or 3P%]

• Most commonly used in [synergy play type with highest % Time, and % Time ], where he/she produces [PPP] PPP
  (Never mention Miscellaneous Play type)

• [adjective] rebounding [POSITION] especially on [Defense/Offense] averaging [ORB/G or DRB/G] ([DRB or ORB] percentile)
  (Include DRB/G if > 3, ORB/G if > 1. Always mention ORB% and DRB%)

• [adjective] facilitator who averages [APG] APG ([APG] percentile) with a [AST%] AST% ([AST%] percentile) and turns it over [adjective] with [TO/G] TO/G ([TO/G] percentile)
  (Only include if USG% > 10%)

• [adjective] defensively, averaging [STL/G or BLK/G] [STL/G or BLK/G]
  (Only include if STL/G or BLK/G is in 80th percentile or above)

• [adjective] free throw shooter at [FT%] ([FT%] percentile) who gets to the line [adverb] at [FT-R] FT-R
  (Only include if player averages more than 2 FTA per game e.g 14% FT-R)

Analyze the provided player data and generate a breakdown strictly adhering to this format. Include only the relevant bullet points based on the player's stats and the given criteria.​​​​​​
"""
      
            },
            {
                "role": "user",
                "content": player_boxscore
            },
            
        ],
    )

    return chat_completion.choices[0].message.content


temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=2.0, value=0.7, step=0.1)


if st.button("Generate Scouting Report from input"):
    scouting_report = get_scouting_report(client,  "gpt-4o", player_boxscore,temperature)
    st.write(scouting_report)
    

# Sample data
import json
with open("players.json", "r") as f:
    data = json.load(f)
sample_data = list(data)

def generate_scouting_report(data):
    
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature)
    st.write(scouting_report)
    

if st.button("Use Sample Data to Generate"):
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    else:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    player_boxscore = str(sample_data[st.session_state.current_index])
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature)
    st.write(scouting_report)
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    
    
