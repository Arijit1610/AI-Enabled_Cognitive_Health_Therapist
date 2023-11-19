import csv
import random
import faker

# Initialize the Faker library with an Indian locale
fake = faker.Faker('en_IN')

doctors = []

# Generate data for 100 doctors
for i in range(1, 501):
    # Create a list of unique languages
    unique_languages = list(set(fake.random_elements(elements=(
        "English", "Hindi", "Marathi", "Tamil", "Bengali", "Telugu"), length=random.randint(1, 4))))
    unique_availability = list(set(fake.random_elements(elements=(
        "Monday", "Tuesday", "Thursday", "Wednesday", "Friday"), length=random.randint(1, 4))))
    # Shuffle the list to randomize the order
    random.shuffle(unique_languages)
    random.shuffle(unique_availability)

    doctor = {
        "id": i,
        "docid": f"doc{i}",
        "name": fake.name(),
        "specialty": random.choice(["Anxiety and Stress Management",
                                    "Family and Relationship Counseling",
                                    "Depression and Mood Disorders",
                                    "Marriage and Couples Counseling"
                                    "Trauma and PTSD",
                                    "Child and Adolescent Counseling",
                                    "Grief and Loss Counseling",
                                    "Substance Abuse and Addiction",
                                    "Couples Therapy",
                                    "Eating Disorders",
                                    "Anger Management",
                                    "Autism Spectrum Disorders"]),
        "PhoneNumber": random.randint(9000000000, 9999999999),
        "location": random.choice(["New Delhi", "Kolkata", "Chennai", "Mumbai", "Jaipur", "Lucknow", "Kanpur"]),
        "experience_years": random.randint(5, 40),
        "patient_reviews": round(random.uniform(3.5, 5.0), 1),
        "availability": unique_availability,
        "languages_spoken": unique_languages
    }
    doctors.append(doctor)
#New Delhi, Kolkata, Chennai, Mumbai, Jaipur, Lucknow, Kanpur
# Define the CSV file name
csv_file = "doctors_data.csv"

# Write the data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=doctors[0].keys())
    writer.writeheader()
    writer.writerows(doctors)

print(f"Data saved to '{csv_file}'.")
