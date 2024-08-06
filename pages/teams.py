
from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# teams 🕵️-🕵️‍♂️")

 

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
                    "content":""" Team Analysis
## Offense
* [TEAM NAME] averages [PPG] [PPG League Rank] with [adjective - efficient/inefficient] [ORTG] [ORTG League Rank]
  * Example:
    * Illinois averages 83.4 PPG (9th) with an extremely efficient 120.7 ORTG (7th).
* They play [adjective - faster/slower] than the average team with [POSSESSIONS PER GAME] possessions per game [POSSESSIONS PER GAME League Rank]
  * Example:
    * They play faster than the average team with 70.7 possessions per game (98th rank).
* The [TEAM NICKNAME] take more [2’s/3’s] compared to [3’s/2’s] with a [2P-R/3P-R] [total 2's/3's] and a [2P-R/3P-R] [total 3's/2's] . They are [adjective] inside the arc with a [2P%] [2P% attmempted]. [Adjective] from 3-point territory with a [3P%] [3P% attempted]
  * Figure out which is higher, 2P-R or 3P-R and mention that stat first, indicating they take more of one type of shot
  * Example:
    * The Fighting Illini take more 2’s compared to 3’s with a 61.4% 2P-R (218) and a 38.6% 3P-R (145). They are extremely efficient inside the arc with a 54.4% 2P% (44). Slightly better than average from beyond 3 with a 34.9% 3P% (126).
* Most of their possessions end in [Synergy Play Type with most % Time] where they score at a rate of [Synergy Play Type PPP] -- add % time context to each stat on this line
  * Example:
    * Most of their possessions end in spot up attempts where they are just a bit better than average with a 0.970 PPP (26.3% of time). 
*[TEAM NAME] is a [adjective] rebounding on the offensive glass team, averaging [Team ORG/G] [Team ORB/G League Rank] and allowing opponents an average of [Opponent DRB/G] [Opponent DRB/G League Rank]
  *Example:
   *Illinois is an elite rebounding team on the offensive glass, averaging 12.8 OR/G (29th) and allowing opponents an average of 23.1 DR/G (59th)
* They are [very/not very] reliant on assists to score with a [Team AST%] [Team AST% League Rank] and do a [adjective] job of taking care of the basketball, turning it over [AST/Game] [AST/Game League Rank]
  * Example:
    * They are not very reliant on an assist to score with only a 45.8% AST% (296th) but do a good job of taking care of the basketball only turning it over 10.6x per game (72nd).
* They do a [adjective] job of getting to the foul line with a [FT-R] [FT-R League Rank] and knock down [FT%] of those attempts [FT% League Rank]
  * Example:
    * Do a good job of getting to the foul line witha 37.1% FT-R (68) and knock down 73.6% of those attempts (103).
## Defense
* The [TEAM NICKNAME] give up [Opponent PPG] [Opponent PPG League Rank] with an average [DRTG] [DRTG League Rank]
  * Example:
    * The Illini give up 73.3 ppg (226) with an average 106.2 DRTG (181)
* Their defense does a [adjective] job of limiting opponents to a [adjective] [2P-R or 3P-R, whichever is lowest]. Their opponents convert [Opponent 2P%] of their 2s [Opponent 2P% total] and [Opponent 3P%] of their 3s [Opponent 3P% total] 
  * Example:
    * Their defense does a great job of limiting teams to a very low 28.3% 3P-R (7th) and forcing teams to take a lot of 2s with a 71.7% 2P-R. Their opponents convert 46.8% of their 2P% (43) and 34.1% of their 3P% (215).
* [TEAM NAME] is a [adjective] defensive rebounding team, grabbing [DRB/G] [DRB/G League Rank] and allowing opponents to grab [Opponent DRB/G] [Opponent DRB/G League Rank]
  * Example:
    * Illinois is an elite defensive rebounding team, grabbing 28.1 DRB/G (16th) and allowing opponents to grab 10.0 ORB/G (166th)
* They [force, hold = good, allow = bad] opponents into a [Opponent AST%] [Opponent AST% League Rank] and force turnovers at a [Opponent TO%] [Opponent TO% League Rank]
  * Example:
    * They force opponents into a 44.1% AST% (37) but rarely force any turnovers with a 12.3% TO% (360).
* Do a [adjective] job of keeping opponents off the foul line with a [Opponent FT-R] [Opponent FT-R League Rank]
  * Example:
    * Do a very good job of keeping opponents off the foul line with a 26.7% FT-R (41).
* [TEAM NAME] does a [adjective] job of not fouling averaging [PF per game] [PF per game League Rank]
  * Example:
    * Illinois does a good job of not fouling averaging on 15.2 fouls per game (317).
---
Full Example for Illinois Men
## Offense
* Illinois averages 83.4 ppg (9th) with an extremely efficient 120.7 ORTG (7th).
* They play faster than the average team with 70.7 possessions per game (98th rank).
* The Fighting Illini take more 2’s compared to 3’s with a 61.4% 2P-R (218) and a 38.6% 3P-R (145). They are extremely efficient inside the arc with a 54.4% 2P% (44). Slightly better than average from beyond 3 with a 34.9% 3P% (126).
* Most of their possessions end in spot up attempts where they are just a bit better than average with a 0.970 PPP (26.3% of time). They really excel in transition (1.167 PPP and 17.9% time) and P&R Ball Handler (0.993 PPP and 12% of the time).
* Illinois is an elite rebounding team with a 35.6% ORB% (21st) and a 73.7% DRB (74th).
* They are not very reliant on an assist to score with only a 45.8% AST% (296th) but do a good job of taking care of the basketball only turning it over 10.6x per game (72nd).
* Do a good job of getting to the foul line with a 37.1% FT-R (68) and knock down 73.6% of those attempts (103).
## Defense
* The Illini give up 73.3 ppg (226) with an average 106.2 DRTG (181).
* Their defense does a great job of limiting teams to a very low 28.3% 3P-R (7th) and forcing teams to take a lot of 2s with a 71.7% 2P-R. Their opponents convert 46.8% of their 2P% (43) and 34.1% of their 3P% (215).
* Illinois is an elite rebounding team holding their opponents to a low 26.3% ORB (74) and 64.4% DRB (21).
* They force opponents into a 44.1% AST% (37) but rarely force any turnovers with a 12.3% TO% (360).
* Do a very good job of keeping opponents off the foul line with a 26.7% FT-R (41).
* Illinois does a good job of not fouling averaging on 15.2 fouls per game (317).
 """
      
            },
            {
                "role": "user",
                "content": player_boxscore
            },
            
        ],
    )

    return chat_completion.choices[0].message.content


temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=2.0, value=0.9,step=0.1)


if st.button("Generate Scouting Report from input"):
    scouting_report = get_scouting_report(client,  "gpt-4o", player_boxscore,temperature)
    st.write(scouting_report)
    

# Sample data
import json
with open("teams.json", "r") as f:
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
    scouting_report
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    
    
