import re
import subprocess as sb
from collections import defaultdict
from typing import List

from .common import ClientMonitor


class ProcessMonitor(ClientMonitor):
    """
    Monitor events by calling a separate process that will return current openvpn status

    """

    def __init__(self, config):
        config = process_config(config,
                                required_fields=['status_command'])
        self._openvpn_status_process = config.get("status_command")

        super().__init__(config)

    def get_current_connections(self) -> dict:
        """
        List of users currently connected

        """
        connections = call_openvpn_status_process(self._openvpn_status_process)
        return connections


def process_config(config: dict, required_fields: List[str]) -> dict:
    """
    Make sure config object has required values

    """
    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    return config


def call_openvpn_status_process(status_command: str) -> dict:
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

        # ignore 'no clients connected line' if.. no clients are connected
        if line.startswith("No Clients Connected!"):
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