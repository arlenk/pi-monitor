# -*- coding: utf-8 -*-
import time

import monitors.openvpn as pmo
import actions.twilio as pt


"""Main module."""
def main():
    config = {'openvpn-status-file': 'openvpn-status.log'}
    monitor = pmo.OpenVPNMonitor(config)

    while True:
        time.sleep(60)
        changes, message = monitor.run()

        if changes:
            print("found changes: {}".format(message))
