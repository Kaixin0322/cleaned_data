import pandas as pd

# Load the game.csv file, replace with your actual file path
games_data = pd.read_csv('/Users/sicilyx/Desktop/data/game/games.csv')

# Overview of the raw data, check the basic structure of the data
print("Basic information of the raw data:")
print(games_data.info())  # Display basic information about the columns
print(games_data.describe())  # Show statistical information for numeric columns
print(games_data.head())  # Display the first 5 rows of the data

# Check unique values in the raw data
print("Unique value statistics in the raw data:")
print(games_data.nunique())

# Check for missing values in the raw data
missing_values_initial = games_data.isnull().sum()
print("Missing values in the raw data:")
print(missing_values_initial)

# Check if there are any duplicate rows in the data
duplicates_initial = games_data.duplicated().sum()
print(f'Number of duplicate rows in the raw data: {duplicates_initial}')

# Select the required columns
required_columns = ['GameId', 'Year', 'Round', 'Date', 'HomeTeam', 'AwayTeam', 
                    'HomeTeamScoreFT', 'AwayTeamScoreFT', 'Venue', 'Attendance', 
                    'MaxTemp', 'MinTemp', 'Rainfall']

filtered_games_data = games_data[required_columns]

# Filter data from 2012 to 2022
filtered_games_data = filtered_games_data[(filtered_games_data['Year'] >= 2012) & (filtered_games_data['Year'] <= 2022)]

# 1. Handling missing values
# Check for missing values
missing_values = filtered_games_data.isnull().sum()
print("Missing values before cleaning:", missing_values)

# Fill missing attendance with 0 and remove commas in numbers
filtered_games_data['Attendance'] = filtered_games_data['Attendance'].replace({',': ''}, regex=True).astype(float)
filtered_games_data['Attendance'].fillna(0, inplace=True)

# Fill missing temperature and rainfall data with column mean
filtered_games_data['MaxTemp'].fillna(filtered_games_data['MaxTemp'].mean(), inplace=True)
filtered_games_data['MinTemp'].fillna(filtered_games_data['MinTemp'].mean(), inplace=True)
filtered_games_data['Rainfall'].fillna(filtered_games_data['Rainfall'].mean(), inplace=True)

# 2. Handling duplicate data
# Check for duplicate rows
duplicates = filtered_games_data.duplicated().sum()
print(f'Number of duplicate rows: {duplicates}')

# Remove duplicate rows
filtered_games_data = filtered_games_data.drop_duplicates()

# 3. Convert data types
# Convert 'Date' column to datetime type
filtered_games_data['Date'] = pd.to_datetime(filtered_games_data['Date'], errors='coerce')

# Ensure scores and other numeric columns are of float type and round to two decimal places
filtered_games_data['HomeTeamScoreFT'] = filtered_games_data['HomeTeamScoreFT'].astype(float).round(2)
filtered_games_data['AwayTeamScoreFT'] = filtered_games_data['AwayTeamScoreFT'].astype(float).round(2)
filtered_games_data['MaxTemp'] = filtered_games_data['MaxTemp'].astype(float).round(2)
filtered_games_data['MinTemp'] = filtered_games_data['MinTemp'].astype(float).round(2)
filtered_games_data['Rainfall'] = filtered_games_data['Rainfall'].astype(float).round(2)

# 4. Handle outliers
# Check for outliers in Home and Away team scores
print(filtered_games_data[['HomeTeamScoreFT', 'AwayTeamScoreFT']].describe())

# Remove unreasonable scores, such as negative values
invalid_scores = filtered_games_data[(filtered_games_data['HomeTeamScoreFT'] < 0) | (filtered_games_data['AwayTeamScoreFT'] < 0)]
if not invalid_scores.empty:
    print("Found invalid scores:", invalid_scores)
filtered_games_data = filtered_games_data[(filtered_games_data['HomeTeamScoreFT'] >= 0) & (filtered_games_data['AwayTeamScoreFT'] >= 0)]

# Check for temperature outliers (e.g., below -5 degrees or above 50 degrees)
filtered_games_data = filtered_games_data[(filtered_games_data['MaxTemp'] <= 50) & (filtered_games_data['MinTemp'] >= -5)]

# 5. Standardize column names
# Strip spaces from column names, convert to lowercase, and replace spaces with underscores
filtered_games_data.columns = filtered_games_data.columns.str.strip().str.lower().str.replace(' ', '_')

# Check for missing values after cleaning
print("Missing values after cleaning:", filtered_games_data.isnull().sum())

# 6. Save cleaned data
# Save data for 2012-2017 and 2018-2022
games_2012_2017 = filtered_games_data[(filtered_games_data['year'] >= 2012) & (filtered_games_data['year'] <= 2017)]
games_2018_2022 = filtered_games_data[(filtered_games_data['year'] >= 2018) & (filtered_games_data['year'] <= 2022)]

games_2012_2017.to_csv('/Users/sicilyx/Desktop/data/cleaned_games_2012_2017.csv', index=False)
games_2018_2022.to_csv('/Users/sicilyx/Desktop/data/cleaned_games_2018_2022.csv', index=False)

print("Cleaned data has been saved successfully with values rounded to two decimal places.")
