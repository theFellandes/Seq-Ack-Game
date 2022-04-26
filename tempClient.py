import time
from socket import *
print("A game for SEQ&ACK calculation.")
print("Uses a stop-and-wait protocol in operation")
print("Client: ")
auto = input("Manual (0) or auto (1)?: ") == '1'
step = 0
seq = step + 1
ack = step + 1
message = "This will be a demonstration for our auto mode CLOSE".split(" ")
prev_list_cli = [-1, -1, -1]
prev_list_sv = []
repetition = 1
response_seq = -1
response_ack = -1
response_msg = ""
client_score = 0
initiate_timeout = 0
start_flag = True

# Client puan ekleme
# Client timeout ekleme
# SEQ ve ACK doğru çalışıp çalışmama kontrolü
# SEQ ve ACK paket boyu düzeltme kontrolleri eklenmeli

serverName = "localhost"
serverPort = 12000

while auto:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    msg = message[step]
    sentence = str(seq) + "," + str(ack) + "," + msg + "," + str(len(msg))
    prev_ack = ack
    clientSocket.send(sentence.encode())
    print("Sent message: ", sentence)
    if msg == 'CLOSE':
        print("Score: " + str(client_score))
        break
    modifiedSentence = clientSocket.recv(1024).decode()
    print("From Server:", modifiedSentence)
    data = modifiedSentence.split(",")
    seq = data[1]
    step += 1
    msg = message[step]
    ack = len(msg) + int(seq) + 1
    if ack < int(seq) or seq == prev_ack:
        step -= 1
        seq = ack
        # resend the previous message! decrement score
        # auto'ysa score'a dokunma ve printleme!
        # Eğer ack < seq bloğuna girerse Seq number'ı ack yapacağız
        # Ack'yı gelen seq + packet length yapacağız
        # Bir önceki gönderilmeyen paketi tekrar göndereceğiz

while not auto:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    seq = int(input("SEQ: "))
    ack = int(input("ACK: "))
    msg = input("Message: ")

    pl = int(input("Enter Packet Length (Default: 1): "))
    packet_loss = input("Do you wish to simulate packet loss? Yes (y) or No (n)? ")
    msg *= pl

    if seq == prev_list_cli[0] and ack == prev_list_cli[1] and msg == prev_list_cli[2] and not start_flag:
        print("Duplicate client side value")

    if repetition % 3 == 0:
        if prev_list_sv[0] == prev_list_sv[3] and prev_list_sv[1] == prev_list_sv[4] and prev_list_sv[2] == prev_list_sv[5]:
            print("Duplicate server side value")
        repetition = 1
        prev_list_sv = None

    if response_seq == ack and response_ack == seq:
        print("Requesting previous package")

    if (ack != seq + len(msg) and not (response_seq == ack and response_ack == seq)) and not start_flag:
        print("Wrong ACK value")
        client_score -= 100

    else:
        print("Correct, Awarded 100 Points")
        client_score += 100

    start_flag = False

    initiate_timeout = int(input("How long would the timeout be in seconds? "))
    if initiate_timeout > 0:
        print("Client timed out. Reconnecting...")
        time.sleep(initiate_timeout)

    clientSocket.connect((serverName, serverPort))
    sentence = str(seq) + "," + str(ack) + "," + msg + "," + str(len(msg))
    if packet_loss.lower() == "y":
        seq = ""
        ack = ""
        msg = ""
        sentence = str(seq) + "," + str(ack) + "," + msg + "," + str(len(msg))
    clientSocket.send(sentence.encode())

    if msg == 'CLOSE':
        clientSocket.close()
        print("Score: " + str(client_score))
        break

    modifiedSentence = clientSocket.recv(1024).decode()
    print("From Server:", modifiedSentence)
    lst = modifiedSentence.split(",")
    response_seq = lst[0]
    response_ack = lst[1]
    response_msg = lst[2]
    clientSocket.close()
    prev_list_cli = [seq, ack, msg]
    prev_list_sv.append(response_seq)
    prev_list_sv.append(response_ack)
    prev_list_sv.append(response_msg)
    repetition += 1
