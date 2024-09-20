
from openai import OpenAI
import json
import streamlit as st
import os 


st.sidebar.markdown('HOCKEY')

     
     
st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha", "teams", "Money Ranger"])

################ PAGE STARTS HERE ############################## 

st.title("FastIntelligence HOCKEY")
#team_voice = st.text_input("Team scout- sample report ")
player_boxscore = st.text_input("Paste Player box scores + sample data")
client = OpenAI(api_key=st.secrets["open_ai"])


def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
         seed=111,
        messages=[
            { "role": "system",
                    "content":"""You are A veteran hockey scout jotting key points about a roster of player into a pad.
                    here's a sample of usual input and a preffered output.
                    input>>> {"Name": "Tyler Bertuzzi", "Number": 59, "Position": "LEFT WING", "S/C": "L", "Weight": "200 lbs", "Height": "6'2"", "GP": 80, "G": 21, "A": 22, "P": 43, "PIM": 53, "+/-": 2, "FO%": 30.8}
                    output >>>High Impact Offensive Threat, Left Handed Winger, Strong Goal Scorer
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
#seed_value = st.radio("Seed Values", [111, 2652, 230, 4432])
temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.1, max_value=2.0, value=0.7, step=0.1)


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
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature )
    st.write(scouting_report)
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    
    
