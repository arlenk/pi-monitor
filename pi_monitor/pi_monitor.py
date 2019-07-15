# -*- coding: utf-8 -*-
import time
import pi_monitor.logger as pml
import pi_monitor.configuration.main as cc


"""Main module."""
def main():
    config = cc.load_configuration("pi-monitor.cfg", ".env")
    monitors = config['monitors']
    actions = config['actions']
    general = config['general']
    logger = pml.get_logger()


    while True:
        time.sleep(60)
        for monitor_name, monitor in monitors.items():
            logger.debug(f"checking monitor: {monitor_name}")
            events = monitor.run()

            for event in events:
                logger.debug(f"found event: {event}")

                for action_name, action in actions.items():
                    logger.debug(f"firing action {action_name}")

                    action.act(event)


