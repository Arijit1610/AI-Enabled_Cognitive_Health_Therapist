import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import euclidean_distances

# Load the data from the CSV file
encoding = 'ISO-8859-1'
data = pd.read_csv('doctors_data.csv', encoding=encoding)
user_location = "Kolkata"
user_preferred_days = "['Monday', 'Friday']"

# Assuming there is only one language preference
user_languages_spoken = "['Bengali']"

user_specialties = ["Anxiety and Stress Management", "Depression and Mood Disorders"]
label_encoders = {}
for column in ["specialty", "location"]:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Convert user preferences to numerical values using label encoders
user_specialties_encoded = label_encoders["specialty"].transform(user_specialties)
user_location_encoded = label_encoders["location"].transform([user_location])[0]

# Assuming there is only one language preference
user_language_encoded = 1 if user_languages_spoken[0] in set(language for languages_list in data["languages_spoken"].apply(eval) for language in languages_list) else 0

# Create a vector for the user's preferences
user_vector = [user_specialties_encoded[0], user_location_encoded]

# Check the lengths of the user-preferred days and doctor availability lists
user_preferred_days_list = eval(user_preferred_days)
data["availability_list"] = data["availability"].apply(eval)
data["availability_length"] = data["availability_list"].apply(len)

# Filter out doctors with availability lists of the same length as the user's preferred days list
filtered_data = data[data["availability_length"] == len(user_preferred_days_list)]

# Filter out doctors with the same location as the user's preferred location
filtered_data = filtered_data[filtered_data["location"] == user_location_encoded]

# Calculate Jaccard similarity between the user's preferred days and each doctor's availability
filtered_data["jaccard_similarity"] = filtered_data["availability_list"].apply(
    lambda x: jaccard_score(user_preferred_days_list, x, average='micro')
)

# Features used for Euclidean distance
distance_features = ["specialty", "location"]
filtered_data["distance"] = euclidean_distances([user_vector], filtered_data[distance_features])[0]

# Combine Jaccard similarity and Euclidean distance to get a combined score
filtered_data["combined_score"] = 0.7 * (1 - filtered_data["distance"]) + 0.3 * filtered_data["jaccard_similarity"]

# Sort the DataFrame by experience, rating, and combined score
recommendations = filtered_data.sort_values(by=["combined_score"], ascending=[False])
print(recommendations)

# Display the recommended doctors
print("Recommended Doctors:")
print(recommendations[["name", "specialty", "location", "languages_spoken", "availability", "experience_years", "patient_reviews"]])
