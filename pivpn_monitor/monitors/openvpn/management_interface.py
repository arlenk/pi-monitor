import socket
from collections import defaultdict
from typing import List

from .common import ClientMonitor


class ManagementInterfaceMonitor(ClientMonitor):
    """
    Monitor events by connecting to openvpn management interface

    """

    def __init__(self, config):
        config = process_config(config,
                                required_fields=['management_port'])
        self._openvpn_management_host = config.get("management_host", "localhost")
        self._openvpn_management_port = config.get("management_port")

        super().__init__(config)


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

        connections = parse_openvpn_management_status(status)
        return connections


def process_config(config: dict, required_fields: List[str]) -> dict:
    """
    Make sure config object has required values

    """
    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    return config


def parse_openvpn_management_status(status: str) -> dict:
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