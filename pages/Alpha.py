
from openai import OpenAI
import json
import streamlit as st
import os 
import random

st.markdown('## Alpha')
st.sidebar.markdown('This is the Alpha page')

####################

st.title("A-eye: AI powered basketball scouting tool, Defensive v 1")
#team_voice = st.text_input("Team scout- sample report ")
player_boxscore = st.text_input("Player box scores")
client = OpenAI(api_key=st.secrets["open_ai"])


# Define the function to get the scouting report
@st.cache_data()
def get_scouting_report(_llm, model, player, temperature, p,seed):
    chat_completion = _llm.chat.completions.create(
        model=model,
        
        messages=[
            {
                "role": "system",
                "content": """You are an expert basketball scout analyzing players using box scores and preparing your team to play against them. 
                write how they play and  defensive strategy tell me why you choose each sentence . use markdown and emoji to emphasize key points. 
                Mimic examples below
                 

                Q: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK 
                All 20-10 4.2 17.2 1.6-4.3 37.2% 0.5-1.8 27.0% 83.3/% 0.5-0.6 1.7 1.2 1.0 0.6 0.0
                Conf 10-6 6.5 21.8 2.5-5.5 45.5% 0.9-2.3 39.1% 100/% 0.6-0.6 1.8
                1.5 1.4 0.7 0.0
                
                A:Efficient and physical PG - driver LEFT 🚀⬅️
                Will take what the defense gives...must keep in front in transition - will go until stopped 🛡️🏃
                Very good 3 point shooter with time and space - moves well off ball (made FOUR 3's v UVA) 🎯🏀
                Keep in front and be in airspace on the catch 🚫✋
                
                Q: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                All, 35-2, 17.2, 5.2, 3.1, 0.7, 66-147, 44.9%, 41-115, 35.7%, 8-13, 61.5%
                Conf, 20-2, 19.2, 4.5, 3.2, 0.8, 33-81, 40.7%, 21-65, 32.3%, 3-4, 75.0%
                
                A:Tall, Pick & Pop 5 man (Can play some 4 w/ #13 Ihgodaro in the game), 
                Hunting 3's!!! - 78/%/ FGA = 3's!!, Set B/S or Slip out - Always Pop - 
                Spot up off drives, All C&S, On fire right now, must take away 3's!! Last 5:
                60% 3PT [9-15], Sneaky athletic on perimeter - Take away 3 = SF & Attack the rim, Will drive to a Barkley. Wants to Attack RT!!, 
                Capable O-Rebounder w/ his size - must hit, Can move his feet pretty well on D in Switch 
                - Attack him & make the right play, KEY: Sprint Back & Locate in Transition 
                - NO 3's!! Make him Bounce into tough, contested 2's, BOX OUT
                
                user: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                All, 34-0, 9.0, 2.0, 1.2, 0.4, 28-74, 37.8%, 7-37, 18.9%, 5-9, 55.6%
                Conf, 19-0, 9.4, 2.5, 1.5, 0.3, 19-45, 42.2%, 4-23, 17.4%, 5-6, 83.3%
                
                A:DRIVER - CAPABLE SHOOTER 🏀🎯
                Athletic guard 🏃‍♂️💪 - Most damage done in Transition 🏃‍♂️💥, Runs the floor hard for easy baskets 🏀⚡,
                Either @ Rim or Shooting a 3 🏀🏹 - No midrange game 🚫📏, Attacks both ways 🔄🔥. LOVES SF!! ❤️🏀 Gets to floater or jump stop finish 🏀🛑,
                1/2 FGA = 3's 🔢🎯. All C&S!! 🎯📤 Will run for 3's in transition & relocate on teammate drives 🏃‍♂️🏀, Low %, better recently Last 5:
                29% 3PT [2-7] 📉📈, Excellent Cutter on teammate dribble penetration ✂️🏀, KEY: Sprint Back in Transition 🏃‍♂️🏃‍♂️, Nothing easy! 🚫❗ GYY -
                Keep the ball in front & make him finish over. Contest shots high! 🚧✋
                
                """
            },
            {
                "role": "user",
                "content": player_boxscore + "take a deep breath analyze the  player and follow the example for grammar,language and tone use always use stats one each line to  highlight your point. short and to the point "
            },
            
        ],
    )

    return chat_completion.choices[0].message.content
