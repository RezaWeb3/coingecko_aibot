import os
from dotenv import load_dotenv
import anthropic 
from pprint import pprint

load_dotenv(override=True)
api_key = os.getenv('ANTHROPIC_API_KEY')
lang_model = anthropic.Anthropic(api_key=api_key)

def generatecode(model, language, code):
    system_message = f'Do not explain anything. Output only pure {language} code. Strip all unnecessary comments or metadata. The generated C++ code must be functionally equivalent, compile-ready, and performance-tuned.Avoid dynamic allocations or high-level abstractions unless necessary Use appropriate standard libraries only when needed for correctness or performance. Minimize runtime overhead and follow best practices for performance-critical C++ code.'
    
    messages =[ 
        {
            'role':'user', 'content':code
        }
    ]
    output = ""
    result = lang_model.messages.stream(max_tokens=1024, system=system_message, messages=messages, model=model)
    with result as stream:
        for text in stream.text_stream:
            yield text


   

 