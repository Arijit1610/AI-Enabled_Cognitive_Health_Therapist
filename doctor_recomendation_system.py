# from sklearn.metrics.pairwise import linear_kernel
# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd
# from sklearn.preprocessing import StandardScaler, LabelEncoder

# encoding = 'ISO-8859-1'
# df = pd.read_csv('doctors_data.csv', encoding=encoding)

# # Data Cleaning

# # Normalize and Scale
# # scaler = StandardScaler()
# # df['experience_years'] = scaler.fit_transform(
# #     df['experience_years'].values.reshape(-1, 1))
# # df['patient_reviews'] = scaler.fit_transform(
# #     df['patient_reviews'].values.reshape(-1, 1))

# # Encoding Categorical Data
# label_encoder = LabelEncoder()
# # df['specialty'] = label_encoder.fit_transform(df['specialty'])
# # df['location'] = label_encoder.fit_transform(df['location'])
# # Text Data Processing
# df['languages_spoken'] = df['languages_spoken'].apply(
# 	lambda x: '|'.join(x.split(',')))

# # Feature Engineering
# df['average_rating'] = df['patient_reviews']


# # Display the preprocessed data
# # print(df.head())
# # import pandas as pd

# # Load the provided DataFrame
# # df = pd.read_csv('doctors_data.csv')  # Replace 'doctors_data.csv' with your CSV file

# # Preprocessing: Combine attributes into a single text feature for each doctor
# df["doctor_features"] = df["availability"] + " " + df["languages_spoken"] + \
# 	" " + df["specialty"].astype(str) + " " + df["average_rating"].astype(str)

# # Create a TF-IDF vectorizer to transform text features into numerical representations
# tfidf_vectorizer = TfidfVectorizer()
# tfidf_matrix = tfidf_vectorizer.fit_transform(df["doctor_features"])

# # Calculate cosine similarities between doctors
# cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)


# def recommend_doctors(preferred_specialty, language_preference, preferred_availability, preferred_location, top_n=10):
# 	# Mapping of numeric specialty labels to string values
# 	# specialty_mapping = {
# 	#    	0: "Psychologist",
# 	# 	1:"Psychiatrist",
# 	# 	2:"Psychiatric nurse",
# 	# 	3:"Psychotherapist" ,
# 	# 	4:"Mental health counselor",
# 	# 	5:"Family and marriage counselor"
# 	#     # Add more mappings as needed
# 	# }

# 	# Convert user's specialty preference to numeric label
# 	# user_specialty_numeric = list(specialty_mapping.keys())[list(
# 		# specialty_mapping.values()).index(preferred_specialty)]

# 	# Filter doctors based on user preferences
# 	filtered_doctors = df[df["location"] == preferred_location]
# 	if len(filtered_doctors) == 0:
# 		return "No doctors match your preferences."

# 	# Calculate scores for each doctor based on preferences
# 	scores = []

# 	for _, doctor in filtered_doctors.iterrows():
# 		score = 0
# 		# Specialty and language preferences are strict criteria
# 		if (doctor["specialty"] == preferred_specialty) and( language_preference in doctor["languages_spoken"]):
# 			score += 2

# 		# Rating is a strict criterion
# 		if doctor["average_rating"] >= 4.0:  # You can adjust the rating threshold as needed
# 			score += 1

# 		if preferred_availability in doctor["availability"]:
# 			score += 1

# 		# You can add more criteria and weights as needed

# 		scores.append((doctor["id"], score))

# 	# Sort doctors by score in descending order
# 	sorted_doctors = sorted(scores, key=lambda x: x[1], reverse=True)

# 	# Extract the top N recommended doctors
# 	recommended_doctors = [
# 		doctor_id for doctor_id, _ in sorted_doctors[:top_n]]

# 	return recommended_doctors

# # preferred_specialty = "Psychologist"  # User provides a string value
# # language_preference = "Bengali"
# # preferred_availability = "Monday"
# # preferred_location = "Kolkata"
# print("list of our specialist: Psychologist,Psychiatrist,Psychiatric nurse,Psychotherapist Mental health counselor, Family and marriage counselor")
# # Example usage:
# preferred_specialty = input("Enter your preferred specialty:")  # User provides a string value
# language_preference = input("Enter your prefered language: ")
# preferred_availability = input("Enter your available days: ")
# preferred_location = input("Enter your prefered location: ")

# recommended_doctors = recommend_doctors(
# 	preferred_specialty, language_preference, preferred_availability, preferred_location)

# print(f"Top recommended doctors for your preferences: {recommended_doctors}")
# print(df.iloc[recommended_doctors,[1,2,3,5,7]])

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

user_specialty = ["Anxiety and Stress Management","Depression and Mood Disorders" ]
label_encoders = {}
for column in ["specialty", "location"]:
	le = LabelEncoder()
	data[column] = le.fit_transform(data[column])
	label_encoders[column] = le

# Convert user preferences to numerical values using label encoders
user_specialty_encoded = label_encoders["specialty"].transform(user_specialty)
user_location_encoded = label_encoders["location"].transform([user_location])[0]
# Assuming there is only one language preference
user_language_encoded = 1 if user_languages_spoken[0] in set(language for languages_list in data["languages_spoken"].apply(eval) for language in languages_list) else 0

# Create a vector for the user's preferences
user_vector = user_specialty_encoded + [user_location_encoded]

# Check the lengths of the user-preferred days and doctor availability lists
user_preferred_days_list = eval(user_preferred_days)
data["availability_list"] = data["availability"].apply(eval)
data["availability_length"] = data["availability_list"].apply(len)

# Filter out doctors with availability lists that include all user-preferred days
filtered_data = data[data["availability_list"].apply(lambda x: set(user_preferred_days_list).issubset(set(x)))]

# Filter out doctors with the same location as the user's preferred location
filtered_data = filtered_data[filtered_data["location"] == user_location_encoded]

# Calculate Jaccard similarity between the user's preferred days and each doctor's availability
filtered_data["jaccard_similarity"] = filtered_data["availability_list"].apply(
    lambda x: jaccard_score(set(user_preferred_days_list), set(x), average='micro') if len(x) > 0 else 0
)

# Features used for Euclidean distance
distance_features = ["specialty", "location"]
filtered_data["distance"] = euclidean_distances([user_vector], filtered_data[distance_features])[0]

# Combine Jaccard similarity and Euclidean distance to get a combined score
filtered_data["combined_score"] = 0.7 * (1 - filtered_data["distance"]) + 0.3 * filtered_data["jaccard_similarity"]

# Sort the DataFrame by combined score
recommendations = filtered_data.sort_values(by=["combined_score"], ascending=[False]).head(10)
print(recommendations)
