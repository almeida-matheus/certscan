try:
    import os
    from collections import OrderedDict
    from OpenSSL import crypto # pyOpenSSL
    from datetime import datetime
    from cryptography import x509 # cryptography
    from cryptography.hazmat.backends import default_backend
except ImportError as e:
    print(f"{e}\nyou must install some libs from requeriments.txt in order to run this script\npip install -r requeriments.txt")

class LocalCertificate:

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def get_file_content(self,file_path):
        ''' get file content of certificate file '''
        try:
            cert_path = os.path.join(self.current_dir, file_path)
            with open(cert_path) as f:
                return f.read()
        except:
            raise OSError("Error: cannot read this file")

    def get_files_dir(self,dir_certs):
        ''' scan dir with certificates to get the path of certificate files '''
        try:
            array_certs_path  = [os.path.join(self.current_dir,dir_certs, f) for f in os.listdir(
                dir_certs) if os.path.isfile(os.path.join(dir_certs, f))]
            return array_certs_path #os.listdir() will get you files and directories in a directory
        except:
            raise OSError("Error: cannot read this directory")

    def get_alternative_names(self,cert_crypto):
        '''return a list of strings containing Subject Alternative Name(san) dns names '''
        crt_san_data = cert_crypto.extensions.get_extension_for_oid(
            x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        ) # extension
        dns_names = crt_san_data.value.get_values_for_type(
            x509.DNSName
        )
        return dns_names

    def get_cert_info(self, cert_content, encoding_type='base64'):
        ''' return dict wih info of certificate  '''
        dict_cert = OrderedDict()
        if encoding_type == 'base64': # base64 - pem
            cert_openssl = crypto.load_certificate(crypto.FILETYPE_PEM, cert_content)
            cert_crypto = x509.load_pem_x509_certificate(str.encode(cert_content), default_backend()) #instance of Certificate
        if encoding_type == 'binary': # binary - der
            cert_openssl = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_content)
            cert_crypto = x509.load_pem_x509_certificate(str.encode(cert_content), default_backend()) 

        dict_cert["common_name_subject"] = cert_openssl.get_subject().commonName
        dict_cert["dns_names"]  = self.get_alternative_names(cert_crypto)
        dict_cert["common_name_issuer"] = cert_openssl.get_issuer().commonName
        dict_cert["organization_name_issuer"] = cert_openssl.get_issuer().organizationName
        dict_cert["has_expired"] = cert_openssl.has_expired() # checks the certificate's time stamp against current time -  Returns true if the certificate has expired

        # date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
        date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
        if cert_openssl.get_notBefore():
           dict_cert["not_before"] = datetime.strptime(cert_openssl.get_notBefore().decode(encoding), date_format)
        if cert_openssl.get_notBefore():
            dict_cert["not_after"] = datetime.strptime(cert_openssl.get_notAfter().decode(encoding), date_format)

        dict_cert["days_to_expire"] = (dict_cert["not_after"] - datetime.now()).days

        dict_cert["self_signed"] = False
        if dict_cert["common_name_subject"] == dict_cert["common_name_issuer"]:
            dict_cert["self_signed"] = True

        return dict_cert

    def print_info(self):
        print('Issued to: issuer.commonName')
        print('Issued by: subject.commonName, subject.O')
        print('Valid from {} to {}')

    def catch_name_info(self,cert_base):
        '''return array with dict info about cert '''
        dict_name = {}
        dict_name["commonName"] = cert_base.commonName
        dict_name["emailAddress"] = cert_base.emailAddress
        dict_name["countryName"] = cert_base.countryName
        dict_name["organizationName"] = cert_base.organizationName
        dict_name["organizationalUnitName"] = cert_base.organizationalUnitName
        # cert_pubkey_bits = cert_openssl.get_pubkey().bits()
        # cert_pubkey_type = cert_openssl.get_pubkey().type()
        # cert_serial_number = cert_openssl.get_serial_number() # Return the certificate serial number.
        # cert_version = cert_openssl.get_version() # Return the certificate version.
        # # test = crypto.X509Extension("issuerAltName",False,"email:"+"test")
        print(cert_base.get_components())
        return dict_name

class OnlineCertificate:

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def get_uri_file(self,file_path):
        ''' get file content of certificate file '''
        try:
            with open(file_path) as file:
                lines = [line.rstrip() for line in file]
                return lines
        except:
            raise OSError("Error: cannot read this file")