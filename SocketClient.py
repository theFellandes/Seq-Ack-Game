from socket import *

serverName = "localhost"
serverPort = 12000
# clientSocket = socket(AF_INET, SOCK_STREAM)
# clientSocket.connect((serverName, serverPort))

manual_auto = input("Duo(2), Solo(1) or Auto(0), Default: Auto")
if manual_auto == '' or ' ' or '\n':
    manual_auto = '0'
seq = input("SEQ: ")
ack = input("ACK: ")
msg = input("Message: ")

while msg != 'CLOSE':
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    # clientSocket.settimeout(1.0)
    # if manual_auto:
    sentence = manual_auto + "," + seq + "," + ack + "," + msg + "," + str(len(msg))
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024).decode()
    print("From Server:", modifiedSentence)
    seq = input("SEQ: ")
    ack = input("ACK: ")
    msg = input("Message: ")
    clientSocket.close()
