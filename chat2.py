# Cyber Final Project - Client/User
# by Shakked Stux


import socket
import select
import threading
import pickle
import time
import Tkinter as tk


def main():
    global clientSocket
    clientSocket = socket.socket()
    port = 7785
    serverIP = '127.0.0.1'
    clientSocket.connect((serverIP,port))

    global root, state
    root = tk.Tk()
    login_page()

    serverIsFine = True
    while serverIsFine:
        rlist, wlist, xlist = select.select([clientSocket], [clientSocket], [])
        if len(rlist) != 0:
            try:
                input = clientSocket.recv(1024)
                a = threading.Thread(target = new_input, args=(input,))
                a.start()
            except: # server stopped working
                serverIsFine = False
        try:
            root.update()
        except:
            pass
        break_length = 0.1
        time.sleep(break_length)
    print ("Server is not fine.")


def new_input(input):
    data = pickle.loads(input)
    print (data)
    if state == "login":
        msg_login(data)
    if state == "create":
        pass


def msg_login(data):
    pass
def msg_create(data):
    pass


def send(string):
    x = pickle.dumps(string)
    clientSocket.send(x)

# |||||||||||||||
def create_new_user(username, password):
    send(["create", username, password])

def login(username, password):
    send(["login", username, password])

def send_new_massage_in_chat(chatKey, theMassage):
    send(["massage", chatKey, theMassage])

def create_new_chat(chatName, chatMembers):
    pass

def add_member_to_chat(chatKey, newMemberUsername):
    send(["add", chatKey, newMemberUsername])

def make_him_manager(chatKey, hisUsername):
    send(["manager", chatKey, hisUsername])

def set_his_name(hisUsername, theName):
    send(["name", hisUsername, theName])

def show_me_chat(chatKey):
    send(["show_chat", chatKey])

def show_me_chat_info(chatKey):
    send(["show_info", chatKey])

def show_me_chats_list():
    send("chats_list")
# |||||||||||||||


class loginPage:
    def __init__(self, top=None):
        global state
        state = "login"
        top.geometry("600x450+650+150")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(relx=0.317, rely=0.244,height=44, relwidth=0.357)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Entry2 = tk.Entry(top)
        self.Entry2.place(relx=0.317, rely=0.467,height=44, relwidth=0.357)
        self.Entry2.configure(background="white")
        self.Entry2.configure(disabledforeground="#a3a3a3")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(insertbackground="black")

        self.Button1 = tk.Button(top, command = self.submit_login)
        self.Button1.place(relx=0.433, rely=0.733, height=33, width=56)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''submit''')

        self.Button2 = tk.Button(top, command = create_page)
        self.Button2.place(relx=0.833, rely=0.733, height=33, width=56)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''create a user''')

    def submit_login(self):
        login(self.Entry1.get(), self.Entry2.get())


class createPage:
    def __init__(self, top=None):
        global state
        state = "create"
        top.geometry("600x450+650+150")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(relx=0.317, rely=0.244,height=44, relwidth=0.357)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Entry2 = tk.Entry(top)
        self.Entry2.place(relx=0.317, rely=0.467,height=44, relwidth=0.357)
        self.Entry2.configure(background="white")
        self.Entry2.configure(disabledforeground="#a3a3a3")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(insertbackground="black")

        self.Button1 = tk.Button(top, command = self.submit_login)
        self.Button1.place(relx=0.433, rely=0.733, height=33, width=56)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''submit''')

        self.Button2 = tk.Button(top, command = login_page)
        self.Button2.place(relx=0.833, rely=0.733, height=33, width=56)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''i have user''')

    def submit_login(self):
        create_new_user(self.Entry1.get(), self.Entry2.get())





def login_page():
    global root
    x = loginPage (root)

def create_page():
    global root
    x = createPage (root)

def chats_list_page():
    global root
    x = chatsListPage (root)

if __name__ == '__main__':
    main()