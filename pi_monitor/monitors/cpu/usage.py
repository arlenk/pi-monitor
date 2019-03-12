import os
from pathlib import Path
from typing import List

from pi_monitor.core import Event


class FreeSpaceMonitor():
    """
    Monitor free disk space

    """

    def __init__(self, config):
        config = process_config(config,
                                required_fields=['path',
                                                 'minimum_space'])
        self.path = config.get("path")
        self.minimum_space = config.get("minimum_space")
        self.minimum_bytes = config.get("minimum_bytes")

        self.listeners = dict()

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
        free_bytes = get_free_bytes(self.path)
        minimum_free_bytes = self.minimum_bytes
        events = []
        print("current free bytes: {}".format(free_bytes))
        if free_bytes <= minimum_free_bytes:
            message = ("free space ({} bytes) below minimum "
                       "threshold ({})".format(free_bytes, self.minimum_space))

            events.append(
                Event(message)
            )

        return events


def get_free_bytes(path: Path) -> float:
    """
    Get free bytes

    """
    import os
    statvfs = os.statvfs(path)

    free_bytes = statvfs.f_bavail * statvfs.f_frsize

    return free_bytes


def process_config(config: dict, required_fields: List[str]) -> dict:
    """
    Make sure config object has required values

    """
    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    path = Path(config['path'])
    if not path.exists():
        raise ValueError("could not find target path: {}".format(path))
    config['path'] = path

    minimum_space = config['minimum_space']
    minimum_bytes = _string_to_bytes(minimum_space)

    # keep minimum space around for reporting
    config['minimum_space'] = minimum_space
    config['minimum_bytes'] = minimum_bytes

    return config


def _string_to_bytes(s: str):
    """
    Convert string representation of disk space into bytes

    :param s: str
    :return: float
    """
    s = s.replace(' ', '')
    num, unit = s[:-1], s[-1]
    num = float(num)

    unit_multiplier = {
        'B': 1.0,
        'K': 1024.0,
        'M': 1024.0 * 1024.0,
        'G': 1024.0 * 1024.0 * 1000,
        'T': 1024.0 * 1024.0 * 1000 * 1000,
        'P': 1024.0 * 1024.0 * 1000 * 1000 * 1000,
    }

    if unit not in unit_multiplier:
        raise ValueError("unknown unit: {}".format(unit))

    multiplier = unit_multiplier[unit]

    bytes = num * multiplier
    return bytes
