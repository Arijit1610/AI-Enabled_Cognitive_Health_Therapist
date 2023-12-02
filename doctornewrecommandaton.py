import pandas as pd
encoding = 'ISO-8859-1'
data = pd.read_csv('doctors_data.csv', encoding=encoding)
print(data)
preferences = ["Anxiety and Stress Management", "Depression and Mood Disorders" , "Depression and Mood Disorders", "Anxiety and Stress Management"]
filtereddoc = data[(data['specialty'].isin(preferences))]
print(filtereddoc.head())

import pandas as pd
encoding = 'ISO-8859-1'
data = pd.read_csv('doctors_data.csv', encoding=encoding)
# print(data)
preferences = ["Anxiety and Stress Management", "Depression and Mood Disorders" , "Anger Management"]
location = ["Kolkata"]
filtereddoc = data[(data['specialty'].isin(preferences)) & (data['location'].isin(location))]
# print(filtereddoc.head())
filtereddoc['score'] = 2
for index, row in filtereddoc.iterrows():
    if 'Bengali' in row['languages_spoken']:
        filtereddoc.at[index, 'score'] += 1
filtereddoc
from datetime import datetime, timedelta

def get_current_and_next_day():
    # Get the current date
    current_date = datetime.now()
    if current_date.weekday() in [5, 6]:  # Saturday is 5, Sunday is 6
            # If it's Saturday or Sunday, set next day to Monday
            current_date = current_date + timedelta(days=(7 - current_date.weekday()))
    # If it's Friday, set next day to Monday
    if current_date.weekday() == 4:  # Friday is 4
        next_day = current_date + timedelta(days=3)  # 3 days to reach Monday
    else:
        # Calculate the next day
        next_day = current_date + timedelta(days=1)

        # Check if the next day is Saturday or Sunday
        if next_day.weekday() in [5, 6]:  # Saturday is 5, Sunday is 6
            # If it's Saturday or Sunday, set next day to Monday
            next_day = current_date + timedelta(days=(7 - current_date.weekday()))

    # Create a list containing the current day and the next day
    days_list = [current_date.strftime('%A'), next_day.strftime('%A')]

    return days_list

# Call the function
result = get_current_and_next_day()

# Print the result
print(result)
for index, row in filtereddoc.iterrows():
    if any(day in row['availability'] for day in result):
        filtereddoc.at[index, 'score'] += 1
filtereddoc.sort_values(by=['score','experience_years','patient_reviews'], ascending=False)