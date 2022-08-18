from ftplib import FTP

## 1.5
ftp = FTP('192.168.1.5')
ftp.login(user='Shweta', passwd='Shweta#123')
ftp.dir()

## 1.4
ftp = FTP('192.168.1.4')
ftp.login(user='Shweta', passwd='Shweta#123')
ftp.dir()

# ftp.cwd('/research_database/surgery media repo/12sep18 pre op & Sx')
path = '/research_database/surgery media repo/12sep18 pre op & Sx/test'
dest = 'D:/Shweta/Surgery/surgery_media/tmp/'
file_name = 'IMG_1998.jpg'
ftp.cwd(path)
ftp.retrbinary("RETR " + file_name, open(dest + file_name, 'wb').write)

def login_ftp(port, user, passwd):
    ftp = FTP(port)
    ftp.login(user, passwd)
    d = ftp.dir()
    return (d)

def download_file_from_ftp(port='192.168.1.4', user='Shweta', passwd='Shweta#123', source_ftp_path='', file_name='', destination_file_path=''):
    ftp = FTP(port)
    ftp.login(user, passwd)
    ftp.cwd(source_ftp_path)
    tmp_file_path = destination_file_path + file_name
    ftp.retrbinary("RETR " + file_name, open(tmp_file_path, 'wb').write)
    return tmp_file_path

# def upload_file_on_ftp(port='192.168.1.5', user='Shweta', passwd='Shweta#123', source_path='tmp', file_name='', destination_ftp_path=''):
#     ftp = FTP(port)
#     ftp.login(user, passwd)
#     ftp.cwd(destination_ftp_path)
#     ftp.storlines("STOR " + file_name , open(source_path+file_name, 'rb'))

def upload_file_on_ftp(port='192.168.1.5', user='Shweta', passwd='Shweta#123', source_path='tmp', file_name_old='',
                       file_name_new = '', destination_ftp_path=''):
    ftp = FTP(port)
    ftp.login(user, passwd)
    ftp.cwd(destination_ftp_path)
    ftp.maxline = 267257104
    ftp.storlines("STOR " + file_name_new , open(source_path+file_name_old, 'rb'))

## renaming the file from tmp

def list_dirs_from_folder(port='192.168.1.4', user='Shweta', passwd='Shweta#123', sx_media_folder_path='tmp'):
    ftp = FTP(port)
    ftp.login(user, passwd)
    ftp.cwd(sx_media_folder_path)
    file_names = ftp.nlst()  ## it will store all available file_names in the list of python
    return file_names

sx_media_folder_path = '/Prashanti Cancer Care/tmp_surgery_media_sk/12sep18 pre op & Sx'
tmp_folder = 'D:/Shweta/Surgery/surgery_media/tmp/trial_tmp/'
destination_ftp_folder = '/research_database/surgery media repo/tmp_sk/trial/'

def rename_file_from_tmp(sx_media_folder_path, tag, tmp_folder, destination_ftp_folder):
    file_names = list_dirs_from_folder(sx_media_folder_path=sx_media_folder_path)
    print(file_names)
    i = 1
    for file_name in file_names:
        print(file_name)
        tmp_file_path = download_file_from_ftp(source_ftp_path=sx_media_folder_path, file_name=file_name, destination_file_path=tmp_folder)
        print(tmp_file_path)
        if file_name.endswith('.jpg'):
            print(i)
            new_file_name = tag + '_' + str(i) + '.jpg'
            print(new_file_name)
            upload_file_on_ftp(source_path=tmp_file_path,
                               file_name_new=new_file_name, destination_ftp_path=destination_ftp_folder)
            i += 1
        elif file_name.endswith('.m4v'):
            i = 1
            print(i)
            new_file_name = tag + '_' + str(i) + '.m4v'
            print(new_file_name)
            upload_file_on_ftp(source_path=tmp_file_path,
                               file_name_new=new_file_name, destination_ftp_path=destination_ftp_folder)
            # i+= 1
    i += 1

rename_file_from_tmp(sx_media_folder_path=sx_media_folder_path, tag='abc', tmp_folder=tmp_folder, destination_ftp_folder=destination_ftp_folder)

import re
import pyqrcode
import os


