FROM debian:bullseye

# Aggiorna l'indice dei pacchetti e installa Python e pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Aggiorna pip
RUN pip3 install --upgrade pip



# Altre dipendenze specificate nel tuo script Python
RUN pip3 install gevent

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia tutti i file Python necessari nella directory di lavoro
COPY mqtt_broker.py /app/mqtt_broker.py

RUN pip install paho-mqtt
# Imposta i permessi di esecuzione per gli script Python
RUN chmod +x /app/mqtt_broker.py


# Comando di avvio dell'applicazione
ENTRYPOINT ["python3", "/app/mqtt_broker.py"]
