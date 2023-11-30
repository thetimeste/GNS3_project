#!/usr/bin/env python3
import socket
import threading
import time
#import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify
import logging
import signal

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Questo è un router</h1></h1>"

@app.route("/post", methods=["POST"])
def post():
    try:
        data = request.get_json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})


def handle_connection(client_socket):
    # Ricevo i dati dal client
    data = client_socket.recv(1024)

    # Elaboro i dati ricevuti
    request_line, request_headers, request_body = data.decode("utf-8").split("\r\n")

    # Creo la risposta
    if request_line.startswith("GET /"):
        response_line = "HTTP/1.1 200 OK"
        response_headers = "Content-Type: text/html\r\n\r\n"
        response_body = "<html><body><h1>Questo è un router</h1></h1><body><html>"
    elif request_line.startswith("POST /"):
        response_line = "HTTP/1.1 200 OK"
        response_headers = "Content-Type: text/plain\r\n\r\n"
        response_body = request_body
    else:
        response_line = "HTTP/1.1 400 Bad request"
        response_headers = "Content-Type: text/plain\r\n\r\n"
        response_body = "La richiesta non è valida "

    # Invio la risposta al client
    client_socket.send(response_line.encode("utf-8"))
    client_socket.send(response_headers.encode("utf-8"))
    client_socket.send(response_body.encode("utf-8"))

    # Chiudo la connessione
    client_socket.close()


def handle_connection_mqtt(client_socket):
    try:
        # Ricevi i dati dal client
        data = client_socket.recv(1024)

        # Stampa i dati ricevuti per debug
        print("Dati ricevuti:", data)

        # Esempio di messaggio MQTT inviato dal dispositivo IoT6
        if data.startswith(b"MQTT_MESSAGE\n"):
            # Estrai il payload MQTT
            message_payload = data.split(b"\n", 1)[1]

            # Pubblica il messaggio sul topic desiderato
            # mqtt_client.publish("data", message_payload)

            # Puoi aggiungere ulteriori logica qui in base ai tuoi requisiti

            # Invia una risposta al dispositivo IoT6
            response = b"Messaggio MQTT ricevuto e pubblicato sul topic 'data'"

            # Invia la risposta al client
            client_socket.sendall(response)

        else:
            # Se il payload non è un messaggio MQTT valido, gestisci diversamente o invia una risposta di errore
            response = b"Comando non valido"

            # Invia la risposta al client
            client_socket.sendall(response)

    except Exception as e:
        print("Errore durante l'elaborazione della richiesta:", str(e))

    finally:
        # Chiudi la connessione
        client_socket.close()

def handle_client(sock):
    while True:
        # Accetto una connessione
        client_socket, _ = sock.accept()

        # Gestione della connessione in un thread separato
        threading.Thread(target=handle_connection_mqtt, args=(client_socket,), daemon=True).start()

def main():
    # Creo un socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5020))
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
    threading.Thread(target=app.run, args=('localhost', 5021), daemon=True).start()

    # Attendo che il flag di running diventi False (ad esempio, quando ricevo un segnale di interruzione)
    while running:
        time.sleep(1)

if __name__ == "__main__":
    main()
