import tkinter as tk
import openai
root = tk.Tk()
root.title("Advance AI application")



def show_user():
   # Create a Label widget
   label = tk.Label(root, text="user:"+str(entry.get()),font=('Arial 16')).pack(padx=10,anchor="w")
   file=open("history.txt","a")
   file.write("\nuser:"+str(entry.get()))
   file.close()
   gpt(str(entry.get()))
   entry.delete(0,"end")
   


openai.api_key="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"
messages=[
    {"role":"system","content":"you are a kind helpful assisstant"}
]
def gpt(query):
    message=query
    if message:
        messages.append({"role":"user","content":message+"in 15 words"},)#11111111111111111111111
        chat=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    reply=chat.choices[0].message.content
    label2=tk.Label(root, text="Assistant:"+str(reply),font=('Arial 16')).pack(padx=10,anchor="w")
    file1=open("history.txt","a")
    file1.write("\nAssistant:"+str(reply))
    file1.close()
    #speak(reply)
    messages.append({"role":"assistant","content":reply})















































entry = tk.Entry(root,width=30, font=('Arial 18'))
entry.place(relx=.5,rely=.9,anchor="n")

button=tk.Button(text="submit",font=('Arial 12'),command=show_user)
button.place(relx=.9,rely=.9)
root.mainloop()