# here we import libraries and read the data
from pandas.core.indexes.datetimes import date
from collections import  deque    # 'dequeueue' class from 'collections' module can be used to implement a queueueue. 
import pandas as pd

data = pd.read_csv('epl_results.csv')
# here we modify datatypes and clean the data
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
data = data[data['Result']!='-']
for col in ['W','HomeGoals','AwayGoals']:
    data[col] = pd.to_numeric(data[col], errors='coerce')


class graph:
    def __init__(self):
        self.num_teams = 20
        self.all_teams = data['HomeTeam'].head(10).tolist() + data['AwayTeam'].head(10).tolist()
        self.adj_list = {team: [] for team in self.all_teams}

    def add_edge(self, week, date, home_team, away_team, home_goals, away_goals, result):
        if len(self.adj_list[home_team]) == 0:
            standings  = [0] * 8
            self.adj_list[home_team].append(standings)

        new_list = [week, date, away_team, home_goals, away_goals, result]
        self.adj_list[home_team].insert(week, new_list)

    def graph_initialization(self):
        for index, row in data.iterrows():
            # Access the values in each column of the current row
            self.add_edge(row['W'], row['Date'], row['HomeTeam'], row['AwayTeam'], row['HomeGoals'], row['AwayGoals'], row['Result'])
    
    def calc_standings(self, home_team_standings, away_team_standings, Match):
         # [match_plaed, wins, draws, losses, goals_for, goals_against, goals_diff, points]
         # [     0     ,  1  ,   2  ,    3  ,    4     ,       5      ,      6    ,  7    ]
         # [week, date, away_team, home_goals, away_goals, result]
         # [0   ,  1 ,      2    ,      3    ,     4     ,    5  ]
        # match played
        home_team_standings[0] += 1
        away_team_standings[0] += 1

        # goals_for, against
        home_team_standings[4] += Match[3]
        away_team_standings[5] += Match[3]
        home_team_standings[5] += Match[4]
        away_team_standings[4] += Match[4]

        # goals_diff
        home_team_standings[6] = (
            home_team_standings[4] - home_team_standings[5]
        )
        away_team_standings[6] = (
            away_team_standings[4] - away_team_standings[5]
        )

        # W, D, L, points
        if Match[5] == "A":
            away_team_standings[1] += 1
            away_team_standings[7] += 3
            home_team_standings[3] += 1
        elif Match[5] == "H":
            home_team_standings[1] += 1
            home_team_standings[7] += 3
            away_team_standings[3] += 1
        else:  # Draw
            away_team_standings[7] += 1
            away_team_standings[2] += 1
            home_team_standings[7] += 1
            home_team_standings[2] += 1
        
        return

    # [match_plaed, wins, draws, losses, goals_for, goals_against, goals_diff, points]
    # [     0     ,  1  ,   2  ,    3  ,    4     ,       5      ,      6    ,  7    ]
    # [week, date, away_team, home_goals, away_goals, result]
    # [0   ,  1 ,      2    ,      3    ,     4     ,    5  ]
    def BFS_round(self, round_number):
        standings = {team: [0] * 8 for team in self.all_teams}
        visited = [[False for j in range(20)] for i in range(20)]
        if round_number == 1:
            for team in self.all_teams[0:10]:
                Match = self.adj_list[team][1]
                away_team = Match[2]
                self.calc_standings(standings[team], standings[away_team], Match)
        else: 
            queue = deque()
            start_node = "Crystal Palace"
            queue.append(start_node)
            while queue:
                team = queue.popleft()
                Matchs = self.adj_list[team]
                for Match in Matchs[1:]:
                    home_team_index = self.all_teams.index(team)
                    away_team_index = self.all_teams.index(Match[2])
                    if not visited[home_team_index][away_team_index] and Match[0] <= round_number:
                        visited[home_team_index][away_team_index] = True
                        queue.append(Match[2])
                        self.calc_standings(standings[team], standings[Match[2]], Match)
        return standings
                       

    def BFS_date(self, date):
        standings = {team: [0] * 8 for team in self.all_teams}
        for team in self.all_teams:
                Matches = self.adj_list[team]
                for Match in Matches[1:]: 
                  if Match[1] <= date:
                    self.calc_standings(standings[team], standings[Match[2]], Match)
                  else:
                      break
        return standings

g = graph()
g.graph_initialization()

def print_standing(standing):
    Final_Standings = [[key] + value for key, value in standing.items()]
    Final_Standings = pd.DataFrame(Final_Standings,columns=['Team','MatchPlayed','W','D','L','G For','G Against','G Diff','Points'])
    Final_Standings = Final_Standings.sort_values(by='Points', ascending=False, ignore_index=True)
    print(Final_Standings.head(20))
    return


def solve():
    inp = input("Traverse using date or round no.? insert d or r: ")
    if inp.lower() == 'r':
        r = int(input("insert round no.: "))
        standing = g.BFS_round(r)
        print_standing(standing)
    elif inp.lower() == 'd':
        d = pd.to_datetime(input("insert date in format of DD/MM/YYYY: "), dayfirst=True)
        standing = g.BFS_date(d)
        print_standing(standing)
    else:
        print("Plz insert a valid input")

while 1:
    solve()
