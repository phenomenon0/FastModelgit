from openai import OpenAI
import json
import streamlit as st
import os 


st.markdown("# Fire Template🏀✨")


####################



st.sidebar.selectbox("Select a page", ["Current", "Beta", "Alpha","Money Ranger"])

################ PAGE STARTS HERE ############################## 
 

client = OpenAI(api_key=st.secrets["open_ai"])


# Define the list of questions
questions = [
    "What is the player's standout characteristics?",
    "How to play against him?",
    "player notes?",
   
]


# Define the function to get the scouting report

def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
        messages=[
            {
                    "role": "system",
                    "content": """System Prompt:
                    
                    You are an expert basketball scout analyzing players using box scores and synergy stats to prepare your team for upcoming games. 

                    Follow these guidelines:
                    1. Use Markdown to emphasize key points.
                    2. Present information in concise bullet points.
                    3. Focus on how the player performs rather than listing raw stats.
                    4. Embed statistics within short, concise sentences.
                    5. Highlight only the 5-6 most important statistics.
                    6. Include percentile ranks in parentheses (e.g., 90th percentile) for boxscore stats. NB: Synergy doesnt have percentile dont fake it
                    7. Write 3 bullet points on defensive strategies to play against them, with a maximum of 1.5 lines each.
                    8. Maintain the overall tone and structure of the examples provided.

                    Player Breakdown Format:
                    - Start with a brief overview of the player's role and efficiency.
                    - Highlight their strengths and unique attributes.
                    - Mention their most effective play types and situations.
                    - Point out any significant weaknesses or areas to exploit.

                    How to Defend Format:
                    - Provide 3 concise, actionable defensive strategies.
                    - Focus on limiting the player's strengths and exploiting weaknesses.
                    - Consider both individual and team defensive approaches.

                    Additional Notes:
                    - Use precise language and avoid unnecessary elaboration.
                    - Ensure all percentages are accurately represented (e.g., 3P% vs 3P-R).
                    - Pay attention to both offensive and defensive statistics when relevant.
                    - Adapt the analysis based on the player's position and role.

                    Remember to stick to the format in the examples, including percentiles in brackets and maintaining the overall tone and structure of the response.
                    
                    
                    
                    user: {"id":"nqWa0YjETNiR8gDpN4zBEQ","result":[{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Cut","syn_%Time":"24.9%","syn_Poss":66,"syn_PTS":72,"syn_PPP":1.091,"syn_FGm":24,"syn_FGM":33,"syn_FGA":57,"syn_FG%":"57.9%","syn_aFG%":"57.9%","syn_%TO":"9.1%","syn_%FT":"9.1%","syn_%SF":"9.1%","syn_%Score":"54.5%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"HandOff","syn_%Time":"0.4%","syn_Poss":1,"syn_PTS":2,"syn_PPP":2.0,"syn_FGm":0,"syn_FGM":1,"syn_FGA":1,"syn_FG%":"100.0%","syn_aFG%":"100.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"100.0%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"ISO","syn_%Time":"4.5%","syn_Poss":12,"syn_PTS":8,"syn_PPP":0.667,"syn_FGm":5,"syn_FGM":3,"syn_FGA":8,"syn_FG%":"37.5%","syn_aFG%":"37.5%","syn_%TO":"25.0%","syn_%FT":"8.3%","syn_%SF":"8.3%","syn_%Score":"33.3%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_%Time":"11.3%","syn_Poss":30,"syn_PTS":14,"syn_PPP":0.467,"syn_FGm":2,"syn_FGM":2,"syn_FGA":4,"syn_FG%":"50.0%","syn_aFG%":"50.0%","syn_%TO":"60.0%","syn_%FT":"26.7%","syn_%SF":"10.0%","syn_%Score":"33.3%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_%Time":"21.5%","syn_Poss":57,"syn_PTS":56,"syn_PPP":0.982,"syn_FGm":23,"syn_FGM":26,"syn_FGA":49,"syn_FG%":"53.1%","syn_aFG%":"53.1%","syn_%TO":"5.3%","syn_%FT":"12.3%","syn_%SF":"12.3%","syn_%Score":"50.9%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"OffScreen","syn_%Time":"0.8%","syn_Poss":2,"syn_PTS":0,"syn_PPP":0.0,"syn_FGm":1,"syn_FGM":0,"syn_FGA":1,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"50.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"0.0%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_%Time":"1.9%","syn_Poss":5,"syn_PTS":4,"syn_PPP":0.8,"syn_FGm":2,"syn_FGM":1,"syn_FGA":3,"syn_FG%":"33.3%","syn_aFG%":"33.3%","syn_%TO":"0.0%","syn_%FT":"40.0%","syn_%SF":"20.0%","syn_%Score":"60.0%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_%Time":"5.7%","syn_Poss":15,"syn_PTS":16,"syn_PPP":1.067,"syn_FGm":5,"syn_FGM":6,"syn_FGA":11,"syn_FG%":"54.5%","syn_aFG%":"54.5%","syn_%TO":"13.3%","syn_%FT":"13.3%","syn_%SF":"13.3%","syn_%Score":"53.3%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Post_Up","syn_%Time":"10.2%","syn_Poss":27,"syn_PTS":26,"syn_PPP":0.963,"syn_FGm":11,"syn_FGM":11,"syn_FGA":22,"syn_FG%":"50.0%","syn_aFG%":"50.0%","syn_%TO":"7.4%","syn_%FT":"18.5%","syn_%SF":"18.5%","syn_%Score":"48.1%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_%Time":"7.9%","syn_Poss":21,"syn_PTS":20,"syn_PPP":0.952,"syn_FGm":9,"syn_FGM":10,"syn_FGA":19,"syn_FG%":"52.6%","syn_aFG%":"52.6%","syn_%TO":"9.5%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"47.6%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Transition","syn_%Time":"10.9%","syn_Poss":29,"syn_PTS":39,"syn_PPP":1.345,"syn_FGm":5,"syn_FGM":19,"syn_FGA":24,"syn_FG%":"79.2%","syn_aFG%":"79.2%","syn_%TO":"13.8%","syn_%FT":"17.2%","syn_%SF":"20.7%","syn_%Score":"65.5%"}]} {"id":"hC6I4dpxRlOZGplrEKSQDw","result":[{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Average","title":null,"G":38,"GS":9,"PTS":9.2,"MIN":"20:33","FGM":3.9,"FGA":7.1,"FG%":"55.0%","3PM":0.0,"3PA":0.0,"3P%":"0.0%","FT%":"55.6%","FTM":1.4,"FTA":2.6,"Reb":7.4,"AST":1.1,"TO":1.5,"STL":1.3,"BLK":2.4},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","title":null,"G":38,"GS":9,"PTS":351,"MIN":"780:52","FGM":148,"FGA":269,"FG%":"55.0%","3PM":0,"3PA":1,"3P%":"0.0%","FT%":"55.6%","FTM":55,"FTA":99,"Reb":280,"AST":43,"TO":58,"STL":48,"BLK":91},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"PercentRank","title":null,"G":38,"GS":9,"PTS":78,"MIN":56,"FGM":84,"FGA":71,"FG%":94,"3PM":0,"3PA":13,"3P%":0,"FT%":25,"FTM":74,"FTA":82,"Reb":96,"AST":61,"TO":39,"STL":85,"BLK":99}]}
                        assistant: Player Breakdown
                        Efficient scorer with a 55.0% FG% (96th percentile) and a 55.2% EFG% (91st percentile).\n
                        High usage player with a 21.5% USG% (70th percentile), averaging 9.2 PPG (73rd percentile).\n
                        Dominant on the boards, with 7.4 REB per game (95th percentile) and an 15.1% ORB% (97th percentile).\n
                        Effective in transition, scoring 1.364 PPP (96th percentile).\n
                        Non-threat from 3-point territory, making 0.0% of 3PA (0th percentile).\n
                        How to Defend\n
                        Focus on contesting her shots inside the arc, where she is highly efficient, with a 55.0% FG% (96th percentile).\n
                        Box out aggressively to mitigate her impact on the boards, as she averages 7.4 REB per game (95th percentile) and has a 15.1% ORB% (97th percentile).\n
                        Allow her to take three-point shots, as she has not made a 3 all year, with a 0.0% 3P% (0th percentile).\n
                        
                        user:{"id":"k3YZcUFQSWGyQtZscyFN6g","result":[{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"Cut","syn_%Time":"4.7%","syn_Poss":17,"syn_PTS":28,"syn_PPP":1.647,"syn_FGm":2,"syn_FGM":12,"syn_FGA":14,"syn_FG%":"85.7%","syn_aFG%":"85.7%","syn_%TO":"0.0%","syn_%FT":"17.6%","syn_%SF":"17.6%","syn_%Score":"88.2%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"HandOff","syn_%Time":"14.0%","syn_Poss":51,"syn_PTS":46,"syn_PPP":0.902,"syn_FGm":18,"syn_FGM":19,"syn_FGA":37,"syn_FG%":"51.4%","syn_aFG%":"55.4%","syn_%TO":"21.6%","syn_%FT":"7.8%","syn_%SF":"3.9%","syn_%Score":"43.1%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"ISO","syn_%Time":"3.6%","syn_Poss":13,"syn_PTS":9,"syn_PPP":0.692,"syn_FGm":8,"syn_FGM":4,"syn_FGA":12,"syn_FG%":"33.3%","syn_aFG%":"33.3%","syn_%TO":"0.0%","syn_%FT":"7.7%","syn_%SF":"7.7%","syn_%Score":"38.5%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_%Time":"5.2%","syn_Poss":19,"syn_PTS":12,"syn_PPP":0.632,"syn_FGm":2,"syn_FGM":3,"syn_FGA":5,"syn_FG%":"60.0%","syn_aFG%":"60.0%","syn_%TO":"26.3%","syn_%FT":"47.4%","syn_%SF":"0.0%","syn_%Score":"42.1%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_%Time":"4.1%","syn_Poss":15,"syn_PTS":17,"syn_PPP":1.133,"syn_FGm":5,"syn_FGM":7,"syn_FGA":12,"syn_FG%":"58.3%","syn_aFG%":"58.3%","syn_%TO":"6.7%","syn_%FT":"13.3%","syn_%SF":"13.3%","syn_%Score":"60.0%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"OffScreen","syn_%Time":"5.2%","syn_Poss":19,"syn_PTS":11,"syn_PPP":0.579,"syn_FGm":10,"syn_FGM":5,"syn_FGA":15,"syn_FG%":"33.3%","syn_aFG%":"36.7%","syn_%TO":"15.8%","syn_%FT":"5.3%","syn_%SF":"5.3%","syn_%Score":"26.3%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_%Time":"24.0%","syn_Poss":87,"syn_PTS":59,"syn_PPP":0.678,"syn_FGm":36,"syn_FGM":26,"syn_FGA":62,"syn_FG%":"41.9%","syn_aFG%":"45.2%","syn_%TO":"25.3%","syn_%FT":"4.6%","syn_%SF":"3.4%","syn_%Score":"32.2%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_%Time":"0.3%","syn_Poss":1,"syn_PTS":0,"syn_PPP":0.0,"syn_FGm":1,"syn_FGM":0,"syn_FGA":1,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"0.0%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"Post_Up","syn_%Time":"0.3%","syn_Poss":1,"syn_PTS":2,"syn_PPP":2.0,"syn_FGm":0,"syn_FGM":1,"syn_FGA":1,"syn_FG%":"100.0%","syn_aFG%":"100.0%","syn_%TO":"0.0%","syn_%FT":"100.0%","syn_%SF":"100.0%","syn_%Score":"100.0%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_%Time":"17.1%","syn_Poss":62,"syn_PTS":56,"syn_PPP":0.903,"syn_FGm":36,"syn_FGM":19,"syn_FGA":55,"syn_FG%":"34.5%","syn_aFG%":"48.2%","syn_%TO":"6.5%","syn_%FT":"6.5%","syn_%SF":"6.5%","syn_%Score":"35.5%"},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","syn_TYPE":"Transition","syn_%Time":"21.5%","syn_Poss":78,"syn_PTS":76,"syn_PPP":0.974,"syn_FGm":26,"syn_FGM":31,"syn_FGA":57,"syn_FG%":"54.4%","syn_aFG%":"57.0%","syn_%TO":"17.9%","syn_%FT":"10.3%","syn_%SF":"10.3%","syn_%Score":"47.4%"}]} {"id":"Ja70n0RRTx-1BYnQ0fErQQ","result":[{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Average","title":null,"G":31,"GS":31,"PTS":10.6,"MIN":"33:21","FGM":4.2,"FGA":9.1,"FG%":"46.6%","3PM":0.8,"3PA":3.2,"3P%":"26.0%","FT%":"53.3%","FTM":1.3,"FTA":2.4,"Reb":2.9,"AST":4.6,"TO":2.1,"STL":1.2,"BLK":0.2},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"Sum","title":null,"G":31,"GS":31,"PTS":328,"MIN":"1033:40","FGM":131,"FGA":281,"FG%":"46.6%","3PM":26,"3PA":100,"3P%":"26.0%","FT%":"53.3%","FTM":40,"FTA":75,"Reb":89,"AST":143,"TO":66,"STL":36,"BLK":6},{"subject":"player","subjectId":"TpM9KSc9Qzujc-EQlFEPDg","aggregate":"PercentRank","title":null,"G":31,"GS":31,"PTS":79,"MIN":95,"FGM":84,"FGA":83,"FG%":67,"3PM":70,"3PA":78,"3P%":41,"FT%":27,"FTM":66,"FTA":75,"Reb":59,"AST":98,"TO":7,"STL":89,"BLK":56}]}
                        assistant: Player Breakdown:\n
                        Average usage guard (19.0% USG, 55th percentile) who plays significant minutes (33.3 MPG) averaging 10.6 PPG on 9.1 FGAs.\n
                        Effective passer with an AST% of 25.4% (97th percentile) and 4.6 assists per game (97th percentile).\n
                        Active defender, averaging 1.2 steals per game (86th percentile) and 2.0 STL% (62nd percentile).\n
                        Frequently involved in handoffs, ranking in the 97th percentile for frequency and producing an average 0.885 PPP (56th percentile).\n
                        Struggles from the free-throw line, converting 53.3% of free throws (12th percentile).\n
                        How to Defend:\n
                        Sag off him on the perimeter as his 3-point shooting is average (26.0%).\n
                        Pressure his playmaking, focusing on his 17.2% TO% (28th percentile).\n
                        Stay alert for his cuts, as he scores effectively 1.684 PPP on cut attempts (98th percentile). \n
                        
                        user:{"id":"dvbSYFpvSC-TykcPUcfk2Q","result":[{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"Cut","syn_%Time":"11.4%","syn_Poss":40,"syn_PTS":43,"syn_PPP":1.075,"syn_FGm":12,"syn_FGM":20,"syn_FGA":32,"syn_FG%":"62.5%","syn_aFG%":"62.5%","syn_%TO":"10.0%","syn_%FT":"12.5%","syn_%SF":"12.5%","syn_%Score":"55.0%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"HandOff","syn_%Time":"4.6%","syn_Poss":16,"syn_PTS":10,"syn_PPP":0.625,"syn_FGm":7,"syn_FGM":4,"syn_FGA":11,"syn_FG%":"36.4%","syn_aFG%":"36.4%","syn_%TO":"12.5%","syn_%FT":"25.0%","syn_%SF":"18.8%","syn_%Score":"37.5%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"ISO","syn_%Time":"9.4%","syn_Poss":33,"syn_PTS":32,"syn_PPP":0.97,"syn_FGm":12,"syn_FGM":14,"syn_FGA":26,"syn_FG%":"53.8%","syn_aFG%":"55.8%","syn_%TO":"15.2%","syn_%FT":"9.1%","syn_%SF":"9.1%","syn_%Score":"48.5%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_%Time":"4.6%","syn_Poss":16,"syn_PTS":16,"syn_PPP":1.0,"syn_FGm":6,"syn_FGM":4,"syn_FGA":10,"syn_FG%":"40.0%","syn_aFG%":"45.0%","syn_%TO":"12.5%","syn_%FT":"25.0%","syn_%SF":"0.0%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_%Time":"15.1%","syn_Poss":53,"syn_PTS":60,"syn_PPP":1.132,"syn_FGm":17,"syn_FGM":27,"syn_FGA":44,"syn_FG%":"61.4%","syn_aFG%":"61.4%","syn_%TO":"5.7%","syn_%FT":"13.2%","syn_%SF":"9.4%","syn_%Score":"58.5%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_%Time":"9.1%","syn_Poss":32,"syn_PTS":24,"syn_PPP":0.75,"syn_FGm":15,"syn_FGM":9,"syn_FGA":24,"syn_FG%":"37.5%","syn_aFG%":"41.7%","syn_%TO":"12.5%","syn_%FT":"15.6%","syn_%SF":"15.6%","syn_%Score":"40.6%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_%Time":"1.1%","syn_Poss":4,"syn_PTS":2,"syn_PPP":0.5,"syn_FGm":2,"syn_FGM":1,"syn_FGA":3,"syn_FG%":"33.3%","syn_aFG%":"33.3%","syn_%TO":"25.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"25.0%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"Post_Up","syn_%Time":"9.7%","syn_Poss":34,"syn_PTS":30,"syn_PPP":0.882,"syn_FGm":14,"syn_FGM":12,"syn_FGA":26,"syn_FG%":"46.2%","syn_aFG%":"46.2%","syn_%TO":"8.8%","syn_%FT":"17.6%","syn_%SF":"14.7%","syn_%Score":"47.1%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_%Time":"12.3%","syn_Poss":43,"syn_PTS":41,"syn_PPP":0.953,"syn_FGm":24,"syn_FGM":15,"syn_FGA":39,"syn_FG%":"38.5%","syn_aFG%":"50.0%","syn_%TO":"0.0%","syn_%FT":"11.6%","syn_%SF":"11.6%","syn_%Score":"39.5%"},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","syn_TYPE":"Transition","syn_%Time":"22.8%","syn_Poss":80,"syn_PTS":107,"syn_PPP":1.338,"syn_FGm":18,"syn_FGM":46,"syn_FGA":64,"syn_FG%":"71.9%","syn_aFG%":"71.9%","syn_%TO":"6.2%","syn_%FT":"16.2%","syn_%SF":"15.0%","syn_%Score":"68.8%"}]} {"id":"KTyCNvT8Sg6JvPrRy92Kew","result":[{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Average","title":null,"G":24,"GS":24,"PTS":16.0,"MIN":"25:27","FGM":6.7,"FGA":12.2,"FG%":"54.8%","3PM":0.6,"3PA":1.8,"3P%":"32.6%","FT%":"51.6%","FTM":2.0,"FTA":3.9,"Reb":7.3,"AST":1.2,"TO":1.4,"STL":1.5,"BLK":0.4},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"Sum","title":null,"G":24,"GS":24,"PTS":384,"MIN":"610:41","FGM":161,"FGA":294,"FG%":"54.8%","3PM":14,"3PA":43,"3P%":"32.6%","FT%":"51.6%","FTM":48,"FTA":93,"Reb":175,"AST":30,"TO":34,"STL":35,"BLK":9},{"subject":"player","subjectId":"mldh5UffRKSL8tCOx6wFvw","aggregate":"PercentRank","title":null,"G":24,"GS":24,"PTS":96,"MIN":72,"FGM":99,"FGA":95,"FG%":85,"3PM":61,"3PA":60,"3P%":59,"FT%":26,"FTM":80,"FTA":91,"Reb":96,"AST":68,"TO":24,"STL":95,"BLK":74}]}
                        assistant: Player Breakdown:\n
                        High usage guard (26.3% USG, 91st percentile) who plays significant minutes (29.6 MPG) averaging 11.3 PPG on 34.9% FG (10th percentile).\n
                        Strong at drawing fouls, averaging 4.3 FTA per game (92nd percentile), converting 78.6% of them (71st percentile).
                        Frequently involved as a pick and roll ball handler, ranking in the 82nd percentile for frequency but producing a below average 0.521 PPP (11th percentile).\n
                        Ineffective in transition, producing 0.814 PPP (15th percentile).\n
                        How to Defend:\n
                        Pressure him on the ball, exploiting his 18.6% TO% (21st percentile).\n
                        Sag off him on the perimeter as his shooting percentage is low (34.9% FG, 10th percentile).\n
                        Be prepared for his drives and how he draws fouls, as he averages 4.3 FTA per game (92nd percentile) and converts them at a 78.6% rate (71st percentile).\n
                        user:"""
            
            },
            {
                "role": "user",
                "content": player_boxscore  
            },
            
        ],
    )

    return chat_completion.choices[0].message.content


temperature = st.slider("Changes behavior- higher is more random🎲", min_value=0.5, max_value=2.0, value=1.5, step=0.1)


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
    
    
