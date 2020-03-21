''' Cyber Final Project - Server | Shakked Stux '''


import socket
import select
import threading
import time
import sqlite3
import pickle
import datetime


def main():
    serverSocket = socket.socket()
    port = 7785
    myIP = '0.0.0.0'
    serverSocket.bind((myIP,port))
    serverSocket.listen(10)

    global connectedUsersSockets, connectedUsersUsername
    connectedUsersSockets = []
    connectedUsersUsername = [] # for 'username_socket' function

    while True:
        rlist, wlist, xlist = select.select([serverSocket] + connectedUsersSockets, connectedUsersSockets, [])
        for userSocket in rlist:
            if userSocket is serverSocket: # new user connected
                (new_socket, address) = serverSocket.accept()
                connectedUsersSockets.append(new_socket)
                connectedUsersUsername.append("")

            else:
                try: # new massage
                    input = userSocket.recv(1024)
                    if input != "":
                        a = threading.Thread(target = new_input, args=(userSocket, input,))
                        a.start()
                except: # user exited, delete him from users and usernames
                    index = connectedUsersSockets.index(userSocket)
                    connectedUsersSockets.pop(index)
                    connectedUsersUsername.pop(index)

        break_length = 0.1
        time.sleep(break_length)


def send(clientSocket, data):
    x = pickle.dumps(data)
    if type(clientSocket) == str: # clientSocket represent username, find the socket.
        clientSocket = username_socket(clientSocket)
    clientSocket.send(x)



def new_input(userSocket, input):
    global connectedUsersSockets
    index = connectedUsersSockets.index(userSocket)
    username = username_socket(userSocket)
    words = pickle.loads(input)
    print (words)
    type = words[0]
    if type == "create":
        create_new_user(words[1], words[2], index, userSocket)
    if type == "login":
        login(words[1], words[2], index, userSocket)
    if type == "chats_list":
        show_user_chats_list(username)
    if type == "show_chat":                   # sometimes functions also need to know the sender.....
        show_chat(userSocket, words[1])
    if type == "show_info":
        show_chat_info(userSocket, words[1])
    if type == "create_chat":
        create_chat(words[1], words[2:])
    if type == "massage":
        new_massage(username, words[1], input[8:])
    if type == "add":
        add_member_to_chat(words[1], words[2])
    if type == "name":
        set_name(username, words[1], words[2])


def username_socket(x):
    global connectedUsersSockets, connectedUsersUsername
    if type(x) == str: # x is username
        index = connectedUsersUsername.index(x)
        y = connectedUsersSockets[index] # socket
    else:
        index = connectedUsersSockets.index(x)
        y = connectedUsersUsername[index] # username
    return y



def create_new_user(username, password, index, socket):
    requirements = is_form_ok(username, password)
    valid = True
    for i in requirements:
        if not i:
            valid = False
    if valid:
        add_user_to_db(username, password)
        create_user_db(username)
        new_user_got_in(username, index)
    else:
        send(socket, requirements)


def is_form_ok(username, password):
    x = len(username)
    y = len(password)
    return [x > 6 and x < 16, y > 10 and y < 20, not is_username_exist(username, password)]


def is_username_exist(username, password):
    conn = sqlite3.connect('database\login.db')
    cursor = conn.execute("SELECT * from users where username = '" + username + "'")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(rows) == 0:
        return False
    return True


def is_user_exist(username, password):
    conn = sqlite3.connect('database\login.db')
    cursor = conn.execute("SELECT * from users where username = '" + username + "'")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    if len(rows) == 0:
        return False
    return True


def new_user_got_in(username, index):
    global connectedUsersSockets
    connectedUsersUsername[index] = username
    show_user_chats_list(username)


def login(username, password, index, socket):
    if is_user_exist(username, password):
        new_user_got_in(username, index)
    else:
        send(socket, "no") # no need for complex massage - user is waiting for it. (same with 'yes')


