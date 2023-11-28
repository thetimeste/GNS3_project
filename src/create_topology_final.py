from gns3fy import Gns3Connector, Project, Node, Link

# Indirizzo del server GNS3
gns3_server = "http://192.168.56.130:80"

# Nome del progetto
project_name = "myProject_matteo_mt"


# Creazione della connessione al server GNS3
gns3 = Gns3Connector(gns3_server)

project=Project(name=project_name,connector=gns3)


project.create()



sdn_switch=Node(
    project_id=project.project_id,
    connector=gns3,
    name="matgo01-sdnswitch2-mt",
    template="matgo01-my-sdnswitch2-mt",
    template_type='docker',
    x=0,
    y=0
)

sdn_switch.create()

sdn_switch.properties
{
 'adapters':6,
 'category':'sdn-switch',
 'console_type':'none',
 'name':'my-sdnswitch2',
 'symbol':'/symbol/multilayer_switch.svg',
  'template_id':'1966b686-93e7-32d5-965f-00138eec461',
  'template_type':'docker'
  }
sdn_switch.ports=[{'adapter_number': 0,
    'data_link_types': {'Ethernet': 'DLT_EN10MB'},
    'link_type': 'ethernet',
    'name': 'sdn_switch0',
    'port_number': 0,
    'short_name': 'eth0'
}, {
    'adapter_number': 0,
    'data_link_types': {'Ethernet': 'DLT_EN10MB'},
    'link_type': 'ethernet',
    'name': 'sdn_switch1',
    'port_number': 1,
    'short_name': 'eth1'
}, {
    'adapter_number': 1,
    'data_link_types': {'Ethernet': 'DLT_EN10MB'},
    'link_type': 'ethernet',
    'name': 'sdn_switch2',
    'port_number': 2,
    'short_name': 'eth2'
}, {
    'adapter_number': 1,
    'data_link_types': {'Ethernet': 'DLT_EN10MB'},
    'link_type': 'ethernet',
    'name': 'sdn_switch3',
    'port_number': 3,
    'short_name': 'eth3'
}, {
    'adapter_number': 2,
    'data_link_types': {'Ethernet': 'DLT_EN10MB'},
    'link_type': 'ethernet',
    'name': 'sdn_switch4',
    'port_number': 4,
    'short_name': 'eth4'
}, {
    'adapter_number': 2,
    'data_link_types': {'Ethernet': 'DLT_EN10MB'},
    'link_type': 'ethernet',
    'name': 'sdn_switch5',
    'port_number': 5,
    'short_name': 'eth5'
}]
my_router=Node(
    project_id=project.project_id,
    connector=gns3,
    name="matgo01-myrouter2-mt",
    template="matgo01-my-router2-mt",
    x=0,
    y=300
)

my_router.create()

my_router.properties
{
 'adapters':3,
 'category':'router',
 'console_type':'none',
 'name':'myrouter2',
 'symbol':'/symbol/router.svg',
 'template_id':'1966b686-93e7-32d5-965f-00138eec462',
 'template_type':'docker'
  }
my_router.ports
[{ 'adapter_number': 0,
        'data_link_types': {'Telnet': 'DLT_EN10MB'},
        'link_type': 'telnet',
        'name': 'my-router0',
        'port_number': 0,
        'short_name': 'e0'
    },
    {
        'adapter_number': 0,
        'data_link_types': {'Telnet': 'DLT_EN10MB'},
        'link_type': 'telnet',
        'name': 'my-router1',
        'port_number': 1,
        'short_name': 'e1'
    },
    {
        'adapter_number': 1,
        'data_link_types': {'Telnet': 'DLT_EN10MB'},
        'link_type': 'telnet',
        'name': 'my-router2',
        'port_number': 2,
        'short_name': 'e2'
}]



iot_device_n6= Node(
        project_id=project.project_id,
        connector=gns3,
        name="matgo01-iot-device-n6-mt",
        template="matgo01-iot-device-n6-mt",
        x=-300,
        y=0
 )

iot_device_n6.create()

iot_device_n6.properties
{'adapters': 2,
 'aux': 5026,
 'category': 'guest',
 'console_auto_start': False,
 'console_http_path': '/',
 'console_http_port': 90,
 'console_resolution': '1024x768',
 'console_type': 'telnet',
 'container_id': 'f26b6aee763a9399c93c86032b75717c57b260e5010e88c4d410ce13554771df',
 'custom_adapters': [],
 'environment': '',
 'extra_hosts': '',
 'extra_volumes': [],
 'image': 'matgo01/iot-device-n6',
 'start_command': '',
 'symbol': ':/symbols/affinity/circle/gray/docker.svg',
 'usage': ''}

iot_device_n6.ports
[{'adapter_number': 0,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth0',
  'port_number': 0,
  'short_name': 'eth0'},
 {'adapter_number': 1,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth1',
  'port_number': 0,
  'short_name': 'eth1'}]

iot_device_n7= Node(
        project_id=project.project_id,
        connector=gns3,
        name="matgo01-iot-device-n7-mt",
        template="matgo01-iot-device-n7-mt",
        x=0,
        y=-300
 )

