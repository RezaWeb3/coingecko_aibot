# Initialize and constants

import os
from dotenv import load_dotenv
from openai import OpenAI
class Openai:
    def __init__(self, model):
        load_dotenv(override=True)
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key and self.api_key.startswith('sk-proj-') and len(self.api_key)>10:
            print("OPEN AI API key looks good so far")
        else:
            print("There might be a problem with your OPEN AI API key? Please visit the troubleshooting notebook!")
            
        self.MODEL = model #'gpt-4o-mini'
        self.openai = OpenAI()


    def askQuestion(self, system_prompt, user_question):
        response = self.openai.chat.completions.create(
            model= self.MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
        )
        result = response.choices[0].message.content
        return result
    
    def askQuestionStream(self, system_prompt, user_question):
        print("Sys:" + system_prompt)
        print("user:" + user_question)
        response_stream = self.openai.chat.completions.create(
            model= self.MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            stream=True
        )

        result = ""
        for chunk in response_stream:
            result += chunk.choices[0].delta.content or ""
            yield result
        
        print("Done yielding")
    
    
    def respondMessages(self, system_prompt, messages):
       
        response = self.openai.chat.completions.create(
            model= self.MODEL,
            messages = [{"role":"system", "content":system_prompt}] + messages
        )
        result = response.choices[0].message.content
        return result

    def respondStream(self, system_prompt, messages):
        response_stream = self.openai.chat.completions.create(
            model = self.MODEL, 
            messages = [{"role":"system", "content":system_prompt}] + messages, 
            stream = True
        )
        
        result = ""
        for chunk in response_stream:
            result += chunk.choices[0].delta.content or ""
            yield result
