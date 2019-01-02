# -*- coding: utf-8 -*-
import time

import pivpn_monitor.configuration.config as cc


"""Main module."""
def main():
    config = cc.load_configuration("pivpn_monitor.cfg", ".env")
    monitors = config['monitors']
    actions = config['actions']

    while True:
        time.sleep(60)
        for monitor_name, monitor in monitors.items():
            print("checking monitor: {}".format(monitor_name))
            changes, message = monitor.run()

            if changes:
                print("found changes: {}".format(message))

                for action_name, action in actions.items():
                    print("firing action {}".format(action_name))

                    action.act(message)


