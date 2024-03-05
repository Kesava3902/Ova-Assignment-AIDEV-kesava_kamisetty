from tkinter import *
import openai
import replicate
from dotenv import load_dotenv
import requests
from PIL import Image,ImageTk
import jarvis as js
load_dotenv()


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class Application:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("OVA")
        #self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome to OVA", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Label(self.window, width=20, height=2, bg=BG_COLOR,fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure()#command=self.text_widget.yview
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.50, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,command=self.show_user)
        send_button.place(relx=0.55, rely=0.008, relheight=0.06, relwidth=0.12)

        #upload button
        upload_button = Button(bottom_label, text="upload", font=FONT_BOLD, width=20, bg=BG_GRAY)
        upload_button.place(relx=0.68, rely=0.008, relheight=0.06, relwidth=0.15)
        
        #speak button
        speak_button = Button(bottom_label, text="Speak", font=FONT_BOLD, width=20, bg=BG_GRAY,command=self.user_speaking)
        speak_button.place(relx=0.83, rely=0.008, relheight=0.06, relwidth=0.14)

    def show_user(self):
        label = Label(self.text_widget, text="user:"+str(self.msg_entry.get()),font=('Arial 16')).pack(padx=10,anchor="w")
        if "generate" in str(self.msg_entry.get()):
            self.image_genaration(str(self.msg_entry.get()))
        else:
            self.gpt(self.msg_entry.get())
        file=open("history.txt","a")
        file.write("\nuser:"+str(self.msg_entry.get()))
        file.close()
        self.msg_entry.delete(0,"end")

    def gpt(self,query):
        openai.api_key="api disclosed"
        messages=[
    {"role":"system","content":"you are a kind helpful assisstant"}
     ]
        message=query
        if message:
            messages.append({"role":"user","content":message+"in 15 words"},)
        chat=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        reply=chat.choices[0].message.content
        label2=Label(self.text_widget, text="Assistant:"+str(reply),font=('Arial 16')).pack(padx=10,anchor="w")
        file1=open("history.txt","a")
        file1.write("\nAssistant:"+str(reply))
        file1.close()
        messages.append({"role":"assistant","content":reply})
        return reply
    
    def image_genaration(self,query):
        output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={
        "width": 768,
        "height": 768,
        "prompt": str(query),
        "refine": "expert_ensemble_refiner",
        "scheduler": "K_EULER",
        "lora_scale": 0.6,
        "num_outputs": 1,
        "guidance_scale": 7.5,
        "apply_watermark": False,
        "high_noise_frac": 0.8,
        "negative_prompt": "",
        "prompt_strength": 0.8,
        "num_inference_steps": 25
    }
    )
        print(output)
        self.image_download(output[0],"output.jpg")
        imageq = Image.open('output.jpg',"r").resize((300,205), Image.ANTIALIAS)
        imageq = ImageTk.PhotoImage(imageq)
        image_label = Label(self.text_widget,image=imageq)
        image_label.pack(anchor="n")
        image_label.image=imageq

    def image_download(self,img_url,filename):
        response =requests.get(img_url)
        if response.status_code == 200:
            with open(filename,"wb") as file:
                file.write(response.content)
        else:
            print("failure occured in image downloading")
        
    def user_speaking(self):
        query=js.takeCommand()
        label = Label(self.text_widget, text="user:"+str(query),font=('Arial 16')).pack(padx=10,anchor="w")
        file=open("history.txt","a")
        file.write("\nuser:"+str(query))
        file.close()
        if "open" in query:
            self.open_website(query)
        else:
            reply=self.gpt(query)
            js.speak(reply)

    def open_website(self,query):
        website = query.split()[1]
        url = "https://www." + website + ".com"
        js.webbrowser.open(url)
        print("Opening " + website)











if __name__=="__main__":
    app=Application()
    app.run()
    
