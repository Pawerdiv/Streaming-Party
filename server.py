import socket
import time

total = []
host = []


def sendHost():
    while True:
        r = total[0].recv(4096)
        if r.decode() == "host":
            total[0].send(str(host[0]).encode())
            break
    while True:
        r = total[1].recv(4096)
        if r.decode() == "host":
            total[1].send(str(host[1]).encode())
            break

    connect()


def connect():

    while True:
        status = total[0].recv(4096)
        total[1].send(status)
        while True:
            try:
                total[1].recv(1000)
            except:
                print("CLIENT PERSO")
                time.sleep(2)
                continue
            finally:
                break
        total[0].send(status)


def sub_server(indirizzo,num, backlog=3):
    global total
    global host
    try:
        s = socket.socket()
        s.bind(indirizzo)
        s.listen(backlog)
        print("Server Inizializzato. In ascolto...")
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")
        print(f"Sto tentando di reinizializzare il server...")
        sub_server(indirizzo, num, backlog=1)
    conn, indirizzo_client = s.accept() #conn = socket_client
    print(f"Connessione Server - Client Stabilita: {indirizzo_client}")
    total.append((conn))
    host.append(num)

    if num == 1:
        total[0].send("ok".encode())
        total[1].send("ok".encode())
        sendHost()


if __name__ == '__main__':
    sub_server(("", 15324), 0)
    sub_server(("", 15324), 1)