import pandas as pd
from trueskill import Rating, rate

def TeamSelection(names, df):
    names_df = df["name"].unique()
    player_map = {}
    for name in names:
        if name in names_df:
            existing_player = df.loc[df['name'] == name]
            print(existing_player["trueskillmu"])
            player_map[name] = float(existing_player["trueskillmu"])
        else:
            player_map[name] = float(Rating().mu)
    
    player_map = dict(sorted(player_map.items(), key=lambda item: item[1]))

    team = 1
    team1 = []
    team2 = []
    for i in player_map:
        print(f"{i} : {player_map[i]}")
        if team % 2 != 0:
            team1.append(i)
        else: 
            team2.append(i)
        team += 1


    return team1, team2

def loadTeamRating(team, df):
    # Extract unique names from DataFrame
    names_df = set(df["name"].unique())
    names = []
    team_ratings = []
    
    # Return None for empty teams
    if len(team) == 0:
        return None, None


    for name in team:
        player = None
        # Check if player exists in DataFrame
        if name in names_df:
            existing_player = df.loc[df['name'] == name]
            mu = existing_player["trueskillmu"].iloc[0]  # Ensure scalar value
            sigma = existing_player["trueskillsigma"].iloc[0]  # Ensure scalar value
            player = Rating(float(mu), float(sigma))
        else:
            player = Rating()  # Default rating for new players

        names.append(name)
        team_ratings.append(player)

    return names, team_ratings


def DfUpdate(df, winners, losers, ratings):
    # Update winners
    for count, name in enumerate(winners):
        if name in df["name"].values:  # Check if name exists in DataFrame
            # Find the row index and update it
            row_index = df.loc[df['name'] == name].index[0]
            df.at[row_index, 'trueskillmu'] = ratings[0][count].mu
            df.at[row_index, 'trueskillsigma'] = ratings[0][count].sigma
            df.at[row_index, 'w'] += 1
            df.at[row_index, 'p'] += 3
            df.at[row_index, 'gp'] += 1
        else:
            # Add a new row for a new player
            new_row = {
                'name': name,
                'trueskillmu': ratings[0][count].mu,
                'trueskillsigma': ratings[0][count].sigma,
                'gp': 1, 'w': 1, 'l': 0, 'd': 0, 'p': 3
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Update losers
    for count, name in enumerate(losers):
        if name in df["name"].values:  # Check if name exists in DataFrame
            # Find the row index and update it
            row_index = df.loc[df['name'] == name].index[0]
            df.at[row_index, 'trueskillmu'] = ratings[1][count].mu
            df.at[row_index, 'trueskillsigma'] = ratings[1][count].sigma
            df.at[row_index, 'l'] += 1
            df.at[row_index, 'gp'] += 1
        else:
            # Add a new row for a new player
            new_row = {
                'name': name,
                'trueskillmu': ratings[1][count].mu,
                'trueskillsigma': ratings[1][count].sigma,
                'gp': 1, 'w': 0, 'l': 1, 'd': 0, 'p': 0
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

def DfDraw(df, winners, losers, ratings):
    # Update winners
    for count, name in enumerate(winners):
        if name in df["name"].values:  # Check if name exists in DataFrame
            # Find the row index and update it
            row_index = df.loc[df['name'] == name].index[0]
            df.at[row_index, 'd'] += 1
            df.at[row_index, 'p'] += 1
            df.at[row_index, 'gp'] += 1
        else:
            # Add a new row for a new player
            new_row = {
                'name': name,
                'trueskillmu': ratings[0][count].mu,
                'trueskillsigma': ratings[0][count].sigma,
                'gp': 1, 'w': 0, 'l': 0, 'd': 1, 'p': 1
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Update losers
    for count, name in enumerate(losers):
        if name in df["name"].values:  # Check if name exists in DataFrame
            # Find the row index and update it
            row_index = df.loc[df['name'] == name].index[0]
            df.at[row_index, 'd'] += 1
            df.at[row_index, 'p'] += 1
            df.at[row_index, 'gp'] += 1
        else:
            # Add a new row for a new player
            new_row = {
                'name': name,
                'trueskillmu': ratings[1][count].mu,
                'trueskillsigma': ratings[1][count].sigma,
                'gp': 1, 'w': 0, 'l': 0, 'd': 1, 'p': 1
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df



def UploadMatchResult(df, team1, team2, winningTeam):
    # Load ratings for both teams
    names1, team1_ratings = loadTeamRating(team1, df)
    names2, team2_ratings = loadTeamRating(team2, df)

    if winningTeam == "Team 1":
        new_ratings = rate([team1_ratings, team2_ratings])
        df = DfUpdate(df, team1, team2, new_ratings)
    elif winningTeam == "Team 2":
        new_ratings = rate([team2_ratings, team1_ratings])
        df = DfUpdate(df, team2, team1, new_ratings)
    else:  # Draw case
        new_ratings = rate([team1_ratings, team2_ratings], ranks=[0, 0])
        df = DfDraw(df, team1, team2, new_ratings)

    return df

