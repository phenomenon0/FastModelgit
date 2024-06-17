from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# Dumbledore's Template🏀✨")


####################



st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha"])

################ PAGE STARTS HERE ############################## 
 

client = OpenAI(api_key=st.secrets["open_ai"])


# Define the list of questions
questions = [
    "What is the player's standout characteristics?",
    "How to play against him?",
    "player notes?",
   
]


# Define the function to get the scouting report
@st.cache_data()
def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
        messages=[
            {
                    "role": "system",
                    "content": """System Prompt:
                    You are an expert basketball scout analyzing players using box scores and advanced statistics to prepare your team for upcoming games. 
                    Use Markdown and emojis to emphasize key points. Answer the question asked about the team    
                    Keep it simple and concise these are matchday instructions  make it lean as veal.
                    use stats only to highlight key points

                """
            },
            {
                "role": "user",
                "content": player_boxscore + " " + questions[0]   + " " + questions[1] + " " + questions[2]
            },
            
        ],
    )

    return chat_completion.choices[0].message.content


temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=2.0, value=1.5, step=0.1)


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
    
    
