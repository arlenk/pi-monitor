"""
Load config file and optional .env (which may contain secrets that should not go in config)

"""
from pathlib import Path
import os

import toml
from . import loader as cl


def load_configuration(config_file, dotenv_file=None, include_os_env=True):
    """
    Read configuration files and return dict of settings

    :param config_file: str
    :param dotenv_file: str | None
    :param include_os_env: bool
    :return:

    """
    config_file = Path(config_file)
    if not config_file.exists():
        raise IOError("could not find config file: {}".format(config_file))

    if dotenv_file:
        dotenv_file = Path(dotenv_file)
        if not dotenv_file.exists():
            raise IOError("could not find .env file: {}".format(dotenv_file))

    env = dict()
    if include_os_env:
        env = os.environ.copy()

    if dotenv_file:
        dotenv = _parse_dotenv(dotenv_file)
        env.update(dotenv)

    config = _parse_config(config_file, env)
    monitors = cl.load_monitors(config)
    actions = cl.load_actions(config)

    config['monitors'] = monitors
    config['actions'] = actions

    return config


def _parse_dotenv(path):
    """
    Parse .env file into a simple dict

    :param path: Path
    :return: dict
    """
    env = dict()

    with path.open() as file:
        for iline, line in enumerate(file):
            line = line.strip()
            if '=' not in line:
                raise ValueError("line {} [line #{}] in {} is missing "
                                 "a key value pair".format(line, iline, path))
            key, value = line.split('=', 1)
            env[key] = value

    return env


def _parse_config(path, env):
    """
    Parse config file, with optional environment variables

    Any values matching $VALUE pattern will be substituted by env[VALUE]

    :param path: str
    :param env: dict
    :return: dict

    """
    path = Path(path)
    if not path.exists():
        raise IOError("could not find config file: {}".format(path))

    s = path.open().read()
    s = s.format(**env)

    config = toml.loads(s)

    return config





