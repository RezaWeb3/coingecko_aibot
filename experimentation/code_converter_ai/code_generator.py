import gradio as gr
import openai_codegenerator as oc
import claude_codegenerator as cc

with open('./code_converter_ai/orginalcode.py', 'r') as file:
    original_code = file.read()



def call_model(model, language, code):
    output = ""
    if model.find("gpt") > -1:
        result = oc.generatecode(model, language, code)
    else:
        result = cc.generatecode(model, language, code)
    if result != None:
        for chunk in result:
            output += chunk
            yield output
    
# older dashboard
'''view = gr.Interface(fn =call_model,
                    inputs=
                        [
                            gr.Radio(["gpt-4o-mini", "gpt-4o", "claude-sonnet-4-20250514"]),
                            gr.Radio(["++", "C#", "javascript", "GO", "RUST", "Solidity"]),
                            gr.Textbox(original_code),
                            gr.Button
                        ],
                        outputs=gr.Markdown(),
                        allow_flagging="never"
                    )
view.launch()'''


def get_prefix(language):
    mapping = {
        "C++": "cpp",
        "C#": "cs",
        "javascript": "js",
        "GO": "go",
        "RUST": "rs",
        "Solidity": "sol"
    }
    return mapping.get(language, "txt")

# gradio dashboard
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Code Converter AI")
    
    with gr.Row():
        model_choice = gr.Radio(["gpt-4o-mini", "gpt-4o", "claude-sonnet-4-20250514"], label="Model")
        language_choice = gr.Radio(["C++", "C#", "javascript", "GO", "RUST", "Solidity"], label="Target Language")
        prefix = gr.Textbox(value="txt", visible=False)
        # Update prefix when language changes
        language_choice.change(fn=get_prefix, inputs=language_choice, outputs=prefix)


    code_input = gr.Textbox(value=original_code, lines=20, label="Original Code")
    submit_btn = gr.Button("Generate Code")
    output_display = gr.Markdown(label="Converted Output")

    #save output to file
    save_btn = gr.Button("Save to File")
    file_output = gr.File(label="Download File")

    # Click event to run model
    submit_btn.click(
        fn=call_model,
        inputs=[model_choice, language_choice, code_input],
        outputs=output_display
    )

    # Save to file
    def save_to_file(output, model_choice, language, prefix):
        path = f"converted_code_{model_choice}_{language}.{prefix}"
        with open(path, "w") as f:
            f.write(output)
        return path

    save_btn.click(fn=save_to_file, inputs=[output_display, model_choice, language_choice, prefix], outputs=file_output)

demo.launch()






