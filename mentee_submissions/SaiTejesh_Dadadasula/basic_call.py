from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=gemini_api)

response = client.models.generate_content(
    model='gemini-3.1-pro-preview',contents='how old is universe?'
)

print(response.text)

client.close()


