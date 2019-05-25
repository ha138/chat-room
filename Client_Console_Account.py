#! /usr/bin/python3.6

from os import system
from _thread import start_new_thread
import socket
from base64 import b64encode, b64decode
from datetime import datetime
import platform


class Start:
    def __init__(self):
        print('\033[1;31;40m')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_size = 8192
        self.name = str(input('Name: '))
        self.server = str(input('Server: '))
        self.port = int(input('Port: '))
        self.decrypt_code = input('Decrypt code: ')
        self.connect()

    def connect(self):
        try:
            self.sock.connect((self.server, self.port))
            self.sock.send(self.encrypt(self.name, '2').encode())
            if platform.system() == 'Linux':
                system('clear')
            if platform.system() == 'Windows':
                system('cls')
            start_new_thread(self.send, ())
            self.receive()
        except OSError:
            print('The server is down')
        except ValueError:
            print('ValueError')

    def receive(self):
        try:
            while True:
                msg = self.sock.recv(self.receive_size).decode()
                if msg == '':
                    self.sock.close()
                    print('End of the session')
                    exit()
                if msg == '#__end':
                    self.sock.close()
                    print('The server is down or your connection is disconnected')
                    exit()
                msg = self.decrypt(msg, self.decrypt_code)
                if msg == '':
                    continue
                if msg[0:2] == 'ch':
                    self.decrypt_code = msg[3:]
                    continue
                if msg == '#__clear':
                    if platform.system() == 'Linux':
                        system('clear')
                    if platform.system() == 'Windows':
                        system('cls')
                    continue
                else:
                    print(datetime.utcnow().strftime("%H:%M:%S") + '  ' + msg)
        except KeyboardInterrupt:
            exit()

    def send(self):
        while True:
            msg = input()
            if msg == '':
                return
            else:
                try:
                    self.sock.send(self.encrypt(msg, self.decrypt_code).encode())
                except:
                    print('The End')
                    exit()

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


Start()
