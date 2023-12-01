#!/usr/bin/env python3
import socket
import threading
import time
from flask import Flask, request, jsonify
import logging
import signal

app = Flask(__name__)

@app.route("/post", methods=["POST"])

#define post method
def post():
    sender_ip = request.remote_addr
    print("Received a payload from", sender_ip)

    # Check if the received data is in JSON format
    try:
        json_data = request.get_json()
        print("Received JSON data:", json_data)
        return("JSON RECEIVED")
    except Exception as e:
        print("Received data is not JSON:", e)
        return("NON-JSON RECEIVED")
    

def handle_connection(client_socket):
    # Receive data from the MQTT client
    data = client_socket.recv(1024)
    client_socket.close()


def handle_client(sock):
    while True:
        # Accetto una connessione
        client_socket, _ = sock.accept()

        # Gestione della connessione in un thread separato
        threading.Thread(target=handle_connection, args=(client_socket,), daemon=True).start()

def main():
    print("Router started")
    # Creo un socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created: ",sock)

    try:
        bind=sock.bind(('0.0.0.0', 5020))
        print("Socket binded on all interfaces (0.0.0.0)")
    except socket.error as e:
        print("Binding failed:", e)
    sock.listen(5)  # Aumentato il numero massimo di connessioni pendenti

    # Utilizzo un flag per controllare se il router deve continuare ad accettare connessioni
    running = True

    # Funzione di gestione del segnale di interruzione per chiudere il socket
    def shutdown_handler(signum, frame):
        nonlocal running
        running = False
        sock.close()

    # Registro la funzione di gestione del segnale di interruzione
    signal.signal(signal.SIGINT, shutdown_handler)

    # Avvio un thread per gestire le connessioni in background
    threading.Thread(target=handle_client, args=(sock,), daemon=True).start()

    # Avvio il server Flask in un thread separato
    threading.Thread(target=app.run, args=('0.0.0.0', 5021), daemon=True).start()

    # Attendo che il flag di running diventi False (ad esempio, quando ricevo un segnale di interruzione)
    while running:
        time.sleep(1)

if __name__ == "__main__":
    main()
    
