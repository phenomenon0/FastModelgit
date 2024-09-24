
from openai import OpenAI
import json
import streamlit as st
import os 


st.sidebar.markdown('HOCKEY')

     
     
st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha", "teams", "Money Ranger"])

################ PAGE STARTS HERE ############################## 

st.title("A-eye: AI powered basketball scouting tool🤖")
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
                    "content":"""You are A veteran hockey scout jotting key points about a roster of player into a pad based on this criteria.
                   


1. Size: Label forwards >6'1" as "big", <5'10" as "undersized". Defenders >6'2" as "big body", <5'10" as "undersized".
2. Position: Identify centers as "Centermen", LW/RW as "Wingers".
3. Offensive Production: Evaluate Goals/GP, Assists/GP, Points/GP for all players. Assess FO% for forwards. Use Value Chart: Elite (90-100), Above Average (60-89), Average (30-59), Below Average (0-29).
4. Ice Time: Label forwards >17 min/game, defenders >20 min/game as "Heavily Utilized".
5. Handedness: Identify left/right-handed players.
6. Penalties: Label players >0.6 PIM/GP as "Heavily Penalized".
7. Shooting: 
   - Forwards: >2.5 shots/GP "shoots everything", >1.8 "shoots lots", <1 "rarely shoots"
   - Defenders: >2.2 shots/GP "shoots everything", >1.2 "shoots lots", <0.5 "rarely shoots"
8. Power Play: Evaluate PP Points/GP, Goals/GP, Assists/GP using Value Chart.
9. Clutch & Defense: 
   - Label >0.65 GWG/GP as "Clutch Goal Scorers"
   - Forwards blocking >0.8 shots/GP, Defenders >2 "Blocks Everything", >1.4 "Shot Blocking"
10. Goalies: 
    - Size: >6'3" "big", <6'0" "undersized"
    - Performance: SV% >0.91 "Top", >0.9 "Strong"
    - Label as starter if played >60% of team games
11. General: Focus on positives. Start with elite characteristics and work down.
 here's a sample of usual input and a preffered output.
                    input>>> {"Name": "Tyler Bertuzzi", "Number": 59, "Position": "LEFT WING", "S/C": "L", "Weight": "200 lbs", "Height": "6'2"", "GP": 80, "G": 21, "A": 22, "P": 43, "PIM": 53, "+/-": 2, "FO%": 30.8}
                    output >>>High Impact Offensive Threat, Left Handed Winger, Strong Goal Scorer

                    make sure output is not more than 12 words.
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
with open("skater919.json", "r") as f:
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
    
    
