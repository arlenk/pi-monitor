import re
import subprocess as sb
from collections import defaultdict

from .common import process_config


class ProcessMonitor():
    """
    Monitor events by calling a separate process that will return current openvpn status

    """

    def __init__(self, config):
        config = process_config(config)

        self.config = config
        self.listeners = []
        self._openvpn_status_process = config.get("status_command")
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
        connections = _call_openvpn_status_process(self._openvpn_status_process)
        return connections


def _call_openvpn_status_process(status_command: str) -> dict:
    """
    Call status command and parse list of currently connected clients from results

    """
    clients = defaultdict(dict)
    command = status_command.split()
    print("about to execute: {}".format(command))
    res = sb.run(command, check=False, stdout=sb.PIPE)

    # todo: check for errors from res... also add a timeout?
    current_status = res.stdout.decode('utf-8')
    print("command returned\n:{}".format(current_status))

    for line in current_status.splitlines():
        print("processing line: {}".format(line))

        # remove escape characters (pivpn bolds some output)
        # re from https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
        # todo: find better way to parse output of pivpn
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        line = ansi_escape.sub('', line)

        # ignore blank lines and comments (lines that start with a blank are
        # part of heading, but not important for us)
        if not line or line.startswith(":") or line.startswith((" ", "\t")):
            continue

        line = line.strip()
        if line.startswith("Name"):
            column_names = line.split('\t')
        else:
            client_values = line.split('\t')
            client = dict(zip(column_names, client_values))
            client["Common Name"] = client["Name"]
            client["Real Address"] = client["Remote IP"]
            common_name = client['Common Name']
            real_address = client['Real Address']

            clients[common_name][real_address] = client

    clients = dict(clients)
    return clients