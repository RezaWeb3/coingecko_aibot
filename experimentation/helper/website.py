# imports
# If these fail, please check you're running from an 'activated' environment with (llms) in the command prompt

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time


# A class to represent a Webpage

# Some websites need you to use proper headers when fetching them and using beautiful soup, we make an object out of the website DOM
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url):
        self.url = url
        
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        options = Options()
        options.add_argument(f"user-agent={userAgent}")
        options.add_argument("--headless")
        # use sellenium to get the page
        driver = webdriver.Chrome(options = options)#, executable_path= "C:/Users/r_sab/chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Check if Title exists, add it to the Webpage class or otherwise ignore
        self.title = soup.title.string if soup.title else "No title found"
        
        if soup.body:
            # get rid of the irrelevant parts of the page
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            # get the remaining parts of the DOM and add them to the text
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        # get each "a" tag and if it has a href tag, add it to the links
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    

