import gradio as gr
import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from helper.polygon_stock import StockNews
import json
from datetime import datetime, timezone

# Initialization
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")



 # set up the system message.
system_message = "You are a helpful assistant for understanding the correlation between recent news and the simple price average of a stock. "
system_message += "Give short story of how the news and SMA of a stock are related to each other."
system_message += "Always be accurate. If you don't know the answer, say so."

MODEL = "gpt-4o-mini"
openai = OpenAI()

   

    #tool function
    # There's a particular dictionary structure that's required to describe our function:

searchNewsPrice_function = {
    "name": "searchNewsPrice",
    "description": "Get the news related to the stock symbol (headline, author, publisher, publishing date, senstiment, reason for the sentiment) and SMA (date, SMA for the stock symbol) of a given stock symbol. Call this whenever you need to know the relationship between the news and SMprice action of a specific stock. As, for example when a customer asks 'How the price of a stock between certain days related to the news. You use those days given by the user that decide how far back you want to go to get the news articles and give starting and ending dates for the articles. This interval should not be more than 14 days.'",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The symbol for the stock",
            },
            "pricestartingdate":{
                "type": "string",
                "description": "the string for the starting date for the SMA of the stock"
            },
            "priceendingdate":{
                "type": "string",
                "description": "the string for the ending date for the SMA of the stock"
            },
                "newsstartingdate":{
                "type": "string",
                "description": "the string for the starting date for getting the news about the stock."
            },
                "newsendingdate":{
                "type": "string",
                "description": "the string for the ending date for getting the news about the stock. "
            }, 
            
        },
        "required": ["symbol", "pricestartingdate", "priceendingdate", "newsstartingdate", "newsendingdate"],
        "additionalProperties": False
    }
}

# this is included in a list of tools:
tools = [{"type": "function", "function": searchNewsPrice_function}]



def handle_searchNewsPriceTool(message, symbol, startingdate, endingdate):
    stocknews = StockNews()
    tool_call = message.tool_calls[0] # get the message for the tool
    tool_call_id = tool_call.id
    arguments = json.loads(tool_call.function.arguments) # loading the object
    results = stocknews.searchNewsPrice(arguments.get("symbol"), arguments.get("pricestartingdate"), arguments.get("priceendingdate"), arguments.get("newsstartingdate"), arguments.get("newsendingdate"))
    print(results)
    
    response = {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": json.dumps(results)
    }
    

   
    return response
    

def chat(message, symbol, startingdate, endingdate):
    usermessage = f"{message}. The symbol for the stock is {symbol} and I want to know more about the relationship between the price action and news of this stock between {startingdate} and {endingdate}"
    messages = [{"role": "system", "content": system_message}] + [{"role": "user", "content": usermessage}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools) # adding the tools

    # check if the response requires running tools
    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message # the original with no role but with the id of the tool
        messages.append(message)
        response_handler = handle_searchNewsPriceTool(message, symbol, startingdate, endingdate)
        messages.append(response_handler) # add proper resoinse and a response from role = tool
        print(messages)
        response = openai.chat.completions.create(model=MODEL, messages=messages)
    
    return response.choices[0].message.content


view = gr.Interface(fn = chat,
                    inputs=
                        [
                            #gr.Radio(["gtp", "claude", "gemini", "deepseek"]),
                            gr.Textbox("I am very curious about the price action"),
                            gr.Textbox("SOFI"),
                            gr.Textbox("2024-10-01"),
                            gr.Textbox("2024-10-14"),
                            # gr.Textbox("2025-09-20"),
                            # gr.Textbox("2025-10-07"),
                        ],
                        outputs=gr.Markdown(label="Response"),
                        allow_flagging="never"
                    )
view.launch()    