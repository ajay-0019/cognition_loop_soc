from google import genai
from dotenv import load_dotenv
import os

from google.genai import types
load_dotenv()

client= genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

response = client.models.generate_content(
                model='gemini-2.5-flash',contents='whats the weather today?',
                config=types.GenerateContentConfig(
                    system_instruction="a formal 19th century butler"
                )
)

print(response.text)

client.close()