import psutil
from typing import List

from pi_monitor.core import Event


class CPUUsageMonitor:
    """
    Monitor CPU Usage

    """

    def __init__(self, config):
        config = process_config(config,
                                required_fields=['maximum_usage',
                                                 ])
        self.maximum_usage = config.get("maximum_usage")
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
        usage = get_cpu_usage()
        maximum_usage = self.maximum_usage

        events = []
        print(f"current cpu usage: {usage}")
        if usage >= maximum_usage:
            message = f"cpu usage ({usage}%) above maximum threshold ({maximum_usage})"

            events.append(
                Event(message)
            )

        return events


def get_cpu_usage() -> float:
    """
    Get current cpu usage

    """
    usage = psutil.cpu_percent()

    return usage


def process_config(config: dict, required_fields: List[str]) -> dict:
    """
    Make sure config object has required values

    """
    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    maximum_usage = config['maximum_usage']

    if not 1 < maximum_usage < 100:
        raise ValueError(f"maximum_usage should be between 1 and 100")

    config['maximum_usage'] = float(maximum_usage)

    return config
