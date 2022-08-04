from ftplib import FTP

class SurgeryMediaManagement():

    def __init__(self, FTP_port_old, FTP_port_new, user_name, password, tag, source_path, tmp_folder_path, destination_path):
        self.FTP_port_old = FTP_port_old
        self.FTP_port_new = FTP_port_new
        self.user_name = user_name
        self.password = password
        self.tag = tag
        self.source_path = source_path
        self.tmp_folder_path = tmp_folder_path
        self.destination_path = destination_path

    def login_ftp_old(self):
        ftp = FTP(self.FTP_port_old)
        ftp.login(user=self.user_name, passwd=self.password)
        ftp.cwd(self.source_path)
        dirs = ftp.nlst()
        return dirs

    def login_ftp_new(self):
        ftp = FTP(self.FTP_port_new)
        ftp.login(user=self.user_name, passwd=self.password)
        ftp.cwd(self.destination_path)
        dirs = ftp.nlst()
        return dirs

    def download_file_from_ftp(self, file_name=''):
        ftp = FTP(self.FTP_port_old)
        ftp.login(self.user_name, self.password)
        ftp.cwd(self.source_path)
        tmp_file_path = self.tmp_folder_path + file_name
        ftp.retrbinary("RETR " + file_name, open(tmp_file_path, 'wb').write)
        return tmp_file_path

    def upload_file_on_ftp(self, file_name_old='', file_name_new=''):
        ftp = FTP(self.FTP_port_new)
        ftp.login(self.user_name, self.password)
        ftp.cwd(self.destination_path)
        ftp.maxline = 267257104
        ftp.storlines("STOR " + file_name_new, open(self.tmp_folder_path + file_name_old, 'rb'))
        print("File " + file_name_new + " uploaded successfully!")

    def rename_file_from_tmp(self):
        file_names = self.login_ftp_old()
        i = 1
        for file_name in file_names:
            ext = file_name[-4:]
            tmp_file_path = self.download_file_from_ftp(file_name=file_name)
            new_file_name = self.tag + '_' + str(i) + ext
            self.upload_file_on_ftp(file_name_old=file_name, file_name_new=new_file_name)
            i+=1






