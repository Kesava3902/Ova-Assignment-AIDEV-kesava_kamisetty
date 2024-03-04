#features includes text to tex
#image generation
#audio to audio
#some functionalities like opening web pages through voice commands.these commands in jarvis python file
import tkinter as tk
import openai
import replicate
from dotenv import load_dotenv
import requests
from PIL import Image,ImageTk
import jarvis as js
load_dotenv()

root = tk.Tk()
root.title("Advance AI application")
root.geometry("600x1200")


def show_user():
   # Create a Label widget
   label = tk.Label(root, text="user:"+str(entry.get()),font=('Arial 16')).pack(padx=10,anchor="w")
   file=open("history.txt","a")
   file.write("\nuser:"+str(entry.get()))
   file.close()
   if "generate" in str(entry.get()):
       image_genaration(str(entry.get()))
   else:
      gpt(str(entry.get()))
      

   entry.delete(0,"end")
   


openai.api_key="Enter api key"#disclosed 
messages=[
    {"role":"system","content":"you are a kind helpful assisstant"}
]
def gpt(query):
    message=query
    if message:
        messages.append({"role":"user","content":message+"in 15 words"},)
        chat=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    reply=chat.choices[0].message.content
    label2=tk.Label(root, text="Assistant:"+str(reply),font=('Arial 16')).pack(padx=10,anchor="w")
    file1=open("history.txt","a")
    file1.write("\nAssistant:"+str(reply))
    file1.close()
    #speak(reply)
    messages.append({"role":"assistant","content":reply})
    return reply

def image_genaration(query):
    output = replicate.run(
    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input={
        "width": 768,
        "height": 768,
        "prompt": str(query),
        "scheduler": "K_EULER",
        "num_outputs": 1,
        "guidance_scale": 7.5,
        "num_inference_steps": 50
    }
    )
    print(output)
    image_download(output[0],"output.jpg")
    imageq = Image.open('output.jpg')
    imageq = ImageTk.PhotoImage(imageq)
    print("done1")
    image_label = tk.Label(root, image=ImageTk.PhotoImage(Image.open('output.jpg')),height=40,width=40)
    image_label.pack()
    image_label.pack_configure()
    print("done2")

def image_download(img_url,filename):
    response =requests.get(img_url)
    if response.status_code == 200:
        with open(filename,"wb") as file:
            file.write(response.content)
    else:
        print("failure occured in image downloading")



def user_speaking():
    query=js.takeCommand()
    label = tk.Label(root, text="user:"+str(query),font=('Arial 16')).pack(padx=10,anchor="w")
    file=open("history.txt","a")
    file.write("\nuser:"+str(query))
    file.close()
    reply=gpt(query)
    js.speak(reply)


entry = tk.Entry(root,width=30, font=('Arial 18'))
entry.place(relx=.5,rely=.9,anchor="n")

button2=tk.Button(text="Speak",font=('Arial 12'),command=user_speaking)
button2.place(relx=.3,rely=.9)

button=tk.Button(text="submit",font=('Arial 12'),command=show_user)
button.place(relx=.9,rely=.9)
root.mainloop()
