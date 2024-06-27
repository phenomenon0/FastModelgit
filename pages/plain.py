
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
                    "content": """# Player Statistics Analysis Prompt

You are tasked with analyzing basketball player statistics and generating insightful descriptions of player performance. Follow these steps to create a comprehensive analysis:

## 1. Data Preparation

Ensure you have the following statistics for each player:

- Points
- Offensive Rebounds
- Defensive Rebounds
- Assists
- Turnovers
- Steals
- Blocks
- 2 pt FG %
- 2ptFGA
- 3 pt FG %
- 3ptFGA
- FT%
- Free Throw Rate
- Points Per Possession

## 2. Statistical Hierarchy

For the following categories, use statistics in this order of preference:
1. Percentage (e.g., Offensive Rebound Percentage)
2. Per 40 minute values
3. Per game values

Categories: Offensive Rebounds, Defensive Rebounds, Assists, Turnovers, Steals, Blocks

## 3. Analysis Steps

### 3.1 Basic Per Game Stats
If only per-game stats are available, use these for initial analysis.

### 3.2 Percentage-based Stats
Prioritize percentage-based stats when available for a more accurate representation.

### 3.3 Contextual Rankings
For each statistic, provide context by ranking the player's performance. Use descriptive language to convey their standing. Examples:

- "[Player] has an offensive rebounding percentage of [X]%, making them one of the better players off the offensive glass."
- "[Player] is a poor free throw shooter at only [X]%."
- "[Player] shoots [X]% on 3-pointers, which is slightly above league average."

### 3.4 Shot Selection and Location Analysis
Analyze the player's shooting performance from five zones:
- At the rim
- Short mid-range
- Long mid-range
- Corner three
- Above the break three

For each zone, comment on:
1. Frequency of shots taken
2. Effectiveness from that location

Example statements:
- "[Player] takes very few shots at the rim ([X]% of their shots) and is an ineffective shooter from that distance ([Y]%)."
- "[Player] takes a lot of corner threes ([X]% of their shots), and is slightly below average at that location ([Y]%)."

### 3.5 Highlight Key Strengths and Weaknesses
Instead of commenting on all stats, focus on the player's top strengths and notable weaknesses. Provide analysis for:
- Top 3-5 statistical strengths
- Bottom 2-3 statistical weaknesses

## 4. Output Format

For each player, provide:

1. A brief overall summary (2-3 sentences)
2. 3-5 sentences highlighting their key strengths, using contextual rankings
3. 2-3 sentences noting their main weaknesses
4. 1-2 sentences about their shot selection and efficiency from different areas of the court

Ensure the analysis is clear, concise, and provides meaningful insights into the player's performance and playing style.
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
    
    
