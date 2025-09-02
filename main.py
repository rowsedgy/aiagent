import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.call_function import call_function, available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    if len(sys.argv) < 2:
        print("At least one argument neeeded")
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
    
    verbose = '--verbose' in sys.argv
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    

    MAX_ITERATIONS = 20
    current_iteration = 0

    while True:
        current_iteration += 1
        if current_iteration > MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)

        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final reponse:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
        
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
        )
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function result")
        if verbose:
            print(f'-> {function_call_result.parts[0].function_response.response}')
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting")
    
    messages.append(types.Content(role='user', parts=function_responses))
        


if __name__ == "__main__":
    main()
