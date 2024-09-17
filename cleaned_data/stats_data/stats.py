import pandas as pd

# Load the player game statistics data file
file_path = '/Users/sicilyx/Desktop/data/stats.csv'
stats_data = pd.read_csv(file_path)

# 1. Overview of the raw data
print("Basic information of the raw data:")
print(stats_data.info())  # Display column information of the data
print(stats_data.describe())  # Display statistics for numeric columns
print(stats_data.head())  # Show the first few rows of the data

# 2. Check for missing values
missing_values = stats_data.isnull().sum()
print("Overview of missing values:")
print(missing_values)

# 3. Handle missing values
# For the 'Subs' column, fill missing values with 'Unknown'
stats_data['Subs'].fillna('Unknown', inplace=True)

# 4. Handle duplicate data
# Check and remove duplicate rows
duplicates = stats_data.duplicated().sum()
print(f'Number of duplicate rows: {duplicates}')
stats_data = stats_data.drop_duplicates()

# 5. Convert data types
# Ensure numeric columns are of float or integer type
numeric_columns = ['Disposals', 'Kicks', 'Marks', 'Handballs', 'Goals', 'Behinds', 'HitOuts', 
                   'Tackles', 'Rebounds', 'Inside50s', 'Clearances', 'Clangers', 'Frees', 
                   'FreesAgainst', 'BrownlowVotes', 'ContestedPossessions', 'UncontestedPossessions', 
                   'ContestedMarks', 'MarksInside50', 'OnePercenters', 'Bounces', 'GoalAssists', 
                   '%Played']

for col in numeric_columns:
    stats_data[col] = pd.to_numeric(stats_data[col], errors='coerce')

# 6. Handle outliers
# For example: assume reasonable goal counts are between 0 and 15, and play percentages do not exceed 100%
stats_data = stats_data[(stats_data['Goals'] >= 0) & (stats_data['Goals'] <= 15)]
stats_data = stats_data[(stats_data['%Played'] >= 0) & (stats_data['%Played'] <= 100)]

# 7. Standardize column names
# Strip spaces from column names and convert them to lowercase
stats_data.columns = stats_data.columns.str.strip().str.lower().str.replace(' ', '_')

# Check the cleaned data
print("Overview of the cleaned data:")
print(stats_data.info())
print(stats_data.isnull().sum())

# 8. Save the cleaned data
cleaned_file_path = '/Users/sicilyx/Desktop/cleaned_stats.csv'
stats_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data has been saved to: {cleaned_file_path}")
