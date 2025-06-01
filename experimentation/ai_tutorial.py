from helper.website import Website
from model_wrappers.open_ai import Openai 
from model_wrappers.llama import Llama


oi = Openai("gpt-4o-mini")
ollama = Llama()



def get_systemprompt_firstagent():
    system_prompt = "You are savvy and efficient business analyst. \
    You are able to look at a business idea and find ways to make it profitable and find creative ways to scale it.\n"
    system_prompt += "You always search for analogous examples worldwide to cite as an exaple."

    return system_prompt

def get_systemprompt_secondagent():
    system_prompt = "You are savvy and efficient business person. \
    You can analyze business ideas shared with you and analyze them thoroughly based on your knowledge and experience.\n"
    system_prompt += "You compare the business to what you know or have seen in the real world to offer pros and cons of the idea."

    return system_prompt

def get_userprompt_firstagent (userquestion):
    user_prompt = f"I have an idea for starting a business in a given city or country.\n \
        My idea is {userquestion}. Would you analyze the idea for me?"

    return user_prompt


def get_userprompt_secondagent(userquestion, userprompt_firstagent, response_first_agent):
    user_prompt = f"I have an idea for starting a business.\n \
        My idea is {userquestion}. I asked this to an AI agent {userprompt_firstagent} suggested the following {response_first_agent}.\n \
            I need you to poke holes in the 1st agent's analysis."
    return user_prompt

location = "Toronto"
user_input = input("Ask your questions?")
print("You entered:", user_input)
print(get_systemprompt_firstagent())
print(get_systemprompt_secondagent())

# first agent
user_input_1st_agent = get_userprompt_firstagent(user_input)
print(get_systemprompt_firstagent(), get_userprompt_firstagent(user_input))

#agent_openai = Openai()
#agent_openai_response = agent_openai.askQuestion(get_systemprompt_firstagent(), get_userprompt_firstagent(user_input))

agent_ollama = Llama()
agent_ollama_response = agent_ollama.askQuestion(get_systemprompt_firstagent(), get_userprompt_firstagent(user_input))

#second agent
print(agent_ollama_response)
#print(get_userprompt_secondagent(user_input, user_input_1st_agent, agent1_response))