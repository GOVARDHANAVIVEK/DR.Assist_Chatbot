from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional, Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from nlp import preprocess_text
from database.db import collection
from pymongo.errors import PyMongoError
app = FastAPI()

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent

# Define the path for static files
STATIC_DIR = BASE_DIR / "static"

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = STATIC_DIR / "index.html"
    with open(index_file, "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

class Message(BaseModel):
    text: str

class AppointmentDetails(BaseModel):
    Doctor_name: Optional[str] = None
    Patient_name: Optional[str] = None
    Appointment_type: Optional[str] = None
    Date_time: Optional[str] = None
    Patient_mobile: Optional[str] = None

@app.post("/track_intent/")
async def handle_initial_message(message:Message):
    try:
        data_item= preprocess_text(message.text)
        intent =data_item['flow']
        extracted_entities = data_item['appointment_details']
        
        # Create an AppointmentDetails instance with the extracted entities
        appointment_details = AppointmentDetails(**extracted_entities)
        print({"appointment_details": appointment_details.dict(), "intent": intent})
        
        # Return the appointment details along with the identified intent
        return {"response": appointment_details.dict(), "intent": intent}
    #     return{"intent":intent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/send_message/')
async def handle_message(message: Message):
    try:
        # Call preprocess_text and unpack its return values
        extracted_context = preprocess_text(message.text)
        intent =extracted_context['flow']
        extracted_entities = extracted_context['appointment_details']
        
        # Create an AppointmentDetails instance with the extracted entities
        appointment_details = AppointmentDetails(**extracted_entities)
        print({"appointment_details": appointment_details.dict(), "intent": intent})
        
        # Return the appointment details along with the identified intent
        return {"response": appointment_details.dict(), "intent": intent}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/schedule_appointment/')
async def schedule__user_appointment(appointment: AppointmentDetails):
    try:
        print("appointment details",appointment.dict())
        # formatted_date_time = parse_datetime(appointment.Date_time)
        appointment_dict = appointment.dict()
        # appointment_dict['Date_time'] = formatted_date_time
        # print("formatted date = ",appointment_dict['Date_time'])
        status,message = add_appointment(appointment_dict)
        print(status,message)
        if status == 200:
            return {"message":message}
        else:
            return {"message":message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PhoneNumber(BaseModel):
    Patient_mobile: str

@app.post('/cancel_appointment/')
async def cancel_user_appointment(phone_number: PhoneNumber):
    try:
        status, message = remove_appointment(phone_number.Patient_mobile)
        if status == 200:
            return {"message": message}
        else:
            raise HTTPException(status_code=status, detail=message)
    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/fetch_appointment/')
async def fetch_user_appointmnet(phone_number: PhoneNumber):
    details_fetched = AppointmentDetails()
    print("details fetched",details_fetched)
    try:

        status,data= fetch_appointment_details(phone_number.Patient_mobile)
        print("statucode",status,"data",data)
        if status == 200:
            # Update the appointment details object with fetched data
            details_fetched.Doctor_name = data.get('Doctor_name')
            details_fetched.Patient_name = data.get('Patient_name')
            details_fetched.Appointment_type = data.get('Appointment_type')
            details_fetched.Date_time = data.get('Date_time')
            details_fetched.Patient_mobile = data.get('Patient_mobile')
            print(details_fetched.dict())
            return {"status_code":200,"response": details_fetched.dict()}
        else:
            return {"status_code":404,"response":data}
    except Exception as e:
        # Log the exception for debugging
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/update_appointment/')
async def update_user_appointment(appointment:AppointmentDetails):
    try:
        print("appointment details",appointment)
        # formatted_date_time = parse_datetime(appointment.Date_time)

        appointment_dict = appointment.dict()
        status,message = update_appointment(appointment_dict)
        print(status,message)
        if status == 200:
            return {"message":message}
        else:
            return {"message":message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_appointment(appointment_dict):
    try:
        print(appointment_dict)
        phone_number = appointment_dict['Patient_mobile']
        print(phone_number)

        user_found = collection.find_one({"Patient_mobile": phone_number})
        if user_found:
            updated_data = collection.update_one(
                {"Patient_mobile": phone_number},  # Query
                {"$set": {
                    "Doctor_name": appointment_dict.get('Doctor_name'),
                    "Patient_name": appointment_dict.get('Patient_name'),
                    "Appointment_type": appointment_dict.get('Appointment_type'),
                    "Date_time": appointment_dict.get('Date_time'),
                    "Patient_mobile": appointment_dict.get('Patient_mobile')
                }}
            )
            print(updated_data)

            if updated_data.modified_count > 0:
                return (200,"Appointment Updated Successfully")
            else:
                return (400,"Appointment Updation Failed.")
        else:
            return (404,"No user found.")
    except PyMongoError as e:
        print(f"Database error: {e}")
        return {"status_code": 500, "message": "Internal Server Error, try again later"}


def fetch_appointment_details(user_number: str):
    try:
        user_found = collection.find_one({"Patient_mobile": user_number})
        if user_found:
            print(type(user_found))
            return (200,user_found)
        return 404,"No Appointment found"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
def remove_appointment(user_number: str):
    try:
        # Find appointment by patient_mobile
        user_found = collection.find_one({"Patient_mobile": user_number})
        if user_found:
            # Delete appointment
            collection.delete_one({"Patient_mobile": user_number})
            return 200, "Appointment has been cancelled."
        else:
            return 404, "Appointment not found."
    except PyMongoError as e:
        # Log the exception for debugging
        print(f"Database error: {e}")
        return 500, str("Internal Server Error , try again later")

def add_appointment(appointment):
    try:
        collection_name = collection
        collection_name.insert_one(appointment)  # Note: `insert_one` not `insertOne`
        return {200,"Appointment added successfully"}
    except PyMongoError as e:
        return {500,str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
