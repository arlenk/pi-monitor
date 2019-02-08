# -*- coding: utf-8 -*-

"""Console script for pivpn_alerts."""
import sys
import click
import pi_monitor.pi_monitor as pm


@click.command()
def main(args=None):
    """Console script for pivpn_alerts."""
    pm.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
