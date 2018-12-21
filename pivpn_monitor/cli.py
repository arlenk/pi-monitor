# -*- coding: utf-8 -*-

"""Console script for pivpn_alerts."""
import sys
import click
import pivpn_alerts as pa


@click.command()
def main(args=None):
    """Console script for pivpn_alerts."""
    pa.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
