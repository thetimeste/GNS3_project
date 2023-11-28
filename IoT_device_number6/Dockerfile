FROM ubuntu:focal

# Installa le dipendenze necessarie
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Aggiorna pip
RUN pip3 install --upgrade pip

# Altre dipendenze specificate nel tuo script Python
RUN pip3 install gevent

# Imposta la directory di lavoro
WORKDIR /app

# Copia tutti i file Python necessari nella directory di lavoro
COPY iot_device_number6.py /app/iot_device_number6.py
#copio il file json
COPY JSON.json /app/JSON.json


# Installa le dipendenze del progetto
RUN pip install paho-mqtt

RUN chmod +x /app/iot_device_number6.py

# Esegui il tuo script Python al lancio del container
ENTRYPOINT ["python3", "/app/iot_device_number6.py"]

