from  model_wrappers.open_ai import Openai
from  model_wrappers.claude import Claude
from model_wrappers.gemini import Geminiai
from model_wrappers.deepseek import Deekseekai

def getaskQuestionStream(model_radio, system_prompt, user_question):
    model = None
    print("Model:" + model_radio)
    if model_radio == "gtp":
        model = Openai("gpt-4o-mini")
    elif model_radio == "claude":
        model = Claude("claude-3-7-sonnet-latest")
    elif model_radio == "gemini":
        model = Geminiai('gemini-2.0-flash')
    elif model_radio == "deepseek":
        model = Deekseekai("deepseek-chat")
    else:
        raise ValueError("Model not defined")

    yield from model.askQuestionStream(system_prompt, user_question)