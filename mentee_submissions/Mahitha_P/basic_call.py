from dotenv import load_dotenv
from google import genai
import os

# Load variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Send prompt to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain Newton's 2nd law in one sentence"
)

# Print response text
print(response.text)