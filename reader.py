import os

class Reader:

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def get_file_content(self,file_name):
        ''' return certificate file contents '''
        try:
            cert_path = os.path.join(self.current_dir, file_name)
            with open(cert_path) as f:
                return f.read()
        except:
            raise OSError("Error: cannot read this file")

    def get_files_in_dir(self,dir_certs):
        ''' scan dir with certificates to return the path of certificate files '''
        try:
            array_certs_path  = [os.path.join(self.current_dir,dir_certs, f) for f in os.listdir(
                dir_certs) if os.path.isfile(os.path.join(dir_certs, f))]
            return array_certs_path #os.listdir() will get you files and directories in a directory
        except:
            raise OSError("Error: cannot read this directory")

    def get_file_lines(self,file_name):
        ''' return a list with each line of the contents of a certificate file '''
        try:
            file_path = os.path.join(self.current_dir, file_name)
            with open(file_path) as f:
                return [line.rstrip() for line in f]
                return f.readlines()
        except:
            raise OSError("Error: cannot read this file")