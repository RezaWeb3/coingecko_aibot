import os
from dotenv import load_dotenv
import requests

class Llama:
    def __init__(self, model):
        
        self.OllOLLAMA_API = "http://localhost:11434/api/chat"
        self.HEADERS = {"Content-Type": "application/json"}
        self.MODEL = model # "llama3.2"

    def askQuestion(self, system_prompt, user_question):
        messages = [
            
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
            
        ]
        payload = {
            "model": self.MODEL,
            "messages": messages,
            "stream": False
        }     

        response = requests.post(self.OllOLLAMA_API, json=payload, headers=self.HEADERS) 
        return (response.json()['message']['content'])

        