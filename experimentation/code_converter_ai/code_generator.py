import gradio as gr
import openai_codegenerator as oc
import claude_codegenerator as cc

with open('./code_converter_ai/orginalcode.py', 'r') as file:
    original_code = file.read()



def call_model(model, language, code):
    if model.find("gpt") > -1:
        return oc.generatecode(model, language, code)
    else:
        return cc.generatecode(model, language, code)
    

view = gr.Interface(fn =call_model,
                    inputs=
                        [
                            gr.Radio(["gpt-4o-mini", "gpt-4o", "claude-sonnet-4-20250514"]),
                            gr.Radio(["++", "C#", "javascript", "GO", "RUST", "Solidity"]),
                            gr.Textbox(original_code),
                        ],
                        outputs=gr.Markdown(),
                        allow_flagging="never"
                    )
view.launch()







