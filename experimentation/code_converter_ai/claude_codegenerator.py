import os
from dotenv import load_dotenv
import anthropic 
from pprint import pprint

load_dotenv(override=True)
api_key = os.getenv('ANTHROPIC_API_KEY')
lang_model = anthropic.Anthropic(api_key=api_key)

def generatecode(model, language, code):
    messages =[ 
        {
            'role':'assistant', 'content':f'Do not explain anything. Output only pure {language} code. Strip all unnecessary comments or metadata. The generated C++ code must be functionally equivalent, compile-ready, and performance-tuned.Avoid dynamic allocations or high-level abstractions unless necessary Use appropriate standard libraries only when needed for correctness or performance. Minimize runtime overhead and follow best practices for performance-critical C++ code.'
        },
        {
            'role':'user', 'content':code
        }
    ]

    result = lang_model.messages.create(max_tokens=1024, messages=messages, model=model)#, stream=True)
    print(result)
    return result.content[0].text

 