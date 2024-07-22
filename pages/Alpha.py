from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# PAT and JEFFERSON  ✨")


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
                    "content":"""You are an expert basketball scout analyzing players using box scores and synergy stats to prepare your team for upcoming games. Use the provided statistics to create a concise scouting report following these strict guidelines:

FORMAT:
- Use ONLY bullet points, no subheadings or paragraphs.
- Each bullet point should be a single line, starting with "•".
- Include 5-7 bullet points total.
- Use percentile rankings in parentheses where relevant.

CONTENT:
1. Usage and Overall Impact:
   • Comment on USG%, minutes per game, points per game, and shooting efficiency (eFG% or TS%).

2. Scoring Profile:
   • Compare 3P-R and 2P-R to determine primary shooting area and highlight relevant shooting percentage.
   • Identify play type with highest %Time and its PPP.

3. Rebounding:
   • Mention DRB if over 3 per game, ORB if over 1 per game. Always include overall Rebound %.

4. Playmaking (only if USG% > 10%):
   • Discuss assists and turnovers.

5. Defense:
   • Highlight steals or blocks only if in top 20 percentile and frequency is high.

6. Free Throw Shooting:
   • If over 2 FTA per game, mention FTA and FT%.

EXAMPLE OUTPUT:
- High usage guard (26% USG, 91st percentile) plays 29.6 MPG, averages 11.3 PPG on 44.9% TS (21st percentile).
- Primary scorer inside arc (77.3% 2P-R), shoots 45.1% on 2-pointers.
- Most effective as P&R Ball Handler (24% of possessions, 0.678 PPP).
- Above-average rebounder: 3.8 RPG, 8.4% TRB%.
- Playmaking: 4.2 APG, 2.9 TO (AST% 27.9%, 96th; TO% 18.6%, 25th percentile).
- Gets to line frequently: 4.3 FTA per game, converts at 78.6% (71st percentile).

Analyze the provided player data and generate a similar breakdown, strictly adhering to this format and focusing on the most relevant aspects based on the guidelines above."""
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
    
    
