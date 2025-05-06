# imports

import os
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI


# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url

        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        options = Options()
        options.add_argument(f"user-agent={userAgent}")
        options.add_argument("--headless")
        
        driver = webdriver.Chrome(options = options)#, executable_path= "C:/Users/r_sab/chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
        print(self.text)
     

def get_user_prompt(website): 
    user_prompt = "This is the content of CoinGecko. " +  website.text
    return user_prompt

# Create a messages list using the same format that we used for OpenAI




def analyze_content (url, tokenname):
    website = Website(url)
    system_prompt = "You are an intelligent crypto day trader. You will be given content to analyze " + tokenname + " and give good advice whether to be bullish or bearish about it."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": get_user_prompt(website)}
    ]
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    print("Ollama...")
    print(response.json())
    #response = ollama.chat(model=MODEL, messages=messages)
    return response
    


# If this doesn't work for any reason, try the 2 versions in the following cells
# And double check the instructions in the 'Recap on installation of Ollama' at the top of this lab
# And if none of that works - contact me!

response = analyze_content("https://www.coingecko.com/en/coins/hyperliquid", "Hyperliquid")
print(response.json()['message']['content'])

