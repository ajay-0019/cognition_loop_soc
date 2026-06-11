from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import json

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Unstructured text input
text_data = """
We interviewed Alex Mercer today.
He is 24 years old and works as a Junior Data Analyst.
His technical toolkit consists of Python, SQL, and Tableau.
"""

# Generate structured JSON response
response = client.models.generate_content(
    model="gemini-2.5-flash",

    config=types.GenerateContentConfig(
        system_instruction="""
        You are a strict data extraction engine.

        Rules:
        - Output ONLY valid raw JSON.
        - Do not include markdown formatting.
        - Do not include explanations.
        - Do not include code blocks.
        - Follow this exact schema:

        {
            "name": "string",
            "age": integer,
            "role": "string",
            "skills": ["string", "string"]
        }
        """
    ),

    contents=text_data
)

# Raw JSON string from model
raw_json = response.text

print("Raw model output:")
print(raw_json)

# Convert JSON string into Python dictionary
parsed_data = json.loads(raw_json)

# Extract only skills list
skills = parsed_data["skills"]

print("\nExtracted skills list:")
print(skills)