import json
from logging import raiseExceptions
from functions_list import available_functions, call_function
import os
import argparse
from typing import List
from openai import OpenAI
from prompts import system_prompt
from dotenv import load_dotenv
def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("Couldn't load the openrouter api key")

    # create a OpenAI object that has functions to send response to specified urls along with api key here
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


# When you call parser.add_argument(...), you are registering a rule or specification with the parser object.
# Argument Name / Destination: Because "user_prompt" doesn't start with dashes (like --user_prompt), argparse treats it as a positional argument. It also uses "user_prompt" as the default destination attribute name.
# Type Converter: It records type=str (or whatever callable you pass, e.g. int, float) to convert or validate the incoming string.
# Help text and requirements: Positional arguments are required by default unless configured otherwise.
#
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt") # 
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    prompt =  args.user_prompt 
#    messages= list()
#    messages.append({"role": "system", "content": system_prompt})
    
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model = "openrouter/free",
        messages = messages,
        temperature=0,
        tools=available_functions,
    )
# printing prompt tokens and response token usage based on the object returned by chat.completions.create

    if response.usage == None:
        raise RuntimeError("Did not get response, response usage property is None")
    else:
        if args.verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Response:")
        print(response.choices[0].message.content)
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                 function_args = json.loads(tool_call.function.arguments or "{}")
                 function_return_val = call_function(tool_call, verbose=args.verbose)
                 print(f"-> {function_return_val['content']}")

if __name__ == "__main__":
    main()
