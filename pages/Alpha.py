from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# PAT and JEFFERSON 🕵️🕵️‍♂️")


####################



st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha"])

################ PAGE STARTS HERE ############################## 
 

client = OpenAI(api_key=st.secrets["open_ai"])




# Define the function to get the scouting report
def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
     seed= 111,
        messages=[
            {
                    "role": "system",
                    "content":"""You are an expert basketball scout analyzing players using box scores and synergy stats. Create a concise scouting report following these strict guidelines:
FORMAT:Use ONLY bullet points, no subheadings or paragraphs.•  Follow the exact structure provided for each bullet point.• if there is a section Spot Ups use "Spot Ups" and not Spot-ups or Spot_ups in description The synergy stats are no properly spelt sometimes e.g Spot_up or PandRBallHandler make them more readable like Spot up P and R Ballhandler 
Only mention percentiles for ORB DRB and FT% . 

Player Breakdown

• [adjective] usage [Position] ([USG%] ) who plays [adjective] minutes ([MPG] mpg) scoring [PPG] PPG ([PPG] percentile) on [adjective] [TS%] TS% ([TS%] percentile) 
Adjective guide for usage:	•	85-99th percentile Extremely high usage
* 71-84th percentile = High usage
* 57-70th percentile = Above average usage
* 43rd-56th percentile = Average usage 
* 29-42nd percentile = Below average usage
* 15-28th percentile = Low usage
* 0-14th percentile = Extremely low usage

• More likely to shoot from the [outside/inside] ([2P-R or 3P-R]% [2P-R or 3P-R]) where he/she shoots a [adjective] [2P% or 3P%] [2P% or 3P%]
• Most commonly used in synergy play type with highest % Time,  where he/she produces [PPP] PPP phrase it like   (Never mention Miscellaneous Play type) 
* Transition = Gets most of [his/her] shots in transition [% Time], where [he/she] produces [PPP]
* Post-Up = Gets most of [his/her] shots in the post [% Time], where [he/she] produces [PPP]
* Cut = Gets most of [his/her] shots cutting off the ball [% Time], where [he/she] produces [PPP]
* Spot Up = Gets most of [his/her] shots as a spot-up shooter [% Time], where [he/she] produces [PPP]
* P&R Ball Handler = Gets most of [his/her] shots as a ball-handler in the pick & roll [% Time] where [he/she] produces [PPP]
* Miscellaneous Plays = use the second most common play type by % Time if this play type represents the player’s highest % Time
* Isolation = Gets most of [his/her] shots in isolation [% Time], where [he/she] produces [PPP]
* P&R Roll Man = Gets most of [his/her] shots as a the roll man in the pick & roll [% Time] where [he/she] produces [PPP]
* Off Screen = Gets most of [his/her] shots coming around off-ball screens [% Time], where [he/she] produces [PPP]
* Offensive Rebounds (Put Backs) = Gets most of [his/her] shots from put backs on the offensive glass [% Time], where [he/she] produces [PPP]
* Handoffs = Gets most of [his/her] shots in off handoffs [% Time], where [he/she] produces [PPP]

Add an additional bullet point for the Synergy Play Type with the second highest % Time using the following format:
	•	Transition: Also frequently gets shots in transition ([% Time]), producing [PPP].
	•	Post-Up: Often gets shots in the post ([% Time]), producing [PPP].
	•	Cut: Frequently gets shots cutting off the ball ([% Time]), producing [PPP].
	•	Spot Up: Often gets shots as a spot-up shooter ([% Time]), producing [PPP].
	•	P&R Ball Handler: Frequently gets shots as a ball-handler in the pick & roll ([% Time]), producing [PPP].
	•	Isolation: Often gets shots in isolation ([% Time]), producing [PPP].
	•	P&R Roll Man: Frequently gets shots as the roll man in the pick & roll ([% Time]), producing [PPP].
	•	Off Screen: Often gets shots coming around off-ball screens ([% Time]), producing [PPP].
	•	Offensive Rebounds (Put Backs): Frequently gets shots from put backs on the offensive glass ([% Time]), producing [PPP].
	•	Handoffs: Often gets shots in off handoffs ([% Time]), producing [PPP].
• [adjective] rebounding [Position] especially on [Defense/Offense] averaging [ORB/G or DRB/G] ([DRB or ORB] percentile)  (Include DRB/G if > 3, ORB/G if > 1. Always mention ORB% and DRB%)
• [adjective] facilitator who averages [APG] APG ([APG] percentile) with a [AST%] AST% ([AST%] percentile) and turns it over [adjective] with [TO/G] TO/G ([TO/G] percentile)  (Only include if USG% > 10%)
• [adjective] defensively, averaging [STL/G or BLK/G] [STL/G or BLK/G]  (Only include if STL/G or BLK/G is in 80th percentile or above)
• [adjective] free throw shooter at [FT%] ([FT%] percentile) who gets to the line [adverb] at [FT-R] FT-R  (Only include if player averages more than 2 FTA per game e.g 14% FT-R)
Analyze the provided player data and generate a breakdown strictly adhering to this format. Include only the relevant bullet points based on the player's stats and the given criteria.​​​​​​"""
      
            },
            {
                "role": "user",
                "content": player_boxscore
            },
            
        ],
    )

    return chat_completion.choices[0].message.content


temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=2.0, value=0.7, step=0.1)


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
    
    
