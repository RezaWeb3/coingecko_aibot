# imports

import os
import json
from dotenv import load_dotenv
import gradio as gr
from model_wrappers.open_ai import Openai
from io import BytesIO
from PIL import Image

MODEL = "gpt-4o-mini"
openai = Openai(MODEL)

system_message = "You are a helpful assistant for a travel agency. When a customer asks for travelling to a city, you first  check the weather in the country for the given city before checking the ticket price to travel to that city.  If the weather is rainy or stormy, give a tarvel warning to the user and ask whether they would still like to travel. If the weather is ok or if the customer said they want to travel anyway,  you will give the ticket price to travel to that city. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
weather = {"england": "Rainy", "france": "Cloudy", "japan": "Sunny", "germany": "Stormy"}


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

weather_function = {
    "name" : "get_weather_country",
    "description" : "Get the weather condition for a country. Call this whenever you need to know how the weather in a country given the city name within that country at the moment. For example, a customer asks for travelling to Paris, but you check the weather in France ",
    "parameters" : {
        "type" : "object",
        "properties":{
            "destination":{
                "type" : "string",
                "description": "The country that the customer is interested to travel"
            }
        }
    },
    "required" : ["destination"],
    "additionalProperties" : False
}

draw_country_weather_function = {
    "name" : "draw_country_weather",
    "description" : f"An image representing a vacation in destination_country with the given weather, showing tourist spots and everything unique in a vibrant pop-art style",
    "parameters" : {
        "type" : "object",
        "properties":{
            "destination_country":{
                "type" : "string",
                "description": "The country that the customer is interested to travel"
            },
            "weather":{
                "type" : "string",
                "description": "The current weather condition in that country"
            }
        }
    },
    "required" : ["destination_country", "weather"],
    "additionalProperties" : False
}




tools = [{"type": "function", "function": price_function},
         {"type": "function", "function": weather_function},
         {"type": "function", "function": draw_country_weather_function}
         ]


def draw_country_weather (destination_country, weather):
    image_data = openai.draw(f"An image representing a vacation in {destination_country} with the {weather} weather, showing tourist spots and everything unique in a vibrant pop-art style")
    return image_data
    #return Image.open(BytesIO(image_data))

def voice (destination_city, price):
    return


def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

def get_weather_country(country):
    print(f"Tool get_weather_country called for {country}")
    country = country.lower()
    return weather.get(country, "Unknown")

# handling tool calls from openai
# handling tool calls from openai
def handle_country_tool_call(response_dict):
    # Access the raw JSON string of the arguments
    arguments_json = response_dict["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    tool_id =  response_dict["choices"][0]["message"]["tool_calls"][0]["id"]
    # Parse it into a dictionary
    arguments = json.loads(arguments_json)
    # Now access the destination_city correctly
    country = arguments["destination"]
    weather = get_weather_country(country)
    
    # building the proper tool response
    response = {
        "role": "tool",
        "content": json.dumps({"country": country,"weather": weather}),
        "tool_call_id": tool_id
    }

    return response, country


def handle_drawing_country_weather(response_dict):
    arguments_json = response_dict["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    tool_id =  response_dict["choices"][0]["message"]["tool_calls"][0]["id"]
    # Parse it into a dictionary
    arguments = json.loads(arguments_json)
    # Now access the destination_city correctly
    country = arguments["destination_country"]
    weather = arguments["weather"]
    image_data = draw_country_weather (country, weather)
    # building the proper tool response
    response = {
        "role": "tool",
        "content": image_data,
        "tool_call_id": tool_id
    }
    
    #Image.open(BytesIO(image_data))
    return response

def handle_city_price(response_dict):
    # Access the raw JSON string of the arguments
    arguments_json = response_dict["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    tool_id =  response_dict["choices"][0]["message"]["tool_calls"][0]["id"]
    # Parse it into a dictionary
    arguments = json.loads(arguments_json)
    # Now access the destination_city correctly
    city = arguments["destination_city"]
    price = get_ticket_price(city)
    
    # building the proper tool response
    response = {
        "role": "tool",
        "content": json.dumps({"city": city,"price": price}),
        "tool_call_id": tool_id
    }

    return response, city


tool_handlers = {
    "get_weather_country": handle_country_tool_call,
    "get_ticket_price" : handle_city_price,
    "draw_country_weather" : handle_drawing_country_weather
    # add more tools here as needed
}

def chat(message, history):
    print (message)
    print (history)
    #return result
    messages = history + [{"role": "user", "content": message}]
    response = openai.respondMessages(system_message, messages, tools)
    print("Right here")
    print(response)
    print(response.choices[0].finish_reason)  
   
   
    while response.choices[0].finish_reason == "tool_calls":
        response_dict = response.model_dump()
        tool_call = response_dict["choices"][0]["message"]["tool_calls"][0]
        function_name = tool_call["function"]["name"]

        # Call the appropriate handler if available
        handler = tool_handlers.get(function_name)

        if (function_name.find("draw") == -1):
            messages.append(response.choices[0].message)
            response, result = handler(response_dict)
            messages.append(response) # add response from a tool
            response = openai.respondMessages(system_prompt=system_message, messages=messages, tools = tools) # have to call again because the response is not a chatCompilation 
        else:
            image_data = handler(response_dict)
            return  history + [(message, BytesIO(image_data["content"]))]
      
    response_dict = response.model_dump()
    print("RESPONSE:")
    print ( response_dict)
    return response_dict["choices"][0]["message"]["content"]     


def chat_fn(message, history):
    # Create a dummy image (replace with your image logic)
    img = Image.new("RGB", (100, 100), color="lightblue")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return history + [
        {"role": "user", "content": {"text": message}},
        {"role": "assistant", "content": {"text": "Here is your image", "files": [buf]}}
    ]


gr.ChatInterface(fn=chat_fn, type="messages", multimodal=True).launch()

