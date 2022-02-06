try:
    from OpenSSL import crypto
    from datetime import datetime
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend
    from collections import OrderedDict
    from socket import socket
    import ssl
except ImportError as e:
    print(f"{e}\nyou must install some libs from requirements.txt in order to run this script\npip install -r requeriments.txt")

class Certificate:

    def _get_alternative_names(self,cert_crypto):
        ''' return a list of strings containing Subject Alternative Name (SAN) dns names '''
        crt_san_data = cert_crypto.extensions.get_extension_for_oid(
            x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        ) # extension
        dns_names = crt_san_data.value.get_values_for_type(
            x509.DNSName
        )
        return dns_names

    def get_cert_info(self, cert_content, encoding_type='base64'):
        ''' returns a dict with certificate information '''
        dict_cert = OrderedDict()
        if encoding_type == 'base64': # base64 - pem
            cert_openssl = crypto.load_certificate(crypto.FILETYPE_PEM, cert_content)
            cert_crypto = x509.load_pem_x509_certificate(str.encode(cert_content), default_backend()) #instance of certificate
        if encoding_type == 'binary': # binary - der
            cert_openssl = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_content)
            cert_crypto = x509.load_der_x509_certificate(cert_content, default_backend())

        dict_cert["subject_common_name"] = cert_openssl.get_subject().commonName
        dict_cert["subject_alt_name"]  = self._get_alternative_names(cert_crypto)
        dict_cert["issuer_common_name"] = cert_openssl.get_issuer().commonName
        dict_cert["issuer_org_name"] = cert_openssl.get_issuer().organizationName
        dict_cert["serial_number"] = cert_openssl.get_serial_number()
        dict_cert["version"] = cert_openssl.get_version()

        dict_cert["has_expired"] = cert_openssl.has_expired() # checks the certificate's time stamp against current time -  returns true if the certificate has expired

        date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
        if cert_openssl.get_notBefore():
           dict_cert["not_before"] = datetime.strptime(cert_openssl.get_notBefore().decode(encoding), date_format) # not_before
        if cert_openssl.get_notBefore():
            dict_cert["not_after"] = datetime.strptime(cert_openssl.get_notAfter().decode(encoding), date_format) # not_after

        dict_cert["days_to_expire"] = (dict_cert["not_after"] - datetime.now()).days # days_to_expire

        dict_cert["self_signed"] = False
        if dict_cert["subject_common_name"] == dict_cert["issuer_common_name"]:
            dict_cert["self_signed"] = True

        return dict_cert

    def get_cert_info_by_domain(self, hostname):
        ''' connect to host to get digital certificate '''
        sckt = socket()
        sckt.connect((hostname, 443)) # establish a connection to the remote server

        context = ssl._create_unverified_context()
        ssl_sckt = context.wrap_socket(sckt, server_hostname=hostname)

        cert_content_bin = ssl_sckt.getpeercert(True)
        return self.get_cert_info(cert_content_bin, 'binary')