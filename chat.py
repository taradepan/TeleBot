import google.generativeai as genai
import cohere
import PIL.Image
import io
import os
import dotenv
dotenv.load_dotenv()

cohere_api=os.environ.get('COHERE_API')
co = cohere.Client(cohere_api)

chat_history = []
user_message = {"role": "USER", "text": """
                Imagine you are an AI Chatbot. your name is Igris. You are designed to help users with their queries, have friendly conversation, etc.
                You were created by Taradepan. Talk like a good friend.                
"""}
bot_message = {"role": "CHATBOT", "text": "got it"}
chat_history.append(user_message)
chat_history.append(bot_message)

genai.configure(api_key=os.environ.get('GEMINI')) 
def gchat(prompt):
    
    response = co.chat(
        message=prompt,
        connectors=[{"id":"web-search"}],   
        chat_history=chat_history,
    )
    answer = response.text
    user_message = {"role": "USER", "text": prompt}
    bot_message = {"role": "CHATBOT", "text": answer}
    chat_history.append(user_message)
    chat_history.append(bot_message)
    print(chat_history)
    return answer

    

def gimg(prompt, file):
    model = genai.GenerativeModel('gemini-pro-vision')
    file_content = file.download_as_bytearray()
    img = PIL.Image.open(io.BytesIO(file_content))
    prompt = "If user doesn't give any prompt then explain what you see in the image in detail otherwise answer based on the prompt. Prompt: "+str(prompt)
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    if chat_history and chat_history[-1]['role'] == "USER":
        chat_history.append(
        {'role':'CHATBOT',
         'text': "there was an error"}
    )
    chat_history.append(
    {'role':'USER',
     'text': "image"}
    )
    chat_history.append(
    {'role':'CHATBOT',
     'text': response.text}
    )
    print(response.text)
    return response.text