from google import genai
from dotenv import load_dotenv
import os
import json

from google.genai import types

load_dotenv()
x = "We interviewed Alex Mercer today. He is 24 years old and works as a Junior Data Analyst. His technical toolkit consists of Python, SQL, and Tableau."

client= genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=x,
            config=types.GenerateContentConfig(
                system_instruction="a strict data parser that outputs ONLY raw JSON, with no conversational text and no markdown formatting wrappers.The target JSON schema must look like this: {'name': 'string', 'age': integer, 'role': 'string', 'skills': ['string', 'string']}"
            )
)

y=json.loads(str(response.text))
print(y)

client.close()