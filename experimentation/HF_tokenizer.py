from huggingface_hub import login
from transformers import AutoTokenizer
from dotenv import load_dotenv
import os

load_dotenv(override=True)
hf_token = os.getenv('HUGGINGFACE_TOKEN')
if hf_token:
    print(f"Huggingface Ke exists and begins {hf_token[:8]}")
else:
    print("Huggingface Key not set")
    
login(hf_token, add_to_git_credential=True)

part = "two"

'''Tokenizers'''
if (part == "first"):
    tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3.1-8B', trust_remote_code=True)

    # encoding
    text = "I am very excited about playing around with tokenizers. This is just an example of how tokenizers work."
    tokens = tokenizer.encode(text)
    print(tokens)

    #decoding
    text2 = tokenizer.decode(tokens)
    print(text2)

    # decoding list
    text3 = tokenizer.batch_decode(tokens)
    print(text3)

    # getting the vocabulary of the tokenizer
    vocab = tokenizer.vocab
    print(vocab)
    print(vocab[".Excel"])

#instruct models for chatting
'''Many models have a variant that has been trained for use in Chats.
These are typically labelled with the word "Instruct" at the end.
They have been trained to expect prompts with a particular format that includes system, user and assistant prompts.

There is a utility method apply_chat_template that will convert from the messages list format we are familiar with, into the right input prompt for this model.'''

if (part == "two"):
    # the output is the prompts tokenized
    models = [{"META_MODEL_NAME" : 'meta-llama/Meta-Llama-3.1-8B-Instruct'}, #meta
    {"PHI3_MODEL_NAME" : "microsoft/Phi-3-mini-4k-instruct"}, #microsoft
    {"QWEN2_MODEL_NAME" :"Qwen/Qwen2-7B-Instruct"}, #alibaba
    {"STARCODER2_MODEL_NAME" : "bigcode/starcoder2-3b"}] #hugging face / nvidia

    for model_dic in models:
        for value in model_dic.values():
            tokenizer = AutoTokenizer.from_pretrained(value, trust_remote_code=True)
            messages = [{"role":"system", "content":"you are a helpful assisstant"},
                        {"role": "user", "content":"Tell a funny joke about monkeys"}
                    ]
            print(value)
            print('------------------------------------')
            if value != "bigcode/starcoder2-3b":
                prompts = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt = True)
                print(prompts)
            else:
                print("Skipping")

            text = "I am excited to show Tokenizers in action to my LLM engineers"
            print()
            print(tokenizer.encode(text))
            print()
            tokens = tokenizer.encode(text)
            print(tokenizer.batch_decode(tokens))

    