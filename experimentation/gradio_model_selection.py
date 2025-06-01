import gradio as gr
import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from model_wrappers.open_ai import Openai
from model_wrappers.claude import Claude
from model_wrappers.deepseek import Deekseekai
import google.generativeai
import anthropic
import helper.ai_model_helper
import helper.brochure_helper


load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
openai_model1 = OpenAI()

openai_wrapper_model  = Openai("gpt-4o-mini")
claude_wrapper_model = Claude("claude-3-7-sonnet-latest")
soup = BeautifulSoup()


def messageGpt(user_prompt):
    messages = [{'role':'system', 'content':'You are a hepful assistant'},
                {'role':'user', 'content':user_prompt}
                ]
    response = openai_model1.chat.completions.create(model = "gpt-4o-mini", messages = messages)
    return response.choices[0].message.content

def test_openai_simplechat():
    view = gr.Interface(fn=messageGpt, 
                inputs=gr.Textbox(label="Enter the text"), 
                outputs=gr.Markdown(label="Response"),
                allow_flagging="never")
    view.launch()

# gradio automatically understands stream
def test_openai_stream():
    #system_prompt = 'You are a hepful assistant'
    view = gr.Interface(fn=openai_wrapper_model.askQuestionStream, 
                        inputs=[gr.Textbox(label="Enter the system prompt"),
                                gr.Textbox(label="Enter the user prompt")],
                        outputs=gr.Markdown(label="Response"),
                        allow_flagging="never"
                        )
    view.launch()

def test_claude_stream():
    view = gr.Interface(fn=claude_wrapper_model.askQuestionStream,
                        inputs=[
                            gr.Textbox(label="System Prompt"),
                            gr.Textbox(label="User Prompt")
                        ],
                        outputs=gr.Markdown(label="Response"),
                        allow_flagging="never")
    view.launch()

    
def test_model_stream():
    view = gr.Interface(fn = helper.ai_model_helper.getaskQuestionStream,
                        inputs=
                            [
                                gr.Radio(["gtp", "claude", "gemini", "deepseek"]),
                                gr.Textbox("You are a smart Assisstant"),
                                gr.Textbox("What are the top 3 best lifelong advices?")
                            ],
                            outputs=gr.Markdown(label="Response"),
                            allow_flagging="never"
                        )
    view.launch()    
    


def create_brochure_test():
    view = gr.Interface(fn =helper.brochure_helper.create_brochure,
                        inputs=
                            [
                                gr.Radio(["gtp", "claude", "gemini", "deepseek"]),
                                gr.Textbox("Brain Mustard"),
                                gr.Textbox("http://brainmustard.com")
                            ],
                            outputs=gr.Markdown(label="Response"),
                            allow_flagging="never"
                        )
    view.launch()

#test_openai_stream()
#test_claude_stream()
test_model_stream()
#create_brochure_test()