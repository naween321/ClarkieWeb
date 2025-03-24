import os
import uuid
from django.conf import settings
from google.cloud.dialogflowcx_v3.types import TextInput, QueryInput
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
import django

# Set the Django settings module (Replace 'your_project.settings' with your actual project settings path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clarkiee.settings')

# Initialize Django
django.setup()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(settings.BASE_DIR) + "/creds.json"

PROJECT_ID = "hackathon-454621"
LOCATION = "us-central1"
AGENT_ID = "eba4b842-c371-47f7-b43e-3f7a710aa927"
SESSION_ID = str(uuid.uuid4())

# Specify the correct regional endpoint
client = SessionsClient(client_options={"api_endpoint": f"{LOCATION}-dialogflow.googleapis.com"})
session = client.session_path(PROJECT_ID, LOCATION, AGENT_ID, SESSION_ID)


def detect_intent_cx(text: str, language_code: str = "en"):
    qi = QueryInput(text=TextInput(text=text), language_code=language_code)
    response = client.detect_intent(request={"session": session, "query_input": qi})
    # Extract text from response messages
    if response.query_result.response_messages:
        for message in response.query_result.response_messages:
            if message.text:
                return message.text.text[0]  # Return the first text response
    return "Thank you for your question. Our team is working on providing the most accurate information " \
           "for your query. This typically takes a few minutes"


print(detect_intent_cx("How are you?"))
