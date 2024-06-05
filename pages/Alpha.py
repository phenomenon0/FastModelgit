
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
    """3 • Chris Paul • G • 6'0" • 175 lbs GP-GS PTS MIN FGM-A FG% 3PM-A 3P% FT% FTM-A REB AST TO STL BLK Regular Season 59-18 9.1 26.3 3.5-8.0 44.0% 1.3-3.6 37.3% 82.7% 0.7-0.9 3.8 6.7 1.3 1.2 0.1 Last 5 5-2 7.4 25.1 3.2-8.2 39.0% 1.0-3.6 27.8% - 0.0-0.0 3.6 5.4 1.4 0.6 0.2 Play Type %Time Poss Points PPP %Rank Rating FGm FGM FGA FG% aFG% %TO %FT %SF %Score P&R Ball Handler 42.1% 239 218 0.912 - - 109 94 203 46.3% 50% 12.1% 3.8% 3.3% 42.3% Spot Up 23.1% 131 149 1.137 - - 73 52 125 41.6% 59.2% 4.6% 0.8% 0.8% 39.7% Isolation 9% 51 54 1.059 - - 26 22 48 45.8% 54.2% 3.9% 2% 2% 45.1% Miscellaneous 8.3% 47 27 0.574 - - 10 3 13 23.1% 34.6% 48.9% 23.4% 0% 29.8% Transition 8.1% 46 34 0.739 - - 20 13 33 39.4% 50% 28.3% 2.2% 2.2% 28.3% Hand Off 4.8% 27 23 0.852 - - 15 11 26 42.3% 44.2% 3.7% 0% 0% 40.7% Offensive Rebounds (put backs) 1.2% 7 10 1.429 - - 1 4 5 80% 80% 14.3% 14.3% 0% 71.4% Off Screen 1.1% 6 3 0.5 - - 4 1 5 20% 30% 16.7% 0% 0% 16.7% Cut 1.1% 6 8 1.333 - - 1 4 5 80% 80% 16.7% 0% 0% 66.7% Post Up 0.9% 5 8 1.6 - - 1 3 4 75% 75% 0% 20% 0% 80% P&R Roll Man 0.5% 3 0 0 - - 3 0 3 0% 0% 0% 0% 0% 0%""",
    """11 • Klay Thompson • G • 6'6" • 220 lbs GP-GS PTS MIN FGM-A FG% 3PM-A 3P% FT% FTM-A REB AST TO STL BLK Regular Season 78-64 17.6 29.7 6.3-14.7 42.9% 3.4-8.9 38.4% 92.7% 1.6-1.8 3.3 2.3 1.5 0.6 0.4Play Type %Time Poss Points PPP %Rank Rating FGm FGM FGA FG% aFG% %TO %FT %SF %Score Off Screen 32.9% 431 472 1.095 - - 221 162 383 42.3% 56.5% 7.4% 5.3% 5.3% 41.3% Spot Up 17.7% 232 250 1.078 - - 137 90 227 39.6% 54% 1.7% 1.7% 1.7% 39.2% Transition 16.1% 211 238 1.128 - - 99 84 183 45.9% 59.6% 8.5% 5.2% 4.7% 44.1% P&R Ball Handler 9.1% 120 113 0.942 - - 51 45 96 46.9% 54.7% 16.7% 3.3% 2.5% 40.8% Hand Off 8.9% 117 111 0.949 - - 61 38 99 38.4% 49.5% 11.1% 6% 6% 36.8% Cut 5% 66 77 1.167 - - 23 35 58 60.3% 60.3% 7.6% 6.1% 6.1% 57.6% Isolation 2.8% 37 35 0.946 - - 16 12 28 42.9% 48.2% 13.5% 10.8% 10.8% 43.2% Miscellaneous 2.7% 35 19 0.543 - - 6 3 9 33.3% 38.9% 54.3% 22.9% 5.7% 28.6% """
,"""Jonathan Kuminga • F • 6'7" • 225 lbs GP-GS PTS MIN FGM-A FG% 3PM-A 3P% FT% FTM-A REB AST TO STL BLK Regular Season 75-46 16.1 26.4 6.2-11.7 52.7% 0.7-2.2 31.7% 74.4% 3.0-4.1 4.8 2.2 1.6 0.7 0.5 Last 5 5-2 12.8 26.8 4.8-9.8 49.0% 0.6-1.8 33.3% 81.2% 2.6-3.2 5.8 3.4 1.2 0.8 0.6 Play Type %Time Poss Points PPP %Rank Rating FGm FGM FGA FG% aFG% %TO %FT %SF %Score Spot Up 22.4% 254 252 0.992 - - 128 94 222 42.3% 51.4% 6.3% 6.7% 6.7% 42.1% Transition 20.4% 231 297 1.286 - - 57 113 170 66.5% 67.6% 10.4% 20.8% 19.9% 64.5% Cut 14.1% 160 205 1.281 - - 43 85 128 66.4% 66.4% 6.2% 17.5% 16.9% 65.6% Post Up 11.6% 131 122 0.931 - - 49 46 95 48.4% 48.4% 15.3% 16.8% 16% 47.3% P&R Ball Handler 9% 102 94 0.922 - - 42 37 79 46.8% 49.4% 11.8% 13.7% 13.7% 46.1% Isolation 7.2% 82 84 1.024 - - 35 30 65 46.2% 47.7% 11% 20.7% 20.7% 46.3% Offensive Rebounds (put backs) 5.2% 59 62 1.051 - - 23 26 49 53.1% 54.1% 6.8% 11.9% 11.9% 52.5% P&R Roll Man 3.5% 40 48 1.2 - - 11 16 27 59.3% 59.3% 10% 25% 25% 62.5% Miscellaneous 3.1% 35 15 0.429 - - 5 4 9 44.4% 44.4% 54.3% 20% 2.9% 28.6% Off Screen 2.1% 24 15 0.625 - - 15 6 21 28.6% 33.3% 8.3% 4.2% 4.2% 29.2% Hand Off 1.4% 16 11 0.688 - - 8 5 13 38.5% 38.5% 12.5% 6.2% 6.2% 37.5%"""]
def generate_scouting_report(data):
    player_boxscore = random.choice(data)
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature, top_p, seed_value)
    st.write(scouting_report)

if st.button("Use Sample Data"):
    generate_scouting_report(sample_data)
