import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key= os.getenv("GEMINI_API_KEY"),  # Replace with your actual Gemini key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

#zero-shot prompt - Directly giving the instructions to the model without any examples
SYSTEM_PROMPT = "You are an coding assistant. You will be given a programming problem, and you need to provide a solution in Python. If the problem is not solvable, explain why. If the problem is solvable, provide a clear and concise solution with comments explaining each step. And only the coding for rest of the query say sorry I cannot help you with that."
response = client.chat.completions.create(
    model="gemini-2.5-flash",  # Or gemini-2.5-flash
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Explain how AI works."},
    ],
)

print(response.choices[0].message.content)
