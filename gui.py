import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from predict import *
import os
from threading import Thread

# Load your model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('./tokenizer')
model = AutoModelForSeq2SeqLM.from_pretrained('./model')


def out():
    prompt = input_box.get("1.0", "end-1c")
    output = predict(prompt, tokenizer=tokenizer, model=model)
    
    # Add a new line after every period in the output
    output = output.replace('.', '.\n')

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output)
    output_box.config(state=tk.DISABLED)


def on_drop(event):
    file_path = os.path.normpath(event.data.replace('{', '').replace('}', ''))
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, file_content)
    except Exception as e:
        print(f"Error loading file: {e}")

def on_resize(event):
    # Update the sizes and positions of widgets when the window is resized
    window.update_idletasks()
    
    
# Create the main window
window = TkinterDnD.Tk()
window.title('Conversation Summarizer')
window.geometry('900x700')
window.configure(bg='black')  # Set background color to black
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.bind('<Configure>', on_resize)

# Create ttk style for customization
style = ttk.Style()
style.configure('TButton',
                padding=(1, 3),
                borderwidth=5,
                relief=tk.RAISED,
                font=("Segoe UI Emoji", 11),
                foreground='black',
                background='#333333'
                )  # Set style properties for the button


# Use ttk themed button with rounded corners
button_frame = tk.Frame(window,
                        background='black'
                        )
button_frame.grid(row=0,
                  column=0,
                  sticky='nsew'
                  )

summarize_button = ttk.Button(button_frame,
                              width=12,
                              text='Summarize',
                              command=out,
                              style='TButton'
                              )
summarize_button.pack(
    side=tk.TOP,
    pady=3
)


# Frame for input
main_frame = tk.Frame(window,
                       background='black'
                       )
main_frame.grid(row=1,
                column=0,
                sticky='nsew',
                padx=10,
                pady=10
                )
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

input_label = tk.Label(main_frame,
                       text='Input box',
                       background='black',
                       font=("Segoe UI Emoji",20,'bold'),
                       foreground='white'
                       )
input_label.grid(row=0,
                 column=0,
                 sticky='nsew'
                 )

input_box = tk.Text(main_frame,
                    bg='#333333',
                    font=("Segoe UI Emoji", 12,'normal'),
                    relief=tk.FLAT,
                    highlightthickness=0,
                    highlightbackground='#000000',
                    insertbackground='white',
                    foreground='white'
                    )
input_box.grid(row=1,
               column=0,
               sticky='nsew',
               padx=5
)

output_label = tk.Label(main_frame,
                       text='Output box',
                       background='black',
                       font=("Segoe UI Emoji",20,'bold'),
                       foreground='white'
                       )
output_label.grid(row=0,
                  column=1,
                  sticky='nsew'
                  )

# Use ttk themed text widget for output with a shiny gray background, thicker border, and circular corners
output_box = tk.Text(main_frame,
                     state=tk.DISABLED,
                     bg='#333333',
                     font=("Times New Roman", 12,'normal'),
                     bd=3,
                     relief=tk.FLAT,
                     highlightthickness=0,
                     highlightbackground='#000000',
                     foreground='white'
                     )
output_box.grid(row=1,
                column=1,
                sticky='nsew',
                padx=5
                )

# Bind the drop event to the on_drop function
input_box.drop_target_register(DND_FILES)
input_box.dnd_bind('<<Drop>>', on_drop)


# Start the Tkinter event loop
window.mainloop()
