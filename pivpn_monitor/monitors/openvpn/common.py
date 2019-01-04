from pathlib import Path
from collections import defaultdict
from abc import ABCMeta, abstractmethod


class ClientMonitor(metaclass=ABCMeta):
    """
    Monitor client connections

    """

    def __init__(self, config: dict):
        config = process_config(config)

        self.config = config
        self.listeners = []

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

    @abstractmethod
    def get_current_connections(self) -> dict:
        pass


def process_config(config: dict) -> dict:
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