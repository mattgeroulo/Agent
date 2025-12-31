import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions , call_function


load_dotenv()

api_key=os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Api key is None")
client=genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt",type=str,help="User prompt")
parser.add_argument("--verbose",action="store_true",help="Enable verbose output")
args= parser.parse_args()
messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]


def main():
    
    for _ in range(20):
        response = client.models.generate_content(model="gemini-2.5-flash",contents=messages , 
                                            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt ))
        

        if not response.usage_metadata:
            raise RuntimeError("API usage_metadata is None")
        if response.candidates:
            for history in response.candidates:
                if history.content:
                    messages.append(history.content)
                
                
        function_results =[]
        if response.function_calls:
            for funCalls in response.function_calls:
                function_call_result = call_function(funCalls)
                if not function_call_result:
                    raise Exception("Error: Empty Function Call Result")
                if not isinstance(function_call_result.parts[0].function_response,types.FunctionResponse):
                    raise Exception("Error: Function response is not of type FunctionResponse")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Empty function result")
                function_results.append(function_call_result.parts[0])
                #print(f"Calling Function: {funCalls.name} ({funCalls.args}) ")
        elif response.text:
            print("Final response:")
            print(response.text)
            return    
            
        messages.append(types.Content(role="tools", parts=function_results))
        """
        if args.verbose:
            print(response.function_calls)
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"-> {function_call_result.parts[0].function_response.response}")
            print(f"{response.text}")
            return 0
        else:
            print(response.text)
            
            return 0"""
    print("Maximum model iterations reached")
    return 1
if __name__=="__main__":
    main()