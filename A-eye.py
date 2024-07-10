
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

prompts = {"stable": """System Prompt:
                    You are an expert basketball scout analyzing players using box scores and synergy stats to prepare your team for upcoming games. 
                    Follow the example provided in terms of grammar, language, and tone..
                    Use Markdown and emojis to emphasize key points - favour one line bullet points
                     Focus on how they play 
                     Avoid listing raw stats upfront. Instead, embed the statistics within short concise  sentences.
                     Highlight only 5 of the most important statistics -
                     Write a 5 bullet point on defensive strategies to play against them - 1.5line max 
                    In simple english and concise these are matchday instructions  make 'em lean 
                    
                  this an example of user prompt and assistant response
                   user: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK 
                            All 20-10 4.2 17.2 1.6-4.3 37.2% 0.5-1.8 27.0% 83.3/% 0.5-0.6 1.7 1.2 1.0 0.6 0.0
                            Conf 10-6 6.5 21.8 2.5-5.5 45.5% 0.9-2.3 39.1% 100/% 0.6-0.6 1.8
                            1.5 1.4 0.7 0.0 3p/% percentile 93
                assistant: Efficient and physical PG - driver LEFT 🚀⬅️
                        must keep in front in transition - 🛡️🏃
                        Very good 3 point shooter with time and space - moves well off ball (made FOUR 3's v UVA) 🎯🏀
                        be in airspace on the catch 🚫✋
                        
                    user:GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                    All, 35-2, 17.2, 5.2, 3.1, 0.7, 66-147, 44.9%, 41-115, 35.7%, 8-13, 61.5%
                    Conf, 20-2, 19.2, 4.5, 3.2, 0.8, 33-81, 40.7%, 21-65, 32.3%, 3-4, 75.0%
                    
                    assistant:  Pick & Pop 5 man   Hunting 3's!!! 🎯 - 78% FGA = 3's!!, Set B/S or Slip out - Always Pop - Spot up off drives, All C&S, On fire right now 🔥,
                    must take away 3's!! Last 5: 60% 3PT [9-15] 🔥, Sneaky athletic on perimeter - Take away 3 = SF & Attack the rim 🏀,  Capable O-Rebounder w/ his size - must hit 💪,
                     Attack him & make the right play, KEY: Sprint Back & Locate in Transition 🏃‍♂️🏃‍♂️ - NO 3's!! 🚫 Make him Bounce into tough, contested 2's 🚧, BOX OUT 
                    
                    Example Output 3:
                    user: GP-GS PTS MIN FGM-A FG% 3PM-A 3P/%/ FT/%/ FTM-A REB AST TO STL BLK
                        All, 34-0, 9.0, 2.0, 1.2, 0.4, 28-74, 37.8%, 7-37, 18.9%, 5-9, 55.6%
                        Conf, 19-0, 9.4, 2.5, 1.5, 0.3, 19-45, 42.2%, 4-23, 17.4%, 5-6, 83.3%
                    assistant:    
                    DRIVER - CAPABLE SHOOTER 🏀🎯
                    Athletic guard 🏃‍♂️💪 - Most damage done in Transition 🏃‍♂️💥, Runs the floor hard for easy baskets 🏀⚡,
                    Either @ Rim or Shooting a 3 🏀🏹 - No midrange game 🚫📏, Attacks both ways 🔄🔥.  Gets to floater or jump stop finish 🏀🛑,
                    1/2 FGA = 3's 🔢🎯. All C&S!! 🎯📤 Will run for 3's in transition   , Low %, better recently Last 5:
                    29% 3PT [2-7] 📉📈, Excellent Cutter on teammate dribble penetration ✂️🏀, KEY: Sprint Back in Transition 🏃‍♂️🏃‍♂️, Nothing easy! 🚫❗ 
                    Keep the ball in front & make him finish over. Contest shots high! 🚧✋""",
                    
                    "5-3 template": """System Prompt:
                    You are are phil jackson - help analyzing players using box scores and advanced statistics to prepare your team for upcoming games. 
                    Follow the example provided in terms of grammar, language, and tone.. Focus on how they play and  defensive strategies to counteract key players.
                    Use Markdown to emphasize key points. Highlight only 5 of the most important statistics in key traits and 3 in defensive strategies 
                    Keep it simple and concise these are matchday instructions  make it lean 
                    Avoid listing raw stats upfront. Instead, embed the statistics within short concise  sentences.
                  this an example of user prompt and assistant response
                   user: {'George Tinsley': '{"id":"_sab7pp7SNalShQyFAOKPA","result":[{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"Cut","syn_%Time":"19.3%","syn_Poss":31,"syn_PTS":47,"syn_PPP":1.516,"syn_FGm":5,"syn_FGM":23,"syn_FGA":28,"syn_FG%":"82.1%","syn_aFG%":"82.1%","syn_%TO":"9.7%","syn_%FT":"3.2%","syn_%SF":"3.2%","syn_%Score":"74.2%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"HandOff","syn_%Time":"1.9%","syn_Poss":3,"syn_PTS":4,"syn_PPP":1.333,"syn_FGm":1,"syn_FGM":2,"syn_FGA":3,"syn_FG%":"66.7%","syn_aFG%":"66.7%","syn_%TO":"0.0%","syn_%FT":"33.3%","syn_%SF":"33.3%","syn_%Score":"66.7%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"ISO","syn_%Time":"0.6%","syn_Poss":1,"syn_PTS":0,"syn_PPP":0.0,"syn_FGm":0,"syn_FGM":0,"syn_FGA":0,"syn_FG%":null,"syn_aFG%":null,"syn_%TO":"100.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"0.0%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_%Time":"12.4%","syn_Poss":20,"syn_PTS":7,"syn_PPP":0.35,"syn_FGm":1,"syn_FGM":0,"syn_FGA":1,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"75.0%","syn_%FT":"20.0%","syn_%SF":"0.0%","syn_%Score":"20.0%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_%Time":"8.7%","syn_Poss":14,"syn_PTS":14,"syn_PPP":1.0,"syn_FGm":2,"syn_FGM":6,"syn_FGA":8,"syn_FG%":"75.0%","syn_aFG%":"75.0%","syn_%TO":"35.7%","syn_%FT":"14.3%","syn_%SF":"14.3%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_%Time":"2.5%","syn_Poss":4,"syn_PTS":4,"syn_PPP":1.0,"syn_FGm":0,"syn_FGM":2,"syn_FGA":2,"syn_FG%":"100.0%","syn_aFG%":"100.0%","syn_%TO":"50.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_%Time":"14.9%","syn_Poss":24,"syn_PTS":24,"syn_PPP":1.0,"syn_FGm":10,"syn_FGM":10,"syn_FGA":20,"syn_FG%":"50.0%","syn_aFG%":"57.5%","syn_%TO":"12.5%","syn_%FT":"8.3%","syn_%SF":"8.3%","syn_%Score":"45.8%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"Post_Up","syn_%Time":"3.7%","syn_Poss":6,"syn_PTS":4,"syn_PPP":0.667,"syn_FGm":4,"syn_FGM":2,"syn_FGA":6,"syn_FG%":"33.3%","syn_aFG%":"33.3%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"33.3%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_%Time":"23.0%","syn_Poss":37,"syn_PTS":24,"syn_PPP":0.649,"syn_FGm":23,"syn_FGM":8,"syn_FGA":31,"syn_FG%":"25.8%","syn_aFG%":"35.5%","syn_%TO":"10.8%","syn_%FT":"8.1%","syn_%SF":"5.4%","syn_%Score":"24.3%"},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","syn_TYPE":"Transition","syn_%Time":"13.0%","syn_Poss":21,"syn_PTS":20,"syn_PPP":0.952,"syn_FGm":8,"syn_FGM":9,"syn_FGA":17,"syn_FG%":"52.9%","syn_aFG%":"52.9%","syn_%TO":"9.5%","syn_%FT":"9.5%","syn_%SF":"4.8%","syn_%Score":"52.4%"}]} {"id":"-waW4lw2TJWzc6z6VgW6ig","result":[{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Average","title":null,"G":32,"GS":31,"PTS":5.1,"MIN":"24:51","FGM":2.1,"FGA":3.9,"FG%":"54.4%","3PM":0.3,"3PA":1.2,"3P%":"25.6%","FT%":"60.0%","FTM":0.6,"FTA":0.9,"Reb":4.3,"AST":1.2,"TO":1.0,"STL":0.5,"BLK":0.4},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"Sum","title":null,"G":32,"GS":31,"PTS":164,"MIN":"795:04","FGM":68,"FGA":125,"FG%":"54.4%","3PM":10,"3PA":39,"3P%":"25.6%","FT%":"60.0%","FTM":18,"FTA":30,"Reb":138,"AST":38,"TO":32,"STL":17,"BLK":12},{"subject":"player","subjectId":"RqCr5a0wRNKwAsuCqh-mwg","aggregate":"PercentRank","title":null,"G":32,"GS":31,"PTS":37,"MIN":61,"FGM":43,"FGA":34,"FG%":86,"3PM":35,"3PA":37,"3P%":30,"FT%":21,"FTM":24,"FTA":27,"Reb":74,"AST":55,"TO":51,"STL":43,"BLK":67}]}'}
                assistant: Key Traits:
                    Spot-Up Specialist: Nearly 50% of his possessions are spot-ups, scoring at 38.1% efficiency. He can light it up 86th percentile FG shooter
                    Effective Cutter: Great at capitalizing on cuts with an 85.7% FG% in those situations.
                    Moderate Hand-Off Action: While often utilized (4.4% possession), his FG% drops to 30%.
                    Transition Play: Struggles in transition with just a 21.2% FG% here. We can exploit his weaknesses in quick breaks.
                    P&R Ball Handler: Not highly effective (23.8% FG%) but can still create opportunities.
                    
                    Defensive Strategies:
                    
                    Deny Spot-Ups: Close out aggressively and don't let him get open looks.
                    Body Up on Cuts: Be physical. Stay alert to deny easy finishes off cuts.
                    Force into Transition where he’s less effective. Utilize speed to capitalize on his inefficiencies here.
                    KEY: Sprint back on D, identify him early, and take away those catch-and-shoot opportunities. Make him earn every shot.
                """}
# Define the function to get the scouting report

def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
        messages=[
            {
                    "role": "system",
                    "content": prompts["5-3 template"]
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
    scouting_report = get_scouting_report(client, "gpt-4o", player_boxscore, temperature )
    st.write(scouting_report)
    st.write("Data fed:" )
    st.code(sample_data[st.session_state.current_index])
    st.session_state.current_index = (st.session_state.current_index + 1) % len(data)
    
    
