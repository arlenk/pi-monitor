from collections import defaultdict
from pathlib import Path
from typing import List

from .common import ClientMonitor


class FileMonitor(ClientMonitor):
    """
    Monitor events by reading log file (may require root privileges)

    """

    def __init__(self, config):
        config = process_config(config,
                                required_fields=['status_file'])
        self._openvpn_status_file = config.get("status_file")

        super().__init__(config)

    def get_current_connections(self) -> dict:
        """
        List of users currently connected

        """
        connections = read_openvpn_status_file(self._openvpn_status_file)
        return connections


def process_config(config: dict, required_fields: List[str]) -> dict:
    """
    Make sure config object has required values

    """
    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    status_file = Path(config['status_file'])

    if not status_file.exists():
        raise ValueError("could not find status file: {}".format(status_file))

    config['status_file'] = status_file
    return config


def read_openvpn_status_file(status_file: Path) -> dict:
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