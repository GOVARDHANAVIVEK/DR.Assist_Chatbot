data = {
    "text": [
        # Scheduling an Appointment
        "I’d like to schedule a General Check-up with Dr. Smith on August 10, 2024, at 10:30 AM. My name is John Doe and my mobile number is 123-456-7890.",
        "Can you book a Dental Cleaning for Alice Johnson with Dr. Brown on August 12, 2024, at 2:00 PM? My contact number is 987-654-3210.",
        "I want to make an appointment for an Eye Examination with Dr. Lee on August 15, 2024, at 11:00 AM. My phone number is 555-123-4567.",
        "Please schedule a Pediatric Visit for Emily Davis with Dr. Wilson on August 20, 2024, at 1:00 PM. My mobile number is 444-555-6666.",
        "Schedule an appointment with Dr. Green for a Physical Examination on September 1, 2024, at 8:00 AM.",
        "I want to book a follow-up visit with Dr. Anderson on September 5, 2024, at 3:00 PM.",
        "I need to schedule a General Check-up with Dr. Smith on August 10, 2024, at 10:30 AM.",
        "Book a consultation with Dr. Taylor on September 15, 2024, at 4:00 PM.",
        "Can you set up a meeting with Dr. Johnson for a Flu Shot on August 25, 2024, at 9:00 AM?",
        "I’d like to reserve a slot with Dr. Brown for a Routine Physical Examination on August 30, 2024, at 2:00 PM.",
        
        # Canceling an Appointment
        "I need to cancel my Routine Physical Examination with Dr. Taylor on August 18, 2024, at 9:00 AM. My name is Michael Clark and my mobile number is 222-333-4444.",
        "Please cancel my Flu Shot appointment with Dr. Thompson on August 22, 2024, at 3:00 PM.",
        "I’d like to cancel the Dermatology Consultation with Dr. Harris on August 25, 2024, at 4:30 PM. My name is Laura Martinez and my phone number is 666-777-8888.",
        "Can you cancel my General Check-up with Dr. Miller on August 30, 2024, at 10:00 AM?",
        "Cancel my appointment with Dr. White on September 10, 2024, at 11:00 AM.",
        "I need to cancel the Cardiology Consultation with Dr. Miller scheduled for September 12, 2024, at 2:00 PM.",
        "Remove my appointment with Dr. Harris on August 19, 2024, at 10:00 AM.",
        "I’d like to cancel the follow-up visit with Dr. Anderson scheduled for September 5, 2024, at 3:00 PM.",
        "Please remove my Flu Shot appointment with Dr. Brown on August 30, 2024.",
        "I want to cancel the Dermatology Consultation with Dr. Smith on August 12, 2024.",
        
        # Updating an Appointment
        "I need to reschedule my Eye Examination with Dr. Davis. Move it to August 12, 2024, at 2:00 PM. My name is Rachel Adams and my mobile number is 555-666-7777.",
        "Can you change my Dental Cleaning appointment with Dr. Johnson to August 17, 2024, at 11:00 AM? My contact number is 444-555-6666.",
        "Please update my Pediatric Visit with Dr. Carter to August 22, 2024, at 9:30 AM. My name is Daniel Walker and my phone number is 777-888-9999.",
        "I’d like to modify my Routine Physical Examination with Dr. White. New date: August 28, 2024, new time: 3:00 PM. My mobile number is 888-999-0000.",
        "Change the date of my Eye Examination with Dr. Davis to August 12, 2024, and the time to 2:00 PM.",
        "Update my Dental Cleaning appointment to August 17, 2024, at 11:00 AM.",
        "Adjust the timing of my Pediatric Visit with Dr. Carter to August 22, 2024, at 9:30 AM.",
        "Reschedule my General Check-up with Dr. Smith to August 10, 2024, at 10:30 AM.",
        "Modify my appointment with Dr. Taylor to August 18, 2024, at 9:00 AM.",
        "Update my consultation with Dr. Green to September 1, 2024, at 8:00 AM.",


        #fetching or viewing
        "view appointment status","fetch my appointment","view my status","fetch appointment","view appointment"
        
    ],
    "intent": [
        # Scheduling an Appointment
        'schedule_appointment', 'schedule_appointment', 'schedule_appointment', 
        'schedule_appointment', 'schedule_appointment', 'schedule_appointment', 
        'schedule_appointment', 'schedule_appointment', 'schedule_appointment', 
        'schedule_appointment',
        
        # Canceling an Appointment
        'cancel_appointment', 'cancel_appointment', 'cancel_appointment', 
        'cancel_appointment', 'cancel_appointment', 'cancel_appointment',
        'cancel_appointment', 'cancel_appointment', 'cancel_appointment',
        'cancel_appointment',
        
        # Updating an Appointment
        'update_appointment', 'update_appointment', 'update_appointment', 
        'update_appointment', 'update_appointment', 'update_appointment', 
        'update_appointment', 'update_appointment', 'update_appointment',
        'update_appointment',
        
        #fetch appointment
        'fetch_appointment','fetch_appointment','fetch_appointment','fetch_appointment','fetch_appointment'

    ]
}

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
import pandas as pd

df = pd.DataFrame(data)
print(df)



# Convert text data into numerical data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['intent']

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['intent'], test_size=0.2, random_state=42)


pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

import joblib

# Train the model
model = pipeline

# Save the trained pipeline to a file
joblib.dump(model, 'trained_model.pkl')