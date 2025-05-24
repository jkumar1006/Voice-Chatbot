# 📞 AI Voice Chatbot – Customer Interaction & Appointment Scheduler
## 🌟 Overview
This project is an AI-powered voice chatbot designed to manage customer inquiries, product comparisons, and appointment scheduling through automated voice interactions.

It integrates:

-Twilio for call handling
-Gemini API for intelligent responses
-Google Cloud Text-to-Speech for voice output

The goal is to enhance customer service by automating conversations and reducing response times.

---
## 🚀 Features
✅ Voice Call Handling – Receive and process voice calls using Twilio.

✅ Speech-to-Text Processing – Convert user speech into text for AI interpretation.

✅ AI-Powered Responses – Use Gemini API to understand and answer queries.

✅ Text-to-Speech Conversion – Reply with natural-sounding audio via Google Cloud TTS.

✅ Appointment Scheduling – Log customer appointments and send confirmations.

✅ Email Notifications – Trigger email confirmations via SMTP.

✅ Flask API Integration – Handle backend request/response flow.

---

## 🏗️ Architecture & Methodology
-Call Reception – User initiates a voice call via Twilio → forwarded to Flask backend

-Speech Processing – User speech is transcribed and intent (e.g., query or appointment) is detected

-AI Interaction – Gemini API is queried to generate contextual responses

-Text-to-Speech – Response is converted to audio using Google Cloud Text-to-Speech

-Response Delivery – Audio is streamed back to the caller

-Appointment Scheduling – Appointment details are logged and an email is sent to confirm

---
## 🛠️ Technologies Used
Component	Tech Stack
Backend	Flask (Python)
Voice API	Twilio
AI Engine	Gemini API
Text-to-Speech	Google Cloud Text-to-Speech
Email Delivery	SMTP Server
Logging	Flask Logging System

---
## 🔄 API Endpoints
Endpoint	Description
/incoming_call	Handles incoming calls from Twilio
/process_speech	Transcribes user speech and extracts intent
/generate_response	Gets AI response and converts it to audio
/schedule_appointment	Logs appointment and sends email confirmation

---
## 🎯 Results & Impact
📌 Automates interactions and reduces human support workload

📌 Enhances efficiency through AI-driven voice communication

📌 Improves user experience by combining voice, AI, and scheduling

📌 Increases customer satisfaction with accurate, real-time responses
