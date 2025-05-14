# Initialize and constants

import os
from dotenv import load_dotenv
from google import generativeai

class Geminiai:
    def __init__(self, model):
        load_dotenv(override=True)
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if self.api_key and len(self.api_key)>10:
            print("Google AI API key looks good so far")
        else:
            print("There might be a problem with your Google AI API key? Please visit the troubleshooting notebook!")
        generativeai.configure(api_key=self.api_key)
        self.MODEL = model #'gemini-2.0-flash'


    def askQuestion(self, system_prompt, user_question):
        gemini = generativeai.GenerativeModel(
            model_name=self.MODEL,
            system_instruction=system_prompt
        )
        response = gemini.generate_content(user_question)

        return response.text
    
    def respondMessages(self, system_prompt, messages):
        gemini = generativeai.GenerativeModel(
            model_name= self.MODEL,
            system_instruction=system_prompt
        )
        #result = gemini.generate_content(messages)

        #return result
        chat = gemini.start_chat(history=[])
        response = None
        for m in messages:
            if m['role'] == 'user':
               # print("USer added")
                chat.send_message(m['content'])
            elif m['role'] == 'model' or m['role'] == 'assistant':
                #print("asssistant added")
                chat._history.append({"role": "model", "parts": [m['content']]})
            #else:   
                #print("nothing added")

        response = chat.send_message(messages[-1]['content'])
        # extracts the parts
        if not response.candidates:
            return ""

        candidate = response.candidates[0]
        parts = candidate.content.parts    
        # Concatenate all text parts if multiple
        result = "".join(part.text for part in parts if hasattr(part, "text"))
        #print(f"in method: {result}")
        return result

       
