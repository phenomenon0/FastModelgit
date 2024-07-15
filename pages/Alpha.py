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
@st.cache_data()
def get_scouting_report(_llm, model, player, temperature):
    chat_completion = _llm.chat.completions.create(
        model=model,
        top_p =1,
     seed= 111,
        messages=[
            {
                    "role": "system",
                    "content":""" you are an expert basketball scout analyzing players using box scores and synergy stats to prepare your team for upcoming games. 
                    Follow the example provided in terms of use of json to generate insights, grammar, language, and tone..
                    Use Markdown to  emphasize key points - favour one line bullet points
                     Focus on how they play 
                     Avoid listing raw stats upfront. Instead, embed the statistics within short concise  sentences.
                     Highlight only 5 of the most important statistics -
                     Write a 3 bullet point on defensive strategies to play against them - 1.5line max 
                    please stick to the format in the examples i.e percentiles in brackets, and the overall tone and structure of the response.
                   
                    
                    user:{"id":"KOo87rV6Q7GOVfTunQnq_g","result":[{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Average","title":null,"G":29,"GS":28,"PTS":11.3,"MIN":"29:37","FGM":3.7,"FGA":10.5,"FG%":"34.9%","3PM":0.6,"3PA":2.4,"3P%":"23.2%","FT%":"78.6%","FTM":3.4,"FTA":4.3,"Reb":3.8,"AST":4.2,"TO":2.9,"STL":1.1,"BLK":0.1,"PPP":0.73,"A/TO":1.48,"%TO":null,"AST%":"27.9%","%SF":null,"TO%":"18.6%","STL%":"2.2%","BLK%":"0.3%","%3P":"22.7%"," /-":null,"Usg%":"26.3%","TS%":"44.9%","eFG%":"37.5%","DR%":"12.2%","OR%":"3.7%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","title":null,"G":29,"GS":28,"PTS":327,"MIN":"858:44","FGM":106,"FGA":304,"FG%":"34.9%","3PM":16,"3PA":69,"3P%":"23.2%","FT%":"78.6%","FTM":99,"FTA":126,"Reb":110,"AST":123,"TO":83,"STL":32,"BLK":2,"PPP":0.73,"A/TO":1.48,"%TO":null,"AST%":"27.9%","%SF":null,"TO%":"18.6%","STL%":"2.2%","BLK%":"0.3%","%3P":"22.7%"," /-":null,"Usg%":"26.3%","TS%":"44.9%","eFG%":"37.5%","DR%":"12.2%","OR%":"3.7%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"PercentRank","title":null,"G":29,"GS":28,"PTS":82,"MIN":85,"FGM":78,"FGA":89,"FG%":21,"3PM":60,"3PA":68,"3P%":35,"FT%":75,"FTM":94,"FTA":94,"Reb":73,"AST":97,"TO":1,"STL":87,"BLK":33,"PPP":21,"A/TO":77,"%TO":null,"AST%":96,"%SF":null,"TO%":25,"STL%":70,"BLK%":28,"%3P":32," /-":null,"Usg%":90,"TS%":21,"eFG%":15,"DR%":48,"OR%":46}]} {"id":"7u7K2labRvKw-E6qEKsLEA","result":[{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Cut","syn_Poss":13,"syn_PTS":20,"syn_PPP":1.538,"syn_FGm":3,"syn_FGM":8,"syn_FGA":11,"syn_FG%":"72.7%","syn_aFG%":"72.7%","syn_%TO":"0.0%","syn_%FT":"15.4%","syn_%SF":"7.7%","syn_%Score":"76.9%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"HandOff","syn_Poss":22,"syn_PTS":23,"syn_PPP":1.045,"syn_FGm":10,"syn_FGM":8,"syn_FGA":18,"syn_FG%":"44.4%","syn_aFG%":"44.4%","syn_%TO":"4.5%","syn_%FT":"18.2%","syn_%SF":"18.2%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"ISO","syn_Poss":61,"syn_PTS":40,"syn_PPP":0.656,"syn_FGm":31,"syn_FGM":9,"syn_FGA":40,"syn_FG%":"22.5%","syn_aFG%":"23.8%","syn_%TO":"14.8%","syn_%FT":"24.6%","syn_%SF":"21.3%","syn_%Score":"34.4%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_Poss":33,"syn_PTS":11,"syn_PPP":0.333,"syn_FGm":10,"syn_FGM":0,"syn_FGA":10,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"48.5%","syn_%FT":"21.2%","syn_%SF":"0.0%","syn_%Score":"21.2%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_Poss":8,"syn_PTS":14,"syn_PPP":1.75,"syn_FGm":1,"syn_FGM":6,"syn_FGA":7,"syn_FG%":"85.7%","syn_aFG%":"85.7%","syn_%TO":"0.0%","syn_%FT":"25.0%","syn_%SF":"25.0%","syn_%Score":"87.5%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"OffScreen","syn_Poss":2,"syn_PTS":2,"syn_PPP":1.0,"syn_FGm":0,"syn_FGM":1,"syn_FGA":1,"syn_FG%":"100.0%","syn_aFG%":"100.0%","syn_%TO":"50.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_Poss":127,"syn_PTS":63,"syn_PPP":0.496,"syn_FGm":69,"syn_FGM":21,"syn_FGA":90,"syn_FG%":"23.3%","syn_aFG%":"23.9%","syn_%TO":"18.9%","syn_%FT":"11.8%","syn_%SF":"7.9%","syn_%Score":"25.2%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Post_Up","syn_Poss":1,"syn_PTS":0,"syn_PPP":0.0,"syn_FGm":1,"syn_FGM":0,"syn_FGA":1,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"0.0%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_Poss":60,"syn_PTS":43,"syn_PPP":0.717,"syn_FGm":33,"syn_FGM":16,"syn_FGA":49,"syn_FG%":"32.7%","syn_aFG%":"42.9%","syn_%TO":"16.7%","syn_%FT":"3.3%","syn_%SF":"3.3%","syn_%Score":"28.3%"},{"subject":"player","subjectId":"gJtrgfuxTtunzLWTYBpwEA","aggregate":"Sum","syn_TYPE":"Transition","syn_Poss":74,"syn_PTS":59,"syn_PPP":0.797,"syn_FGm":25,"syn_FGM":20,"syn_FGA":45,"syn_FG%":"44.4%","syn_aFG%":"45.6%","syn_%TO":"24.3%","syn_%FT":"16.2%","syn_%SF":"10.8%","syn_%Score":"39.2%"}]}
                    assistant: Player Breakdown:
                    High usage guard (26.3% USG, 91st percentile) who plays significant minutes (29.6 MPG) averaging 11.3 PPG on 34.9% FG (10th percentile).
                    Effective passer with an AST% of 27.9% (97th percentile) and 4.8 assists per game (92nd percentile).
                    Strong at drawing fouls, averaging 4.3 FTA per game (92nd percentile), converting 78.6% of them (71st percentile).
                    Frequently involved as a pick and roll ball handler (31.1% of the time) but only producing 0.521 PPP.
                    Ineffective in transition, producing 0.814 PPP.
                    How to Defend:
                    Pressure him on the ball, exploiting his 18.6% TO% (21st percentile).
                    Sag off him on the perimeter as his shooting percentage is low (34.9% FG, 10th percentile).
                    Be prepared for his drives and how he draws fouls, as he averages 4.3 FTA per game (92nd percentile) and converts them at a 78.6% rate (71st percentile).
                    
                    user:{"id":"eQDOScAxRq2CRjmCjB1noA","result":[{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Average","title":null,"G":75,"GS":75,"PTS":14.7,"MIN":"30:05","FGM":5.4,"FGA":10.7,"FG%":"50.6%","3PM":1.2,"3PA":3.1,"3P%":"37.4%","FT%":"74.0%","FTM":2.7,"FTA":3.6,"Reb":7.2,"AST":3.8,"TO":2.1,"STL":0.8,"BLK":0.5,"PPP":1.02,"A/TO":1.79,"%TO":null,"AST%":"17.7%","%SF":null,"TO%":"14.8%","STL%":"1.2%","BLK%":"1.3%","%3P":"29.3%"," /-":null,"Usg%":"20.3%","TS%":"59.7%","eFG%":"56.0%","DR%":"21.9%","OR%":"3.9%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","title":null,"G":75,"GS":75,"PTS":1102,"MIN":"2256:38","FGM":406,"FGA":803,"FG%":"50.6%","3PM":88,"3PA":235,"3P%":"37.4%","FT%":"74.0%","FTM":202,"FTA":273,"Reb":540,"AST":286,"TO":160,"STL":60,"BLK":36,"PPP":1.02,"A/TO":1.79,"%TO":null,"AST%":"17.7%","%SF":null,"TO%":"14.8%","STL%":"1.2%","BLK%":"1.3%","%3P":"29.3%"," /-":null,"Usg%":"20.3%","TS%":"59.7%","eFG%":"56.0%","DR%":"21.9%","OR%":"3.9%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"PercentRank","title":null,"G":75,"GS":75,"PTS":82,"MIN":83,"FGM":82,"FGA":80,"FG%":76,"3PM":66,"3PA":65,"3P%":69,"FT%":40,"FTM":87,"FTA":89,"Reb":92,"AST":84,"TO":9,"STL":70,"BLK":69,"PPP":56,"A/TO":48,"%TO":null,"AST%":72,"%SF":null,"TO%":21,"STL%":37,"BLK%":43,"%3P":28," /-":null,"Usg%":69,"TS%":71,"eFG%":64,"DR%":86,"OR%":49}]} {"id":"yI8rImKjQVCYqb9tnOZBzg","result":[{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Cut","syn_Poss":83,"syn_PTS":102,"syn_PPP":1.229,"syn_FGm":29,"syn_FGM":41,"syn_FGA":70,"syn_FG%":"58.6%","syn_aFG%":"58.6%","syn_%TO":"3.6%","syn_%FT":"21.7%","syn_%SF":"21.7%","syn_%Score":"61.4%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"HandOff","syn_Poss":38,"syn_PTS":37,"syn_PPP":0.974,"syn_FGm":15,"syn_FGM":12,"syn_FGA":27,"syn_FG%":"44.4%","syn_aFG%":"53.7%","syn_%TO":"18.4%","syn_%FT":"13.2%","syn_%SF":"10.5%","syn_%Score":"42.1%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"ISO","syn_Poss":82,"syn_PTS":77,"syn_PPP":0.939,"syn_FGm":41,"syn_FGM":24,"syn_FGA":65,"syn_FG%":"36.9%","syn_aFG%":"40.0%","syn_%TO":"4.9%","syn_%FT":"20.7%","syn_%SF":"18.3%","syn_%Score":"43.9%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_Poss":45,"syn_PTS":20,"syn_PPP":0.444,"syn_FGm":9,"syn_FGM":7,"syn_FGA":16,"syn_FG%":"43.8%","syn_aFG%":"46.9%","syn_%TO":"55.6%","syn_%FT":"8.9%","syn_%SF":"0.0%","syn_%Score":"22.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_Poss":56,"syn_PTS":52,"syn_PPP":0.929,"syn_FGm":26,"syn_FGM":23,"syn_FGA":49,"syn_FG%":"46.9%","syn_aFG%":"46.9%","syn_%TO":"7.1%","syn_%FT":"10.7%","syn_%SF":"8.9%","syn_%Score":"44.6%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"OffScreen","syn_Poss":16,"syn_PTS":21,"syn_PPP":1.312,"syn_FGm":3,"syn_FGM":8,"syn_FGA":11,"syn_FG%":"72.7%","syn_aFG%":"86.4%","syn_%TO":"25.0%","syn_%FT":"6.2%","syn_%SF":"6.2%","syn_%Score":"56.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_Poss":170,"syn_PTS":138,"syn_PPP":0.812,"syn_FGm":61,"syn_FGM":53,"syn_FGA":114,"syn_FG%":"46.5%","syn_aFG%":"51.3%","syn_%TO":"24.1%","syn_%FT":"11.8%","syn_%SF":"9.4%","syn_%Score":"38.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_Poss":29,"syn_PTS":34,"syn_PPP":1.172,"syn_FGm":13,"syn_FGM":15,"syn_FGA":28,"syn_FG%":"53.6%","syn_aFG%":"60.7%","syn_%TO":"3.4%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"51.7%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Post_Up","syn_Poss":37,"syn_PTS":30,"syn_PPP":0.811,"syn_FGm":14,"syn_FGM":13,"syn_FGA":27,"syn_FG%":"48.1%","syn_aFG%":"48.1%","syn_%TO":"18.9%","syn_%FT":"13.5%","syn_%SF":"13.5%","syn_%Score":"43.2%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_Poss":263,"syn_PTS":300,"syn_PPP":1.141,"syn_FGm":119,"syn_FGM":110,"syn_FGA":229,"syn_FG%":"48.0%","syn_aFG%":"58.1%","syn_%TO":"6.5%","syn_%FT":"9.9%","syn_%SF":"9.9%","syn_%Score":"48.3%"},{"subject":"player","subjectId":"lZSNGukiR2iN41eYhK2i8A","aggregate":"Sum","syn_TYPE":"Transition","syn_Poss":253,"syn_PTS":289,"syn_PPP":1.142,"syn_FGm":65,"syn_FGM":100,"syn_FGA":165,"syn_FG%":"60.6%","syn_aFG%":"64.8%","syn_%TO":"17.4%","syn_%FT":"22.5%","syn_%SF":"20.9%","syn_%Score":"54.9%"}]}
                    assistant: Player Breakdown
                    Versatile forward with a balanced game, plays significant minutes (30.1 MPG, 79th percentile), and averages 14.7 PPG (79th percentile).
                    Efficient scorer with a 56.0% EFG% (61st percentile) and excels inside the arc with a 70.7% 2P-R (72nd percentile).
                    Strong rebounder, pulling down 7.2 REB per game (91st percentile) and a 21.9% DRB% (86th percentile).
                    Effective in spot-up situations, scoring 1.153 PPP.
                    Struggles with ball security, committing 2.1 TOs per game (11th percentile) and has a 14.8% TO% (19th percentile).
                    How to Defend
                    Focus on closing out on his spot-up opportunities as he scores 1.153 PPP.
                    Apply pressure to force turnovers; he commits 2.1 TOs per game (11th percentile) and has a 14.8% TO% (19th percentile).
                    Box out aggressively to limit his impact on the boards, as he averages 7.2 REB per game (91st percentile) and has a 21.9% DRB% (86th percentile).
                     
                    
                    user:{"id":"4rEV8OPQSJGd_eYFwNUEYQ","result":[{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Average","title":null,"G":33,"GS":32,"PTS":11.6,"MIN":"28:39","FGM":4.1,"FGA":7.6,"FG%":"54.0%","3PM":0.3,"3PA":1.2,"3P%":"27.5%","FT%":"62.3%","FTM":3.0,"FTA":4.8,"Reb":5.9,"AST":1.1,"TO":1.2,"STL":0.8,"BLK":0.7,"PPP":1.05,"A/TO":0.95,"%TO":null,"AST%":"6.9%","%SF":null,"TO%":"10.4%","STL%":"1.6%","BLK%":"2.7%","%3P":"15.9%"," /-":null,"Usg%":"19.8%","TS%":"58.3%","eFG%":"56.2%","DR%":"14.7%","OR%":"9.3%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","title":null,"G":33,"GS":32,"PTS":382,"MIN":"945:12","FGM":136,"FGA":252,"FG%":"54.0%","3PM":11,"3PA":40,"3P%":"27.5%","FT%":"62.3%","FTM":99,"FTA":159,"Reb":196,"AST":36,"TO":38,"STL":26,"BLK":24,"PPP":1.05,"A/TO":0.95,"%TO":null,"AST%":"6.9%","%SF":null,"TO%":"10.4%","STL%":"1.6%","BLK%":"2.7%","%3P":"15.9%"," /-":null,"Usg%":"19.8%","TS%":"58.3%","eFG%":"56.2%","DR%":"14.7%","OR%":"9.3%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"PercentRank","title":null,"G":33,"GS":32,"PTS":83,"MIN":82,"FGM":83,"FGA":75,"FG%":84,"3PM":48,"3PA":50,"3P%":44,"FT%":38,"FTM":92,"FTA":96,"Reb":92,"AST":63,"TO":33,"STL":73,"BLK":89,"PPP":84,"A/TO":50,"%TO":null,"AST%":36,"%SF":null,"TO%":75,"STL%":50,"BLK%":77,"%3P":26," /-":null,"Usg%":60,"TS%":77,"eFG%":77,"DR%":65,"OR%":81}]} {"id":"SKafCXSUTQy1I75vJlFf8g","result":[{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"Cut","syn_Poss":84,"syn_PTS":97,"syn_PPP":1.155,"syn_FGm":22,"syn_FGM":37,"syn_FGA":59,"syn_FG%":"62.7%","syn_aFG%":"62.7%","syn_%TO":"6.0%","syn_%FT":"27.4%","syn_%SF":"25.0%","syn_%Score":"64.3%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"ISO","syn_Poss":11,"syn_PTS":10,"syn_PPP":0.909,"syn_FGm":4,"syn_FGM":4,"syn_FGA":8,"syn_FG%":"50.0%","syn_aFG%":"50.0%","syn_%TO":"18.2%","syn_%FT":"9.1%","syn_%SF":"9.1%","syn_%Score":"45.5%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_Poss":25,"syn_PTS":17,"syn_PPP":0.68,"syn_FGm":3,"syn_FGM":2,"syn_FGA":5,"syn_FG%":"40.0%","syn_aFG%":"40.0%","syn_%TO":"40.0%","syn_%FT":"40.0%","syn_%SF":"8.0%","syn_%Score":"40.0%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_Poss":47,"syn_PTS":60,"syn_PPP":1.277,"syn_FGm":10,"syn_FGM":21,"syn_FGA":31,"syn_FG%":"67.7%","syn_aFG%":"67.7%","syn_%TO":"6.4%","syn_%FT":"34.0%","syn_%SF":"34.0%","syn_%Score":"66.0%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"OffScreen","syn_Poss":1,"syn_PTS":3,"syn_PPP":3.0,"syn_FGm":0,"syn_FGM":1,"syn_FGA":1,"syn_FG%":"100.0%","syn_aFG%":"150.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"100.0%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_Poss":4,"syn_PTS":4,"syn_PPP":1.0,"syn_FGm":2,"syn_FGM":2,"syn_FGA":4,"syn_FG%":"50.0%","syn_aFG%":"50.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"50.0%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_Poss":29,"syn_PTS":34,"syn_PPP":1.172,"syn_FGm":7,"syn_FGM":13,"syn_FGA":20,"syn_FG%":"65.0%","syn_aFG%":"67.5%","syn_%TO":"10.3%","syn_%FT":"20.7%","syn_%SF":"17.2%","syn_%Score":"58.6%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"Post_Up","syn_Poss":21,"syn_PTS":18,"syn_PPP":0.857,"syn_FGm":7,"syn_FGM":6,"syn_FGA":13,"syn_FG%":"46.2%","syn_aFG%":"46.2%","syn_%TO":"14.3%","syn_%FT":"28.6%","syn_%SF":"19.0%","syn_%Score":"47.6%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_Poss":83,"syn_PTS":66,"syn_PPP":0.795,"syn_FGm":42,"syn_FGM":23,"syn_FGA":65,"syn_FG%":"35.4%","syn_aFG%":"41.5%","syn_%TO":"9.6%","syn_%FT":"14.5%","syn_%SF":"13.3%","syn_%Score":"34.9%"},{"subject":"player","subjectId":"reZgTYFlSY2jJQfWBwKIkA","aggregate":"Sum","syn_TYPE":"Transition","syn_Poss":49,"syn_PTS":64,"syn_PPP":1.306,"syn_FGm":13,"syn_FGM":24,"syn_FGA":37,"syn_FG%":"64.9%","syn_aFG%":"66.2%","syn_%TO":"6.1%","syn_%FT":"22.4%","syn_%SF":"22.4%","syn_%Score":"63.3%"}]}
                    assistant:Player Breakdown:
                    Above average 19.8% usage (60th percentile) forward who plays 28.6 mpg averaging 11.6 points per contest on 58.3% TS% (77th percentile). 
                    Very active on both offensive (2.2 ORB’s per game) and defensive (3.7 DRB’s per game) glass. 
                    Most efficient scoring the ball in transition (1.333 PPP) and offensive rebounding situations (1.271 PPP).
                    Majority of his work is done inside the arc as seen with his below average 15.9% 3P-R and a below average 27.5% 3P%. 
                    Very good at getting to the foul line with a 63.1% FT-R (93rd percentile) but struggles to convert while he’s there shooting only 62.3% from the stripe (25th percentile). 
                    Things to Consider:
                    What can we do to keep him off of the foul line or are we ok with putting him there because of his low percentage at the line? Especially in cutting situations which he is in 24% of the time.
                    What can we do to limit his activity on the backboard? Both offensively and defensively. 
                    Is he someone we are comfortable with baiting into shots from the perimeter because of his 27.5% 3p%? 
                    user: {"id":"cRsv_WVzQjukNR1Lb2L2bg","result":[{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Average","title":null,"G":38,"GS":9,"PTS":9.2,"MIN":"20:33","FGM":3.9,"FGA":7.1,"FG%":"55.0%","3PM":0.0,"3PA":0.0,"3P%":"0.0%","FT%":"55.6%","FTM":1.4,"FTA":2.6,"Reb":7.4,"AST":1.1,"TO":1.5,"STL":1.3,"BLK":2.4,"PPP":0.94,"A/TO":0.74,"%TO":null,"AST%":"8.7%","%SF":null,"TO%":"15.5%","STL%":"3.3%","BLK%":"10.7%","%3P":"0.4%"," /-":null,"Usg%":"21.5%","TS%":"55.5%","eFG%":"55.0%","DR%":"20.2%","OR%":"15.1%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","title":null,"G":38,"GS":9,"PTS":351,"MIN":"780:52","FGM":148,"FGA":269,"FG%":"55.0%","3PM":0,"3PA":1,"3P%":"0.0%","FT%":"55.6%","FTM":55,"FTA":99,"Reb":280,"AST":43,"TO":58,"STL":48,"BLK":91,"PPP":0.94,"A/TO":0.74,"%TO":null,"AST%":"8.7%","%SF":null,"TO%":"15.5%","STL%":"3.3%","BLK%":"10.7%","%3P":"0.4%"," /-":null,"Usg%":"21.5%","TS%":"55.5%","eFG%":"55.0%","DR%":"20.2%","OR%":"15.1%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"PercentRank","title":null,"G":38,"GS":9,"PTS":78,"MIN":56,"FGM":84,"FGA":71,"FG%":94,"3PM":0,"3PA":13,"3P%":0,"FT%":25,"FTM":74,"FTA":82,"Reb":96,"AST":61,"TO":39,"STL":85,"BLK":99,"PPP":87,"A/TO":52,"%TO":null,"AST%":38,"%SF":null,"TO%":70,"STL%":87,"BLK%":99,"%3P":13," /-":null,"Usg%":71,"TS%":85,"eFG%":90,"DR%":91,"OR%":96}]} {"id":"5383TX6WSiq-WXIbddXtlg","result":[{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Cut","syn_Poss":66,"syn_PTS":72,"syn_PPP":1.091,"syn_FGm":24,"syn_FGM":33,"syn_FGA":57,"syn_FG%":"57.9%","syn_aFG%":"57.9%","syn_%TO":"9.1%","syn_%FT":"9.1%","syn_%SF":"9.1%","syn_%Score":"54.5%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"HandOff","syn_Poss":1,"syn_PTS":2,"syn_PPP":2.0,"syn_FGm":0,"syn_FGM":1,"syn_FGA":1,"syn_FG%":"100.0%","syn_aFG%":"100.0%","syn_%TO":"0.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"100.0%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"ISO","syn_Poss":12,"syn_PTS":8,"syn_PPP":0.667,"syn_FGm":5,"syn_FGM":3,"syn_FGA":8,"syn_FG%":"37.5%","syn_aFG%":"37.5%","syn_%TO":"25.0%","syn_%FT":"8.3%","syn_%SF":"8.3%","syn_%Score":"33.3%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Miscellaneous","syn_Poss":30,"syn_PTS":14,"syn_PPP":0.467,"syn_FGm":2,"syn_FGM":2,"syn_FGA":4,"syn_FG%":"50.0%","syn_aFG%":"50.0%","syn_%TO":"60.0%","syn_%FT":"26.7%","syn_%SF":"10.0%","syn_%Score":"33.3%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"OffensiveRebound","syn_Poss":57,"syn_PTS":56,"syn_PPP":0.982,"syn_FGm":23,"syn_FGM":26,"syn_FGA":49,"syn_FG%":"53.1%","syn_aFG%":"53.1%","syn_%TO":"5.3%","syn_%FT":"12.3%","syn_%SF":"12.3%","syn_%Score":"50.9%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"OffScreen","syn_Poss":2,"syn_PTS":0,"syn_PPP":0.0,"syn_FGm":1,"syn_FGM":0,"syn_FGA":1,"syn_FG%":"0.0%","syn_aFG%":"0.0%","syn_%TO":"50.0%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"0.0%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"PandRBallHandler","syn_Poss":5,"syn_PTS":4,"syn_PPP":0.8,"syn_FGm":2,"syn_FGM":1,"syn_FGA":3,"syn_FG%":"33.3%","syn_aFG%":"33.3%","syn_%TO":"0.0%","syn_%FT":"40.0%","syn_%SF":"20.0%","syn_%Score":"60.0%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"PandRRollMan","syn_Poss":15,"syn_PTS":16,"syn_PPP":1.067,"syn_FGm":5,"syn_FGM":6,"syn_FGA":11,"syn_FG%":"54.5%","syn_aFG%":"54.5%","syn_%TO":"13.3%","syn_%FT":"13.3%","syn_%SF":"13.3%","syn_%Score":"53.3%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Post_Up","syn_Poss":27,"syn_PTS":26,"syn_PPP":0.963,"syn_FGm":11,"syn_FGM":11,"syn_FGA":22,"syn_FG%":"50.0%","syn_aFG%":"50.0%","syn_%TO":"7.4%","syn_%FT":"18.5%","syn_%SF":"18.5%","syn_%Score":"48.1%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Spot_Up","syn_Poss":21,"syn_PTS":20,"syn_PPP":0.952,"syn_FGm":9,"syn_FGM":10,"syn_FGA":19,"syn_FG%":"52.6%","syn_aFG%":"52.6%","syn_%TO":"9.5%","syn_%FT":"0.0%","syn_%SF":"0.0%","syn_%Score":"47.6%"},{"subject":"player","subjectId":"W0sp8z1OQ0ipmLSASOgQDQ","aggregate":"Sum","syn_TYPE":"Transition","syn_Poss":29,"syn_PTS":39,"syn_PPP":1.345,"syn_FGm":5,"syn_FGM":19,"syn_FGA":24,"syn_FG%":"79.2%","syn_aFG%":"79.2%","syn_%TO":"13.8%","syn_%FT":"17.2%","syn_%SF":"20.7%","syn_%Score":"65.5%"}]}
                    Player Breakdown
                    Efficient scorer with a 55.0% FG% (96th percentile) and a 55.2% EFG% (91st percentile).
                    High usage player with a 21.5% USG% (70th percentile), averaging 9.2 PPG (73rd percentile).
                    Dominant on the boards, with 7.4 REB per game (95th percentile) and an 15.1% ORB% (97th percentile).
                    Effective in transition, scoring 1.364 PPP.
                    Non-threat from 3-point territory, making 0.0% of 3PA (0th percentile).
                    How to Defend
                    Focus on contesting her shots inside the arc, where she is highly efficient, with a 55.0% FG% (96th percentile).
                    Box out aggressively to mitigate her impact on the boards, as she averages 7.4 REB per game (95th percentile) and has a 15.1% ORB% (97th percentile).
                    Allow her to take three-point shots, as she has not made a 3 all year, with a 0.0% 3P% (0th percentile).
                    ***************************************************************************************************************************
                     user: """
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
    
    
