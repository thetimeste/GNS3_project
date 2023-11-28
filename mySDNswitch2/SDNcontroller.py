import heapq
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
#from ryu.lib.packet import packet, ethernet, arp, ipv4, ether_types
from ryu.lib.packet.ether_types import ETH_TYPE_IP
from ryu.lib import hub
from ryu.cmd import manager
import networkx as nx


class MyController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MyController, self).__init__(*args, **kwargs)
        self.switches = {}
        self.topology = nx.Graph()
        self.datapath_list = {}
        self.flow_stats = None
        self.datapaths = None
        self.controller_ip = "127.0.0.1"
        self.controller_port = 6653
        self.switch_mac = None
        self.THRESHOLD = 80  # Imposta la soglia di congestione desiderata
        self.link_bandwidths = {}  # Dizionario per memorizzare le larghezze di banda dei link

    def get_switch_mac(self, datapath):
        return self.switch_mac

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.switch_mac = datapath.id
        self.logger.info(f"Switch MAC address: {self.switch_mac}")

        match_arp = datapath.ofproto_parser.OFPMatch(eth_type=0x0806)
        actions_arp = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER, datapath.ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 1, match_arp, actions_arp)

        match_ipv4 = datapath.ofproto_parser.OFPMatch(eth_type=ETH_TYPE_IP)
        actions_ipv4 = [datapath.ofproto_parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER, datapath.ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 1, match_ipv4, actions_ipv4)

        hub.spawn(self.monitor_network)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    def monitor_network(self):
        while True:
            hub.sleep(1)  # Intervallo di monitoraggio
            flow_stats = self.get_flow_stats()
            self.detect_congestion(flow_stats)
            self.balance_traffic()

    def balance_traffic(self):
        # Implementazione di una semplice strategia di bilanciamento del carico
        for congested_link in self.get_congested_links():
            alternative_link = self.get_alternative_link(congested_link)
            if alternative_link:
                self.logger.info(f"Rebalancing traffic from link {congested_link} to {alternative_link}")
                self.update_flow_rules(congested_link, alternative_link)

    def get_congested_links(self):
        congested_links = []
        for link, bandwidth in self.link_bandwidths.items():
            if bandwidth > self.THRESHOLD:
                congested_links.append(link)
        return congested_links

    def get_alternative_link(self, congested_link):
        # Logica per ottenere un link alternativo non congestionato
        link_bandwidths = self.get_link_bandwidths()

        # link alternativo che non sia congestato e soddisfi la soglia
        for link, bandwidth in link_bandwidths.items():
            if link != congested_link and bandwidth < self.THRESHOLD:
                return link

        return None

    def update_flow_rules(self, old_link, new_link):
        # Logica per aggiornare le regole di flusso
        # Ottenere gli ID dei datapath corrispondenti ai link
        old_dp_id = self.get_datapath_id_from_link(old_link)
        new_dp_id = self.get_datapath_id_from_link(new_link)

        # Ottenere i datapath
        old_datapath = self.get_datapath(old_dp_id)
        new_datapath = self.get_datapath(new_dp_id)

        # Verifica se i datapath sono validi prima di procedere
        if old_datapath is not None and new_datapath is not None:
            self.logger.info(f"Updating flow rules from link {old_link} to {new_link}")
            self.install_flow_rules(old_datapath, new_datapath)


    def get_link_bandwidths(self):
        # Questa è una simulazione di larghezza di banda fissa per i link
        link_bandwidths = {
            'link1': 100,
            'link2': 80,
            'link3': 120,
        }

        return link_bandwidths

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        # Gestione delle risposte delle statistiche di flusso
        stats = ev.msg.body
        congested_link = self.detect_congestion(stats)
        if congested_link:
            self.handle_congestion(congested_link)

    def detect_congestion(self, flow_stats):
        # Logica per rilevare la congestione
        # e determinare se un link è congestionato in base al tuo criterio
        for stat in flow_stats:
            # se la larghezza di banda è superiore alla soglia, considera il link congestionato
            if stat.byte_count > self.THRESHOLD:
                return stat.match['in_port']  # Ritorna il numero di porta in ingresso del link congestionato
        return None

    def get_datapath(self, dp_id):
        # Logica per ottenere il datapath in base all'ID
        # cercando tra i datapath noti
        for dp in self.datapaths.values():
            if dp.id == dp_id:
                return dp
        return None

    def handle_congestion(self, congested_link):
        self.logger.info(f"Congestion detected on link {congested_link}")
        alternative_link = self.get_alternative_link(congested_link)

        if alternative_link:
            self.logger.info(f"Rebalancing traffic from link {congested_link} to {alternative_link}")
            self.update_flow_rules(congested_link, alternative_link)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        datapath = ev.msg.datapath
        stats = ev.msg.body

        # Memorizza le statistiche di flusso nel dizionario
        self.flow_stats[datapath.id] = stats

    def get_flow_stats(self):
        # Invia richiesta di statistiche di flusso a tutti gli switch
        for datapath_id in self.get_datapath_ids():
            datapath = self.get_datapath(datapath_id)
            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser

            req = parser.OFPFlowStatsRequest(datapath)
            datapath.send_msg(req)

        # Attendi che le risposte siano gestite
        hub.sleep(1)

        # Restituisci le statistiche di flusso raccolte
        return self.flow_stats

    def get_datapath_ids(self):
        # Logica per ottenere gli ID dei datapath (switch) nella rete
        #  ottenere gli switch registrati presso l'applicazione Ryu
        return [dp.id for dp in self.datapath_list]

    def get_datapath_id_from_link(self, link_name):
        # Logica per ottenere l'ID del datapath in base al nome del link
        #  utilizzare una mappatura o una funzione di ricerca
        # che associa i nomi dei link agli ID dei datapath
        link_to_dp_id_mapping = {'link1': 1, 'link2': 2, 'link3': 3}
        return link_to_dp_id_mapping.get(link_name)

    def install_flow_rules(self, old_datapath, new_datapath):
        # Logica per installare le nuove regole di flusso
        # utilizzo le API OpenFlow per inviare i comandi agli switch
        # Invia le istruzioni al vecchio datapath per rimuovere le regole correlate al vecchio link
        self.remove_old_flow_rules(old_datapath)

        # Invia le istruzioni al nuovo datapath per aggiungere le nuove regole relative al nuovo link
        self.add_new_flow_rules(new_datapath)

    def remove_old_flow_rules(self, datapath):
        # Logica per rimuovere le vecchie regole di flusso
        # inviare comandi OpenFlow per rimuovere regole specifiche
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Definisci il match per le regole che desideri rimuovere
        match = parser.OFPMatch(eth_type=0x0806)  # Esempio: ARP

        # Crea il messaggio FlowMod per rimuovere la regola
        mod = parser.OFPFlowMod(
            datapath=datapath,
            command=ofproto.OFPFC_DELETE,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            match=match
        )

        # Invia il messaggio al datapath per rimuovere la regola
        datapath.send_msg(mod)

    def add_new_flow_rules(self, datapath):
        # Logica per aggiungere le nuove regole di flusso
        #  inviare comandi OpenFlow per aggiungere nuove regole
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Definisci il match e le azioni per le nuove regole
        match = parser.OFPMatch(eth_type=0x0806)  # Esempio: ARP
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]

        # Crea il messaggio FlowMod per aggiungere la nuova regola
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=2,  # Imposta la priorità della regola
            match=match,
            instructions=[parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        )

        # Invia il messaggio al datapath per aggiungere la regola
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.datapath_list[datapath.id] = datapath
        self.logger.info(f"Switch connected: {datapath.id}")
        self.update_topology()

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, CONFIG_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == ofp_event.OFPSC_SWITCH_DISCONNECTED:
            if datapath.id in self.datapath_list:
                del self.datapath_list[datapath.id]
                self.logger.info(f"Switch disconnected: {datapath.id}")
                self.update_topology()

    def update_topology(self):
        # Aggiorna la topologia del grafo
        self.topology.clear()

        # Aggiungi nodi per gli switch attualmente connessi
        self.topology.add_nodes_from(self.datapath_list.keys())

        # Aggiungi archi per i collegamenti tra gli switch
        for dp_id, datapath in self.datapath_list.items():
            # Considera solo i collegamenti di tipo OpenFlow
            for port in datapath.ports.values():
                if port.state == 0:  # Stato 0 indica il link è connesso
                    peer_dp_id = port.peer.dpid
                    self.topology.add_edge(dp_id, peer_dp_id)

        self.logger.info(f"Updated network topology: {self.topology.edges}")

    def dijkstra(self, source, destination):
        """
        Implementa l'algoritmo di Dijkstra per trovare il percorso più breve tra due nodi.

        :param source: Nodo di partenza.
        :param destination: Nodo di destinazione.
        :return: Percorso più breve come lista di nodi.
        """
        if source not in self.switches or destination not in self.switches:
            print("Nodi non validi.")
            return None

        # Inizializzazione delle distanze con un valore elevato
        distances = {node: float('inf') for node in self.switches}
        distances[source] = 0

        # Coda di priorità per gestire i nodi da esplorare
        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Se abbiamo già esplorato questo nodo con una distanza minore, ignoriamolo
            if current_distance > distances[current_node]:
                continue

            # Esplora i vicini del nodo corrente
            for neighbor_link in self.switches[current_node].links:
                neighbor = neighbor_link.destination
                weight = 1  # Ponderazione di default, potrebbe essere basata sulla larghezza di banda, ritardo, ecc.

                # Aggiorna la distanza se troviamo un percorso più breve
                if distances[current_node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[current_node] + weight
                    heapq.heappush(priority_queue, (distances[neighbor], neighbor))

        # Costruisci il percorso dalla destinazione al nodo di partenza
        path = [destination]
        current_node = destination
        while current_node != source:
            next_node = min(self.switches[current_node].links, key=lambda link: distances[link.destination])
            path.insert(0, next_node.destination)
            current_node = next_node.destination

        return path


def main():
        # Specifico il nome del modulo Ryu che contiene la classe del tuo controller

        mod_name = 'mio_modulo_ryu'

        # Specifico il nome della classe del tuo controller all'interno del modulo Ryu
        cls_name = 'MyController'

        # Costruisco l'argomento da passare a Ryu per eseguire il tuo controller
        argv = [
            'ryu-manager',
            '--ofp-tcp-listen-port', '6653',  # Porta su cui il controller ascolterà le connessioni OpenFlow
            f'{mod_name}.{cls_name}'  # Modulo.Class
        ]

        # Eseguo il controller utilizzando il gestore di comandi Ryu
        manager.main(argv)

if __name__ == '__main__':
        main()
