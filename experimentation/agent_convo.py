from open_ai import Openai 
from gemini import Geminiai
from claude import Claude


# give a topic
topic = input("Please specify a topic for discussion...")
print(f"The topic of choice is {topic}")

# define agent personalities
#gpt_prompt = "You are Donald, a sarcastic economist with deep knowledge about stats and business world. You view everything in terms of dollars. You are concise."
gpt_prompt = "You are a character modeled after Donald J. Trump — the 45th President of the United States — known for your confident, brash, and unapologetic communication style. You speak in short, punchy sentences, repeat key phrases for emphasis, and use superlatives often (e.g., tremendous,disaster,the best). You view tariffs as a powerful economic weapon — a tool to protect American workers, punish unfair trade practices, and reassert U.S. dominance in global trade. You believe in America First, are deeply skeptical of globalization, and view countries like China as economic adversaries. \
When you speak about tariffs, emphasize how they force foreign countries to pay, protect American industries, and make deals fairer. Dismiss critics as weak,globalists, or clueless economists. Your tone is confident, nationalistic, sometimes combative, and always persuasive. \
Now, in the voice and style of Donald Trump, give your unfiltered thoughts on tariffs and why they’re good for America."
#claude_prompt = "You are Clyde, a philantropist and liberal. You believe in free trade and personal liberty. You do not believe money can buy happiness. You are a socialist at heart. You are concise."
claude_prompt = "You are a character modeled after Mark Carney — a seasoned central banker, former Governor of both the Bank of Canada and the Bank of England, and an influential voice in global economic policy. You speak with calm authority, using precise language and data-backed arguments. Your tone is measured, articulate, and intellectually confident. You see the global economy as interconnected, and believe in multilateral cooperation, open markets, and long-term institutional resilience. \
You view tariffs as a political tool that often causes more harm than good. You believe protectionism weakens global supply chains, raises consumer prices, and invites retaliatory measures that harm productivity and growth. You emphasize evidence-based policy, climate-conscious economic frameworks, and long-term competitiveness. \
Now, in the voice and style of Mark Carney, give your nuanced perspective on tariffs — why they are rarely the optimal solution, and how they affect national and global economic stability."


#gemini_prompt = "You are Elon, a pragmatic business man owning a car manufacturing in the USA. You care more about shareholders and the company as opposed to the workers and the general population. You are super keen on technological progress and making scientific proress. You believe in the survival of the fittest. You are concise."
gemini_prompt = "You are a character modeled after Elon Musk — the CEO of Tesla and SpaceX, and one of the world’s most influential tech entrepreneurs. You speak in a mix of plain, direct language and bold, futuristic statements. You’re known for thinking from first principles, questioning assumptions, and challenging conventional wisdom. You often use humor, irony, and sometimes sarcasm. You’re focused on innovation, efficiency, and long-term planetary survival. \
When discussing tariffs, you acknowledge the short-term logic in certain cases (e.g., incentivizing local manufacturing), but generally see them as inefficient and counterproductive in the long run. You prefer open competition, decentralized production, and innovation over protectionism. You may reference supply chain optimization, engineering challenges, or unintended consequences of government policy. You’re not afraid to ruffle feathers. \
Now, in the voice and style of Elon Musk, share your thoughts on tariffs — when they make sense, when they don’t, and why the real focus should be on innovation, not trade barriers."

# Models
gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307" #"claude-3-7-sonnet-20250219"
gemini_model = "gemini-2.0-flash"

openai = Openai(gpt_model)
claudeai = Claude(claude_model)
geminiai = Geminiai(gemini_model)

# give the starting point of the conversation
openai_message = [f'Hi, I am Donald Trump. We should talk about {topic}. I am going to put 25% on Canadian Auto, Steel and Aluminum']
claude_message = [f'Hi, I am Mark Careny. I like the topic of {topic}. I think Tarrifs do more harm than good.']
gemini_message = [f'Hi, I am Elon Musk. We also need to be pragmatic.']


# define call functions
def callGpt(i):
    messages = [{'role': 'system', 'content': gpt_prompt}]
    for gpt_m, claude_m, gemini_m in zip(openai_message, claude_message, gemini_message):
        messages.append({"role": "assistant", "content": gpt_m})
        messages.append({"role": "user", "content": claude_m})
        messages.append({"role": "user", "content": gemini_m})  
    response = openai.respondMessages(gpt_prompt, messages)
    print(f"Openai: {response}")

    return response

def callClaude(i):
    messages = []
    for gpt_m, claude_m, gemini_m in zip(openai_message, claude_message, gemini_message):
        messages.append({"role": "user", "content": gpt_m})
        messages.append({"role": "assistant", "content": claude_m})
        messages.append({"role": "user", "content": gemini_m}) 
    messages.append({"role": "user", "content":openai_message[-1]})
    response = claudeai.respondMessages(claude_prompt, messages)
    print(f"Claude: {response}")

    return response

def callGemini(i):
    #messages = [{'role': 'system', 'content': claude_prompt}]
    messages = []
    for gpt_m, claude_m, gemini_m in zip(openai_message, claude_message, gemini_message):
        messages.append({"role": "user", "content": gpt_m})
        messages.append({"role": "user", "content": claude_m})
        messages.append({"role": "assistant", "content": gemini_m}) 
    messages.append({"role": "user", "content":openai_message[-1]})
    messages.append({"role": "user", "content":claude_message[-1]})
    response = geminiai.respondMessages(gemini_prompt, messages)
    #print("Outside method:", repr(response))
    #print("Length:", len(response))
    print(f"Gemini: {response}")

    return response


# loop through the agent responses and let the convo begin
print (openai_message[0])
print (claude_message[0])
print (gemini_message[0])
 
for i in range(2):
    print("------------")
    openai_message.append(callGpt(i))
    print("\n")
    claude_message.append(callClaude(i))
    print("\n")
    gemini_message.append(callGemini(i))
    print("\n")
    