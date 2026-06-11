from dotenv import load_dotenv
from google import genai
import os
import time

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Try making 15 rapid API calls
for i in range(15):
    try:
        print(f"\nRequest {i + 1}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say hello in one short sentence."
        )

        print(response.text)

    except Exception as e:
        print("Rate limit or API error encountered:")
        print(e)

        print("Waiting for 10 seconds before retrying...")
        time.sleep(10)

        # Retry once after waiting
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Say hello in one short sentence."
            )

            print("Retry successful:")
            print(response.text)

        except Exception as retry_error:
            print("Retry failed:")
            print(retry_error)