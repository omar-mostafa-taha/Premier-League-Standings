import pandas as pd
from collections import  deque    # 'dequeueue' class from 'collections' module can be used to implement a queueueue. 
data = pd.read_csv('epl_results.csv')
data.head()

# here we modify datatypes and clean the data
data['Date'] = pd.to_datetime(data['Date']) #,format='DD/MM/YYYY'
data = data[data['Result']!='-']
for col in ['W','HomeGoals','AwayGoals']:
    data[col] = data[col].astype(int)

print(data)

class graph:
    def __init__(self):
        self.num_teams = 20
        self.adj_list = {team: [] for team in data['HomeTeam'].head(10).tolist() + data['AwayTeam'].head(10).tolist()}
        # self.visited = [False] * (self.num_teams + 1)

    def add_edge(self, visited, week, date, home_team, away_team, home_goals, away_goals, result):
        if len(self.adj_list[home_team]) == 0:
            self.adj_list[home_team].append([])

        new_list = [visited ,week, date, away_team, home_goals, away_goals, result]
        self.adj_list[home_team].insert(week, new_list)

    def graph_initialization(self):
        for index, row in data.iterrows():
            # Access the values in each column of the current row
            visited = False
            round_number = (row['W'])
            match_date = row['Date']
            home_team = row['HomeTeam']
            away_team = row['AwayTeam']
            home_goals = row['HomeGoals']
            away_goals = row['AwayGoals']
            result = row['Result']
            self.add_edge(visited ,round_number, match_date, home_team, away_team, home_goals, away_goals, result)
    
    def calc_standings(self, round_number):
        queue =  deque()
        start_node = 'Crystal Palace'
        queue.append(start_node)
        while queue:
            node = queue.popleft()
            values = self.adj_list[node]
            for value in values[1:]:
                if not value[0]:
                    value[0] = True
                    queue.append(value[3])
        return


g = graph()
g.graph_initialization()
print("\n\n\n\t\t\t\t\t\t\t\t\tBefore BFS values[0] are set to False")
print(g.adj_list)

g.calc_standings(2)         # Function to traverse the graph using BFS and calc the standings
print("\n\n\n\n\t\t\t\t\t\t\t\t\tAfter BFS values[0] are set to True")
print(g.adj_list)
