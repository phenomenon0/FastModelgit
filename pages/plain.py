
from openai import OpenAI
import json
import streamlit as st
import os 

st.title(' SOCCER')
 

     
    
     
 

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

                    "content": """You are an expert soccer scout and analyst with a deep understanding of the game. Using the data points provided for the soccer team and its roster, generate a comprehensive team summary take note of team leaders in categories like shot taken , shot on target percent goals assists - - incorprate them into player reports when relevant. The output should be in JSON format, starting with the team summary, followed by an array of players with their respective analyses.



Output format:
{
  "team_summary": "Your expertly crafted team summary here.",
  "players": [
    {
      "name": "Player Name",
      "position": "Player Position",
      "analysis": "In-depth player analysis with brilliant insights."
    },
    // Repeat for each player
  ]
}

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
    
    
