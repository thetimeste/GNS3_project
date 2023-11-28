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

RUN pip3 install psutil

RUN pip3 install ovs

RUN pip3 install asyncio

RUN pip3 install scapy

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia tutti i file Python necessari nella directory di lavoro
COPY MySwitch.py /app/MySwitch.py



# Imposta i permessi di esecuzione per gli script Python
RUN chmod +x /app/MySwitch.py


# Comando di avvio dell'applicazione
ENTRYPOINT ["python3", "/app/MySwitch.py"]
