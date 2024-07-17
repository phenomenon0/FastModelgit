
from openai import OpenAI
import json
import streamlit as st
import os 

st.title(' A Plain Jane ')
 

     
    
     
 

################ PAGE STARTS HERE ############################## 

 
#team_voice = st.text_input("Team scout- sample report ")
client = OpenAI(api_key=st.secrets["open_ai"])

# Define the function to get the scouting report

def get_scouting_report(_llm, model, player, temperature,seed):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
        messages=[
            {
                    "role": "system",

                    "content": """Prompt:You are an expert basketball scout analyzing players using only box scores and percentage rank to prepare your team for upcoming games. 
                    ignore the syn stats 
                    Follow the example provided in terms of grammar, language, and tone..
                    Use Markdown and emojis to emphasize key points - favour one line bullet points
                     Focus on how they play 
                     Avoid listing raw stats upfront. Instead, embed the statistics within short concise  sentences.
                     Highlight only 9  of the most important statistics - 1 line max 
                    
                    In simple english and concise these are matchday instructions  make 'em lean 
                    
                  this an example of user prompt and assistant response
                   user: {
  "player": {
    "scoring": {
      "points_per_game": 4.2,
      "minutes_per_game": 17.2,
      "percentile": 60
    },
    "shooting": {
      "fg_percentage": {
        "overall": 37.2,
        "conference": 45.5,
        "percentile": 70
      },
      "3p_percentage": {
        "overall": 27.0,
        "conference": 39.1,
        "percentile": 75
      }
    },
    "free_throws": {
      "percentage": {
        "overall": 83.3,
        "conference": 100,
        "percentile": 90
      }
    },
    "assists_turnovers": {
      "assists_per_game": 1.2,
      "turnovers_per_game": 1.0,
      "ratio_percentile": 60
    },
    "defense": {
      "steals_per_game": 0.7,
      "blocks_per_game": 0.0
    }
  },
  "defensive_strategies": {
    "perimeter_defense": {
      "3p_percentage": 27.0,
      "percentile": 40
    },
    "pressure_ball_handler": {
      "focus": "average FG%"
    },
    "help_defense_rotations": {
      "3p_percentage_conference": 39.1,
      "percentile": 75
    }
  }
}

                assistant: 🏀 Scoring: Averages 4.2 points in 17.2 minutes, ranking in the 60th percentile. \n
                            🎯 2-Point FG%: Improved FG% to 45.5% in conference play, ranking in the 70th percentile.\n
                            🎯 3-Point FG%: Conference 3P% of 39.1%, placing them in the 75th percentile.\n
                            💪 Free Throws: 83.3% overall, perfect 100% in conference games, ranking in the 90th percentile.\n
                            🔄 Assist-to-Turnover Ratio: Solid with 1.2 assists to 1.0 turnovers, ranking in the 60th percentile.\n
                            🚫 Perimeter Defense: Contest all 3-point shots, exploiting their 27% season average (40th percentile).\n
                            🔒 Pressure the Ball Handler: Force tough mid-range shots, focusing on their average FG% 28% .\n
                            👥 Help Defense and Rotations: Quick help defense to counter their 75th percentile 3P% in conference play.\n
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
    
    
