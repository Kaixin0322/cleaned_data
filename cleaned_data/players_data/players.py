import pandas as pd

# Load the file
file_path = '/Users/sicilyx/Desktop/data/player/players.csv'
players_data = pd.read_csv(file_path)

# Overview of the original data, check basic data structure
print("Basic information of the original data:")
print(players_data.info())  # Display column information
print(players_data.describe())  # Display statistical information for numerical columns
print(players_data.head())  # Display the first few rows of data

# Check for missing values
missing_values = players_data.isnull().sum()
print("Overview of missing values:")
print(missing_values)

# 1. Handling missing values
# Fill missing values in the 'Origin' column, as the origin of players has a minimal effect on the ranking system, can be filled with 'Unknown'
players_data['Origin'].fillna('Unknown', inplace=True)

# 2. Handling duplicate data
# Check and remove duplicate rows
duplicates = players_data.duplicated().sum()
print(f'Number of duplicate rows: {duplicates}')
players_data = players_data.drop_duplicates()

# 3. Data type conversion
# Convert the 'Dob' column to datetime type and format it to 'YYYY-MM-DD' for Tableau compatibility
players_data['Dob'] = pd.to_datetime(players_data['Dob'], errors='coerce').dt.strftime('%Y-%m-%d')

# Ensure 'Height' and 'Weight' are numeric types
players_data['Height'] = players_data['Height'].astype(float)
players_data['Weight'] = players_data['Weight'].astype(float)

# 4. Handling outliers
# Check the statistical data for 'Height' and 'Weight' to identify any extreme values
print("Statistical description of numerical columns:")
print(players_data[['Height', 'Weight']].describe())

# Assume a reasonable height range of 150-240cm and a weight range of 50-180kg, remove records with unreasonable values
players_data = players_data[(players_data['Height'] >= 150) & (players_data['Height'] <= 240)]
players_data = players_data[(players_data['Weight'] >= 50) & (players_data['Weight'] <= 180)]

# 5. Standardizing column names
# Remove spaces from column names, and convert to lowercase
players_data.columns = players_data.columns.str.strip().str.lower().str.replace(' ', '_')

# Check the cleaned data
print("Overview of the cleaned data:")
print(players_data.info())
print(players_data.isnull().sum())

# Save the cleaned data with the correct date format for Tableau
cleaned_file_path = '/Users/sicilyx/Desktop/cleaned_players.csv'
players_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data saved to: {cleaned_file_path}")
