from __future__ import print_function
import logging
import sys
import os
import transformers
import torch
import tkinter as tk
from twilio.rest import Client

padding = 1
phone_number = "+17752275908"

logging.basicConfig(level='ERROR')

check_count = 0

account_sid= "AC7a4b5fbc13f00328b31eb600b155eb5d"
auth_token= "85a4fd768eee6bf127e72bdc7d7398ed"

client = Client(account_sid, auth_token)

sms_save = ""
phone_number_to = ''
options = []
remember = "Remember That This is a message board, "

# Loading in gpt2
gpt_tokenizer = transformers.GPT2Tokenizer.from_pretrained(str(sys.argv[1]))
# Loading in model
gpt_model = transformers.GPT2LMHeadModel.from_pretrained(str(sys.argv[1]))



def send_text(message_body, to, from_, chain):
    client.messages.create(
        to=to,
        from_=from_,
        body=message_body
    )

    chain.write('You: ' + message_body + '\n')

# Text generation function
def gen_text(prompt_text, tokenizer, model, n_seqs=1, max_length=25):

    encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=False, return_tensors="pt")

    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=max_length + len(encoded_prompt[0]),
        temperature=1.0,
        top_k=0,
        top_p=0.9,
        repetition_penalty=1.2,
        do_sample=True,
        num_return_sequences=n_seqs,
    )

    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()
    generated_sequences = []
    
    i = 1
    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        #generated_sequences = generated_sequence.tolist()
        generated_sequences.append(str(i))
        i += 1
        text = tokenizer.decode(generated_sequence)
        total_sequence = (
            text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True, )) :]
        )
        
        generated_sequences.append(total_sequence.split('You:')[0].split('Him:')[0])
    
    return generated_sequences

def init_sms(entry, sms_save, text_label):
    sms_save = open('SMS_MSGS/%s.txt' % entry, 'a+')
    send_text("Yoo how is it going amigo", entry, phone_number, sms_save)
    text_label.config(text=(open('SMS_MSGS/%s.txt' % entry, 'r')).read())

def refresh(phone_number_to):
    text_label.config(text=(open('SMS_MSGS/%s.txt' % phone_number_to, 'r')).read())

def onKeyPress(event, phone_number_entry):
    if event.char == '`':
        refresh(phone_number_entry)

def evaluate(label, phone_number_to):
    sms_save = open('SMS_MSGS/%s.txt' % phone_number_to, 'a+')
    sms = open('SMS_MSGS/%s.txt' % phone_number_to, 'r')

    separator = '\n'

    global options 

    if label == 'g':
        refresh(phone_number_to)
        options = gen_text(remember + sms.read() + "You: ", gpt_tokenizer, gpt_model, n_seqs=4,max_length=20)
        gpt2_label.config(text=separator.join(options))
    elif label == '1':
        send_text(options[1], phone_number_to, phone_number, sms_save)
        refresh(phone_number_to)
    elif label == '2':
        send_text(options[3], phone_number_to, phone_number, sms_save)
        refresh(phone_number_to)
    elif label == '3':
        send_text(options[5], phone_number_to, phone_number, sms_save)
        refresh(phone_number_to)
    elif label == '4':
        send_text(options[7], phone_number_to, phone_number, sms_save)
        refresh(phone_number_to)
    elif label[0] == 'o':
        send_text(label[len('o'):], phone_number_to, phone_number, sms_save)
        refresh(phone_number_to)
    elif label[0] == 'r':
        remember += label[len('r'):] + ','
    elif label == 's':


root = tk.Tk()

frame = tk.Frame(root)
frame.place(relx=0.05, rely=0.05, relwidth=0.9,relheight=0.9)

phone_number_entry = tk.Entry(frame, text="Phone Number")
phone_number_entry.place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.05)

canvas = tk.Canvas(frame, bg="#c3c3c3")
canvas.place(relx=0.05, rely=0.11,relwidth=0.45, relheight=0.8)

scrollbar = tk.Scrollbar(frame, command=canvas.yview, orient=tk.VERTICAL)
scrollbar.place(relx=0.49, rely=0.11, relheight=0.8)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

start_button = tk.Button(frame, text="start", command=lambda: init_sms(phone_number_entry.get(), sms_save, text_label), bg="#fa8b0d")
start_button.place(relx=0.51, rely=0.05, relwidth=0.45, relheight=0.05)

text_label = tk.Label(canvas, anchor="nw", bg="#c3c3c3", text='waiting...', justify=tk.LEFT, wraplength=500)
text_label.place(relx=0.10, rely=0.0, relwidth=1, relheight=1)

canvas.create_window((0,0), window=text_label)

gpt2_label = tk.Label(frame, anchor="nw", bg="#c3c3c3", text='waiting', justify=tk.LEFT, wraplength=500)
gpt2_label.place(relx=0.51, rely=0.11, relwidth=0.45, relheight=0.8)

send_button = tk.Button(frame, text="send", bg="#c3c3c3", command=lambda: evaluate(gpt_entry.get(), phone_number_entry.get()))
send_button.place(relx=0.76, rely=0.92, relwidth=0.2, relheight=0.05)

gpt_entry = tk.Entry(frame, bg="#c3c3c3")
gpt_entry.place(relx=0.05, rely=0.92, relwidth=0.7, relheight=0.05)

root.bind('<KeyPress>', lambda event: onKeyPress(event, phone_number_entry.get()))
root.mainloop()

sms_save.close()
