import socket
import time
import select
import random

QnA = {"Q" + str(i): i for i in range(1, 101)}  # using dictionary comprehension
# Q1:1 ; Q2:2 ; Q3:3 ... Q100:100 ; answer to Qn is n
clients = []  # list to store the connection objects of the clients
scores = [0, 0, 0]  # maintain the score of each player


# create a socket to establish connection between client and server
def create_socket():
    try:
        global host
        global port
        global server
        host = ""
        port = 9999
        server = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global server

        server.bind((host, int(port)))
        server.listen(3)  # number of connections allowed before refusing new ones

    except socket.error:
        print("Socket binding error occurred")


# Handling connections from multiple players and saving to a list
def accepting_connections():
    count = 0

    while True:
        client, address = server.accept()
        server.setblocking(1)  # prevents timeout
        count += 1  # increasing the count of number of connections
        clients.append(client)  # adding the connection object to the list

        if count < 3:
            print("client {} with address {} is connected".format(count, address[0]))
            client.send(str.encode(
                "+1 for all correct answers\n-0.5 for all incorrect answers (or buzzed yet unanswered questions)"))
            client.send(str.encode("You are player : " + str(count)))
            time.sleep(1)  
            client.send(str.encode("Welcome"))

        else:  # all have been connected; triggered the moment player3 connects; thus game starts
            print("client {} with address {} is connected".format(count, address[0]))
            client.send(str.encode(
                "+1 for all correct answers\n-0.5 for all incorrect answers (or buzzed yet unanswered questions)"))
            print("All three players connected. Start game.")
            time.sleep(1)
            client.send(str.encode("You are player : " + str(count)))
            time.sleep(1)
            client.send(str.encode("Welcome"))

            quiz()
            break  # don't accept any more connections


def quiz():
    for i in range(len(QnA)):  # iterate through the dict
        question = random.choice(list(QnA.keys()))  # choose question randomly
        answer = QnA[question]  #  answer - mapped as value to question as key
        QnA.pop(question)  # remove that question : answer from the dict to ensure no repetitions
        for client in clients:
            time.sleep(0.1)
            client.send(str.encode("Q. " + question + "\n" + "Press any alphanumeric key to buzz."))
            # send question to each player
        key_press = select.select(clients, [], [], 10)  # 10 is the timeout
        # key_press is a tuple of lists - outgoing, incoming and error 

        if len(key_press[0]) > 0:  # if somebody has pressed the buzzer
            who_buzzed = key_press[0][0]  # the player who buzzed the earliest
            buzz = str(who_buzzed.recv(1024), "utf-8")  # receiving the buzz value
            key_press = ()
            for client in clients:
                if client != who_buzzed:  # send message to other players
                    client.send(str.encode(
                        "Sorry, player " + str(clients.index(who_buzzed) + 1) + " has pressed the buzzer."))

            for client in range(len(clients)):
                if clients[client] == who_buzzed:
                    who_buzzed_index = client  # t is index of player who buzzed

            if buzz.isalnum():
                who_buzzed.send(str.encode("You have buzzed, please answer."))
                answer_keypress = select.select(clients, [], [], 10)

                if len(answer_keypress[0]) > 0:
                    attempt = str(who_buzzed.recv(1024), "utf-8")
                    if str(attempt) == str(answer):
                        scores[who_buzzed_index] = scores[who_buzzed_index] + 1
                        who_buzzed.send(str.encode("Correct answer, You get 1 point"))
                        if scores[who_buzzed_index] == 5:
                            for client in clients:
                                client.send(str.encode("end game"))
                                time.sleep(1)
                            break
                    else:
                        who_buzzed.send(str.encode("Wrong answer :(, you get a penalty."))
                        scores[who_buzzed_index] = scores[who_buzzed_index] - 0.5
                        time.sleep(1)
                else:
                    who_buzzed.send(str.encode("Your 10 seconds to answer have elapsed." + "\n" + "You get a penalty "
                                                                                                  "as you did not "
                                                                                                  "answer."))
                    scores[who_buzzed_index] = scores[who_buzzed_index] - 0.5

        else:
            for client in clients:
                client.send(str.encode("Question is passed."))


if __name__ ==  "__main__":
    create_socket()
    bind_socket()
    accepting_connections()
    score_winner = 0  # marks of winner
    index_winner = 0  # index of winner

    score_winner = max(scores)
    index_winner = scores.index(score_winner)

    #end all connections with goodbye message
    for client in clients:
        #if winner has scored 5 and client is not winner
        if clients.index(client) != index_winner and score_winner == 5:
            client.send(
                str.encode("Player " + str(index_winner) + "has won with " + str(score_winner) + " points."))
        
        #if winner has scored 5 and client is winner
        else if clients.index(client) == index_winner and score_winner == 5:
            client.send(str.encode("You are the winner with " + str(score_winner) + " points. Congratulations!"))
        
        #if winner has scored < 5 (number of questions has been exceeded)
        else:
            client.send(str.encode("Number of questions exceeded - TIE!!!"))
        
        #close connection
        try:
            client.close()
        except:
            continue



