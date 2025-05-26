from helper.website import Website
import helper.ai_model_helper 


def create_brochure (model, companyname, url):
    website = Website(url)
    contents = website.get_contents()
    system_prompt = "You are a smart assisstant. You will be given the content of a website and you will create a short brochure explaining the main value proposition of the website."
    user_prompt = f'Please make a brochure for {companyname} given this website content: {contents}'
    print (user_prompt)
    yield from helper.ai_model_helper.getaskQuestionStream(model, system_prompt, user_prompt)
    

