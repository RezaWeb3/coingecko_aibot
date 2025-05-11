# Initialize and constants

import os
from dotenv import load_dotenv
from openai import OpenAI
class Deekseekai:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if self.api_key and len(self.api_key)>10:
            print("DEEPSEEK AI API key looks good so far")
        else:
            print("There might be a problem with your DEEPSEEK AI API key? Please visit the troubleshooting notebook!")
            
        self.MODEL = 'deepseek-chat'
        self.deepseekai = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")



    def askQuestion(self, system_prompt, user_question):
        response = self.deepseekai.chat.completions.create(
            model= self.MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
        )
        result = response.choices[0].message.content
        return result

    
