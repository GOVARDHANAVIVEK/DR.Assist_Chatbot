let appointmentDetails = {};
let intent_tracking = "";

document.addEventListener("DOMContentLoaded", function() {
    
    
    setTimeout(function() {
        addMessage("Welcome to DR.Assist! How can I help you today?", 'bot-message');
    }, 2000);
});

// function addMessage(message, className,appointmentDetails=null) {
//     const chatBody = document.getElementById('chat-body');
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add(className);

//     const messageContent = document.createElement('div');
//     messageContent.classList.add('message');

//     messageContent.textContent = message;
//     messageDiv.appendChild(messageContent);
//     chatBody.appendChild(messageDiv);

//     // Scroll to the bottom of the chat body
//     chatBody.scrollTop = chatBody.scrollHeight;
    
//     if (message=="fetching appointment" && className =='bot-message') {
//         if(appointmentDetails){
//             console.log(appointmentDetails)
//         const appointmentCard = document.getElementById('appointment-card');
//         appointmentCard.innerHTML = `
        
//             <h2>Appointment Details</h2>
//             <div class="appointment-detail">
//                 <strong>Patient Name:</strong> <span>${appointmentDetails.Patient_name}</span>
//             </div>
//             <div class="appointment-detail">
//                 <strong>Patient Mobile:</strong> <span>${appointmentDetails.Patient_mobile}</span>
//             </div>
//             <div class="appointment-detail">
//                 <strong>Appointment Type:</strong> <span>${appointmentDetails.Appointment_type}</span>
//             </div>
//             <div class="appointment-detail">
//                 <strong>Doctor Name:</strong> <span>${appointmentDetails.Doctor_name}</span>
//             </div>
//             <div class="appointment-detail">
//                 <strong>Date & Time:</strong> <span>${appointmentDetails.Date_time}</span>
//             </div>
//         `;
//         appointmentCard.classList.remove('hidden');
//     } else {
//         const appointmentCard = document.getElementById('appointment-card');
//         appointmentCard.classList.add('hidden');
//     }
// }
// }
function addMessage(message, className, appointmentDetails = null) {
    const chatBody = document.getElementById('chat-body');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(className);

    // Clear any existing content in messageDiv
   

    if (message === "fetching appointment" && className === 'bot-message') {
        messageDiv.innerHTML = '';
        if (appointmentDetails) {
            // Create the appointment card HTML
            const appointmentCardHTML = `
                <div class="appointment-card">
                    <h2>Appointment Details</h2>
                    <div class="appointment-detail">
                        <strong>Patient Name:</strong> <span>${appointmentDetails.Patient_name}</span>
                    </div>
                    <div class="appointment-detail">
                        <strong>Patient Mobile:</strong> <span>${appointmentDetails.Patient_mobile}</span>
                    </div>
                    <div class="appointment-detail">
                        <strong>Appointment Type:</strong> <span>${appointmentDetails.Appointment_type}</span>
                    </div>
                    <div class="appointment-detail">
                        <strong>Doctor Name:</strong> <span>${appointmentDetails.Doctor_name}</span>
                    </div>
                    <div class="appointment-detail">
                        <strong>Date & Time:</strong> <span>${appointmentDetails.Date_time}</span>
                    </div>
                </div>
            `;
    
            // Set the appointment card HTML as the message content
            messageDiv.innerHTML = appointmentCardHTML;
        } else {
            // If no appointment details are available, show a fallback message
            messageDiv.innerHTML = '<div class="message">No appointment details available.</div>';
        }
    } else {
        // For other messages
        const messageContent = document.createElement('div');
        messageContent.classList.add('message');
        messageContent.textContent = message;
        messageDiv.appendChild(messageContent);
    }

    chatBody.appendChild(messageDiv);

    // Scroll to the bottom of the chat body
    chatBody.scrollTop = chatBody.scrollHeight;
}


document.getElementById("chat-button").addEventListener("click", function () {
    document.getElementById('chat-window').classList.toggle('hidden');
    document.getElementById("chat-button").style.display = "none";
});

