import pandas as pd
encoding = 'ISO-8859-1'
data = pd.read_csv('doctors_data.csv', encoding=encoding)
# print(data)
preferences = ["Anxiety and Stress Management", "Depression and Mood Disorders" , "Anger Management"]
location = ["Kolkata"]
filtereddoc = data[(data['specialty'].isin(preferences)) & (data['location'].isin(location))]
# print(filtereddoc.head())
filtereddoc['score'] = 2