#openai strategy is to tweak either temperature or top_p to get the desired output not both 
seed_value = st.radio("Seed Values", [111, 22, 23, 4])
temperature = st.slider("Temperature", min_value=0.7, max_value=1.8, value=0.8, step=0.1)
top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=0.9, step=0.1)

if st.button("Generate Scouting Report"):
    scouting_report = get_scouting_report(client,  "gpt-4o", player_boxscore,temperature, top_p, seed=seed_value)
    st.write(scouting_report)
    
sample_data = [
    """3 • Chuma Okeke • F • 6'7" • 229 lbs GP-GS PTS MIN FGM-A FG% 3PM-A 3P% FT% FTM-A REB AST TO STL BLK Regular Season 42-8 2.5 9.8 0.9-2.5 36.4% 0.5-1.9 29.1% 40.0% 0.0-0.1 1.8 0.5 0.3 0.2 0.2 Spot Up 46.3% 57 44 0.772 - - 39 15 54 27.8% 40.7% 5.3% 0% 0% 26.3% P&R Ball Handler 3.3% 4 7 1.75 - - 1 3 4 75% 75% 0% 25% 25% 75% Transition 13% 16 17 1.062 - - 6 6 12 50% 70.8% 25% 0% 0% 37.5% Cut 6.5% 8 10 1.25 - - 3 5 8 62.5% 62.5% 0% 0% 0% 62.5% Isolation 2.4% 3 3 1 - - 1 1 2 50% 75% 33.3% 0% 0% 33.3% P&R Roll Man 3.3% 4 3 0.75 - - 3 1 4 25% 37.5% 0% 0% 0% 25% Offensive Rebounds (put backs) 4.9% 6 4 0.667 - - 2 2 4 50% 50% 16.7% 16.7% 16.7% 33.3% Off Screen 4.9% 6 3 0.5 - - 5 1 6 16.7% 25% 0% 0% 0% 16.7% Hand Off 10.6% 13 11 0.846 - - 5 5 10 50% 55% 23.1% 0% 0% 38.5% Miscellaneous 4.9% 6 1 0.167 - - 3 0 3 0% 0% 33.3% 16.7% 0% 16.7%""",
    """11 • Klay Thompson • G • 6'6" • 220 lbs GP-GS PTS MIN FGM-A FG% 3PM-A 3P% FT% FTM-A REB AST TO STL BLK Regular Season 78-64 17.6 29.7 6.3-14.7 42.9% 3.4-8.9 38.4% 92.7% 1.6-1.8 3.3 2.3 1.5 0.6 0.4Play Type %Time Poss Points PPP %Rank Rating FGm FGM FGA FG% aFG% %TO %FT %SF %Score Off Screen 32.9% 431 472 1.095 - - 221 162 383 42.3% 56.5% 7.4% 5.3% 5.3% 41.3% Spot Up 17.7% 232 250 1.078 - - 137 90 227 39.6% 54% 1.7% 1.7% 1.7% 39.2% Transition 16.1% 211 238 1.128 - - 99 84 183 45.9% 59.6% 8.5% 5.2% 4.7% 44.1% P&R Ball Handler 9.1% 120 113 0.942 - - 51 45 96 46.9% 54.7% 16.7% 3.3% 2.5% 40.8% Hand Off 8.9% 117 111 0.949 - - 61 38 99 38.4% 49.5% 11.1% 6% 6% 36.8% Cut 5% 66 77 1.167 - - 23 35 58 60.3% 60.3% 7.6% 6.1% 6.1% 57.6% Isolation 2.8% 37 35 0.946 - - 16 12 28 42.9% 48.2% 13.5% 10.8% 10.8% 43.2% Miscellaneous 2.7% 35 19 0.543 - - 6 3 9 33.3% 38.9% 54.3% 22.9% 5.7% 28.6% """
,""""""]
def generate_scouting_report(data):
    player_boxscore = random.choice(data)
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature, top_p, seed_value)
    st.write(scouting_report)

if st.button("Use Sample Data"):
    generate_scouting_report(sample_data)
