import csv

def ReadFile(file_name):
    # Create an empty list to hold the contents of the CSV file
    content = []
    
    # Open the file using the csv module
    with open(file_name, 'r') as input_file:
    # Create a CSV reader object
      reader = csv.reader(input_file)

    # Ignore the first line of the file (header row)
      next(reader)

    # Read in each line of the CSV file
      for line in reader:
        round, date, home_team, away_team, home_goals, away_goals, result = line
        content.append(line)
        # Convert the numeric fields to integers
        try:
            home_goals = int(home_goals)
            away_goals = int(away_goals)
        except ValueError:
            print(f"Invalid integer value for home goals or away goals in line: {line}")
            continue
        
    # Return the 2D list of strings
    return content


content = ReadFile("epl_results.csv")
print(content[0][0])