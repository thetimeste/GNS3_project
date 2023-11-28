class Link:
    def __init__(self, name, port_name, switch_name, peer_name):
        """
        Inizializza un oggetto Link con i nomi della porta, dello switch e del peer.
        :param port_name: Nome della porta.
        :param switch_name: Nome dello switch.
        :param peer_name: Nome del peer.
        :param in_use: disponibilità del link.
        :param bandwidth:larghezza di banda.
        :param:bandwidth_usage:uso larghezza di banda.
        """
        self.name = name
        self.port_name = port_name
        self.switch_name = switch_name
        self.peer_name = peer_name
        self.in_use = False
        self.bandwidth = 0
        self.bandwidth_usage = 0

    def __str__(self):
        """
        Restituisce una rappresentazione leggibile dell'oggetto Link.

        :return: Stringa rappresentativa dell'oggetto Link.
        """
        return f"Link({self.port_name}-{self.switch_name}-{self.peer_name})"

    def get_bandwidth_usage(self):
        """
        Restituisce l'utilizzo della larghezza di banda del link.

        :return: Utilizzo della larghezza di banda.
        """
        return self.bandwidth_usage

    def set_bandwidth_usage(self, bandwidth_usage):
        """
        Imposta l'utilizzo della larghezza di banda del link.

        :param bandwidth_usage: Utilizzo della larghezza di banda da impostare.
        """
        self.bandwidth_usage = bandwidth_usage

    def is_available(self):
        """
        Verifica se il link è disponibile.

        :return: True se il link è disponibile, False altrimenti.
        """
        return not self.in_use

    def use_link(self):
        """
        Segna il link come in uso.
        """
        self.in_use = True

    def release_link(self):
        """
        Rilascia il link segnandolo come non in uso.
        """
        self.in_use = False

    def get_switch_port(self):
        """
        Restituisce il nome della porta dello switch associato al link.

        :return: Nome della porta dello switch.
        """
        return self.switch_name

    def get_peer_device(self):
        """
        Restituisce il nome del peer associato al link.

        :return: Nome del peer.
        """
        return self.peer_name

    def get_bandwidth(self):
        """
        Restituisce la larghezza di banda del link.

        :return: Larghezza di banda del link.
        """
        return self.bandwidth
