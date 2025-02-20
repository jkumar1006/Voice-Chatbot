from flask import Flask, request, send_file, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather
from google.cloud import texttospeech
import os
import requests
import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

app = Flask(__name__)

# Secure secret key (make sure to use a strong, random key)
app.secret_key = ''

# Configure Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-cloud-key.json"

# Gemini API configuration
api_key = ''
gemini_api_url = ''

# Twilio configuration
twilio_account_sid = ""
twilio_auth_token = ""

tts_client = texttospeech.TextToSpeechClient()

# SMTP configuration for sending emails
smtp_server = 'localhost'
smtp_port = 1025  # Port as per  SMTP server setup
smtp_user = None  # No user needed for local SMTP
smtp_password = None  # No password needed for local SMTP
email_from = 'your_email@example.com'  # Sender email address
email_to = 'recipient_email@example.com'  # Recipient email address

# Set up logging
logging.basicConfig(level=logging.INFO)

# Global variable to store appointment details
appointment_details = {}

def extract_time(speech_result):
    # Extract time using regex
    time_pattern = re.compile(r'\b\d{1,2}(:\d{2})?\s*(am|pm|a\.m\.|p\.m\.)?\b', re.IGNORECASE)
    match = time_pattern.search(speech_result)
    if match:
        time_str = match.group().lower()
        # Add default "pm" if no am/pm is specified
        if "am" not in time_str and "pm" not in time_str:
            time_str += " pm"
        return time_str
    else:
        return "time not recognized"

@app.route('/')
def index():
    return "Welcome to the Car Inquiry Assistant!"

@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    try:
        response = VoiceResponse()
        gather = Gather(input='speech', action='/process_speech', speechTimeout='auto')
        gather.say("Hi, you can ask me anything about cars or book an appointment. What do you want to do?")
        response.append(gather)
        logging.info("Gathering speech input from the caller.")
        return str(response)
    except Exception as e:
        logging.error(f"Error in incoming_call: {e}")
        return str(VoiceResponse().say("An error occurred. Please try again later.")), 500

@app.route('/process_speech', methods=['POST'])
def process_speech():
    try:
        logging.info(f"Form data received: {request.form}")
        speech_result = request.form.get('SpeechResult')
        if not speech_result:
            logging.error("SpeechResult not found or is empty in the request form data.")
            response = VoiceResponse()
            gather = Gather(input='speech', action='/process_speech', speechTimeout='auto')
            gather.say("I did not understand your question. Please try again.")
            response.append(gather)
            return str(response)

        logging.info(f"Transcription: {speech_result}")

        if "book an appointment" in speech_result.lower():
            response = VoiceResponse()
            gather = Gather(input='speech', action='/get_appointment_date', speechTimeout='auto')
            gather.say("Sure, I can help with that. Please provide the date for the appointment.")
            response.append(gather)
            return str(response)

        # Send the question to Gemini API
        gemini_response = get_gemini_response(speech_result)
        if gemini_response is None:
            logging.error("No response from Gemini API.")
            response = VoiceResponse()
            gather = Gather(input='speech', action='/process_speech', speechTimeout='auto')
            gather.say("I couldn't find an answer to your question. Please try again.")
            response.append(gather)
            return str(response)

        # Convert Gemini API response to speech
        response_text = gemini_response
        response_audio_path = synthesize_speech(response_text)

        # Prepare the response to play the synthesized speech
        response = VoiceResponse()
        audio_url = url_for('static', filename='response.mp3', _external=True)
        response.play(audio_url)
        gather = Gather(input='speech', action='/process_speech', speechTimeout='auto')
        gather.say("Do you have any other questions about cars?")
        response.append(gather)

        # Logging for successful completion
        logging.info(f"Response audio path: {response_audio_path}")
        return str(response)
    except Exception as e:
        logging.error(f"Error in process_speech: {e}")
        response = VoiceResponse()
        response.say("An error occurred while processing your request. Please try again later.")
        return str(response), 500

