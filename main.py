import streamlit as st
import pandas as pd

import utils

file_name = 'data.csv'
df = pd.read_csv(file_name)

def team_picker():
    st.title('Team Picker')
    holder_text = "Enter player"
    players = st.text_input("Players for Tonight", holder_text)
    st.dataframe(df['name'])
    players = players.upper()
    players_list = players.split()


    if players == holder_text:
        st.write("WAITING FOR PLAYERS")

    elif len(players_list) !=  10:
        st.write(f"Error: Not 10 players. Currently have {len(players_list)} players")

    else:
        team1, team2 = utils.TeamSelection(players_list, df) 
        st.write(f"Team1: {team1}")
        st.write(f"Team2: {team2}")

def upload_page_results():
    st.title('Upload Game Results')
    holder_text = "Enter Team:"
    team1 = st.text_input("Team 1", holder_text).upper().split()
    team2 = st.text_input("Team 2", holder_text).upper().split()

    whatTeamWon = st.radio("What team won:", ["Team 1", "Team 2", "Draw"])

    with st.popover("Submit"):
        st.markdown(f"{whatTeamWon} won, are you sure?")
        if st.button("Confirm"):
            global df
            df = pd.read_csv(file_name)
            df = utils.UploadMatchResult(df, team1, team2, whatTeamWon)
            df.to_csv(file_name , encoding='utf-8', index=False, header=True)
            st.toast("Team results submmitted")

        
def display_table():
    st.title('Greater Glasgow U70 Premier Monday Night 5s League')
    global df
    df = pd.read_csv(file_name)
    st.dataframe(df)


pg = st.navigation([st.Page(team_picker, title = "Pick Team"), st.Page(upload_page_results, title = "Upload Game Results"), st.Page(display_table, title = "Check Table")])
pg.run()
