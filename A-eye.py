
from openai import OpenAI
import json
import streamlit as st
import tiktoken

st.markdown('## Current Branch')
st.sidebar.markdown('This is the Current Branch')
st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha"])

################ PAGE STARTS HERE ############################## 

st.title("A-eye: AI powered basketball scouting tool")
#team_voice = st.text_input("Team scout- sample report ")
player_boxscore = st.text_input("Player box scores")
client = OpenAI()


# Define the function to get the scouting report
@st.cache_data()
def get_scouting_report(_llm, model, player, temperature, p,seed):
    chat_completion = _llm.chat.completions.create(
        model=model,
   
        messages=[
            {
                    "role": "system",
                    "content": """System Prompt:
                    You are an expert basketball scout analyzing players using box scores and advanced statistics to prepare your team for upcoming games. 
                    Follow the example provided in terms of grammar, language, and tone.. Focus on how they play and  defensive strategies to counteract key players.
                    Use Markdown and emojis to emphasize key points. Highlight only 5 of the most important statistics 
                    Keep it simple and concise these are matchday instructions  make it lean 
                    
                    Example Output:
                    Player Analysis:
                    Hub of Their Offense - His constant movement fuels their offense. Cannot relax! 🚨

                    Leads the NBA in 3PAs/game: Over 12 per game. 🏀
                    4PT Threat: Most dangerous in transition. 🏃‍♂️💨
                    18 picks/game: Be ready for pick-and-roll plays. Loves to use hostage dribble and snake the P/R.
                    Contain and Defend Without Fouling: #1 in NBA in FT% (92.0%). 🚫🏀
                    Undersized Defender: Can be targeted. Will gamble defensively (charge taker). ⚠️
                    
                    
                    Example Output 2:
                    🚗 Driver First
                    💪 Strong Driver - always trying to get middle / likes to shoot floaters at MAC logo 🏀 - has to feel your chest early 👊 / Away 🏠
                    🙋‍♂️ Hold play for him / Elbow Isos
                    🏀 Novas in half court and transition / Shooting the ball well lately 🎯
                    🐜 Pesky defender - must be ball strong 💪
                    
                    Example Output 3:
                    🔫 Spot-Up Perimeter Scorer
                    🎨 Crafty around the paint - Plays off two - High Flippers off glass in paint 🏀 - MUST HARD CONTEST ✋
                    🎭 Ball fakes, step throughs, head fakes - deceptive - Stay solid and keep your shield 🛡️ and feet 🦶 in front of him & rim 🏀
                    📞 Calls for High Pick & Rolls end of Shot Clock ⏰ - goes to Midrange in the end of shot clock situations
                    🚫 MUST ANNOY HIS RHYTHM WITH ULTRA-PHYSICALITY 💪
                """
            },
            {
                "role": "user",
                "content": player_boxscore + "analyze player coach and follow the example as well as you can in terms of grammar,language and tone."
            },
            
        ],
    )

    return chat_completion.choices[0].message.content

#token length 
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens



#openai strategy is to tweak either temperature or top_p to get the desired output not both 
seed_value = st.radio("Seed Values", [111, 2652, 230, 4432])
temperature = st.slider("Temperature", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=0.9, step=0.1)

if st.button("Generate Scouting Report"):
    scouting_report = get_scouting_report(client,  "gpt-3.5-turbo", player_boxscore,temperature, top_p, seed_value)
    st.write(scouting_report)
    st.markdown(f"Number of output tokens: :green[{num_tokens_from_string(scouting_report, 'cl100k_base')}]  input tokens: :red[300]")
    
    
    
