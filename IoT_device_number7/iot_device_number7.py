#!/usr/bin/env python3
import os
import time
import paho.mqtt.client as mqtt
#from mySDNswitch2.MySwitch import MySwitch

#il dispositivo utilizza il protocollo di cominicazione mqtt

class IoTDeviceNumber7:

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
        message = f"MQTT_MESSAGE\n{data}"
        self.client.connect("127.0.0.1", 5020)
        print(f"connesso al router ")
        self.client.publish( "data", message)
        print(f"dati pubblicati")
        #client.disconnect()

    def check_mqtt_status(self):
        #controlla lo stato del server mqtt

        try:
            self.client.connect("127.0.0.1", 5020)
            return True
        except Exception as e:
            return False






def main():
    #creazione switch sdn
    #switch = MySwitch("mySDNSwitch","127.0.0.1",90)
    #switch.connect()

    #creazione dispositivo iot
    #device= IoTDeviceNumber3('192.168.3.1', 'aa:bb:cc:dd:ee:ff', switch)
    device = IoTDeviceNumber7('192.168.3.1', 'aa:bb:cc:dd:ee:ff')

    #Indico il path
    path = os.path.join('JSON1.json')

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
