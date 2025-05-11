from website import Website
from open_ai import Openai 
from llama import Llama
from deepseek import Deekseekai
from claude import Claude
from gemini import Geminiai


deepseekai = Deekseekai()
claude = Claude()
gemeniai = Geminiai()

def get_systemprompt_firstagent():
    system_prompt = "You are a humorous and crude jokester."
    return system_prompt

def get_userprompt_firstagent ():
    user_prompt = f"Tell a music related joke. "
    return user_prompt



#response = deepseekai.askQuestion(get_systemprompt_firstagent(), get_userprompt_firstagent())
#response = claude.askQuestion(get_systemprompt_firstagent(), get_userprompt_firstagent())
response = gemeniai.askQuestion(get_systemprompt_firstagent(), get_userprompt_firstagent())
print(response)
