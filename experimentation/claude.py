
import os
from dotenv import load_dotenv
import anthropic

class Claude:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if self.api_key and len(self.api_key)>10:
            print("ANTHROPIC AI API key looks good so far")
        else:
            print("There might be a problem with your ANTHROPIC AI API key? Please visit the troubleshooting notebook!")
        self.MODEL = "claude-3-7-sonnet-latest"  
        self.claudeai = anthropic.Anthropic()


    def askQuestion(self, system_prompt, user_question):
        response = self.claudeai.messages.create(
            max_tokens=200,
            messages=[
                {"role": "user", "content": user_question},
            ],
            temperature=0.7,
            system=system_prompt,
            model=self.MODEL
        )
           
        result = response.content[0].text
        return result
