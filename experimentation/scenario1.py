from website import Website
from open_ai import Openai 
from llama import Llama


oi = Openai()
ollama = Llama()



# User: asks question about a business idea
user_input = input("What is your busiess idea? Where would you like to pursue this business?")
print("You entered:", user_input)


# Agent1: Gives a summary of an opinion about the business with a clear verdict whether one should pursue it or not
system_prompt_agent1 = "You are savvy and efficient business analyst. \
   You are given a business idea in a specific location. You analyze the business idea and identify top 3 reasons why this idea is a good idea. \
   You offer your response in 100 words or fewer. \
   Then you offer a point form actions that one needs to take to execute this idea successfully \
   "

user_prompt_agent1 = f"My idea is {user_input}."
agent1 = Openai()
agent1_response = agent1.askQuestion(system_prompt_agent1, user_prompt_agent1)

print("-------------------------------")
print("Agent 1's idea about the business")
print (agent1_response)

# agent2: looks at the summary and poke holes in the strategy or practicality of the idea using analougous examples of the idea as an opposition
system_prompt_agent_2 = "You are savvy and efficient business analyst. \
   You are given a business idea with analysis of someone else that why the business is a good idea with some actions to be taken in order to launch it successfully. " \
   "You read this and poke holes in the analysis and find analogous examples why this idea might not be a good idea. " \
   "You can include examples of other countries. \
   You also can share the blindspots and shortcomings of the actions listed by the other analyst. \
   Share your response in 1000 words or fewer. \
   "

user_prompt_agent2 = f"The business idea is {user_input}. The analysis of the analyst is {agent1_response}."
agent2 = Llama()
agent2_response = agent2.askQuestion(system_prompt_agent_2, user_prompt_agent2)

print("-------------------------------")
print("Agent 2's critique for the analysis of the business idea and the analysts response")
print (agent2_response)

# agent1: Reads the critic and defends why the critic is not valid or more data is needed.
# user sees this interation

system_prompt_agent_1 = "You are savvy and efficient business analyst. \
   You are open to critism. Someone asked you about their business idea. You have given your opinion and action plan. \
   Then another analyst criticizes your opinion and action plans. You read both of these, try to make a more balanced view. \
   Initially, you revise your initial opinion whether you think the idea is still strong or not.  \
   If the idea is still strong, give a GO decision to the user but offer a more balanced point of view and revise the action steps based on the critism if you think the crisim is valid. \
   If the idea is no longer strong enough, explain to the user why you have revised your position and what were the blind spots or flaws in the initial advis you gave.  \
   "

user_prompt_agent1 = f"The business idea is {user_input}. Your initial advise and actions were {agent1_response}. The second analysts critic was {agent2_response}."
agent1_response = agent1.askQuestion(system_prompt_agent_1, user_prompt_agent1)
print("-------------------------------")
print("Revised position by the first agent:")
print (agent1_response)


