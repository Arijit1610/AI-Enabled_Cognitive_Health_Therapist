import pandas as pd
encoding = 'ISO-8859-1'
data = pd.read_csv('doctors_data.csv', encoding=encoding)
print(data)
preferences = ["Anxiety and Stress Management", "Depression and Mood Disorders" , "Depression and Mood Disorders", "Anxiety and Stress Management"]
filtereddoc = data[(data['specialty'].isin(preferences))]
print(filtereddoc.head())