def add_user_to_db(username, password):
    conn = sqlite3.connect('database\login.db')
    conn.execute("INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "' )")
    conn.commit()
    conn.close()


def create_user_db(username):
    create_chats_list(username)
    create_names_table(username)


def create_chats_list(username):
    conn = sqlite3.connect('database\users\{}.db'.format(username)) # ?
    conn.execute('''
    CREATE TABLE IF NOT EXISTS chats
        (
        chatKey text,
        name text,
        number int
        );
    ''')
    conn.commit()
    conn.close()

def create_names_table(username):
    conn = sqlite3.connect('database\users\{}.db'.format(username)) # ?
    conn.execute('''
    CREATE TABLE IF NOT EXISTS names
        (
        username text,
        name text
        );
    ''')
    conn.commit()
    conn.close()






def show_user_chats_list(username):
    conn = sqlite3.connect('database\users\{}.db'.format(username))
    cursor = conn.execute("SELECT * from chats")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    send(username, rows)


def show_chat(userSocket, chatKey):
    conn = sqlite3.connect('database\chats\{}.db'.format("a" + chatKey))
    cursor = conn.execute("SELECT * from massages")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    send(userSocket, rows)


def show_chat_info(userSocket, chatKey):
    conn = sqlite3.connect('database\chats\{}.db'.format("a" + chatKey))
    cursor = conn.execute("SELECT * from members")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    send(userSocket, rows)





def create_chat(name, members):
    key = find_last_chatKey() + 1
    create_chat_db(members, key)
    add_chat_to_users_db(members, key, name)

def create_chat_db(members, key):
    conn = sqlite3.connect("database\chats\{}.db".format('a' + key))
    create_massages_table(conn)
    create_chat_members_table(conn, members)
    conn.commit()
    conn.close()

def create_massages_table(conn):
    conn.execute('''
    CREATE TABLE IF NOT EXISTS massages
        (
        massage text,
        time text,
        username text
        );
    ''')

def create_chat_members_table(conn, members):
    conn.execute('''
    CREATE TABLE IF NOT EXISTS members
        (
        username text
        );
    ''')
    for member in members:
        add_member_to_members_table(conn, member)

def add_member_to_members_table(conn, member):
    conn.execute('''
    INSERT INTO members
        (username) \
        VALUES (''' + "'" + member + "'" + ''')
    ''')
    conn.commit()
    conn.close()

def add_chat_to_users_db(members, key, name):
    for member in members: # (member username - this is what identify each user)
        add_chat_to_user_db(member, key, name)

def add_chat_to_user_db(member, key, name):
    conn = sqlite3.connect("database\users\{}.db".format(member))
    conn.execute('''
    INSERT INTO chats IF NOT EXISTS
        (chatKey, name, number) \
        VALUES (''' + "'" + key + "', '" + name + "','" + 0 + "'" + ''')
    ''')
    conn.commit()
    conn.close()

def find_last_chatKey():
    pass

def add_member_to_chat(key, member):
    conn = sqlite3.connect("database\chats\{}.db".format('a' + key))
    add_member_to_members_table(conn, member)
    # name = ... ??...
    add_chat_to_user_db(member, key, name)





def new_massage(username, chatKey, massage):
    add_massage_to_db(chatKey, username, massage)
    send_to_users(chatKey, username, massage)


def add_massage_to_db(chatKey, username, massage):
    conn = sqlite3.connect("database\chats\{}.db".format(chatKey))
    time = get_time_str()
    conn.execute('''
    INSERT INTO massages
        (massage, time, username) \
        VALUES (''' + massage + ", " + time + ",'" + username + "'" + ''')
    ''')
    conn.commit()
    conn.close()

def get_time_str():
    d = datetime.datetime.now() # date
    return str(d.year) + " " + \
           str(d.month) + " " + \
           str(d.day) + " " + \
           str(d.hour) + " " + \
           str(d.minute) + " " + \
           str(d.second)



def send_to_users(chatKey, username, massage):
    global connectedUsersUsername
    members = find_members(chatKey)
    for member in members: # (member username - this is what identify each user)
        if member in connectedUsersUsername:
            update_user_chat_page(username_socket(member), username, massage)
        else:
            let_user_know(chatKey, member)

def find_members(key):
    conn = sqlite3.connect('database\chats\{}.db'.format("a" + key))
    cursor = conn.execute("SELECT username from members")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def update_user_chat_page(socket, sender, massage):
    send(socket, [sender, massage])

def let_user_know(chatKey, username):
    conn = sqlite3.connect("database\users\?.db", (username))
    conn.execute('''UPDATE chats SET number += 1 WHERE key = ?''', (chatKey)) # ?
    conn.commit()
    conn.close()



def set_name(theOneWhoChangeTheName, username, name):
    conn = sqlite3.connect("database\users\{}.db".format(theOneWhoChangeTheName))
    conn.execute("UPDATE names SET name = " + name + " WHERE username = " + username)
    conn.commit()
    conn.close()



if __name__ == '__main__':
    main()