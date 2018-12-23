# -*- coding: utf-8 -*-
import time

import configuration.config as cc
import configuration.loader as cl


"""Main module."""
def main():
    config = cc.load_configuration("pivpn_monitor.cfg", ".env")
    monitors = cl.load_monitors(config)
    actions = cl.load_actions(config)

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