@app.route('/get_appointment_date', methods=['POST'])
def get_appointment_date():
    try:
        global appointment_details
        logging.info(f"Form data received: {request.form}")
        speech_result = request.form.get('SpeechResult')
        if not speech_result:
            logging.error("SpeechResult not found or is empty in the request form data.")
            response = VoiceResponse()
            gather = Gather(input='speech', action='/get_appointment_date', speechTimeout='auto')
            gather.say("I did not understand the date. Please provide the date for the appointment.")
            response.append(gather)
            return str(response)

        appointment_details['date'] = speech_result.strip()
        logging.info(f"Appointment date set to: {appointment_details['date']}")
        response = VoiceResponse()
        gather = Gather(input='speech', action='/get_appointment_time', speechTimeout='auto')
        gather.say("Got it. Now please provide the time for the appointment.")
        response.append(gather)
        return str(response)
    except Exception as e:
        logging.error(f"Error in get_appointment_date: {e}")
        response = VoiceResponse()
        response.say("An error occurred while processing your request. Please try again later.")
        return str(response), 500

@app.route('/get_appointment_time', methods=['POST'])
def get_appointment_time():
    try:
        global appointment_details
        logging.info(f"Form data received: {request.form}")
        speech_result = request.form.get('SpeechResult')
        if not speech_result:
            logging.error("SpeechResult not found or is empty in the request form data.")
            response = VoiceResponse()
            gather = Gather(input='speech', action='/get_appointment_time', speechTimeout='auto')
            gather.say("I did not understand the time. Please provide the time for the appointment.")
            response.append(gather)
            return str(response)

        appointment_details['time'] = extract_time(speech_result)
        logging.info(f"Appointment time set to: {appointment_details['time']}")
        send_confirmation_email(appointment_details)
        response = VoiceResponse()
        response.say(f"Your appointment has been booked for {appointment_details['date']} at {appointment_details['time']}. A confirmation email has been sent.")
        logging.info(f"Appointment confirmed: {appointment_details['date']} at {appointment_details['time']}")
        appointment_details = {}  # Clear appointment details after sending confirmation
        return str(response)
    except Exception as e:
        logging.error(f"Error in get_appointment_time: {e}")
        response = VoiceResponse()
        response.say("An error occurred while processing your request. Please try again later.")
        return str(response), 500

@app.route('/status_callback', methods=['POST'])
def status_callback():
    call_sid = request.form.get('CallSid')
    call_status = request.form.get('CallStatus')
    logging.info(f"Call SID: {call_sid} has changed status to {call_status}")
    return '', 200

def get_gemini_response(question):
    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": question
                        }
                    ]
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
        }

        logging.info(f"Making request to Gemini API with payload: {payload}")
        response = requests.post(gemini_api_url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            logging.info(f"Gemini API response: {response_json}")
            if 'candidates' in response_json and len(response_json['candidates']) > 0:
                return response_json['candidates'][0]['content']['parts'][0]['text']
            else:
                return "No answer found in Gemini API response."
        else:
            logging.error(f"Error from Gemini API: {response.status_code} {response.text}")
            return None
    except Exception as e:
        logging.error(f"Exception while calling Gemini API: {e}")
        return None

def synthesize_speech(text):
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        response_audio_path = "static/response.mp3"

        with open(response_audio_path, 'wb') as out:
            out.write(response.audio_content)
        logging.info(f"Synthesized speech saved at {response_audio_path}")

        return response_audio_path
    except Exception as e:
        logging.error(f"Error in synthesize_speech: {e}")
        return None

def send_confirmation_email(details):
    try:
        subject = "Appointment Confirmation"
        body = f"Your appointment has been booked for {details['date']} at {details['time']}."

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # No need to login since we are using a local SMTP server without auth
            server.sendmail(email_from, email_to, msg.as_string())
        
        logging.info("Confirmation email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending confirmation email: {e}")

@app.route('/static/<path:filename>', methods=['GET'])
def static_files(filename):
    try:
        return send_file(os.path.join('static', filename), mimetype='audio/mpeg')
    except Exception as e:
        logging.error(f"Error in serving static file {filename}: {e}")
        return "File not found", 404

if __name__== '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)

