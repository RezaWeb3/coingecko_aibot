import gradio as gr
import os
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import anthropic
import helper.ai_model_helper
import helper.airline_ticket_api
import helper.brochure_helper
import json
import helper.airline_ticket_api as airline_api

# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4o-mini"
openai = OpenAI()

# set up the system message.
system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


#tool function
# There's a particular dictionary structure that's required to describe our function:

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

# this is included in a list of tools:
tools = [{"type": "function", "function": price_function}]

def get_ticket_price(destination_city):
    return helper.airline_ticket_api.getTicketPrice(destination_city)

# handling tool calls from openai
def handle_price_tool_call(message):
    tool_call = message.tool_calls[0] # get the message for the tool
    arguments = json.loads(tool_call.function.arguments) # loading the object
    city = arguments.get('destination_city') # get the city
    price = get_ticket_price(city) # getting the price for that city
    # building the proper tool response
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price}),
        "tool_call_id": tool_call.id
    }
    return response, city

# Just simple result back. no streaming needed given the short answers
def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools) # adding the tools

    # check if the response requires running tools
    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        
        response, city = handle_price_tool_call(message)
        messages.append(message) # add the original message with no role
        messages.append(response) # add proper resoinse and a response from role = tool
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content




gr.ChatInterface(fn=chat, type="messages").launch()