document.getElementById("close-chat").addEventListener("click", function () {
    location.reload();
    document.getElementById("chat-window").classList.add("hidden");
    document.getElementById("chat-button").style.display = "block";
});
function showForm() {
    document.getElementById('form-container').classList.remove('hidden');
    document.getElementById('chat-body').scrollTop = document.getElementById('chat-body').scrollHeight; // Scroll to bottom
}
function hideForm() {
    document.getElementById('form-container').classList.add('hidden');
}
document.getElementById("send-button").addEventListener("click", async function () {
    const userInput = document.getElementById("chat-input").value;
      
    if (userInput) {
        addMessage(userInput, 'user-message');

        if(!intent_tracking){
            intent_tracking = await track_intent(userInput);
            console.log(intent_tracking)
        }
        
        switch(intent_tracking) {
            case "fetch_appointment_flow":
                handleFetchAppointment(userInput)
                break;
            case "schedule_appointment_flow":
                handleScheduleAppointment(userInput);
                break;
            case "cancel_appointment_flow":
                handleCancelAppointment(userInput);
                break;
            case "update_appointment_flow":
                handleUpdateAppointment(userInput);
                break;
            default:
                addMessage("I'm sorry, I didn't understand that. Can you please clarify?", 'bot-message');
        }

        document.getElementById("chat-input").value = ""; // Clear input field
    }
});

function handleFetchAppointment(userInput){
    if (isNaN(Number(userInput))) {
        addMessage("Please provide your mobile number to fetch your appointment details", 'bot-message');
    } else {
        appointmentDetails.Patient_mobile = userInput;
        FetchDetails(appointmentDetails);
    }
}

document.getElementById("chat-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        document.getElementById("send-button").click();
    }
});

async function track_intent(utterance) {
    try {
        const response = await fetch('/track_intent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: utterance })
        });
        const data = await response.json();
        appointmentDetails = data.response;
        return data.intent || "";
    } catch (error) {
        console.error('Error tracking intent:', error);
        addMessage("Sorry, something went wrong. Please try again.", 'bot-message');
        return "";
    }
}

async function ScheduleAppointment() {
    try {
        const response = await fetch('/schedule_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appointmentDetails)
        });

        // Wait for the JSON response
        const data = await response.json(); 
        console.log("Received data:", data);

        if (response.ok && data) {
            addMessage(data.message, 'bot-message');
            end_of_dialog();
        } else {
            addMessage("Failed to schedule the appointment. Please try again.", 'bot-message');
        }
    } catch (error) {
        console.error('Error scheduling appointment:', error);
        addMessage("Sorry, something went wrong. Please try again.", 'bot-message');
    }
}

let isFirstInteraction = true; // Flag to track the first interaction
let missing_found = false;

function handleScheduleAppointment(userInput) {
    // Skip the first interaction
    if (isFirstInteraction) {
        isFirstInteraction = false;
        addMessage("Great! Let's gather the necessary details for scheduling your appointment.", 'bot-message');
        missing_found = checkForMissingValues();
        return;
    }

    if (Object.keys(appointmentDetails).length === 0) {
        sendMessage(userInput);
    } else {
        console.log("missing", missing_found);
        if (missing_found) {
            for (const [key, value] of Object.entries(appointmentDetails)) {
                if (!value) {
                    appointmentDetails[key] = userInput;
                    missing_found = checkForMissingValues(); // Recheck for missing values after updating
                    break;
                }
            }
        } 

        // If no more missing values, proceed to schedule the appointment
        if (!missing_found) {
            ScheduleAppointment();
        }
    }
}

function checkForMissingValues() {
    for (const [key, value] of Object.entries(appointmentDetails)) {
        if (!value) {
            addMessage(`Please provide ${key.replace('_', ' ')}:`, 'bot-message');
            return true; // Return true if a missing value is found
        }
    }
    return false; // Return false if no missing values are found
}


function checkForMobileNumberForCancellation() {
    if (!appointmentDetails.Patient_mobile) {
        addMessage("Please provide your mobile number to cancel the appointment:", 'bot-message');

    }
    return false;
}
function assignValue(value) {
    appointmentDetails.Patient_mobile = value;
    cancelAppointment()
}
async function cancelAppointment() {
    console.log(appointmentDetails)
    try {
        const response = await fetch('/cancel_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appointmentDetails)
        });
        
        const data = await response.json()
        if (response.ok && data) {
            addMessage(data.message, 'bot-message');
            end_of_dialog()
        } else {
            addMessage("Failed to cancel the appointment. Please try again.", 'bot-message');
        }
    } catch (error) {
        console.error('Error cancelling appointment:', error);
        addMessage("Sorry, something went wrong. Please try again.", 'bot-message');
    }
}

