#!/usr/bin/env python

import argparse
import requests
from requests.exceptions import SSLError, ConnectionError


def main() -> None:
    parser = argparse.ArgumentParser(
        'ssl-check',
        description='Check SSL websites for valid certificates',
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-u',
        '--urls',
        nargs='+',
        type=str,
        help='Websites to process.',
    )
    group.add_argument(
        '-f',
        '--file',
        type=str,
        help='File to parse. 1 url per line.',
    )
    args = parser.parse_args()

    if args.urls is not None:
        for url in args.urls:
            test_url(url)
        exit(0)
    if args.file is not None:
        with open(args.file, 'r') as f:
            while True:
                url = f.readline().strip()

                if not url:
                    break
                test_url(url)


def test_url(url: str) -> None:
    try:
        requests.get(f'https://{url}')
    except SSLError as e:
        print(f'The site https://{url} has an INVALID SSL certificate.')
        print(f'{e}\n')
    except ConnectionError:
        print(f'Could not connect to https://{url}')
    else:
        print(f'https://{url} has a valid certificate.')


if __name__ == '__main__':
    main()
