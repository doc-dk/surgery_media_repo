import ftplib
import os
from ftplib import FTP

class SurgeryMediaManagement():

    def __init__(self, ftp_user_name, ftp_password, source_path, destination_path):
        self.user_name = ftp_user_name
        self.password = ftp_password
        self.source_path = source_path
        self.destination_path = destination_path

    @staticmethod
    def create_tmp_folder(path='tmp'):
        if not os.path.isdir(path):
            os.mkdir(path)
            print("tmp folder created at current repo!")
        else:
            print('tmp folder already exist!')
        return

    @staticmethod
    def delete_tmp_folder(path='tmp'):
        os.rmdir(path)
        print("tmp folder deleted!")  ## ? if the tmp is balnk then only remove tmp or remove it without checking
        return

    def login_ftp_old(self):
        ftp = FTP('192.168.1.4')
        ftp.login(user=self.user_name, passwd=self.password)
        ftp.cwd(self.source_path)
        dirs = ftp.nlst()
        return dirs

    def login_ftp_new(self):
        ftp = FTP('192.168.1.5')
        ftp.login(user=self.user_name, passwd=self.password)
        ftp.cwd(self.destination_path)
        dirs = ftp.nlst()
        return dirs

    def download_file_from_ftp(self, file_name):
        ftp = FTP('192.168.1.4')
        ftp.login(self.user_name, self.password)
        ftp.cwd(self.source_path)
        ftp.retrbinary("RETR " + file_name, open('tmp/' + file_name, 'wb').write)
        print("file " + file_name + " downloaded successfully!")
        return

    def upload_file_on_ftp(self, file_name, tag):
        ftp = FTP('192.168.1.5')
        ftp.login(self.user_name, self.password)
        ftp.cwd(self.destination_path)
        ftp.maxline = 267257104
        ftp.storlines("STOR " + tag, open('tmp/' + file_name, 'rb'))
        print("File " + tag + " uploaded successfully!")
        return

    @staticmethod
    def get_file_extension(file_name):
        spllited_file_name = str.split(file_name, '.')
        extension = spllited_file_name[-1]
        return "." + extension

    def rename_file(self, file_name, tag):
        os.rename(os.path.join("tmp/", file_name), os.path.join("tmp/", tag))
        print(file_name + " was renamed by " + tag + " successfully!")

    # def rename_file_from_tmp(self):
    #     file_names = self.login_ftp_old()
    #     i = 1
    #     for file_name in file_names:
    #         # get extension as str after first '.' from end of file_name
    #         ext = file_name[-4:]ta
    #         # tmp_file_path = self.download_file_from_ftp(file_name=file_name)  ## tmp_file_path is not usefull
    #         new_file_name = self.tag + '_' + str(i) + ext
    #         # rename file here
    #         # self.upload_file_on_ftp(file_name=file_name, tag=new_file_name)
    #         i+=1

    def get_check_sum(self, test):

def update_repo(tag, ftp_user_name, ftp_password, media_list_df):
    
    
    smm = SurgeryMediaManagement(ftp_user_name='Shweta',
                                 ftp_password='Shweta#123',
                                 source_path='/Prashanti Cancer Care/tmp_surgery_media_sk/12sep18 pre op & Sx',
                                 destination_path='/research_database/surgery media repo/tmp_sk/trial_v3')

    smm.create_tmp_folder()
    try:
        file_names = smm.login_ftp_old()
        for index, file_name in enumerate(file_names):
            print(file_name)
            smm.download_file_from_ftp(file_name=file_name)
            ext = smm.get_file_extension(file_name)
            new_name = tag + "_" + str(index+1) + ext
            smm.rename_file(file_name, tag= new_name)
            smm.upload_file_on_ftp(new_name, tag= new_name)
    except ftplib.all_errors as e:
        print('FTP fail! ', e)
    smm.delete_tmp_folder()

    #write to db table that error/success log


if __name__ == '__main__':
    import pandas as pd
    tag = input('tag: ')
    ftp_user_name = input('ftp_user_name')
    ftp_password = input('ftp_password: ') 
    media_list_file = input('media_list_file: ')
    media_list_df = pd.read_excel('media_list_file')
    update_repo(tag, ftp_user_name, ftp_password, media_list_df)