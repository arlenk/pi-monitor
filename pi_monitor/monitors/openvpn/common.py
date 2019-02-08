from abc import ABCMeta, abstractmethod
from collections import defaultdict

from pi_monitor.core import Event
from typing import List


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

    def run(self) -> List[Event]:
        """
        Run monitor to look for any new Events

        :return:
        """
        prior = self.connections
        current = self.get_current_connections()
        self.connections = current

        new, dropped = compare_connections(prior, current)

        events = []
        if new:
            message = "found {} new connection(s):\n".format(len(new))
            for client, client_connections in new.items():
                for real_address, details in client_connections.items():
                    message += "user {} from address {}".format(details['Common Name'],
                                                                details['Real Address'])
            events.append(
                Event(message, dict(new=new))
            )

        return events

    @abstractmethod
    def get_current_connections(self) -> dict:
        pass



def compare_connections(prior: dict, current: dict) -> (dict, dict):
    """
    Determine new (and dropped) connections between prior and current connections

    :param prior:
    :param current:
    :return:
    """

    new = _connection_diff(prior, current)
    dropped = _connection_diff(current, prior)

    return new, dropped


def _connection_diff(a: dict, b: dict) -> dict:
    """
    Difference (a-b) between two dicts of connections

    :param a:
    :param b:
    :return:
    """
    dropped = defaultdict(dict)
    for client, client_connections in b.items():
        for real_address, details in client_connections.items():
            if (client not in a or
                    real_address not in a[client]):
                dropped[client][real_address] = details
    dropped = dict(dropped)

    return dropped
