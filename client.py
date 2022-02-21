import socket
import time
import select
import sys

#socket connections are hardcoded
client = socket.socket()
port = 9999
client.connect(('localhost', int(port)))  # connect to server

intro_msg = str(client.recv(1024), "utf-8")  # intro 
print(intro_msg)
questions = 100
current_question = 0
player_msg = str(client.recv(1024), "utf-8")  # You are player: n
print(player_msg)
welcome_msg = str(client.recv(1024), "utf-8")  # Welcome to the quiz!
print(welcome_msg)

while current_question < questions:  # index of question running < total number of questions

    data = str(client.recv(1024), "utf-8")  # question received OR moving on message OR to end the game
    if data == "end game":
        break  # end of game
    print(data)
    read, _, _ = select.select([sys.stdin, client], [], [], 10)  # 10 is the timeout

    if len(read) > 0:
        if read[0] == sys.stdin:  # somebody buzzed
            # print("Value of c[0]: {}".format(c[0]))
            # print("Value of sys.stdin: {}".format(sys.stdin))
            buzz = input()  # input for buzz value
            client.send(str.encode(buzz))
        else:  # no buzzers
            next_question = str(read[0].recv(1024), "utf-8")  # next question
            print(next_question)
            current_question = current_question + 1
            continue

    answer_prompt = str(client.recv(1024), "utf-8") 
    print(answer_prompt)
    if answer_prompt == 'You have buzzed, please answer within 10s.':
        read1, _, _ = select.select([sys.stdin, client], [], [], 10)
        if len(read1) > 0:
            if read1[0] == sys.stdin:
                attempt = input()
                time.sleep(1)
                client.send(str.encode(attempt))
                current_question = current_question + 1
                result = str(client.recv(1024), "utf-8")  # correct answer, you get 1 point
                print(result)
            else:
                elapsed = str(client.recv(1024), "utf-8")  # 10 seconds to answer (after buzz) have elapsed
                print(elapsed)

unknown1 = str(client.recv(1024), "utf-8")
print(unknown1)
