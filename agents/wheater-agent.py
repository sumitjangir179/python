import os
import json
from pyexpat.errors import messages
import requests

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Add it to your .env file."
    )


# ============================================================
# 2. Create Gemini client
# ============================================================

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# ============================================================
# 3. Weather function
# ============================================================

def get_temperature(city_name: str) -> str:
    response = requests.get(f"https://wttr.in/{city_name.lower()}?format=%C+%t")

    if(response.status_code == 200):
        return response.text

    return f"Error: Unable to fetch weather data for {city_name}."


SYSTEM_PROMPT = """
    You are an expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN, and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps. 
    Once you think enough PLAN has been done, finally you can give the OUTPUT.
    You can also call the tools if required from the list of available tools.

    Rules:
     - Strictly follow the given JSON output format
     - Only run one step at a time
     - The sequence of steps is START (where user gives an input), PLAN (That can be multiple time) and OUTPUT.

    Output JSON format:
      {step: "START" | "PLAN" | "OUTPUT", | "TOOL" , "content" : "string", "tool" : "string", "input" : "string",}

    Available tools:
    1. get_temperature(city_name: str) -> str: get the city name as an input as an string and return the current temperature of the city in string format.

    Examples:
      START: What is the current weather in Delhi?
      PLAN: {"step": "PLAN", "content": "Seems like user is interested in getting the current weather of Delhi in India."}
      PLAN: {"step": "PLAN", "content": "Let's see if we have any available tools from the list of available tools."}
      PLAN: {"step": "PLAN", "content": "Great ! We have get_temperature tool from the list of available tools."}
      PLAN: {"step": "PLAN", "content": "I need to call get_temperature tool to get the current temperature of Delhi."}
      PLAN: {"step": "TOOL",  "tool": "get_temperature", "input": "Delhi"}
      PLAN: {"step": "OBSERVE",  "tool": "get_temperature", "output": "The current temperature in Delhi is 35°C."}
      PLAN: {"step": "PLAN", "content": "I have got the whole current weather of Delhi."}
      OUTPUT: {"step": "OUTPUT", "content": "The current temperature in Delhi is 35°C."}

"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]

available_tools = {
    "get_temperature": get_temperature,
}


while True:
    user_input = input("> ")

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        while True:
            response = client.chat.completions.create(
                model="gemini-3.6-flash",
                response_format={"type": "json_object"},
                messages=messages
            )

            raw_message = response.choices[0].message
            content = raw_message.content

            print("RAW:", content)

            messages.append({
                "role": "assistant",
                "content": content
            })

            parsed_message = json.loads(content)

            step = parsed_message["step"]

            if step == "START":
                print(f"\n{parsed_message['content']}\n")
                continue

            elif step == "PLAN":
                print(f"\n{parsed_message['content']}\n")

                # Give the model another turn so Gemini
                # does not receive a conversation ending in assistant.
                messages.append({
                    "role": "user",
                    "content": "Continue to the next step."
                })

                continue

            elif step == "TOOL":
                tool_name = parsed_message["tool"]
                tool_input = parsed_message["input"]

                print(
                    f"\nCalling tool: {tool_name} "
                    f"with input: {tool_input}\n"
                )

                tool_response = available_tools[tool_name](tool_input)

                print(f"\nTool response: {tool_response}\n")

                messages.append({
                    "role": "user",
                    "content": json.dumps({
                        "step": "OBSERVE",
                        "tool": tool_name,
                        "output": tool_response
                    })
                })

                continue

            elif step == "OUTPUT":
                print(f"\n{parsed_message['content']}\n")
                break

    except Exception as e:
        print("\nError:")
        print(e)