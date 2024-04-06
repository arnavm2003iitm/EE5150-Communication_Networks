from socket import *
import time 

# server address to send to 
serverAddressPort = ('', 12000)

# maximum buffer size of data recieved
bufferSize = 1024

# define a client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# set a timeout of 1 second before an exception
clientSocket.settimeout(1)

for i in range(0, 10):
    # defining a message with sequence_number
    msgFromClient = "Ping " + str(i)

    try:
        # time of sending the message frame
        sendTime = time.time()

        # send the message frame
        clientSocket.sendto(str.encode(msgFromClient + " " + str(sendTime)), serverAddressPort)

        # attempt to recieve the message frame from server
        msgFromServer = clientSocket.recvfrom(bufferSize)

        # time of recieval of message from server
        recvTime = time.time()

        # round trip time of pinger
        rtt = recvTime - sendTime

        # print the message recived from server
        msg = "Server Message: {} Round Trip Time: {}".format(msgFromServer[0], rtt)
        print(msg)

    except:
        # throw an error message on unsuccessful attempt to recieve a message
        print("Request timed out")

