# REPORT ON THE NETWORK PROGRAMMING ASSIGNMENT


# OPERATION INSTRUCTIONS
1. Download the compressed folder, and extract all.
2. Open 4 separate Terminals/Shell windows, and in each, cd into the Socket-Quiz directory
3. run the command - python3 server.py on one of them, then run python3 client.py on the rest (Note: the order is important - the server must be
    on before the clients send connection requests)
4. Respond according to the prompts!

                                *      *      *       *

# CONCEPTS FROM COMPUTER NETWORKS
Since there is no GUI involved, there is minimal Application layer programmming. The OS CLI and Python3 I/O takes care of it. 
The programming handles the Network Layer transception. 
The socket uses TCP (default), because it is errorless and ordered, although it lacks timing guarantees (leading to occasional bugs in the executed code).
The server hosts the clients, and is always 'ON'. 

                                *      *      *       *

# LANGUAGE TOOLS
The programming has been done in Python 3.7, using select module to handle the simultaneous transactions.
All the non-standard components used are described briefly below:

methods for the socket class -

1. socket() - initialise a socket object (by default using the TCP)
2. bind(port) - binds socket to port specified as (hostname,port number)
3. listen(n) - 'listens' for n connection requests, then stops listening.
4. accept() - accepts connection request, and returns connection object and client address
5. send(data) - sends encoded information to reciever.
6. recv(BUFSIZE) - recieves information from the connection channel (of maxsize == BUFSIZE).
7. close() - closes socket 
8. setblocking(boolean) - to decide whether or not the socket should timeout

methods for the string class -

1. encode() - encodes the string (by default, to utf-8) for transmission
2. decode() - decodes the string (by default, from utf-8) on reception.

the select module (handles low-level network layer functions powerfully) -
select.select() - returns 3 lists - connection objects (outgoing), connection objects (incoming) and those throwing error. 


# DESIGN AND STRUCTURE
There are two modules - one for the server side and the other for the client side.
After a question is printed, there is 10s time window for the buzz. The first buzzer must answer the question, or face a penalty. If no one buzzes,
the question is passed. 
If any player scores above 5 points, he wins, and the game ends.
If all questions are exhausted, then it is a tie. 
 
  ## SERVER side

  There is 1 main function - quiz() - that handles the main quiz event
  Apart from this, there are 3 support functions to initialise the game by accepting and establishing connections to the client. 

  create_socket() initialises a socket object for the server with proper exception handling.

  bind_socket() binds the socket to port.

  accepting_connections() - the server 'listens' for connections, and exits the loop after three connections have been made. The number of
                            connections it listens for > 3 so that there is a margin to account for packet loss or delay. quiz() is called within
                            this function.

  quiz() - responsible for executing the quiz; basically one for loop which runs until the questions are exhausted.
            the function ends the quiz if a player scores 5 points.  


  The main code is executed using the main module - to prevent any imported modules from being executed. 

  ## CLIENT side

  The client side code runs as long the number of questions used up is less than the total - or whenever a winner is declared.
  The code is a simple if-else ladder. 
  Once the loop exit occurs, the execution terminates after a message is printed.

Apart from Python3's readability and crispness, the code is commented for the logic, apart from the report.
