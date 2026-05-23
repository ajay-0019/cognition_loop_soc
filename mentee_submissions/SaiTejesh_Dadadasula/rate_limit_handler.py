from google import genai
from dotenv import load_dotenv
import os
import time

from google.genai import errors


load_dotenv()

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

for i in range(10):
    try:
        print(client.models.generate_content(model='gemini-2.5-flash',contents='Hi').text)
    except errors.APIError:
        print("API error trying after 65 seconds..... (either resource or server error)")
        time.sleep(65)

client.close()

