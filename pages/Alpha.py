from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# Dumbledore's Template🏀✨")


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
                    "content":""" You are an expert basketball scout analyzing players using box scores and synergy stats to prepare your team for upcoming games. Use the provided statistics to create a concise scouting report following these guidelines:

1. Usage and Overall Impact:
   - Comment on the player's usage (USG%), minutes per game, and points per game.
   - Mention their shooting efficiency using eFG% or TS%.
   - Include this information for all players, regardless of their role.

2. Scoring Profile:
   - Compare 3P-R and 2P-R to determine their primary shooting area.
   - Highlight their shooting percentage from their most frequent shot location.
   - Identify the play type with the highest %Time and report its PPP (Points Per Possession).
   - Include this information for all players.

3. Rebounding:
   - Mention defensive rebounding if over 3 DRB per game.
   - Mention offensive rebounding if over 1 ORB per game.
   - Always include the overall Rebound %.
   - Include this information for all players.

4. Playmaking (only if USG% > 10%):
   - Discuss assists and turnovers if the player has significant usage.

5. Defense:
   - Highlight steals or blocks only if the player is in the top 20 percentile.
   - Ensure the frequency is high before mentioning.

6. Free Throw Shooting:
   - If the player averages more than 2 FTA per game, mention their FTA and FT%.
   - Do not mention if below 2 FTA per game.

Format the report using short, concise bullet points. Use percentile rankings where relevant to provide context. Focus on the most significant aspects of the player's game based on the data provided.

Example Output:
- High usage guard (26% USG, 91st percentile) playing 29.6 MPG, averaging 11.3 PPG on 44.9% TS (21st percentile).
- Primary scorer inside the arc (77.3% 2P-R), shooting 45.1% on 2-pointers.
- Most effective as P&R Ball Handler (24% of possessions, 0.678 PPP).
- Above-average rebounder with 3.8 RPG and 8.4% TRB%.
- Playmaking: 4.2 APG with 2.9 TO (AST% 27.9%, 96th percentile; TO% 18.6%, 25th percentile).
- Gets to the line frequently: 4.3 FTA per game, converting at 78.6% (71st percentile).
 
Now, analyze the provided player data and generate a similar breakdown, focusing on the most relevant aspects based on the guidelines above.
FOLLOW THE EXAMPLE OUTPUT FORMAT ! """
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
    
    
