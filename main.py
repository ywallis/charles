import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

MAX_ITERATIONS = 20


def verbose_print(user_prompt: str, response_item: types.GenerateContentResponse):
    print("User prompt:", user_prompt)

    if response_item.usage_metadata is None:
        raise Exception("Couldn't get usage details from model")

    print("Prompt tokens:", response_item.usage_metadata.prompt_token_count)
    print("Response tokens:", response_item.usage_metadata.candidates_token_count)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        print("A Gemini API Key is needed for Charles to work")
        sys.exit(1)

    arguments = sys.argv
    if len(arguments) == 1:
        print("Charles expects a prompt")
        sys.exit(1)

    verbose = "--verbose" in arguments

    user_prompt: str = sys.argv[1]

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iteration = 0

    while iteration < MAX_ITERATIONS:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        if not response.function_calls:
            print(response.text)
            return response.text

        for function_call_part in response.function_calls:
            if verbose:
                print(
                    f"Calling function: {function_call_part.name}({function_call_part.args})"
                )

            result = call_function(function_call_part)
            if result.parts is None or result.parts[0].function_response is None:
                raise Exception("No result from function")
            if result.parts[0].function_response.response is None:
                raise Exception("No result from function")

            if verbose:
                print(f"-> {result.parts[0].function_response.response}")

            messages.append(result)

            iteration += 1

        if verbose:
            verbose_print(user_prompt, response)


if __name__ == "__main__":
    main()
