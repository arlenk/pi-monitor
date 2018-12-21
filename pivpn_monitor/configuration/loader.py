"""
Load monitors, actions, etc. specified in config files

"""
import importlib
import copy


def load_monitors(config):
    """
    Load monitors defined in config dict

    :param config: dict
    :return: dict
    """
    # TODO: move validation to its own function
    if 'monitors' not in config:
        raise ValueError("no monitors defined i config file!")

    config = copy.deepcopy(config['monitors'])
    monitors = dict()

    for name, values in config.items():
        print("loading: {}".format(name))
        if 'class' not in values:
            raise ValueError("no class defined for monitor {}".format(name))

        cls = values.pop('class')
        c = _try_importing_class(cls)
        monitor = c(values)
        monitors[name] = monitor

    return monitors


def _try_importing_class(name):
    """
    Try import a class such as "monitors.openvpn.OpenVPNMonitor"

    :param name:
    :return:
    """

    module, cls = name.rsplit('.', 1)
    print("trying to import module: {}".format(module))

    # TODO: how do we avoid hardcoding this
    module = "pivpn_monitor.{}".format(module)
    m = importlib.import_module(module)

    if not hasattr(m, cls):
        raise ValueError("class {} not defined in {}".format(cls, module))
    c = getattr(m, cls)

    return c






