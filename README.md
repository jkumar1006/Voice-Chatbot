📞 AI Voice Chatbot - Customer Interaction & Appointment Scheduler

🌟 Overview

This project is an AI-powered voice chatbot designed to handle customer inquiries, product comparisons, and appointment scheduling through automated voice interactions. The chatbot utilizes Twilio for call handling, Gemini API for AI responses, and Google Cloud Text-to-Speech for converting responses into audio. This system enhances customer service efficiency by automating interactions and reducing response time.

🚀 Features

✅ Voice Call Handling – Uses Twilio to receive and process voice calls.✅ Speech-to-Text Processing – Converts user speech to text for intent recognition.✅ AI-Powered Responses – Processes user queries using Gemini API.✅ Text-to-Speech Conversion – Generates spoken responses using Google Cloud Text-to-Speech.✅ Appointment Scheduling – Allows customers to book appointments.✅ Email Notifications – Sends confirmation emails via SMTP server.✅ Flask API Integration – Manages request handling and response delivery.

🏗️ Architecture & Methodology

1️⃣ Call Reception – User initiates a call, which is forwarded to the Flask-based backend via Twilio.2️⃣ Speech Processing – Extracts speech and determines intent (query or appointment request).3️⃣ AI Interaction – Queries are sent to Gemini API for response generation.4️⃣ Text-to-Speech Conversion – Converts AI responses into an audio format.5️⃣ Response Delivery – Plays the generated audio response back to the caller.6️⃣ Appointment Scheduling – If an appointment is requested, the system logs details and sends an email confirmation.

🛠️ Technologies Used

Backend: Flask (Python)

Voice API: Twilio

AI Processing: Gemini API

Text-to-Speech: Google Cloud Text-to-Speech

Email Notifications: SMTP Server

Logging & Debugging: Flask Logging System

🔄 API Endpoints

/incoming_call – Handles incoming Twilio calls.

/process_speech – Processes user speech and extracts intent.

/generate_response – Queries Gemini API and converts responses into speech.

/schedule_appointment – Captures appointment details and sends email confirmations.

🎯 Results & Impact

📌 Automates customer interactions, reducing workload on support teams.📌 Enhances response efficiency with AI-driven conversational intelligence.📌 Provides a seamless experience by integrating voice recognition, AI, and scheduling in one system.📌 Improves customer satisfaction with quick and accurate responses.

