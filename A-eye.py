
from openai import OpenAI
import json
import streamlit as st
import os 

st.markdown('## Current Branch')
st.sidebar.markdown('This is the Current Branch')

     
    
     
st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha", "Plain Jane", "Money Ranger"])

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
                     mention at least 1 statistic that supports any statement being made
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
                    Use Markdown to emphasize key points. Highlight only 5 of the most important statistics in key traits and 3 in defensive strategies  mention at least 1 statistic that supports any statement being made
                     
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
                    Deny Spot-Ups 1.22PPP : Close out aggressively and don't let him get open looks.
                    Body Up on Cuts: 28% of moves  Be physical. Stay alert to deny easy finishes off cuts.
                    Force into Transition where he’s less effective 0.13 PPP 30% of moves  
                    
                    user:{"id":"KOo87rV6Q7GOVfTunQnq_g","result":[{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Average","title":null,"G":29,"GS":28,"PTS":11.3,"MIN":"29:37","FGM":3.7,"FGA":10.5,"FG%":"34.9%","3PM":0.6,"3PA":2.4,"3P%":"23.2%","FT%":"78.6%","FTM":3.4,"FTA":4.3,"Reb":3.8,"AST":4.2,"TO":2.9,"STL":1.1,"BLK":0.1,"PPP":0.73,"A/TO":1.48,"%TO":null,"AST%":"27.9%","%SF":null,"TO%":"18.6%","STL%":"2.2%","BLK%":"0.3%","%3P":"22.7%"," /-":null,"Usg%":"26.3%","TS%":"44.9%","eFG%":"37.5%","DR%":"12.2%","OR%":"3.7%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","title":null,"G":29,"GS":28,"PTS":327,"MIN":"858:44","FGM":106,"FGA":304,"FG%":"34.9%","3PM":16,"3PA":69,"3P%":"23.2%","FT%":"78.6%","FTM":99,"FTA":126,"Reb":110,"AST":123,"TO":83,"STL":32,"BLK":2,"PPP":0.73,"A/TO":1.48,"%TO":null,"AST%":"27.9%","%SF":null,"TO%":"18.6%","STL%":"2.2%","BLK%":"0.3%","%3P":"22.7%"," /-":null,"Usg%":"26.3%","TS%":"44.9%","eFG%":"37.5%","DR%":"12.2%","OR%":"3.7%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"PercentRank","title":null,"G":29,"GS":28,"PTS":82,"MIN":85,"FGM":78,"FGA":89,"FG%":21,"3PM":60,"3PA":68,"3P%":35,"FT%":75,"FTM":94,"FTA":94,"Reb":73,"AST":97,"TO":1,"STL":87,"BLK":33,"PPP":21,"A/TO":77,"%TO":null,"AST%":96,"%SF":null,"TO%":25,"STL%":70,"BLK%":28,"%3P":32," /-":null,"Usg%":90,"TS%":21,"eFG%":15,"DR%":48,"OR%":46}]} {"id":"7u7K2labRvKw-E6qEKsLEA","result":[{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Cut","syn_Poss":13,"syn_PTS":20,"syn_PPP":1.538,"syn_FGm":3,"syn_FGM":8,"syn_FGA":11,"syn_FG%":"72.7%","syn_aFG%":"72.7%","syn_%TO":"0.0%","syn_%FT":"15.4%","syn_%SF":"7.7%","syn_%Score":"76.9%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"HandOff","syn_Poss":22,"syn_PTS":23,"syn_PPP":1.045,"syn_FGm":10,"syn_FGM":8,"syn_FGA":18,"syn_FG%":"44.4%","syn_aFG%":"44.4%","syn_%TO":"4.5%","syn_%FT":"18.2%","syn_%SF":"18.2%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"ISO","syn_Poss":61,"syn_PTS":40,"syn_PPP":0.656,"syn_FGm":31,"syn_FGM":9,"syn_FGA":40,"syn_FG%":"22.5%","syn_aFG%":"23.8%","syn_%TO":"14.8%","syn_%FT":"24.6%","syn_%SF":"21.3%","syn_%Score":"34.4%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_Poss":33,"syn_PTS":11,"syn_PPP":0.333,"syn_FGm":10,"syn_FGM":0,"syn_FGA":10,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"48.5%","syn_%FT":"21.2%","syn_%SF":"0.0%","syn_%Score":"21.2%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_Poss":8,"syn_PTS":14,"syn_PPP":1.75,"syn_FGm":1,"syn_FGM":6,"syn_FGA":7,"syn_FG%":"85.7%","syn_aFG%":"85.7%","syn_%TO":"0.0%","syn_%FT":"25.0%","syn_%SF":"25.0%","syn_%Score":"87.5%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"OffScreen","syn_Poss":2,"syn_PTS":2,"syn_PPP":1.0,"syn_FGm":0,"syn_FGM":1,"syn_FGA":1,"syn_FG%":"100.0%","syn_aFG%":"100.0%","syn_%TO":"50.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_Poss":127,"syn_PTS":63,"syn_PPP":0.496,"syn_FGm":69,"syn_FGM":21,"syn_FGA":90,"syn_FG%":"23.3%","syn_aFG%":"23.9%","syn_%TO":"18.9%","syn_%FT":"11.8%","syn_%SF":"7.9%","syn_%Score":"25.2%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Post_Up","syn_Poss":1,"syn_PTS":0,"syn_PPP":0.0,"syn_FGm":1,"syn_FGM":0,"syn_FGA":1,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"0.0%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_Poss":60,"syn_PTS":43,"syn_PPP":0.717,"syn_FGm":33,"syn_FGM":16,"syn_FGA":49,"syn_FG%":"32.7%","syn_aFG%":"42.9%","syn_%TO":"16.7%","syn_%FT":"3.3%","syn_%SF":"3.3%","syn_%Score":"28.3%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Transition","syn_Poss":74,"syn_PTS":59,"syn_PPP":0.797,"syn_FGm":25,"syn_FGM":20,"syn_FGA":45,"syn_FG%":"44.4%","syn_aFG%":"45.6%","syn_%TO":"24.3%","syn_%FT":"16.2%","syn_%SF":"10.8%","syn_%Score":"39.2%"}]}
                    assistant: Key traits:
                    High usage guard (26.3% USG, 91st percentile) who plays significant minutes (29.6 MPG) averaging 11.3 PPG on 34.9% FG (10th percentile).
                    Effective passer with an AST% of 27.9% (97th percentile) and 4.8 assists per game (92nd percentile).
                    Strong at drawing fouls, averaging 4.3 FTA per game (92nd percentile), converting 78.6% of them (71st percentile).
                    Frequently involved as a pick and roll ball handler (31.1% of the time) but only producing 0.521 PPP.
                    Ineffective in transition, producing 0.814 PPP.
                    Defensive strategies:
                    Pressure him on the ball, exploiting his 18.6% TO% (21st percentile).
                    Sag off him on the perimeter as his shooting percentage is low (34.9% FG, 10th percentile).
                    Be prepared for his drives and how he draws fouls, as he averages 4.3 FTA per game (92nd percentile) and converts them at a 78.6% rate (71st percentile).
                    
                    user:{"id":"eQDOScAxRq2CRjmCjB1noA","result":[{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Average","title":null,"G":75,"GS":75,"PTS":14.7,"MIN":"30:05","FGM":5.4,"FGA":10.7,"FG%":"50.6%","3PM":1.2,"3PA":3.1,"3P%":"37.4%","FT%":"74.0%","FTM":2.7,"FTA":3.6,"Reb":7.2,"AST":3.8,"TO":2.1,"STL":0.8,"BLK":0.5,"PPP":1.02,"A/TO":1.79,"%TO":null,"AST%":"17.7%","%SF":null,"TO%":"14.8%","STL%":"1.2%","BLK%":"1.3%","%3P":"29.3%"," /-":null,"Usg%":"20.3%","TS%":"59.7%","eFG%":"56.0%","DR%":"21.9%","OR%":"3.9%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","title":null,"G":75,"GS":75,"PTS":1102,"MIN":"2256:38","FGM":406,"FGA":803,"FG%":"50.6%","3PM":88,"3PA":235,"3P%":"37.4%","FT%":"74.0%","FTM":202,"FTA":273,"Reb":540,"AST":286,"TO":160,"STL":60,"BLK":36,"PPP":1.02,"A/TO":1.79,"%TO":null,"AST%":"17.7%","%SF":null,"TO%":"14.8%","STL%":"1.2%","BLK%":"1.3%","%3P":"29.3%"," /-":null,"Usg%":"20.3%","TS%":"59.7%","eFG%":"56.0%","DR%":"21.9%","OR%":"3.9%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"PercentRank","title":null,"G":75,"GS":75,"PTS":82,"MIN":83,"FGM":82,"FGA":80,"FG%":76,"3PM":66,"3PA":65,"3P%":69,"FT%":40,"FTM":87,"FTA":89,"Reb":92,"AST":84,"TO":9,"STL":70,"BLK":69,"PPP":56,"A/TO":48,"%TO":null,"AST%":72,"%SF":null,"TO%":21,"STL%":37,"BLK%":43,"%3P":28," /-":null,"Usg%":69,"TS%":71,"eFG%":64,"DR%":86,"OR%":49}]} {"id":"yI8rImKjQVCYqb9tnOZBzg","result":[{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Cut","syn_Poss":83,"syn_PTS":102,"syn_PPP":1.229,"syn_FGm":29,"syn_FGM":41,"syn_FGA":70,"syn_FG%":"58.6%","syn_aFG%":"58.6%","syn_%TO":"3.6%","syn_%FT":"21.7%","syn_%SF":"21.7%","syn_%Score":"61.4%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"HandOff","syn_Poss":38,"syn_PTS":37,"syn_PPP":0.974,"syn_FGm":15,"syn_FGM":12,"syn_FGA":27,"syn_FG%":"44.4%","syn_aFG%":"53.7%","syn_%TO":"18.4%","syn_%FT":"13.2%","syn_%SF":"10.5%","syn_%Score":"42.1%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"ISO","syn_Poss":82,"syn_PTS":77,"syn_PPP":0.939,"syn_FGm":41,"syn_FGM":24,"syn_FGA":65,"syn_FG%":"36.9%","syn_aFG%":"40.0%","syn_%TO":"4.9%","syn_%FT":"20.7%","syn_%SF":"18.3%","syn_%Score":"43.9%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_Poss":45,"syn_PTS":20,"syn_PPP":0.444,"syn_FGm":9,"syn_FGM":7,"syn_FGA":16,"syn_FG%":"43.8%","syn_aFG%":"46.9%","syn_%TO":"55.6%","syn_%FT":"8.9%","syn_%SF":"0.0%","syn_%Score":"22.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_Poss":56,"syn_PTS":52,"syn_PPP":0.929,"syn_FGm":26,"syn_FGM":23,"syn_FGA":49,"syn_FG%":"46.9%","syn_aFG%":"46.9%","syn_%TO":"7.1%","syn_%FT":"10.7%","syn_%SF":"8.9%","syn_%Score":"44.6%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"OffScreen","syn_Poss":16,"syn_PTS":21,"syn_PPP":1.312,"syn_FGm":3,"syn_FGM":8,"syn_FGA":11,"syn_FG%":"72.7%","syn_aFG%":"86.4%","syn_%TO":"25.0%","syn_%FT":"6.2%","syn_%SF":"6.2%","syn_%Score":"56.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_Poss":170,"syn_PTS":138,"syn_PPP":0.812,"syn_FGm":61,"syn_FGM":53,"syn_FGA":114,"syn_FG%":"46.5%","syn_aFG%":"51.3%","syn_%TO":"24.1%","syn_%FT":"11.8%","syn_%SF":"9.4%","syn_%Score":"38.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_Poss":29,"syn_PTS":34,"syn_PPP":1.172,"syn_FGm":13,"syn_FGM":15,"syn_FGA":28,"syn_FG%":"53.6%","syn_aFG%":"60.7%","syn_%TO":"3.4%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"51.7%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Post_Up","syn_Poss":37,"syn_PTS":30,"syn_PPP":0.811,"syn_FGm":14,"syn_FGM":13,"syn_FGA":27,"syn_FG%":"48.1%","syn_aFG%":"48.1%","syn_%TO":"18.9%","syn_%FT":"13.5%","syn_%SF":"13.5%","syn_%Score":"43.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_Poss":263,"syn_PTS":300,"syn_PPP":1.141,"syn_FGm":119,"syn_FGM":110,"syn_FGA":229,"syn_FG%":"48.0%","syn_aFG%":"58.1%","syn_%TO":"6.5%","syn_%FT":"9.9%","syn_%SF":"9.9%","syn_%Score":"48.3%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Transition","syn_Poss":253,"syn_PTS":289,"syn_PPP":1.142,"syn_FGm":65,"syn_FGM":100,"syn_FGA":165,"syn_FG%":"60.6%","syn_aFG%":"64.8%","syn_%TO":"17.4%","syn_%FT":"22.5%","syn_%SF":"20.9%","syn_%Score":"54.9%"}]}
                    assistant: Key Traits
                    Versatile forward with a balanced game, plays significant minutes (30.1 MPG, 79th percentile), and averages 14.7 PPG (79th percentile).
                    Efficient scorer with a 56.0% EFG% (61st percentile) and excels inside the arc with a 70.7% 2P-R (72nd percentile).
                    Strong rebounder, pulling down 7.2 REB per game (91st percentile) and a 21.9% DRB% (86th percentile).
                    Effective in spot-up situations, scoring 1.153 PPP.
                    Struggles with ball security, committing 2.1 TOs per game (11th percentile) and has a 14.8% TO% (19th percentile).
                    Defensive Strategies:
                    Focus on closing out on his spot-up opportunities as he scores 1.153 PPP.
                    Apply pressure to force turnovers; he commits 2.1 TOs per game (11th percentile) and has a 14.8% TO% (19th percentile).
                    Box out aggressively to limit his impact on the boards, as he averages 7.2 REB per game (91st percentile) and has a 21.9% DRB% (86th percentile).
                """}
# Define the function to get the scouting report

def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
         seed=111,
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
    
    
