import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    print("A Gemini API Key is needed for this to work")
    sys.exit(1)


client = genai.Client(api_key=api_key)


def verbose_print(user_prompt: str, response_item: types.GenerateContentResponse):
    print("User prompt:", user_prompt)

    if response_item.usage_metadata is None:
        raise Exception("Couldn't get usage details from model")

    print("Prompt tokens:", response_item.usage_metadata.prompt_token_count)
    print("Response tokens:", response_item.usage_metadata.candidates_token_count)


def main():
    arguments = sys.argv
    if len(arguments) == 1:
        print("Charles expects a prompt")
        sys.exit(1)

    user_prompt: str = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(response.text)
    if "--verbose" in arguments:
        verbose_print(user_prompt, response)


if __name__ == "__main__":
    main()
