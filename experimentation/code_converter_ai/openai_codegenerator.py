import os
from dotenv import load_dotenv
from openai import OpenAI
from pprint import pprint

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
lang_model = OpenAI(api_key=api_key)

def generatecode(model, language, code):
    messages =[ 
        {
            'role':'system', 'content':f'Do not explain anything. Output only pure {language} code. Strip all unnecessary comments or metadata. The generated C++ code must be functionally equivalent, compile-ready, and performance-tuned.Avoid dynamic allocations or high-level abstractions unless necessary Use appropriate standard libraries only when needed for correctness or performance. Minimize runtime overhead and follow best practices for performance-critical C++ code.'
        },
        {
            'role':'user', 'content':code
        }
    ]

    pprint(messages)



    result = lang_model.chat.completions.create(messages=messages, model=model)#, stream=True)
    return result.choices[0].message.content
   # for chunk in result:       
   #     delta = chunk.choices[0].delta.content
   #     if delta != None:
   #         output += delta
   #         yield delta 
 