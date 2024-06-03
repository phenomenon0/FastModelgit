
from openai import OpenAI
import json
import streamlit as st
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
                
                Q: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                All, 34-0, 9.0, 2.0, 1.2, 0.4, 28-74, 37.8%, 7-37, 18.9%, 5-9, 55.6%
                Conf, 19-0, 9.4, 2.5, 1.5, 0.3, 19-45, 42.2%, 4-23, 17.4%, 5-6, 83.3%
                
                A: DRIVER - CAPABLE SHOOTER
                Athletic guard - Most damage done in Transition, Runs the floor hard for easy baskets,
                Either @ Rim or Shooting a 3 - No midrange game, Attacks both ways. LOVES SF!! Gets to floater or jump stop finish, 
                1/2 FGA = 3's. All C&S!! Will run for 3's in transition & relocate on teammate drives, Low %, better recently Last 5:
                29% 3PT [2-7], Excellent Cutter on teammate dribble penetration, KEY: Sprint Back in Transition, Nothing easy! GYY - 
                Keep the ball in front & make him finish over. Contest shots high!

                
                """
            },
            {
                "role": "user",
                "content": player_boxscore + "analyze player"
            },
            
        ],
    )

    return chat_completion.choices[0].message.content
#openai strategy is to tweak either temperature or top_p to get the desired output not both 
seed_value = st.radio("Seed Values", [111, 22, 23, 4])
temperature = st.slider("Temperature", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
top_p = st.slider("Top P", min_value=0.1, max_value=1.0, value=0.9, step=0.1)

if st.button("Generate Scouting Report"):
    scouting_report = get_scouting_report(client,  "gpt-3.5-turbo", player_boxscore,temperature, top_p, seed=seed_value)
    st.write(scouting_report)
    
