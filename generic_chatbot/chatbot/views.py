from django.shortcuts import render
import os
import openai

OS = 0 #0 for dev env 1 for linux env
autodec = 1
import platform
if platform.system() == 'Windows' and autodec == 1:
    OS=0
elif platform.system() == 'Linux' and autodec == 1:
    OS=1

if OS == 0:
    baseurl = "chatbot/"
    ipbase = "http://127.0.0.1:8069/"
elif OS == 1:
    baseurl = "path/to/chatbot"
    ipbase = 'hostIP'

MAX_CONTEXT_QUESTIONS = 3

#Replace instructions with your instructions 
INSTRUCTIONS = """
You are an AI tasked with answering questions
"""

Welcome_Message="Hello I am Chatty Cathy, how may I help you?"
def home(request):
    if 'question' in request.GET:
        question=request.GET['question']
        with open(baseurl+'pqa.txt', 'r') as file:
            pqa = file.read()
        
        pqa = pqa.split("¥")
        
        respon=main(question,pqa)
        with open(baseurl+'pqa.txt', 'w') as file:
            try:
                try:
                    xe=pqa[-2]+"¥"+pqa[-1]+"¥"+str(question)+"¥"+str(respon)
                except:
                    xe=pqa[-1]+"¥"+str(question)+"¥"+str(respon)
            except:
                xe=str(question)+"¥"+str(respon)
            file.write(xe)
        
        return render(request, 'home.html', {'title':'Chatbot',"respon" : respon,"previous_question" : question,"previous_answer" : respon, "control": Welcome_Message})
    else:
        respon = Welcome_Message
        return render(request, 'home.html', {'title':'Chatbot',"respon" : respon,"previous_question" : "","previous_answer" : respon, "control": Welcome_Message})


openai.api_key =  "APIKEY goes here"               # or use this to make it more secure os.getenv("OPENAI_API_KEY")

def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    temp3=[]

    for i in range(len(previous_questions_and_answers)):
        if i//2==1:
            continue
        try:
            temp3.append((previous_questions_and_answers[i],previous_questions_and_answers[i+1]))
        except:
            pass
    for question, answer in temp3[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })
    # print(messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",    
        messages=messages,
        temperature=0.05,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.1,

    )
    return completion.choices[0].message.content

def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None

def main(question,previous_questions_and_answers):
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    # previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = question
        # check the question is safe
        errors = get_moderation(new_question)
        if errors:
            return(
                "Sorry, you're question didn't pass the moderation check:"
            )
        
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        return (response)