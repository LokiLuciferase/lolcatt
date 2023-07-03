#!/usr/bin/env python3
from argparse import ArgumentParser

from lolcatt.ui.lolcatt import LolCatt


def main():
    parser = ArgumentParser(description='LolCatt')
    parser.add_argument('url_or_path', nargs='?', help='URL or path to file')
    parser.add_argument('-d', '--device', default=None, help='Device to cast to')
    parsed = parser.parse_args()

    lolcatt = LolCatt(device_name=parsed.device)

    if parsed.url_or_path is not None:
        lolcatt.cast(parsed.url_or_path)
    lolcatt.run()


if __name__ == '__main__':
    main()
