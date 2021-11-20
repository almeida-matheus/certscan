from datetime import date, datetime
from rich import print
import json

class Printer:

    def __init__(self, array_dict_cert):
        self.array_dict_cert = array_dict_cert

    def print_json(self):
        ''' convert dict to json format'''
        def json_serial(obj):
            '''json serializer for objects not serializable by default json code'''
            if isinstance(obj, (datetime, date)): # checks to find out if object is of class datetime or date, and then uses .isoformat() to produce a serialized version of it
                return obj.isoformat()
            raise TypeError (f'Error: type {type(obj)} not serializable')

        print(json.dumps(self.array_dict_cert, indent=4, default=json_serial))

    def print_text(self):
        ''' convert dict to text table format '''
        for dict_cert in self.array_dict_cert:
            print('Issued to: [green bold]{}[/]'.format(dict_cert["common_name_subject"]))
            print('Issued by: [green bold]{} - {}[/]'.format(dict_cert["common_name_issuer"], dict_cert["organization_name_issuer"]))
            print('Alternative names: [green]{}[/]'.format(" ".join(str(name) for name in dict_cert["dns_names"])))
            print('Valid from [green bold]{}[/] to [green bold]{}[/]'.format(
                dict_cert["not_before"].strftime('%d/%m/%Y'), dict_cert["not_after"].strftime('%d/%m/%Y')))
            if not dict_cert["has_expired"]:
                print('[green bold]{}[/] days left for certificate to expire'.format(dict_cert["days_to_expire"]))
            else:
                print('It has been [red bold]{}[/] days since the certificate expired'.format(abs(dict_cert["days_to_expire"])))
            if dict_cert["self_signed"]:
                print('Certificate is [red bold]self signed[/]')
            print('')

    def print_csv(self):
        ''' convert dict to csv format '''
        print('common_name_subject,alternative_names,common_name_issuer,organization_name_issuer,has_expired,not_before,not_after,days_to_expire,self_signed')
        for d in self.array_dict_cert:
            print('{},{},{},{},{},{},{},{},{}'.format(
                d['common_name_subject'],";".join(str(name) for name in d["dns_names"]),d['common_name_issuer'],d['organization_name_issuer'],d['has_expired'],d["not_before"].strftime('%d/%m/%Y'),d["not_after"].strftime('%d/%m/%Y'),d['days_to_expire'],d['self_signed']))