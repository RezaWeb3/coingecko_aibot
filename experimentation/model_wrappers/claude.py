
import os
from dotenv import load_dotenv
import anthropic

class Claude:
    def __init__(self, model):
        load_dotenv(override=True)
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if self.api_key and len(self.api_key)>10:
            print("ANTHROPIC AI API key looks good so far")
        else:
            print("There might be a problem with your ANTHROPIC AI API key? Please visit the troubleshooting notebook!")
        self.MODEL = model #"claude-3-7-sonnet-latest"  
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

    def respondMessages(self, system_prompt, messages):
        response = self.claudeai.messages.create(
            max_tokens = 100,
            model= self.MODEL,
            temperature=0.7,
            system = system_prompt,
            messages=messages     
        )
        result = response.content[0].text
        return result
    
    def askQuestionStream(self, system_prompt, user_question):
        result = ""
        with self.claudeai.messages.stream(
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_question}],
            model=self.MODEL,
        ) as stream:
            for text in stream.text_stream:
                result += text or ""
                yield result
    
