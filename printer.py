from datetime import date, datetime
from rich import print # rich
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
            raise TypeError (f'error: type {type(obj)} not serializable')

        print(json.dumps(self.array_dict_cert, indent=4, default=json_serial))

    def print_text(self):
        ''' convert dict to text table format '''
        for dict_cert in self.array_dict_cert:
            print('Issued to: [green bold]{}[/]'.format(dict_cert["subject_common_name"]))
            print('Issued by: [green bold]{} - {}[/]'.format(dict_cert["issuer_common_name"], dict_cert["issuer_org_name"]))
            print('Alternative names: [green]{}[/]'.format(" ".join(str(name) for name in dict_cert["subject_alt_name"])))
            print('Valid from [bright_cyan]{}[/] to [bright_cyan]{}[/]'.format(
                dict_cert["not_before"].strftime('%d/%m/%Y'), dict_cert["not_after"].strftime('%d/%m/%Y')))
            if not dict_cert["has_expired"]:
                print('[bright_cyan]{}[/] days left for certificate to expire'.format(dict_cert["days_to_expire"]))
            else:
                print('It has been [red bold]{}[/] days since the certificate expired'.format(abs(dict_cert["days_to_expire"])))
            if dict_cert["self_signed"]:
                print('Certificate is [red bold]self signed[/]')
            print('')

    def print_csv(self):
        ''' convert dict to csv format '''
        print('[bright_white]subject_common_name,alternative_names,issuer_common_name,issuer_org_name,has_expired,not_before,not_after,days_to_expire,self_signed[/]')
        for d in self.array_dict_cert:
            print('{},{},{},{},{},{},{},{},{}'.format(
                d['subject_common_name'],";".join(str(name) for name in d["subject_alt_name"]),d['issuer_common_name'],d['issuer_org_name'],d['has_expired'],d["not_before"].strftime('%d/%m/%Y'),d["not_after"].strftime('%d/%m/%Y'),d['days_to_expire'],d['self_signed']))