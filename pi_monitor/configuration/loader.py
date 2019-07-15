"""
Load monitors, actions, etc. specified in config files

"""
import importlib
import copy
import pi_monitor.logger as pml


def load_monitors(config):
    """
    Load monitors defined in config dict

    :param config: dict
    :return: dict
    """
    logger = pml.get_logger()

    # TODO: move validation to its own function
    if 'monitors' not in config:
        raise ValueError("no monitors defined i config file!")

    config = copy.deepcopy(config['monitors'])
    monitors = dict()

    for name, values in config.items():
        logger.debug(f"loading: {name}")
        if 'class' not in values:
            raise ValueError("no class defined for monitor {}".format(name))

        cls = values.pop('class')
        c = _try_importing_class(cls)
        monitor = c(values)
        monitors[name] = monitor

    return monitors


def load_actions(config):
    """
    Load actions defined in config dict

    :param config: dict
    :return: dict
    """
    logger = pml.get_logger()

    # TODO: move validation to its own function
    if 'actions' not in config:
        raise ValueError("no actions defined i config file!")

    config = copy.deepcopy(config['actions'])
    actions = dict()

    for name, values in config.items():
        logger.debug(f"loading: {name}")
        if 'class' not in values:
            raise ValueError("no class defined for monitor {}".format(name))

        cls = values.pop('class')
        c = _try_importing_class(cls)
        action = c(values)
        actions[name] = action

    return actions


def _try_importing_class(name):
    """
    Try import a class such as "monitors.openvpn.OpenVPNMonitor"

    :param name:
    :return:
    """
    logger = pml.get_logger()

    module, cls = name.rsplit('.', 1)
    logger.debug(f"trying to import module: {module}")

    # TODO: how do we avoid hardcoding this
    module = "pi_monitor.{}".format(module)
    m = importlib.import_module(module)

    if not hasattr(m, cls):
        raise ValueError("class {} not defined in {}".format(cls, module))
    c = getattr(m, cls)

    return c






