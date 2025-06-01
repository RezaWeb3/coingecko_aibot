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

def chat(message, history):
    #open ai
    system_message = "You are a helpful assistant"
    openai_model = Openai("gpt-4o-mini")
    prompt = history + [{"role": "user", "content": message}]
    
    yield from openai_model.respondStream(system_message, prompt)
   # return "Hello!"

gr.ChatInterface(fn=chat, type="messages").launch()