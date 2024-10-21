
from openai import OpenAI
import json
import streamlit as st
import os 


st.sidebar.markdown('Soccer ***_****')

     
     


st.title("Eyes on the ball ")
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
                    "content":"""You are an insightful soccer scout -- given a set of stats you are to help give our team the edge when playing them next, focus on being descriptive and incisive here are some good examples
INPUT-  {
  "players": [
    {
      "number": "21",
      "name": "Matthew Roou",
      "position": "F",
      "stats": {
        "gamesPlayed": 13,
        "gamesStarted": 12,
        "minutesPlayed": 984,
        "goals": 12,
        "assists": 0,
        "points": 24,
        "shots": 45,
        "shotPercentage": 26.7,
        "shotsOnGoal": 24,
        "sogPercentage": 53.3,
        "yellowCards": 0,
        "redCards": 0,
        "foulsCommitted": 12,
        "foulsSuffered": 13,
        "pkaAttempted": 3,
        "pkaGoals": 3,
        "gameWinningGoals": 3,
        "goalsLeft": 1,
        "goalsRight": 7,
        "goalsHeader": 1
      }
    },
    {
      "number": "13",
      "name": "Bryce Boneau",
      "position": "M",
      "stats": {
        "gamesPlayed": 13,
        "gamesStarted": 13,
        "minutesPlayed": 1037,
        "goals": 1,
        "assists": 7,
        "points": 9,
        "shots": 10,
        "shotPercentage": 10.0,
        "shotsOnGoal": 5,
        "sogPercentage": 50.0,
        "yellowCards": 2,
        "redCards": 0,
        "foulsCommitted": 14,
        "foulsSuffered": 13,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "11",
      "name": "Jack Flanagan",
      "position": "F",
      "stats": {
        "gamesPlayed": 13,
        "gamesStarted": 12,
        "minutesPlayed": 791,
        "goals": 3,
        "assists": 1,
        "points": 7,
        "shots": 16,
        "shotPercentage": 18.8,
        "shotsOnGoal": 6,
        "sogPercentage": 37.5,
        "yellowCards": 0,
        "redCards": 0,
        "foulsCommitted": 14,
        "foulsSuffered": 8,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 3,
        "goalsHeader": 0
      }
    },
    {
      "number": "10",
      "name": "KK Baffour",
      "position": "M",
      "stats": {
        "gamesPlayed": 13,
        "gamesStarted": 13,
        "minutesPlayed": 990,
        "goals": 1,
        "assists": 4,
        "points": 6,
        "shots": 31,
        "shotPercentage": 3.2,
        "shotsOnGoal": 13,
        "sogPercentage": 41.9,
        "yellowCards": 3,
        "redCards": 0,
        "foulsCommitted": 14,
        "foulsSuffered": 27,
        "pkaAttempted": 1,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "22",
      "name": "Nolan Spicer",
      "position": "M",
      "stats": {
        "gamesPlayed": 13,
        "gamesStarted": 10,
        "minutesPlayed": 791,
        "goals": 2,
        "assists": 1,
        "points": 5,
        "shots": 14,
        "shotPercentage": 14.3,
        "shotsOnGoal": 8,
        "sogPercentage": 57.1,
        "yellowCards": 0,
        "redCards": 0,
        "foulsCommitted": 1,
        "foulsSuffered": 20,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 2,
        "goalsRight": 0,
        "goalsHeader": 0
      }
    },
    {
      "number": "5",
      "name": "Kyle Genenbacher",
      "position": "D",
      "stats": {
        "gamesPlayed": 13,
        "gamesStarted": 13,
        "minutesPlayed": 1117,
        "goals": 2,
        "assists": 1,
        "points": 5,
        "shots": 7,
        "shotPercentage": 28.6,
        "shotsOnGoal": 3,
        "sogPercentage": 42.9,
        "yellowCards": 3,
        "redCards": 0,
        "foulsCommitted": 5,
        "foulsSuffered": 6,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 0,
        "goalsHeader": 2
      }
    },
    {
      "number": "15",
      "name": "Ian Shaul",
      "position": "M",
      "stats": {
        "gamesPlayed": 12,
        "gamesStarted": 5,
        "minutesPlayed": 550,
        "goals": 1,
        "assists": 2,
        "points": 4,
        "shots": 9,
        "shotPercentage": 11.1,
        "shotsOnGoal": 3,
        "sogPercentage": 33.3,
        "yellowCards": 1,
        "redCards": 0,
        "foulsCommitted": 4,
        "foulsSuffered": 5,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 1,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "2",
      "name": "Mitch Ferguson",
      "position": "D",
      "stats": {
        "gamesPlayed": 12,
        "gamesStarted": 12,
        "minutesPlayed": 1031,
        "goals": 1,
        "assists": 2,
        "points": 4,
        "shots": 8,
        "shotPercentage": 12.5,
        "shotsOnGoal": 3,
        "sogPercentage": 37.5,
        "yellowCards": 1,
        "redCards": 0,
        "foulsCommitted": 0,
        "foulsSuffered": 6,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "23",
      "name": "Stevie Dunphy",
      "position": "F",
      "stats": {
        "gamesPlayed": 11,
        "gamesStarted": 0,
        "minutesPlayed": 164,
        "goals": 1,
        "assists": 0,
        "points": 2,
        "shots": 4,
        "shotPercentage": 25.0,
        "shotsOnGoal": 1,
        "sogPercentage": 25.0,
        "yellowCards": 0,
        "redCards": 0,
        "foulsCommitted": 6,
        "foulsSuffered": 2,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "8",
      "name": "Nico Bartlett",
      "position": "M",
      "stats": {
        "gamesPlayed": 3,
        "gamesStarted": 0,
        "minutesPlayed": 47,
        "goals": 1,
        "assists": 0,
        "points": 2,
        "shots": 1,
        "shotPercentage": 100.0,
        "shotsOnGoal": 1,
        "sogPercentage": 100.0,
        "yellowCards": 0,
        "redCards": 0,
        "foulsCommitted": 2,
        "foulsSuffered": 1,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "16",
      "name": "Jacob Bartlett",
      "position": "M",
      "stats": {
        "gamesPlayed": 12,
        "gamesStarted": 6,
        "minutesPlayed": 788,
        "goals": 1,
        "assists": 0,
        "points": 2,
        "shots": 9,
        "shotPercentage": 11.1,
        "shotsOnGoal": 2,
        "sogPercentage": 22.2,
        "yellowCards": 2,
        "redCards": 0,
        "foulsCommitted": 12,
        "foulsSuffered": 12,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 1,
        "goalsLeft": 0,
        "goalsRight": 1,
        "goalsHeader": 0
      }
    },
    {
      "number": "7",
      "name": "Nate Zimmermann",
      "position": "F",
      "stats": {
        "gamesPlayed": 2,
        "gamesStarted": 0,
        "minutesPlayed": 46,
        "goals": 0,
        "assists": 1,
        "points": 1,
        "shots": 1,
        "shotPercentage": 0.0,
        "shotsOnGoal": 0,
        "sogPercentage": 0.0,
        "yellowCards": 0,
        "redCards": 0,
        "foulsCommitted": 0,
        "foulsSuffered": 0,
        "pkaAttempted": 0,
        "pkaGoals": 0,
        "gameWinningGoals": 0,
        "goalsLeft": 0,
        "goalsRight": 0,
        "goalsHeader": 0
      }
    },
    
OUTPUT 

**Mathew Roou 5'10  F**- is an elite finisher with 12 games in 12 games and an elite 30% conversion rate from 40 shots. he gets fouled often and is the designated PK taker he has scored 3 out of 3 from the penalty spot. Force out wide don't allow him to shoot

**Bryce M** -  Is the creative hub of the team, supplying 7 assists in 12 games. He gets fouled often but also puts in a shift for the team fouling 13 times to his 12 fouls received . He averages one shot a game. Cover passing lanes and angles.

**Kyle Genebacher D** -  Solid CB who has played all minutes this season. Solid in the air in either box. Scoring two headed goals and providing an assist. Be aware of him on corners and set pieces. 

**Jack Flannagan F**- 3 goals and 1 assist and has the third most shots in the team and most points .Started 11 out of 12 playing 714 of 1024 available minutes. 

**Nolan Spicer M**  -- with 2 goals and 1 assists. He is difficult to get off the ball cleanly and has been fouled 18 times - 2nd highest on the team. 

**KK Bafour M**  - High offensive output and likes to get involved. Shoots often with 28 shots (2nd highest on team) scoring only once but his 42.9% shots on target rate suggests he could score more. He is second highest assister with 4 assists, he likes to get involved with 3 cards in 12 games he's started. 

**Dunphy F** 10 substitute appearances for a combined 150 minutes , as a forward. Scoring 1 goal and providing 2 assists in that limited time frame. Watch out when he comes on.

**Mitch Fergusson D**  who likes two go forward. With 2 assists to show for it nad he's been fouled 5 times and does let loose the occasional shot 4 in 11 starts. 
                    

reply in JSON """
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
sample_data = data
sample_data =str(sample_data)

def generate_scouting_report(data):
    
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature)
    st.write(scouting_report)
    

if st.button("Use Sample Data to Generate"):
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    else:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    player_boxscore = str(sample_data)
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature )
    st.write(scouting_report)
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    
    
