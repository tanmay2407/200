# importing elements
import socket
from threading import Thread
import random
# making a server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# making and binding ipaddress and port
ip = '127.0.0.1'
port = 8000
server.bind((ip, port))
# running the server maybe :)
server.listen()
# creating list of client name messages and question answer
clients = []
nicknames = []
questions = [
  "What is 10 + 2? \n a) 2 \n b) 12 \n c) 21 \n d) 9",
  "What is 10-1? \n a) 3 \n b) 8 \n c) 9 \n d) 0",
  "what is 0+1? \n a) 1 \n b) 2 \n c) 3 \n d) 4"
]
answers = ["c","c","a"]
# number of question 
numberOfQ = len(questions)

# funtions
def getRandomQuestion(conn):
  randomIndex = random.randint(0, len(questions)-1)
  randomQuestion = questions[randomIndex]
  randomAnswer = answers[randomIndex]
  conn.send(randomQuestion.encode("utf-8"))
  return randomIndex, randomQuestion, randomAnswer


def clientThread(conn, addr):
  point = 0
  conn.send("Welcome to the Quizes".encode("utf-8"))
  conn.send("Answer each question with a, b, c, or d.".encode("utf-8"))
  conn.send("best of luck \n\n".encode("utf-8"))
  index, question, answer = getRandomQuestion(conn)

  while True:
    try:
      message = conn.recv(2048).decode("utf-8")
      if message:
        if message.lower() == answer:
          point += 1
          conn.send(f"Correct! Your point is {point}\n\n".encode("utf-8"))
        else:
          conn.send(f"Incorrect! Your point is still {point}\n\n".encode("utf-8"))
        removeQuestion(index)
        index, question, answer = getRandomQuestion(conn)
      else:
        remove(conn)
        removeNicename(nickname)
    except:
      continue
def removeNicename(nickname):
  if(nickname in nicknames):
    nicknames.remove(nickname)

def removeQuestion(index):
  questions.pop(index)
  answers.pop(index)
        
def remove(conn):
  if conn in clients:
    clients.remove(conn)

# making sending and reciving of question in a loop 
while True:
  conn, addr = server.accept()
  conn.send('NICKNAME'.encode('utf-8'))
  nickname = conn.recv(2048).decode('utf-8')
  clients.append(conn)
  nicknames.append(nickname)
  print(f"{nickname} connected")

  newThread = Thread(target=clientThread, args=(conn,nickname))
  newThread.start()