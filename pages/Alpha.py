from openai import OpenAI
import json
import streamlit as st
import os 
import pandas as pd

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
                    "content":"""You are a basketball scout writng a report based on a players stats follow this template to report 

Player Breakdown
• [adjective] usage [Position] ([USG%] ) who plays [adjective] minutes ([MPG] mpg) scoring [PPG] PPG ([PPG] percentile) on [adjective] [TS%] TS% ([TS%] percentile)

• More likely to shoot from the [outside/inside] ([2P-R or 3P-R]% [2P-R or 3P-R]) where he/she shoots a [adjective] [2P% or 3P%] [2P% or 3P%]



• [adjective] rebounding [Position] especially on [Defense/Offense] averaging [ORB/G or DRB/G] ([DRB or ORB] percentile)
  (Include DRB/G if > 3, ORB/G if > 1. Always mention ORB% and DRB%)

• [adjective] facilitator who averages [APG] APG ([APG] percentile) with a [AST%] AST% ([AST%] percentile) and turns it over [adjective] with [TO/G] TO/G ([TO/G] percentile)
  (Only include if USG% > 10%)

• [adjective] defensively, averaging [STL/G or BLK/G] [STL/G or BLK/G]
  (Only include if STL/G or BLK/G is in 80th percentile or above)

• [adjective] free throw shooter at [FT%] ([FT%] percentile) who gets to the line [adverb] at [FT-R] FT-R
  (Only include if player averages more than 2 FTA per game e.g 14% FT-R)


example
'USG%: 14.8; MPG: 15.0; PPG: 3.9; TS%: 51.6; TS% percentile: 45.0; 3PR: 8.6; 2PR: 91.4; 3P%: 11.1; 3P% percentile: 25.0; DRB%: 19.5; DRB% percentile: 87.0; ORB%: 8.3; ORB% percentile: 77.0; AST%: 2.8; AST% percentile: 14.0; TO%: 15.4; TO% percentile: 42.0; STL/G: 0.4; BLK/G: 0.2; STL% percentile: 40.0; BLK% percentile: 53.0; STL%: 1.4; FT%: 64.7; FTRate: 32.4; FTRate percentile: 56.0'

<ul>\\n <li>Low usage forward (14.8% USG) who plays average minutes (15.0 MPG) scoring 3.9 PPG on below average 51.6% TS% (45th percentile).</li>\\n \\n <li>More likely to shoot from the inside (91.4% 2P-R) where he shoots a balanced 52.1% 2P%.</li>\\n \\n <li>Gets most of his shots cutting off the ball,\<li>High rebounding forward, performing better on the defensive glass with a DRB% 19.5% (87th percentile) compared to ORB% 8.3% (77th percentile).</li>\\n \\n <li>Weak facilitator who assists on 2.8% of the team\'s field goals while on the court (14th percentile) and turns the ball over on 15.4% of their possessions (42nd percentile).</li>\\n \\n <li>Average defensively, averaging 0.4 STL/G.</li>\\n \\n <li>Weak free throw shooter at 64.7% who gets to the line frequently at 32.4% FT-R (56th percentile).</li>\\n</ul>"""
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
    

#sample data mini 
sample= pd.read_csv('small 50.csv')
sample_data = sample.Stats

def generate_scouting_report(data):
    
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature)
    st.write(scouting_report)
    

if st.button("Use Sample Data to Generate"):
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    else:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(sample_data)
    player_boxscore = str(sample_data[st.session_state.current_index])
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature)
    st.write(scouting_report)
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(sample_data)
    
    
