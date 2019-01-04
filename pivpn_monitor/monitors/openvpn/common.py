from abc import ABCMeta, abstractmethod
from collections import defaultdict


class ClientMonitor(metaclass=ABCMeta):
    """
    Monitor client connections

    """
    def __init__(self, config: dict):
        self.config = config
        self.listeners = dict()
        self.connections = self.get_current_connections()

    def add_listener(self, name: str, action):
        """
        Add action as a listener to events from this monitor

        :param name:
        :param action:
        :return:
        """
        self.listeners[name] = action

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


