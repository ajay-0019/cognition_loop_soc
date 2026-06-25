## Week 1 Tasks: Infrastructure and Control

This week focuses on establishing your local development environment and using the Google Gemini API to return predictable data formats.


---


### Task 1: Environment Configuration
1. Open your terminal and initialize a Python virtual environment:
   `python -m venv venv`
2. Activate your virtual environment:
   * Windows: `venv\Scripts\activate`
   * Mac/Linux: `source venv/bin/activate`
3. Install the specific Google Gemini SDK and the environment manager:
   `pip install google-genai python-dotenv`
4. Obtain a free API Key from Google AI Studio.
5. Create a file named `.env` in the root of your project directory and add your key:
   `GEMINI_API_KEY=your_actual_api_key_here`

### Task 2: Programmatic Execution (basic_call.py)
Create a script named `basic_call.py` that connects to the Gemini API and prints a simple response.
* Use `python-dotenv` to import your key securely into your script.
* Initialize the Gemini client using the `gemini-2.5-flash` model.
* Pass a basic prompt (e.g., "Explain Newton's 2nd law in one sentence") and print the raw text response to your terminal.

### Task 3: Managing Rate Limits (rate_limit_handler.py)
The free tier for `gemini-2.5-flash` limits you to 10 requests per minute. Since autonomous agents run loops, they can hit this limit instantly and crash your script. 
* Write a script named `rate_limit_handler.py`.
* Create a simple `for` loop that attempts to call the API 15 times rapidly. 
* Use a `try...except` block to catch the rate limit exception. When caught, your script should use `time.sleep()` to pause execution for a few seconds before automatically trying again, rather than crashing entirely.

### Task 4: System Instruction Manipulation (persona_call.py)
Create a script named `persona_call.py` to change the behavior of the model.
* When initializing the model, use the `system_instruction` parameter.
* Set a ruleset directing the model to act as a highly specific persona (e.g., a formal 19th-century butler or a vintage computer terminal from the 1980s).
* Send a generic prompt like "How is the weather today?" and print the response to prove the persona constraints are strictly followed.

### Task 5: Strict Data Extraction (json_extractor.py)
To trigger external code later, our engine requires clean data structures, not conversational text. Create a script named `json_extractor.py`.
* Copy this exact unstructured block of text into your script as a variable:
    "We interviewed Alex Mercer today. He is 24 years old and works as a Junior Data Analyst. His technical toolkit consists of Python, SQL, and Tableau."
* Set a `system_instruction` directing the model to act as a strict data parser that outputs ONLY raw JSON, with no conversational text and no markdown formatting wrappers.
* The target JSON schema must look like this:
    `{"name": "string", "age": integer, "role": "string", "skills": ["string", "string"]}`
* Inside your script, pass the model's raw string output directly into Python's native `json.loads()` function. Extract and print just the skills list to verify the conversion worked without syntax errors.

---

## Expected Outputs for Week 1

Upon executing your code locally, your scripts must produce the following terminal outcomes:

* **basic_call.py**: A standard paragraph or sentence answering your query cleanly.
* **rate_limit_handler.py**: Your terminal should show the first requests succeeding, a pause when the limit is hit, and then the remaining requests completing successfully.
* **persona_call.py**: A text response written entirely within the voice and vocabulary of your chosen system instruction ruleset.
* **json_extractor.py**: The terminal must display a native Python list (e.g., `['Python', 'SQL', 'Tableau']`). If your script encounters a `JSONDecodeError` or displays markdown characters, your system prompt is not strict enough.

---

## Submission Protocol

1. Fork this repository to your personal GitHub account.
2. Navigate to the `/mentee_submissions` directory and create a new directory titled `Firstname_Lastname`.
3. Place your four Python scripts within this directory.
4. Open a Pull Request (PR) against the main repository prior to the Week 1 deadline.

---

### A Note Before You Begin
This might feel like we are just writing basic API scripts right now, but you are actually laying the foundation for something massive. The string parsing, error handling, and system instructions you are mastering this week are the exact mechanisms that will act as the "brain" of your autonomous agent. Every complex software system starts with a successful baseline. Read the documentation, debug the errors, and have fun building!
