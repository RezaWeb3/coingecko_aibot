from openai import OpenAI
import gradio as gr
import io
import os
import dotenv
import glob
import time


# getting the api keys
dotenv.load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error in getting the api key")
else:
    print("Api key found")

#set up the client
client = OpenAI(api_key=api_key)
model = "gpt-4o-mini"

#loading context
context = {}
employees = glob.glob("./knowledgebase/knowledge-base/employees/*")
for employee in employees:
    part = employee.split('\\')[1]
    fullname = part[0: len(part)-3]
    doc = ""
    with open(employee, "r", encoding="utf-8") as f:
        doc = f.read()
    context[fullname] = doc


prods = glob.glob("./knowledgebase/knowledge-base/products/*")
for prod in prods:
    part = prod.split('\\')
    prodname = part[1][0:len(part)-3]
    doc = ""
    with open(prod, "r", encoding="utf-8") as f:
        doc = f.read()
    context[prodname] = doc
print(context)
# helper function to get the relevant context given the message
def getRelevantContext (message):
    print("Getting relevant info: " + message)
    for name in context.keys():
        if name.lower() in message.lower():
            print("found")
            return context[name]
    return None

# if there is a context, prepare a proper promp as additional context
def add_context(message):
    additional_context = getRelevantContext(message)
    if additional_context:
        return message + '.The following context might be helpful in responding to the user:' + additional_context
    else:
        return message



# Define the function that will handle messages
def respond(message, history):
    # system prompt
    system_prompt = "You are an expert on insurllm. Use only the provided relevant data when answering questions about insurllm. If you do not have sufficient data to answer, do not guess or fabricate a response. Instead, reply: \"I don’t have the data to answer that.\" If the comment is not relevant to a product or person in insurllm, just respond normally."
    
    messages = [{'role':'system', 'content':system_prompt}]
    for usermsg, assistantmsg in history:
        messages.append({'role':'user', 'content': usermsg})
        messages.append({'role':'assistant', 'content': assistantmsg})
    additinalcontext = add_context(message)
    messages.append({"role": "user", "content": additinalcontext})
   
    print(messages)
    #for human_msg, bot_msg in history:
    #    messages.append({"role": "user", "content": [{"type": "text", "text": human_msg}]})
    #    messages.append({"role": "assistant", "content": [{"type": "text", "text": bot_msg}]})
    
    response = client.chat.completions.create(messages=messages, max_tokens=1024, stream=True, model=model)
    output = ""
    for chunk in response:
        output += chunk.choices[0].delta.content or ""
        yield output


def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.3)
        yield "You typed: " + message[: i+1]
        

# Create the ChatInterface
demo = gr.ChatInterface(
    fn=respond,
    title="Simgple RAG"
)

# Launch the app
demo.launch()
