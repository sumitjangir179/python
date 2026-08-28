import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key= os.getenv("GEMINI_API_KEY"),  # Replace with your actual Gemini key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

#few-shot prompt - Directly giving the instructions to the model with a few examples of input-output pairs to help the model understand the task better
#few shot prompt is widely used for few-shot learning and increases the chances of getting a better response from the model.
# we can get the structured response using the few shot prompt by providing the examples of input-output pairs to the model. The model will learn from the examples and will be able to generate the output for the new input provided by the user.
SYSTEM_PROMPT = """You are an coding assistant. You will be given a programming problem, and you need to provide a solution in Python. If the problem is not solvable, explain why. If the problem is solvable, provide a clear and concise solution with comments explaining each step. And only the coding for rest of the query say sorry I cannot help you with that.

Output should be in the following format:

Rules:
- The code should be in Python.
- The code should be clear and concise.
- The code should be easy to understand.
    {{
        code: string or null
        message: string
        isCode: boolean
   
    }}

Examples:
Problem: Write a function that adds two numbers.
Solution: def add(a, b): return a + b

Problem: Write a function that multiplies two numbers.
Solution: def multiply(a, b): return a * b

Problem: Write a function that divides two numbers.
Solution: def divide(a, b): return a / b

Problem: Write a function that subtracts two numbers.
Solution: def subtract(a, b): return a - b




"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",  # Or gemini-2.5-flash
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Explain how AI works."},
    ],
)

print(response.choices[0].message.content)
