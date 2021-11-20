# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import argparse
from certificate import LocalCertificate, OnlineCertificate
from printer import Printer

__version__ = '0.0.1'
__description__ = """\
command line tool to scan digital certificate information
"""

def print_info(dict_cert):
    printer = Printer(dict_cert)
    if args.text: printer.print_text()
    elif args.csv: printer.print_csv()
    else: printer.print_json()

if __name__ == '__main__':
    local_cert = LocalCertificate()
    online_cert = OnlineCertificate()

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-u','--uri', help='get certificate information from a URI')
    parser.add_argument('-r','--read', help='get certificate information from read a file containing URIs')
    parser.add_argument('-f','--file', type=argparse.FileType('r', encoding='UTF-8'), help='get certificate information from local file certificate')
    parser.add_argument('-d','--dir', help='get information from certificates that are within a local directory')
    parser.add_argument('-j','--json', action='store_true', help='show output in json format')
    parser.add_argument('-t','--text', action='store_true', help='show output in text format')
    parser.add_argument('-c','--csv', action='store_true', help='show output in csv format')
    parser.add_argument('-v','--version', action='store_true', help='show certscan version')
    # parser.add_argument('-h','--help', action='store_true', help='show this help message')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        parser.exit()

    if args.file:
        dict_cert = local_cert.get_cert_info(args.file.read(), 'base64')
        print_info([dict_cert])
        parser.exit()

    if args.dir:
        array_certs = local_cert.get_files_dir('certs')
        for cert in array_certs:
            dict_cert = local_cert.get_cert_info(cert.read(), 'base64')
        parser.exit()