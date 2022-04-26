from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    # Duo(2), Manual(1) or Auto(0)
    sentence = connectionSocket.recv(1024)
    sentence = sentence.decode()
    lst = sentence.split(",")
    manual_auto = lst[0]
    print(manual_auto)

    if manual_auto == '2':
        seq = input("SEQ: ")
        ack = input("ACK: ")
        msg = lst[3]

        ans = ack + "," + str(ack) + "," + msg + "," + lst[4]

        sentence = ans
        connectionSocket.send(sentence.encode())

    elif manual_auto == '1':
        seq = lst[1]
        ack = lst[2]
        msg = lst[3]
        length = len(msg)

        temp = length + int(ack)

        ans = ack + "," + str(temp) + "," + msg + "," + lst[4]

        sentence = ans
        connectionSocket.send(sentence.encode())
        if msg == 'CLOSE':
            connectionSocket.close()

    else:
        seq = input("SEQ: ")
        ack = input("ACK: ")
        msg = lst[3]

        ans = ack + "," + str(ack) + "," + msg + "," + lst[4]

        sentence = ans
        connectionSocket.send(sentence.encode())

