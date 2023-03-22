'''
create surgery media files names, download from server, rename with media names
and upload on server
'''
import re
import pandas as pd
import shutil
import os
from datetime import datetime as dt
from collections import defaultdict
from pccm_db_functions import AddUpdate as sql
from pccm_db_functions import AskYN as ask
from pccm_db_functions import FtpFileFunctions


class SurgeryTable:

    def __init__(self, conn, server_user_name, server_pwd,
                 server_ip, data_sheet_name):
        self.conn = conn
        self.server_user_name = server_user_name
        self.server_pwd = server_pwd
        self.server_ip = server_ip
        self.repo_ip = '192.168.1.5'
        self.repo_location = 'surgery_repo'
        self.tmp ='/home/ix/repos'
        self.data_sheet_name = data_sheet_name

    def create_media_tagged_datasheet(self):
        
        '''
        from user created datasheet create media tags and return df 
        of input data with additional column of media names
        '''

        df = pd.read_excel(os.path.join(self.tmp, 'input_docs', self.data_sheet_name))
        df.columns = [re.sub(' ', '_', str.lower(str.strip(col))) for col in df.columns]
        df.surgery_date = df.surgery_date.apply(lambda x: dt.strptime(x, '%d_%m_%y'))
        df.media_date = df.media_date.apply(lambda x: dt.strptime(x, '%d_%m_%y'))
        df = df.assign(image_interval=df.media_date-df.surgery_date)
        df_media = df.drop(['file_name'], axis=1).drop_duplicates()
        for location in df_media.current_server_location.drop_duplicates().tolist():
            dat = df_media.loc[df_media.current_server_location == location]
            img_interval = dat.image_interval.tolist()[0]
            img_int_string = '_days_from_surgery'
            if isinstance(img_interval, int) and img_interval > 30:
                img_int_string = '_months_from_surgery'
                img_interval = round(img_interval/30, 0)
            elif isinstance(img_interval, int) and img_interval > 365:
                img_int_string = '_years_from_surgery'
                img_interval = round(img_interval/365, 0)
            img_label = str(img_interval) + img_int_string
            surgery_media = dat.media_detail.tolist()[0]
            surgery_media_detail = dat.surgery__media_type.tolist()[0]
            sx_date = dt.strftime(dat['surgery_date'].tolist()[0], '%Y_%m_%d')
            file_name = re.sub('/', '_', dat.file_number.tolist()[0])
            tag = '|'.join([file_name, sx_date, surgery_media,
                            surgery_media_detail, img_label])
            df_media.loc[df_media.current_server_location == location].assign(
                         media_tag=tag, inplace=True)
        df_media_merge = df_media[['media_tag', 'current_server_location']]
        df_media_tag = df.merge(df_media_merge,  on='current_server_location', 
                                how='left')
        return df_media_tag

    def create_repo_filename(self):
        df_media_tag = self.create_media_tagged_datasheet
        dat = pd.DataFrame()
        for media_tag in df_media_tag.media_tag.drop_duplicates().tolist():
            dat = df_media_tag.loc[df_media_tag.media_tag == media_tag]
            dat.reset_index(drop=True, inplace=True)
            file_names = dat.file_name.tolist()
            file_name_dict = defaultdict()
            for old in file_names:
                if re.search('\.', old):
                    ext = re.split('\.', old)[-1:][0]
                elif re.search('image', media_tag):
                    ext = 'jpg'
                else:
                    ext = 'm4v'
                i = dat.index[dat.file_name == old]
                i = str((i.values+1)[0])
                new_file_name = media_tag + i + '\.' + ext
                file_name_dict = { 
                    **{file_name_dict}, 
                    **{'file_name': old, 'repo_file_name': new_file_name}}
            names_df = pd.DataFrame.from_dict(file_name_dict)
            dat = pd.merge(dat, names_df, on='file_name', how='left')
        df_new_name = df_media_tag.merge(dat, on = 'media_tag', how='left')    
        return df_new_name
    
    def download_old_files(self, file_number):
        df_new_name = self.create_repo_filename()
        old_files_df = df_new_name[df_new_name.file_number == file_number]
        status_df = defaultdict(dict)
        for tag in old_files_df.media_tag.drop_duplicates().tolist():
            df_tbd = old_files_df[old_files_df.media_tag == tag]
            ext = 'jpg'
            old_file_type = df_tbd.media_type.drop_duplicates().tolist()[0]
            if not re.search('image', old_file_type):
                ext = 'm4v'
            # old_files = old_files_df.file_names.to_list()
            # old_file_names = [file+'\.' + ext for file in old_files]
            server_path = old_files_df.loc[
                'media_tag' == tag
                ].current_server_location.drop_duplicates().tolist()[0]
            # old_file_paths = [
            #     os.join.path(server_path, old_file_name) for old_file_name in
            #     old_file_names]
            # for old_file_path in old_file_paths:
            ftpff = FtpFileFunctions(ftp_ip=self.server_ip,
                                     user=self.server_user_name,
                                     pwd=self.server_pwd, 
                                     destination_path=server_path)
            ftp = ftpff.ftp_connect()
            download_dest = os.path.join(self.tmp, file_number)
            if not shutil.isdir(os.path.join(self.tmp, file_number)):
                os.mkdir(os.path.join(self.tmp, file_number))
            for old in df_tbd.file_names.to_list():
                download = ftpff.ftp_download(ftp, download_dest)
                ftpff.ftp_disconnect(ftp)
                status_df = {
                    **{status_df},
                    **ask.op_status_dict(
                        file_name=old, op_type='old_download',
                        op_name='download files from current server location',
                        user_name=self.user_name, status_op=download)
                        }
            df_done = df_tbd.merge(status_df, on=('file_name'), how='left')
        df_old_download = old_files.merge(df_done, on='file_name')      
        return (df_old_download)

    def rename_files(self, df_old_download):
        dat_to_rename = df_old_download.loc[
            df_old_download.status_download == 'success'
            ]
        renamed = defaultdict(dict)
        for old in dat_to_rename.file_name.drop_duplicates().tolist():
            file_number = dat_to_rename.loc[
                dat_to_rename.file_name == old
                ].file_number.drop_duplicates().tolist()[0]
            new = dat_to_rename.loc[
                    dat_to_rename.file_name == old
                    ].repo_file_name.drop_duplicates().tolist()[0]
            old_file = os.path.join(self.tmp, file_number, old)
            new_file = os.path.join(self.tmp, new)
            os.rename(old_file, new_file)
            print(new_file)
            renamed = {**{renamed},
                       **ask.op_status_dict(file_name=old,
                                            op_type='rename_file',
                                            op_name='rename files',
                                            user_name=self.user_name,
                                            status_op=True)}
        renamed_df = pd.DataFrame.from_dict(renamed)
        dat_renamed = df_old_download.merge(renamed_df, on='file_name', 
                                            how='left')
        return dat_renamed

    def copy_files_to_repo(self, dat_renamed):
        df_to_upload = dat_renamed.loc[dat_renamed.rename_status == 'success']
        ftpff = FtpFileFunctions(ftp_ip=self.repo_ip,
                                 user=self.server_user_name,
                                 pwd=self.server_pwd, 
                                 destination_path = self.repo_location)
        ftp = ftpff.ftp_connect()
        uploaded = defaultdict()
        for new in df_to_upload.repo_file_name.tolist():
            new_file = os.path.join(self.tmp, new)
            upload = ftpff.ftp_upload(new_file)
            ftpff.ftp_diconnect()
            uploaded = {**{uploaded},
            **{'repo_file_name': new, 
                'repo_upload': sql.output_op_status(
                    old_file = new,
                    file_op = 'download file to tmp', 
                    status = upload), 
                'repo_upload_time': sql.today(),
                'upload_by': self.user_name
                }}
        uploaded_df = pd.DataFrame.from_dict(uploaded)
        dat_to_upload = dat_renamed.merge(uploaded_df, on='repo_file_name', 
                                          how='left')
        return (dat_to_upload)
    
        
    def run(self):
        df_media_tag = self.create_media_tagged_datasheet()
        df_new_name = self.create_repo_filename(df_media_tag)
        df_old_download = self.download_old_files()
        df_new_name = self.rename_files(df_old_download)
        df_copied = self.copy_files_to_repo(df_new_name)
        return df_copied

if __name__ == '__main__':
    server_user_name = 'Devaki'
    server_pwd = 'Secure@2023'
    server_ip = '192.168.1.5' 
    data_sheet_name