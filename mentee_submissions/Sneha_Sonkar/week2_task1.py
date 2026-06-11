import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from your root .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("Groq client initialized successfully!")