function handleCancelAppointment(userInput) {
    if (!appointmentDetails.Patient_mobile) {
        if (isNaN(Number(userInput))) {
            checkForMobileNumberForCancellation();
        } else {
            assignValue(userInput);
        }
    } else {
        cancelAppointment();
    }
}
async function FetchDetails(userInput) {
    console.log(userInput);
    try {
        const response = await fetch('/fetch_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userInput)
        });

        const data = await response.json();
        console.log(data);

        if (data.status_code === 200) {
            if(intent_tracking ==="update_appointment_flow"){
            addMessage("Please update the details you want to update from the form displayed", 'bot-message');

            showForm() 

            populateForm(data.response);

            document.getElementById('submit-update').addEventListener('click', function(event) {
                event.preventDefault();
                console.log("update");
                update_user_data(document);
                document.getElementById("form-container").classList.add("hidden");
              });
        }else{
            appointmentDetails.Doctor_name = data.response.Doctor_name;
            appointmentDetails.Patient_name = data.response.Patient_name
            appointmentDetails.Appointment_type = data.response.Appointment_type
            appointmentDetails.Date_time = data.response.Date_time;
            appointmentDetails.Patient_mobile = data.response.Patient_mobile;
            addMessage('fetching appointment','bot-message',appointmentDetails)
           
            end_of_dialog()
        }
        } else {
            addMessage(data.response, 'bot-message');
            end_of_dialog()
        }
    } catch (error) {
        console.error('Error fetching appointment:', error);
        addMessage("Sorry, something went wrong. Please try again.", 'bot-message');
    }
}

let isSubmitting = false;
async function update_user_data(document){
    if (isSubmitting) return;
    isSubmitting = true;
    const submitButton = document.getElementById('submit-update');
    submitButton.disabled = true; // Disable the button
    appointmentDetails.Doctor_name = document.getElementById('Doctor_name').value;
    appointmentDetails.Patient_name = document.getElementById('Patient_name').value;
    appointmentDetails.Appointment_type = document.getElementById('Appointment_type').value;
    appointmentDetails.Date_time = document.getElementById('Date_time').value;
    appointmentDetails.Patient_mobile = document.getElementById('Patient_mobile').value;
    console.log(JSON.stringify(appointmentDetails))

    try {
        const response = await fetch('/update_appointment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appointmentDetails)
        });
        
        const data = await response.json()
        console.log(data)
        if (response.ok && data) {
            addMessage(data.message,'bot-message')      
            end_of_dialog()
        } else {
            addMessage("Failed to update the appointment. Please try again.", 'bot-message');
        }
    } catch (error) {
        console.error('Error updating appointment:', error);
        addMessage("Sorry, something went wrong. Please try again.", 'bot-message');
    }finally {
        submitButton.disabled = false; // Re-enable the button if necessary
    }
 isSubmitting = false;
    // document.getElementById('update-form').classList.add('hidden');
    document.getElementById('appointment-form').reset();
}
function populateForm(details) {
    console.log("populated..")
    document.getElementById("Doctor_name").value = 
        (typeof appointmentDetails !== 'undefined' && appointmentDetails.Doctor_name) ? appointmentDetails.Doctor_name : 
        details.Doctor_name ? details.Doctor_name : 
        '';

    document.getElementById("Patient_name").value = 
        (typeof appointmentDetails !== 'undefined' && appointmentDetails.Patient_name) ? appointmentDetails.Patient_name : 
        details.Patient_name ? details.Patient_name : 
        '';

    document.getElementById("Appointment_type").value = 
        (typeof appointmentDetails !== 'undefined' && appointmentDetails.Appointment_type) ? appointmentDetails.Appointment_type : 
        details.Appointment_type ? details.Appointment_type : 
        '';

    document.getElementById("Date_time").value = 
        (typeof appointmentDetails !== 'undefined' && appointmentDetails.Date_time) ? appointmentDetails.Date_time : 
        details.Date_time ? details.Date_time : 
        '';

    document.getElementById('Patient_mobile').value = 
        (typeof appointmentDetails !== 'undefined' && appointmentDetails.Patient_mobile) ? appointmentDetails.Patient_mobile : 
        details.Patient_mobile ? details.Patient_mobile : 
        '';
}



function handleUpdateAppointment(userInput) {
    if (isNaN(Number(userInput))) {
        addMessage("Please provide your mobile number to fetch your appointment details to update:", 'bot-message');
    } else {
        appointmentDetails.Patient_mobile = userInput;
        FetchDetails(appointmentDetails);
    }
}

// Existing functions: sendMessage, checkForMissingValues, scheduleAppointment, cancelAppointment, etc.

function end_of_dialog() {
    intent_tracking = "";
    appointmentDetails = {};
    hideForm();
    setTimeout(() => {
        addMessage("Let me know if you need anything else.", 'bot-message');
    }, 1000);
}
