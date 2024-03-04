import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import openai

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)
openai.api_key="Enter your api key here"
messages=[
    {"role":"system","content":"you are a kind helpful assisstant"}
]

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Tony starks JARIVSR. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...",e)  
        speak("say that again please...")
        return "None"
    return query

def open_website(query):
    website = query.split()[1]
    url = "https://www." + website + ".com"
    webbrowser.open(url)
    print("Opening " + website)
    

def chatgpt(query):
    message=query
    if message:
        messages.append({"role":"user","content":message},)
        chat=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    reply=chat.choices[0].message.content
    print(f"ChatGPT:{reply}")
    speak(reply)
    messages.append({"role":"assistant","content":reply})

    pass
if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()
           
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif "open" in query:
            open_website(query)
        
        elif "notepad" in query:
            os.startfile("notepad.exe")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        
        elif "stop" in query:
            speak("thanks sir")
            break
        else:
            chatgpt(query)
