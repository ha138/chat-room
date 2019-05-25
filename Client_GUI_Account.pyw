#! /usr/bin/python3.6

from os import system
from _thread import start_new_thread
import socket
from base64 import b64encode, b64decode
from datetime import datetime
from time import sleep

while True:
    try:
        from tkinter import Entry, Label, Text, END, Menu, Tk, Button
        from tkinter import messagebox

        break
    except:
        print('tkinter not installed')
        input('sudo apt-get install python3-tk')
        system('sudo apt-get install python3-tk')


class Start:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = False
        self.receive_size = 8192
        self.text_color = '#00FFFF'

    def connect(self):
        if self.connection:
            return
        if e_name.get() == '':
            messagebox.showwarning('Error', 'Enter your name')
            e_name.focus()
            return
        if e_server.get() == '':
            messagebox.showwarning('Error', 'Enter the server address')
            e_server.focus()
            return
        if e_port.get() == '':
            messagebox.showwarning('Error', 'Enter the port')
            e_port.focus()
            return
        try:
            self.sock.connect((str(e_server.get()), int(e_port.get())))
            self.sock.send(self.encrypt(e_name.get(), '2').encode())
            start_new_thread(self.receive, ())
            e_message.focus()
            self.connection = True
            top.title('Connected to ' + e_server.get())
        except OSError:
            messagebox.showwarning('OSError', 'The server is down')
        except ValueError as e:
            messagebox.showwarning('ValueError', str(e))

    def receive(self):
        while True:
            msg = self.sock.recv(self.receive_size).decode()
            if msg == '':
                self.sock.close()
                self.inbox_insert('End of the session')
                top.title('End of the session')
                sleep(2)
                top.quit()
            if msg == '#__end':
                self.sock.close()
                self.inbox_insert('End of the session')
                top.title('End of the session')
                sleep(2)
                top.quit()
            msg = self.decrypt(msg, e_decrypt_code.get())
            if msg == '':
                continue
            if msg[0:2] == 'ch':
                e_decrypt_code.delete(0, END)
                e_decrypt_code.insert(0, msg[3:])
                continue
            if msg == '#__clear':
                inbox.configure(state='normal')
                inbox.delete(1.0, END)
                inbox.configure(state='disable')
                continue
            else:
                self.inbox_insert(msg)

    def send(self):
        if not self.connection:
            messagebox.showwarning('Error', 'You are not connected to the server')
            e_message.delete(0, END)
            e_name.focus()
            return
        msg = e_message.get()
        if msg == '':
            return
        else:
            try:
                self.sock.send(self.encrypt(msg, e_decrypt_code.get()).encode())
            except:
                self.inbox_insert('The End')
                messagebox.showwarning('Error', 'The server is down or your connection is disconnected')
                top.quit()
            e_message.delete(0, END)

    @staticmethod
    def inbox_insert(text):
        inbox.configure(state='normal')
        inbox.insert(END, datetime.utcnow().strftime("%H:%M:%S") + '  ' + text + '\n')
        inbox.configure(state='disabled')
        inbox.see(END)

    @staticmethod
    def encrypt(text, key):
        output = ''
        out = 0
        key = str(key)
        for item in key:
            out = out + ord(item)
        key = int(out)
        text = b64encode(text.encode()).decode()
        for item in text:
            output = output + str(ord(item) + key) + '.'
        return output

    @staticmethod
    def decrypt(text, key):
        try:
            output = ''
            out = 0
            key = str(key)
            for item in key:
                out = out + ord(item)
            key = int(out)
            text = str(text).split('.')
            for item in text:
                if item == '':
                    break
                output = output + chr(int(int(item) - key))
            output = b64decode(output.encode()).decode()
            return output
        except ValueError:
            return ''


start = Start()

# form

top = Tk()
top.geometry('760x455')
top.config(bg='#111111')
top.title('Not connected yet')
top.resizable(False, False)

