from pathlib import Path
from collections import defaultdict


class OpenVPNMonitor():
    """
    Monitor events such as client connections

    """
    def __init__(self, config):
        config = _process_config(config)

        self.config = config
        self.listeners = []
        self._openvpn_status_file = config.get("status_file")
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
                column_names = line.split('\t')[2:] # drop HEADER and CLIENT_LIST
            elif line.startswith("CLIENT_LIST"):
                client_values = line.split('\t')[1:]
                client = dict(zip(column_names, client_values))
                common_name = client['Common Name']
                real_address = client['Real Address']

                clients[common_name][real_address] = client

    clients = dict(clients)
    return clients


def _process_config(config):
    """
    Make sure config object has required values

    """
    required_fields = [
        "status_file",
    ]

    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    status_file = Path(config['status_file'])

    if not status_file.exists():
        raise ValueError("could not find status file: {}".format(status_file))

    config['status_file'] = status_file
    return config





