import json
from gns3util import Server, check_server_version, create_docker_template, environment_dict_to_string, get_all_templates, read_local_gns3_config,create_docker_template_router,create_docker_template_switch
import requests

indirizzo_ip = "0.0.0.0"
porta = 3080
utente = "admin"
password = "gns3"

# Crea l'oggetto Server
server = Server(addr=indirizzo_ip, port=porta,auth=(utente, password),user=utente, password=password)

create_docker_template_switch(server,name="matgo01-my-sdnswitch2-mt",image="my-sdnswitch2-mt",environment='')
create_docker_template_router(server,"matgo01-my-router2-mt","my-router2-mt",' ')
create_docker_template(server,"matgo01-iot-device-n6-mt","iot-device-n6-mt",' ')
#create_docker_template(server,"matgo01-iot-device-n7-mt","iot-device-n7-mt",' ')
#create_docker_template(server,"matgo01-iot-device-n8-mt","iot-device-n8-mt",' ')
#create_docker_template(server,"matgo01-mqtt-broker2-mt","mqtt-broker2-mt")