menu = Menu(top, tearoff=0)
menu.add_command(label='Cut')
menu.add_command(label='Copy')
menu.add_command(label='Paste')


def show_menu(e):
    w = e.widget
    menu.entryconfigure('Cut', command=lambda: w.event_generate('<<Cut>>'))
    menu.entryconfigure('Copy', command=lambda: w.event_generate('<<Copy>>'))
    menu.entryconfigure('Paste', command=lambda: w.event_generate('<<Paste>>'))
    menu.tk.call('tk_popup', menu, e.x_root, e.y_root)


# e_message

e_message = Entry(font=('times', 16), bd=0)
e_message.place(x=20, y=360, height=30, width=640)
e_message.config(bg='#000000', fg=start.text_color, highlightbackground='#000000', insertbackground=start.text_color)
e_message.bind("<Return>", lambda event: start.send())
e_message.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

# send

b_send = Button(text='Send', command=lambda: start.send(), font=('times', 15), bd=0)
b_send.place(x=660, y=360, height=30, width=80)
b_send.config(bg='#222222', fg=start.text_color, highlightbackground='#111111')

# message_show

inbox = Text(font=('times', 18), bd=0)
inbox.place(x=20, y=20, height=320, width=720)
inbox.config(bg='#000000', fg=start.text_color, state='disable', highlightbackground='#111111')
inbox.bind_class('Text', "<Button-3><ButtonRelease-3>", show_menu)

# name , port , server , connect

e_name = Entry(font=('times', 15), bd=0)
e_name.place(x=80, y=400, width=92, height=30)
e_name.config(bg='#000000', fg=start.text_color, highlightbackground='#000000', insertbackground=start.text_color)
e_name.bind('<Return>', lambda event: e_server.focus())
e_name.focus()

e_server = Entry(font=('times', 15), bd=0)
e_server.place(x=242, y=400, width=130, height=30)
e_server.config(bg='#000000', fg=start.text_color, highlightbackground='#000000', insertbackground=start.text_color)
e_server.bind("<Return>", lambda event: e_port.focus())
e_server.insert(0, 'ha138.ddns.net')

e_port = Entry(font=('times', 15), bd=0)
e_port.place(x=425, y=400, width=50, height=30)
e_port.config(bg='#000000', fg=start.text_color, highlightbackground='#000000', insertbackground=start.text_color)
e_port.bind("<Return>", lambda event: e_decrypt_code.focus())
e_port.insert(0, '9999')

e_decrypt_code = Entry(font=('times', 15), bd=0)
e_decrypt_code.place(x=600, y=400, width=80, height=30)
e_decrypt_code.config(bg='#000000', fg=start.text_color, highlightbackground='#000000',
                      insertbackground=start.text_color)
e_decrypt_code.bind("<Return>", lambda event: start.connect())
e_decrypt_code.insert(0, '1234')

b_connect = Button(text='Connect', command=lambda: start.connect(), font=('times', 15), bd=0)
b_connect.place(x=660, y=400, width=80, height=30)
b_connect.config(bg='#222222', fg=start.text_color, highlightbackground='#111111')

# Label

l_name = Label(text='Name :', font=('times', 15), bd=0)
l_name.place(x=20, y=400, width=60, height=30)
l_name.config(bg='#111111', fg=start.text_color, highlightbackground='#111111')

l_server = Label(text='Server :', font=('times', 15), bd=0)
l_server.place(x=172, y=400, width=70, height=30)
l_server.config(bg='#111111', fg=start.text_color, highlightbackground='#111111')

l_port = Label(text='Port :', font=('times', 15), bd=0)
l_port.place(x=375, y=400, width=50, height=30)
l_port.config(bg='#111111', fg=start.text_color, highlightbackground='#111111')

l_decrypt_code = Label(text='decrypt code :', font=('times', 15), bd=0)
l_decrypt_code.place(x=480, y=400, width=120, height=30)
l_decrypt_code.config(bg='#111111', fg=start.text_color, highlightbackground='#111111')

top.mainloop()
