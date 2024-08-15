import nltk
from nltk.corpus import stopwords
import spacy
import spacy.displacy
from spacy.tokens import DocBin
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
import re
import json
import random
from mlmain import model
import joblib
from sklearn.pipeline import Pipeline
from typing import Optional, Dict, List, Tuple
from pydantic import BaseModel, Field, ValidationError




# Load the trained model
pipeline = joblib.load('trained_model.pkl')

# Function to predict intent
def predict_intent(text):
    # Predict the intent for a given text
    prediction = pipeline.predict([text])
    return prediction[0]


# Download NLTK resources (only needs to be done once)
nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load('en_core_web_lg')
db=DocBin()
custom_nlp = spacy.blank('en')
with open('custom_ner_file.json') as f:
    data = json.load(f)

# Process each annotation in the dataset
for item in data['annotations']:
    text = item[0]  # Text of the document
    annotations = item[1]  # Annotations for entities

    # Create a SpaCy Doc object
    doc = custom_nlp(text)

    # Extract entities and create spans
    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            ents.append(span)
    
    # Set the entities for the doc
    doc.ents = ents
    

    # Add the doc to the DocBin
    db.add(doc)

# Save the DocBin object to disk
db.to_disk("./custom_ner.spacy")

# def preprocess_text(text):
#     text = re.sub(r'\s+', ' ', text).strip()
#     nlp_ner = spacy.load('model-best')
#     doc = nlp_ner(text)
    
    
#     # intent = identify_intent(text)
#     intent = predict_intent(text)
#     print(intent)

#     response = {
#         "text": text,
#         "intent": intent,
#         "entities": [(ent.text, ent.label_) for ent in doc.ents],
#         "tokens": [token.text for token in doc]
#     }
#     # print(response['entities'])
#     # return response['entities']
#     # Add a greeting response if the intent is a greeting
#     if intent == 'greeting':
#         greeting_vocab = ['hello', 'hi', 'greetings', 'hey', 'hola']
#         random_ = random.choice(greeting_vocab)
#         print(random_)
#         response['response'] =random.choice(greeting_vocab)
#     elif intent == "schedule_appointment":

#         print(prompt_for_missing_values(response['entities']))
#         return(prompt_for_missing_values(response['entities']))
        
#     elif intent == "cancel_appointment":
#         print(prompt_for_missing_values(response['entities']))
#         return(prompt_for_missing_values(response['entities']))
#     elif intent == "update_appointment":
#         print(prompt_for_missing_values(response['entities']))
#         return(prompt_for_missing_values(response['entities']))
#     else:
#         response['response']="sorry i didnt get it"
#         return response['response']

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    nlp_ner = spacy.load('model-best')
    doc = nlp_ner(text)

    # Identify the intent using the trained model
    intent = predict_intent(text)
    print("Identified Intent:", intent)

    response = {
        "text": text,
        "intent": intent,
        "entities": [(ent.text, ent.label_) for ent in doc.ents],
        "tokens": [token.text for token in doc]
    }
    context_data = {
        "appointment_details" : "",
        "flow":""
    }
    # Add a greeting response if the intent is a greeting
    if intent == 'greeting':
        greeting_vocab = ['hello', 'hi', 'greetings', 'hey', 'hola']
        random_ = random.choice(greeting_vocab)
        print(random_)
        context_data['response'] = random_
        context_data['flow'] = "greeting_flow"
    elif intent in ["schedule_appointment", "cancel_appointment", "update_appointment","fetch_appointment"]:
        appointment_details = prompt_for_missing_values(response['entities'])
        context_data['appointment_details'] = appointment_details
        context_data['flow'] = f"{intent}_flow"
    else:
        context_data['response'] = "Sorry, I didn't get it"
        context_data['flow'] = "unknown_flow"

    # Send the response dictionary to the frontend
    print("context_data",context_data)
    return context_data


greeting_words = {'hello', 'hi', 'greetings', 'hey', 'hola'}
def identify_intent(text: str) -> str:
    # Tokenize text using NLTK
    tokens = word_tokenize(text.lower())
    
    # Check for greeting words
    if any(word in greeting_words for word in tokens):
        return 'greeting'
    
    return 'unknown'


class Appointment(BaseModel):
    Doctor_name: Optional[str] = Field(default=None, description="Doctor's name")
    Patient_name: Optional[str] = Field(default=None, description="Patient's name")
    Appointment_type: Optional[str] = Field(default=None, description="Type of the appointment")
    Date_time: Optional[str] = Field(default=None, description="Date and time of the appointment")
    patient_mobile: Optional[str] = Field(default=None, description="Patient's mobile number")

def gather_details(entities: Dict[str, str]) -> BaseModel:
    # Extract details from the dictionary, ensuring correct labels
    appointment = Appointment(
        Doctor_name=next((ent for ent, label in entities.items() if label == "DOCTOR_NAME"), None),
        Patient_name=next((ent for ent, label in entities.items() if label == "PATIENT_NAME"), None),
        Appointment_type=next((ent for ent, label in entities.items() if label == "APPOINTMENT_TYPE"), None),
        Date_time=next((ent for ent, label in entities.items() if label == "DATE_TIME"), None),
        patient_mobile=next((ent for ent, label in entities.items() if label == "PHONE_NUMBER"), None)
    )
    
    return dict(appointment)

def prompt_for_missing_values(Entities):
    Entities = dict(Entities)
    appointment_details = gather_details(Entities)
    print(appointment_details)
    return appointment_details



    