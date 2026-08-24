import os
import json
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
    """
    Get the current temperature for a city using wttr.in.

    Args:
        city_name: Name of the city.

    Returns:
        Current temperature in Celsius.
    """

    url = f"https://wttr.in/{city_name}?format=j1"

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "weather-agent/1.0"
        },
    )

    response.raise_for_status()

    data = response.json()

    temperature = data["current_condition"][0]["temp_C"]

    return (
        f"The current temperature in {city_name} "
        f"is {temperature}°C."
    )


# ============================================================
# 4. Tell Gemini about our function
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_temperature",
            "description": (
                "Get the current temperature for a city. "
                "Use this function whenever the user asks "
                "for the current temperature or weather temperature."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": (
                            "The name of the city, "
                            "for example Delhi, Mumbai, or Jaipur."
                        ),
                    }
                },
                "required": ["city_name"],
            },
        },
    }
]


# ============================================================
# 5. System prompt
# ============================================================

SYSTEM_PROMPT = """
You are a helpful weather assistant.

You have access to a tool called get_temperature.

When the user asks for the current temperature of a city:

1. Identify the city.
2. Call get_temperature with the city name.
3. Wait for the tool result.
4. Use the tool result to answer the user.
5. Never invent current temperature data.

If the user does not provide a city, ask them which city
they want the temperature for.

Do not reveal private chain-of-thought or internal reasoning.
"""


# ============================================================
# 6. Conversation history
# ============================================================

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
]


# ============================================================
# 7. Chat loop
# ============================================================

while True:

    user_input = input(
        "\nYou (type 'exit' to quit): "
    )

    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------

    if user_input.lower().strip() == "exit":
        print("Goodbye!")
        break

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    try:

        # ====================================================
        # 8. First call to Gemini
        # ====================================================

        response = client.chat.completions.create(
            model="gemini-3.6-flash",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # ====================================================
        # 9. Check whether Gemini wants to call a tool
        # ====================================================

        if assistant_message.tool_calls:

            # Add Gemini's tool-call message to history
            messages.append(assistant_message)

            # =================================================
            # 10. Execute every requested tool
            # =================================================

            for tool_call in assistant_message.tool_calls:

                function_name = tool_call.function.name

                function_arguments = json.loads(
                    tool_call.function.arguments
                )

                print(
                    f"\n[Tool call] {function_name}"
                )

                print(
                    f"[Arguments] {function_arguments}"
                )

                # ---------------------------------------------
                # Execute our Python function
                # ---------------------------------------------

                if function_name == "get_temperature":

                    city_name = function_arguments[
                        "city_name"
                    ]

                    tool_result = get_temperature(
                        city_name
                    )

                else:
                    tool_result = (
                        f"Unknown function: {function_name}"
                    )

                print(
                    f"[Tool result] {tool_result}"
                )

                # =================================================
                # 11. Send tool result back to Gemini
                # =================================================

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    }
                )

            # =================================================
            # 12. Ask Gemini for the final answer
            # =================================================

            final_response = client.chat.completions.create(
                model="gemini-3.6-flash",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            final_message = (
                final_response.choices[0].message
            )

            # Save final response
            messages.append(
                {
                    "role": "assistant",
                    "content": final_message.content,
                }
            )

            print("\nAssistant:")
            print(final_message.content)

        else:

            # =================================================
            # No tool was required
            # =================================================

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                }
            )

            print("\nAssistant:")
            print(assistant_message.content)

    except Exception as e:

        print("\nError:")
        print(e)
