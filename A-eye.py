
from openai import OpenAI
import json
import streamlit as st
import os 

st.markdown('## Current Branch')
st.sidebar.markdown('This is the Current Branch')

     
    
     
st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha", "Plain Jane"])

################ PAGE STARTS HERE ############################## 

st.title("A-eye: AI powered basketball scouting tool🏀🤖")
#team_voice = st.text_input("Team scout- sample report ")
player_boxscore = st.text_input("Paste Player box scores + synergy scores here or try sample data")
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
                    "content": """System Prompt:
                    You are an expert basketball scout analyzing players using box scores and advanced statistics to prepare your team for upcoming games. 
                    Follow the example provided in terms of grammar, language, and tone.. Focus on how they play and  defensive strategies to counteract key players.
                    Use Markdown and emojis to emphasize key points. Highlight only 5 of the most important statistics 
                    Keep it simple and concise these are matchday instructions  make it lean 
                    Avoid listing raw stats upfront. Instead, embed the statistics within short concise  sentences.
                  this an example of user prompt and assistant response
                   user: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK 
                            All 20-10 4.2 17.2 1.6-4.3 37.2% 0.5-1.8 27.0% 83.3/% 0.5-0.6 1.7 1.2 1.0 0.6 0.0
                            Conf 10-6 6.5 21.8 2.5-5.5 45.5% 0.9-2.3 39.1% 100/% 0.6-0.6 1.8
                            1.5 1.4 0.7 0.0
                assistant: Efficient and physical PG - driver LEFT 🚀⬅️
                        Will take what the defense gives...must keep in front in transition - will go until stopped 🛡️🏃
                        Very good 3 point shooter with time and space - moves well off ball (made FOUR 3's v UVA) 🎯🏀
                        Keep in front and be in airspace on the catch 🚫✋
                        
                    user:GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                    All, 35-2, 17.2, 5.2, 3.1, 0.7, 66-147, 44.9%, 41-115, 35.7%, 8-13, 61.5%
                    Conf, 20-2, 19.2, 4.5, 3.2, 0.8, 33-81, 40.7%, 21-65, 32.3%, 3-4, 75.0%
                    
                    assistant:Tall, Pick & Pop 5 man   Hunting 3's!!! 🎯 - 78% FGA = 3's!!, Set B/S or Slip out - Always Pop - Spot up off drives, All C&S, On fire right now 🔥,
                    must take away 3's!! Last 5: 60% 3PT [9-15] 🔥, Sneaky athletic on perimeter - Take away 3 = SF & Attack the rim 🏀,  Capable O-Rebounder w/ his size - must hit 💪,
                    Can move his feet pretty well on D in Switch 🔄 - Attack him & make the right play, KEY: Sprint Back & Locate in Transition 🏃‍♂️🏃‍♂️ - NO 3's!! 🚫 Make him Bounce into tough, contested 2's 🚧, BOX OUT 
                    
                    Example Output 3:
                    user: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                        All, 34-0, 9.0, 2.0, 1.2, 0.4, 28-74, 37.8%, 7-37, 18.9%, 5-9, 55.6%
                        Conf, 19-0, 9.4, 2.5, 1.5, 0.3, 19-45, 42.2%, 4-23, 17.4%, 5-6, 83.3%
                    assistant:    
                    DRIVER - CAPABLE SHOOTER 🏀🎯
                    Athletic guard 🏃‍♂️💪 - Most damage done in Transition 🏃‍♂️💥, Runs the floor hard for easy baskets 🏀⚡,
                    Either @ Rim or Shooting a 3 🏀🏹 - No midrange game 🚫📏, Attacks both ways 🔄🔥. LOVES SF!! ❤️🏀 Gets to floater or jump stop finish 🏀🛑,
                    1/2 FGA = 3's 🔢🎯. All C&S!! 🎯📤 Will run for 3's in transition & relocate on teammate drives 🏃‍♂️🏀, Low %, better recently Last 5:
                    29% 3PT [2-7] 📉📈, Excellent Cutter on teammate dribble penetration ✂️🏀, KEY: Sprint Back in Transition 🏃‍♂️🏃‍♂️, Nothing easy! 🚫❗ GYY -
                    Keep the ball in front & make him finish over. Contest shots high! 🚧✋
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
seed_value = st.radio("Seed Values", [111, 2652, 230, 4432])
temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=1.0, value=0.7, step=0.1)


if st.button("Generate Scouting Report from input"):
    scouting_report = get_scouting_report(client,  "gpt-4o", player_boxscore,temperature, seed_value)
    st.write(scouting_report)
    

# Sample data
import json
with open("players.json", "r") as f:
    data = json.load(f)
sample_data = list(data)

def generate_scouting_report(data):
    
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature,  seed_value)
    st.write(scouting_report)
    

if st.button("Use Sample Data to Generate"):
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
    
    
