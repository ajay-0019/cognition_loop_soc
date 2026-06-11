import os
import json
import requests
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# -------------------------------------------------------------------
# 1. Define the Real Python Tool
# -------------------------------------------------------------------
def get_random_number_fact(category="math"):
    """Fetches a random number fact from the Numbers API based on a category."""
    try:
        url = f"http://numbersapi.com/random/{category}?json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return json.dumps({"number": data.get("number"), "fact": data.get("text")})
        return json.dumps({"error": "Could not fetch trivia at this time."})
    except Exception as e:
        return json.dumps({"error": str(e)})

# -------------------------------------------------------------------
# 2. Describe the Tool to Groq (JSON Schema with a parameter)
# -------------------------------------------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_random_number_fact",
            "description": "Call this tool when the user asks for a random number fact, trivia, or math truth.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["math", "trivia"],
                        "description": "The type of number fact to retrieve."
                    }
                },
                "required": [],
            },
        },
    }
]

def run_agent():
    user_prompt = "Give me a fun, random mathematical fact!"
    print(f"User: {user_prompt}\n")

    messages = [
        {
            "role": "system", 
            "content": "You are an eccentric, brilliant statistics and math professor who loves sharing quirky number facts enthusiastically."
        },
        {"role": "user", "content": user_prompt}
    ]
    
   # Step 1: Send the tool schema to the robust 70B model
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Swapped to active flagship model
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )


    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        print("[Agent Decision]: Groq requested a tool call.")
        
        available_functions = {
            "get_random_number_fact": get_random_number_fact,
        }
        
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            
            function_args = json.loads(tool_call.function.arguments)
            category_arg = function_args.get("category", "math")
            
            print(f"[Executing Local Python Tool]: Running {function_name}(category='{category_arg}')...")
            tool_output = function_to_call(category=category_arg)
            print(f"[Tool Output Received]: {tool_output}\n")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": tool_output,
            })
        
        # Step 2: Request the final conversational answer from the same model
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Match model here
            messages=messages
        )
        
        print("Professor Groq's Final Answer:")
        print(final_response.choices[0].message.content)
    else:
        print("Groq's Direct Answer:")
        print(response_message.content)

if __name__ == "__main__":
    run_agent()