iot_device_n7.create()

iot_device_n7.properties
{'adapters': 2,
 'aux': 5026,
 'category': 'guest',
 'console_auto_start': False,
 'console_http_path': '/',
 'console_http_port': 95,
 'console_resolution': '1024x768',
 'console_type': 'telnet',
 'container_id': 'f26b6aee763a9399c93c86032b75717c57b260e5010e88c4d410ce13554771dg',
 'custom_adapters': [],
 'environment': '',
 'extra_hosts': '',
 'extra_volumes': [],
 'image': 'matgo01/iot-device-n7',
 'start_command': '',
 'symbol': ':/symbols/affinity/circle/gray/docker.svg',
 'usage': ''}

iot_device_n7.ports
[{'adapter_number': 0,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth0',
  'port_number': 0,
  'short_name': 'eth0'},
 {'adapter_number': 1,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth1',
  'port_number': 0,
  'short_name': 'eth1'}]

iot_device_n8= Node(
        project_id=project.project_id,
        connector=gns3,
        name="matgo01-iot-device-n8-mt",
        template="matgo01-iot-device-n8-mt",
        x=300,
        y=0
 )

iot_device_n8.create()

iot_device_n8.properties
{'adapters': 2,
 'aux': 5026,
 'category': 'guest',
 'console_auto_start': False,
 'console_http_path': '/',
 'console_http_port': 100,
 'console_resolution': '1024x768',
 'console_type': 'telnet',
 'container_id': 'f26b6aee763a9399c93c86032b75717c57b260e5010e88c4d410ce13554771dh',
 'custom_adapters': [],
 'environment': '',
 'extra_hosts': '',
 'extra_volumes': [],
 'image': 'matgo01/iot-device-n8',
 'start_command': '',
 'symbol': ':/symbols/affinity/circle/gray/docker.svg',
 'usage': ''}

iot_device_n8.ports
[{'adapter_number': 0,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth0',
  'port_number': 0,
  'short_name': 'eth0'},
 {'adapter_number': 1,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth1',
  'port_number': 0,
  'short_name': 'eth1'}]
mqtt_broker= Node(
        project_id=project.project_id,
        connector=gns3,
        name="matgo01-mqtt-broker2-mt",
        template="matgo01-mqtt-broker2-mt",
        x=0,
        y=400
)

mqtt_broker.create()

mqtt_broker.properties
{'adapters': 2,
 'aux': 5026,
 'category': 'guest',
 'console_auto_start': False,
 'console_http_path': '/',
 'console_http_port': 100,
 'console_resolution': '1024x768',
 'console_type': 'telnet',
 'container_id': 'f26b6aee763a9399c93c86032b75717c57b260e5010e88c4d410ce13554771dh',
 'custom_adapters': [],
 'environment': '',
 'extra_hosts': '',
 'extra_volumes': [],
 'image': 'matgo01/mqtt_broker',
 'start_command': '',
 'symbol': ':/symbols/affinity/circle/gray/docker.svg',
 'usage': ''}

mqtt_broker.ports
[{'adapter_number': 0,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth0',
  'port_number': 0,
  'short_name': 'eth0'},
 {'adapter_number': 1,
  'data_link_types': {'Telnet': 'DLT_EN10MB'},
  'link_type': 'telnet',
  'name': 'eth1',
  'port_number': 0,
  'short_name': 'eth1'}]

#crazione link fra i nodi
# Create connections
link_router_switch = Link(
    project_id=project.project_id,
    connector=gns3,
    nodes=[
        dict(node_id=my_router.node_id, adapter_number=0, port_number=0),
        dict(node_id=sdn_switch.node_id, adapter_number=0, port_number=0)
    ]
)

link_router_switch.create()
link_router_mqtt_broker = Link(
    project_id=project.project_id,
    connector=gns3,
    nodes=[
        dict(node_id=my_router.node_id, adapter_number=1, port_number=2),
        dict(node_id=mqtt_broker.node_id, adapter_number=0, port_number=0)
    ]
)

link_router_mqtt_broker.create()

link_switch_device_n6 = Link(
    project_id=project.project_id,
    connector=gns3,
    nodes=[
        dict(node_id=iot_device_n6.node_id, adapter_number=0,port_number=0),
        dict(node_id=sdn_switch.node_id,adapter_number=0,port_number=1)
    ]
)

link_switch_device_n6.create()

link_switch_device_n7 = Link(
    project_id=project.project_id,
    connector=gns3,
    nodes=[
        dict(node_id=iot_device_n7.node_id,adapter_number=0,port_number=0),
        dict(node_id=iot_device_n7.node_id, adapter_number=1,port_number=2)
    ]
)

link_switch_device_n7.create()

link_switch_device_n8 = Link(
    project_id=project.project_id,
    connector=gns3,
    nodes=[
        dict(node_id=iot_device_n8.node_id, adapter_number=0,port_number=0),
        dict(node_id=iot_device_n8.node_id, adapter_number=2,port_number=3)
    ]
)

link_switch_device_n8.create()
