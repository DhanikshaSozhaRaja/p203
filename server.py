import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
questions = [
    "\n Grand Central Terminal, Park Avenue, New York is the world's \n a. largest railway station \n b. highest railway station \n c. longest railway station \n d. none of the above",
    "\n Entomology is the science that studies \n a. Behavior of human beings \n b. Insects \n c. The origin and history of technical and scientific terms \n d. The formation of rocks",
    "\n Eritrea, which became the 182nd member of the UN in 1993, is in the continent of \n a. Asia \n b. Africa \n c. Europe \n d. Australia",
    "\n Garampani sanctuary is located at \n a. Junagarh, Gujarat \n b. Diphu, Assam \n c. Kohima, Nagaland \n d. Gangtok, Sikkim",
    "\n For which of the following disciplines is Nobel Prize awarded? \n a. Physics and Chemistry \n b. Physiology or Medicine \n c. Literature, Peace and Economics \n d. All of the above",
]

answers = ['a', 'b', 'b', 'b', 'd']

print("Server has started...")

def get_rand_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1) 
    random_question = questions[random_index] 
    random_answer = answers[random_index] 
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, addr):
    conn.send("Welcome to the quiz game!".encode('utf-8'))
    conn.send("You will recieve a question. The answer to that question should be of a,b,c,d".encode('utf-8'))
    index,question,answer = get_rand_question_answer(conn)
    score = 0
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score+=1
                    conn.send("Hurray! Your score is ", score.encode('utf-8'))
                else:
                    conn.send("Your answer is incorrect :(".encode('utf-8'))
                remove_question(index)
                index,question, answer = get_rand_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
