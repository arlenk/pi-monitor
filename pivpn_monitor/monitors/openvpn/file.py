from pathlib import Path

from collections import defaultdict

from .common import ClientConnectionMonitor


class FileMonitor(ClientConnectionMonitor):
    """
    Monitor events by reading log file (may require root privileges)

    """

    def __init__(self, config):
        super().__init__(config)

        self._openvpn_status_file = config.get("status_file")
        self.connections = self.get_current_connections()

    def get_current_connections(self) -> dict:
        """
        List of users currently connected

        """
        connections = _read_openvpn_status_file(self._openvpn_status_file)
        return connections


def _read_openvpn_status_file(status_file: Path) -> dict:
    """
    Read list of currently connected clients from status file

    """
    clients = defaultdict(dict)
    with status_file.open() as f:
        for line in f:
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