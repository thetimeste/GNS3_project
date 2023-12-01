import time
import json
import os
import requests

# MQTT broker details (replace with your router's MQTT broker info)
router_ip = "192.168.0.1"
router_port = 5021
router_address = f"http://{router_ip}:{router_port}/post"

# Constructing a path using os.path.join()
path = "/app/JSON2.json"


def send_http_data():
    
    print("PATH: ",path)
    with open(path, 'r') as f:
        json_data = json.load(f)

    json_string = json.dumps(json_data)
    print(json_string)
    
    response = requests.post(router_address, json=json_data)
   
    response = requests.post(router_address, "json=json_data")
    # Check the response status
    if response.status_code == 200:
        print("Request successful")
        
    else:
        print(f"Request failed with status code: {response.status_code}")


def main():
    while True:
        send_http_data()
        time.sleep(10)

if __name__== '__main__':
    main()

"""
#il dispositivo utilizza il protocollo di cominicazione mqtt

class IoTDeviceNumber6:

    #def __init__(self,ip,mac,switch):
        #self.ip=ip
        #self.mac=mac
        #self.switch=switch

    def __init__(self,ip,mac):
        self.ip=ip
        self.mac=mac
        self.client = mqtt.Client()
        # Configurazione TLS
        #self.client.tls_set(ca_certs="/etc/ssl/certs/ca-certificates.crt")


    #def connect(self):
           #apertura connessione allo switch
         #self.conn=self.switch.conncet(self.ip,self.mac)

    #def send(self,data):
          #invio dati allo switch
         #self.conn.send(data)

    def disconnect(self):
        #chiudo la connesione
        self.client.disconnect()

    def send_data(self,data):
        #invio dati allo switch tramite mqtt
        print("sending data")
        self.client.connect(host="192.168.0.2", port=5021)
        print("connesso al router ")
        self.client.publish("data", data)
    def check_mqtt_status(self):
        #controlla lo stato del server mqtt
        client = mqtt.Client()
        try:
            client.connect("192.168.0.2", 5021)
            return True
        except Exception as e:
            print(e)
            return False




def main():
    #creazione switch sdn
    #sdn_controller=SDNController('localhost',90)
    #switch = MySwitch("mySDNSwitch",'Bridge', sdn_controller.sdn_address,sdn_controller.sdn_port)
    #switch.connect()
    print("main started")
    device = IoTDeviceNumber6('192.168.0.3', 'aa:bb:cc:dd:ee:ff')
    path = os.path.join('/JSON.json')
    print("path: ",path)
    with open(path) as f:
        data = f.read()
    print("got data")
    device.send_data(data)

    while True:
        time.sleep(10)
        device.send_data()

    #creazione dispositivo iot
    #device= IoTDeviceNumber3('192.168.3.1', 'aa:bb:cc:dd:ee:ff', switch)
    
    #Indico il path
    path = os.path.join('/app/JSON.json')

    #apertura e lettura file json
    with open(path) as f:
        data = f.read()

    #invio dati
    device.send_data(data)

    #ciclo di controllo sullo stato del server mqtt
    while True:
        if device.check_mqtt_status():
            #se il server mqtt è attivo, continua a funzionare
            time.sleep(10)
            continue
        else:
            #se il server mqtt non è attivo, si spegne
            device.disconnect()
            break

if __name__== '__main__':
    main()

"""

