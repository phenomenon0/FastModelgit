
from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# teams 🕵️🕵️‍♂️")


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
                    "content":"""Generate a scouting report for a basketball team based on the provided JSON data. 
                    The report should follow this exact format:
format:
## Offense
* [TEAM NAME] averages [PPG] PPG ([PPG League Rank]) with an [adjective - efficient/inefficient] [ORTG] ORTG ([ORTG League Rank]).
* They play [adjective - faster/slower] than the average team with [POSSESSIONS PER GAME] possessions per game ([POSSESSIONS PER GAME League Rank]).
* The [TEAM NICKNAME] take more [2's/3's] compared to [3's/2's] with a [2P-R]% 2P-R ([2P-R League Rank]) and a [3P-R]% 3P-R ([3P-R League Rank]). They are [adjective] inside the arc with a [2P%]% 2P% ([2P% League Rank]). [Adjective] from 3-point territory with a [3P%]% 3P% ([3P% League Rank]).
* Most of their possessions end in [Synergy Play Type with most % Time] where they score at a rate of [Synergy Play Type PPP] PPP ([% Time]% of time).
* [TEAM NAME] is a [adjective] rebounding team with a [Team ORB%]% ORB% ([Team ORB% League Rank]) and a [Team DRB%]% DRB% ([Team DRB% League Rank]).  
* They are [very/not very] reliant on assists to score with a [Team AST%]% AST% ([Team AST% League Rank]) and do a [adjective] job of taking care of the basketball, turning it over [TO/Game] times per game ([TO/Game League Rank]).
* They do a [adjective] job of getting to the foul line with a [FT-R]% FT-R ([FT-R League Rank]) and knock down [FT%]% of those attempts ([FT% League Rank]).

## Defense 
* The [TEAM NICKNAME] give up [Opponent PPG] PPG ([Opponent PPG League Rank]) with an [adjective] [DRTG] DRTG ([DRTG League Rank]).
* Their defense does a [adjective] job of limiting opponents to a [adjective] [Opponent 2P-R or 3P-R, whichever is lowest]% [2P-R or 3P-R]. Their opponents convert [Opponent 2P%]% of their 2s ([Opponent 2P% League Rank]) and [Opponent 3P%]% of their 3s ([Opponent 3P% League Rank]).
* [TEAM NAME] is a [adjective] rebounding team, with their opponents grabbing a [adjective] [Opponent ORB%]% ORB% ([Opponent ORB% League Rank]) and [Opponent DRB%]% DRB% ([Opponent DRB% League Rank]).
* They [force/hold/allow] opponents into a [Opponent AST%]% AST% ([Opponent AST% League Rank]) and force turnovers at a [Opponent TO%]% rate ([Opponent TO% League Rank]). 
* Do a [adjective] job of keeping opponents off the foul line with a [Opponent FT-R]% FT-R ([Opponent FT-R League Rank]).
* [TEAM NAME] does a [adjective] job of not fouling, averaging [PF per game] fouls per game ([PF per game League Rank]).

Replace the bracketed stats with the corresponding values from the provided JSON. Choose appropriate adjectives based on the stats and ranks. Determine whether the team takes more 2's or 3's by comparing 2P-R and 3P-R."""
      
            },
            {
                "role": "user",
                "content": player_boxscore
            },
            
        ],
    )

    return chat_completion.choices[0].message.content


temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=2.0, value=0.9., step=0.1)


if st.button("Generate Scouting Report from input"):
    scouting_report = get_scouting_report(client,  "gpt-4o", player_boxscore,temperature)
    st.write(scouting_report)
    

# Sample data
import json
with open("teams.json", "r") as f:
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
    
    
