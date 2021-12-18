#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import resources

__version__ = '1.0.0'
__description__ = """\
command line tool to scan digital certificate information from local files or by parsing domain name
"""

def print_info(dict_cert):
    printer = resources.Printer(dict_cert)
    if args.text: printer.print_text()
    elif args.csv: printer.print_csv()
    else: printer.print_json()

if __name__ == '__main__':
    cert = resources.Certificate()
    reader = resources.Reader()

    parser = argparse.ArgumentParser(description=__description__)
    group = parser.add_mutually_exclusive_group()
    # parser.add_argument('-f','--file', type=argparse.FileType('r', encoding='UTF-8'), help='get certificate information from local file certificate')
    group.add_argument('-f','--file', help='get certificate information from local file certificate')
    group.add_argument('-d','--dir', help='get information from certificates that are within a local directory')
    group.add_argument('-u','--uri', help='get certificate information from a URI')
    group.add_argument('-r','--read', help='get certificate information from read a file containing URIs')
    parser.add_argument('-j','--json', action='store_true', help='show output in json format')
    parser.add_argument('-t','--text', action='store_true', help='show output in text format')
    parser.add_argument('-c','--csv', action='store_true', help='show output in csv format')
    group.add_argument('-v','--version', action='store_true', help='show certscan version')
    # parser.add_argument('-h','--help', action='store_true', help='show this help message')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        parser.exit()

    try:
        if args.file:
            file_content, format_cert = reader.get_file_content(args.file)
            dict_cert = cert.get_cert_info(file_content, format_cert)

            # dict_cert = cert.get_cert_info(args.file.read())
            print_info([dict_cert])
            parser.exit()

        if args.dir:
            array_dict_cert = []
            array_certs_path = reader.get_files_in_dir('certs')
            for cert_path in array_certs_path:
                file_content, format_cert = reader.get_file_content(cert_path)
                array_dict_cert.append(cert.get_cert_info(file_content, format_cert))
            print_info(array_dict_cert)
            parser.exit()

        if args.uri:
            dict_cert = cert.get_cert_info_by_domain(args.uri)
            print_info([dict_cert])
            parser.exit()

        if args.read:
            array_dict_cert = []
            array_hosts = reader.get_file_lines(args.read)
            for host in array_hosts:
                array_dict_cert.append(cert.get_cert_info_by_domain(host))
            print_info(array_dict_cert)
            parser.exit()
    except Exception as e:
        print(e)
