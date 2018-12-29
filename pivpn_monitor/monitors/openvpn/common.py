from pathlib import Path


def process_config(config):
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