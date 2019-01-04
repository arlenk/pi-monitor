import socket
from collections import defaultdict

from .common import ClientMonitor


class ManagementInterfaceMonitor(ClientMonitor):
    """
    Monitor events by connecting to openvpn management interface

    """

    def __init__(self, config):
        super().__init__(config,
                         required_fields=['management_port'])

        self._openvpn_management_host = config.get("management_host", "localhost")
        self._openvpn_management_port = config.get("management_port")
        self.connections = self.get_current_connections()

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