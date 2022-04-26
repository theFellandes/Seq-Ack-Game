import time
from socket import *
print("A game for SEQ&ACK calculation.")
print("Uses a stop-and-wait protocol in operation")
print("Server: ")
auto = input("Manual (0) or auto (1)?: ") == '1'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
server_score = 0
start_flag = True
prev_list = [-1, -1, -1]
print('The server is ready to receive')

# Server puan ekleme
# Server timeout ekleme
# SEQ ve ACK doğru çalışıp çalışmama kontrolü
# SEQ ve ACK paket boyu düzeltme kontrolleri eklenmeli

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    sentence = sentence.decode()
    lst = sentence.split(",")

    print("Received message: ", sentence)

    if auto:
        seq = lst[0]
        ack = lst[1]
        msg = lst[2]
        length = len(msg)

        if msg == 'CLOSE':
            connectionSocket.close()
            break

        temp = length + int(seq) + 1

        if seq and ack and msg == "":
            # eski seq ack ve msg'yi ans'a kaydet.
            pass

        ans = ack + "," + str(temp) + "," + msg + "," + lst[3]

        sentence = ans
        connectionSocket.send(sentence.encode())
        print("Sent message: ", ans)

    else:
        # Timeout manual'de yapılacak, inputları verirken yapılacak
        # Eğer timeout olduysa connection'ı kapatıp yeniden bağlanmayı deneyebiliriz
        # Server'da timeout olduysa connection'ı tümden kapatsın yeniden açmasın.
        # Client'ta timeout olduysa connection yeniden bağlanmayı denesin.
        # settimeout'la yapılır timeout
        # input olarak send-not send alalım, not send giderse loop'ta
        #  dönelim ve belli bir süre bekleyip timed out diyelim, client tekrar
        #   göndermeyi denesin. Server not send'i manual'de client'a true-false
        #    olarak göndersin. Duplicate ve lost packet'lere bir yol bulmak lazım.
        #       Server duplicate packet'leri ACK numaralarından anlamalı. Lost
        #         Packetler de aynı şekilde. Manual kısmında buna ayar getirmeliyiz.
        seq = input("SEQ: ")
        ack = input("ACK: ")
        packet_loss = input("Do you wish to simulate packet loss? Yes (y) or No (n)? ")
        msg = lst[2]

        if int(ack) != int(seq) + len(msg) and not start_flag:
            print("Wrong ACK value")
            server_score -= 100

        else:
            print("Correct, Awarded 100 Points")
            server_score += 100

        initiate_timeout = int(input("How long would the timeout be in seconds? "))
        if initiate_timeout > 0:
            print("Server timed out. Reconnecting...")
            time.sleep(initiate_timeout)

        start_flag = False

        ans = ack + "," + str(ack) + "," + msg + "," + lst[3]

        if packet_loss.lower() == "y":
            seq = ""
            ack = ""
            msg = ""
            ans = ack + "," + str(ack) + "," + msg + "," + lst[3]

        sentence = ans
        connectionSocket.send(sentence.encode())

        if msg == 'CLOSE':
            connectionSocket.close()
            print("Score: " + str(server_score))
            break
        print("Sent message: ", ans)
