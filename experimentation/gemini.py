# Initialize and constants

import os
from dotenv import load_dotenv
from google import generativeai

class Geminiai:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if self.api_key and len(self.api_key)>10:
            print("Google AI API key looks good so far")
        else:
            print("There might be a problem with your Google AI API key? Please visit the troubleshooting notebook!")
        generativeai.configure(api_key=self.api_key)
        self.MODEL = 'gemini-2.0-flash'


    def askQuestion(self, system_prompt, user_question):
        gemini = generativeai.GenerativeModel(
            model_name=self.MODEL,
            system_instruction=system_prompt
        )
        response = gemini.generate_content(user_question)

        return response.text

    
