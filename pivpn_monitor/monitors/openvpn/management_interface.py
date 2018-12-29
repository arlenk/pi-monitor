import socket
from collections import defaultdict

from .common import process_config


class ManagementInterfaceMonitor():
    """
    Monitor events by connecting to openvpn management interface

    """

    def __init__(self, config):
        config = process_config(config)

        self.config = config
        self.listeners = []
        self._openvpn_management_host = config.get("management_host", "localhost")
        self._openvpn_management_port = config.get("management_port")
        self.connections = self.get_current_connections()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def run(self):
        prior_connections = self.connections
        current_connections = self.get_current_connections()
        self.connections = current_connections

        new_connections = defaultdict(dict)
        for client, client_connections in current_connections.items():
            for real_address, details in client_connections.items():
                if (client not in prior_connections or
                   real_address not in prior_connections[client]):
                    new_connections[client][real_address] = details
        new_connections = dict(new_connections)

        if len(new_connections):
            message = "found {} new connection(s):\n".format(len(new_connections))
            for client, client_connections in new_connections.items():
                for real_address, details in client_connections.items():
                    message += "user {} from address {}".format(details['Common Name'],
                                                                details['Real Address'])
        else:
            message = ''

        return len(new_connections), message

    def get_current_connections(self):
        """
        List of users currently connected

        """
        try:
            s = socket.create_connection(
                (self._openvpn_management_host, self._openvpn_management_port),
                10
            )
        except Exception as e:
            print("error connecting to management port: {}".format(e))
            return dict()

        s.settimeout(1)
        try:
            s.send("status")
            status = s.recv(4 * 1024)
        except Exception as e:
            print("error reading status")
            return dict()

        status = status.decode('utf8')
        print("received status: {}".format(status))

        connections = _parse_openvpn_management_status(status)
        return connections


def _parse_openvpn_management_status(status: str) -> dict:
    """
    Read list of currently connected clients from status file

    """
    lines = status.splitlines()
    clients = defaultdict(dict)

    for line in lines:
        line = line.strip()
        if line.startswith("HEADER\tCLIENT_LIST"):
            column_names = line.split('\t')[2:]  # drop HEADER and CLIENT_LIST

        elif line.startswith("CLIENT_LIST"):
            client_values = line.split('\t')[1:]
            client = dict(zip(column_names, client_values))
            common_name = client['Common Name']
            real_address = client['Real Address']

            clients[common_name][real_address] = client

    clients = dict(clients)
    return clients