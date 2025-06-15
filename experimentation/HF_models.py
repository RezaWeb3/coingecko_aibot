'''# Models
And now - this colab unveils the heart (or the brains?) of the transformers library - the models:
https://colab.research.google.com/drive/1hhR9Z-yiqjUe7pJjVQw4c74z_V3VchLy?usp=sharing
This should run nicely on a low-cost or free T4 box.'''

#  pip install -q requests torch bitsandbytes transformers sentencepiece accelerate

from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
import torch
import gc
import os
from dotenv import load_dotenv

load_dotenv(override=True)
hf_token = os.getenv('HUGGINGFACE_TOKEN')
if hf_token:
    print(f"Huggingface Ke exists and begins {hf_token[:8]}")
else:
    print("Huggingface Key not set")
    
login(hf_token, add_to_git_credential=True)


# models
# instruct models

LLAMA = "meta-llama/Meta-Llama-3.1-8B-Instruct"
PHI3 = "microsoft/Phi-3-mini-4k-instruct"
GEMMA2 = "google/gemma-2-2b-it"
QWEN2 = "Qwen/Qwen2-7B-Instruct" 
MIXTRAL = "mistralai/Mixtral-8x7B-Instruct-v0.1" # If this doesn't fit it your GPU memory, try others from the hub



# Quantization Config - this allows us to load the model into memory and use less memory. Losing precision

# PLS note that this requires GPU
quant_config = BitsAndBytesConfig(
    load_in_4bit=True, # 32 bits --> 4 bits
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4" # --> Normalizing to 4 bits 
)

modelname = LLAMA

if modelname == LLAMA:
    messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Tell a light-hearted joke for a room of Data Scientists"}
    ]
    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(modelname)
    tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cpu") # if you have gpu, change it to "cuda"/ pt stands for pytorch

    # models
    model = AutoModelForCausalLM.from_pretrained(modelname, device_map="auto")#, quantization_config=quant_config) # we usually use causal LLMs
    output = model.generate(inputs=inputs, max_new_tokens=80)
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(text)
elif modelname == GEMMA2:
    messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Tell a light-hearted joke for a room of Data Scientists"}
    ]
    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(modelname)
    tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cpu") # if you have gpu, change it to "cuda"/ pt stands for pytorch

    # models
    model = AutoModelForCausalLM.from_pretrained(modelname, device_map="auto")#, quantization_config=quant_config) # we usually use causal LLMs
    output = model.generate(inputs=inputs, max_new_tokens=80)
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(text)
else:
    print("error - model does not exist")
