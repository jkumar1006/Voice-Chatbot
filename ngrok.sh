#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install necessary packages from requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing default packages."
    pip install Flask twilio google-cloud-texttospeech requests aiosmtpd
    pip freeze > requirements.txt
fi


# Start ngrok tunnel
ngrok http 5000

