from datetime import datetime as dt
from dateutil import relativedelta
from ftplib import FTP
import pandas as pd
import os
# add ask and sql functions here.


class AddUpdate:

    def today():
        today = dt.now().strftime("%Y_%m_%d")
        return today 

    def output_op_status(old_file, op, status):
        if status:
            status = 'success'
            print(old_file, op, status)
        else:
            status = 'failed'
            print(old_file, op, status)
        return status


class AskYN:

    def get_days_interval(date_first, date_second, date_format='%d.%m.%Y'):
        days_interval = 'zero'
        if date_first == 'NA' or date_second == 'NA':
            days_interval = 'NA'
        elif date_first != date_second:
            first = dt.strptime(date_first, date_format)
            second = dt.strptime(date_second, date_format)
            days_interval = (second-first).days
        return days_interval


    def get_calender_interval(date_first, date_second, date_format='%d.%m.%Y'):
        days, years, months = ['NA', ] * 3
        if date_first != date_second:
            first = dt.strptime(date_first, date_format)
            second = dt.strptime(date_second, date_format)
            delta_day = relativedelta.relativedelta(second-first)
            days = (second-first).days
            months = round(delta_day.months +
                        (delta_day.years*12) + (delta_day.days/30), ndigits=2)
            years = round(delta_day.years + (delta_day.months/12) +
                        (delta_day.days/365), ndigits=2)
        return dict(days=str(days), months=str(months), years=str(years))
       
    def op_status_dict(file_name, op_type, op_name, user_name, status_op):
        status_label = op_type + '_status'
        time_label = op_type + '_time'
        update_label = user_name + '_by'
        status_dict = {
            'file_name': file_name,
            status_label: AddUpdate.output_op_status(old_file=file_name, 
                                                     op=op_name,
                                                     status=status_op),
            time_label: AddUpdate.today(),
            update_label: user_name
            }
        return status_dict


class FtpFileFunctions:
    
    def __init__(self, ftp_ip, user, pwd, destination_path):
        self.ftp_ip = ftp_ip
        self.user = user
        self.pwd = pwd
        # self.destination_path = destination_path

    def ftp_connect(self):
        ftp = FTP(self.ftp_ip)
        ftp.login(user=self.user, passwd=self.pwd)
        # ftp.cwd(self.destination_path)
        return ftp
    
    # def ftp_get_file_list(ftp):
    #     dirs = ftp.nlst()
    #     return dirs
    
    def ftp_download_files(self, file_names):
        ftp = self.ftp_connect()
        downloads = pd.DataFrame(dict)
        download = False
        for file_name in file_names:
            filename = os.path.basename(file_name)
            local_filename = os.path.join('tmp/', file_name)
            try:
                with open(local_filename, 'wb') as f:
                # Define the callback as a closure so it can access 
                # the opened file in local scope
                    def callback(data):
                        f.write(data)
                    ftp.retrbinary('RETR %s' % filename, callback)
                    print("file " + file_name + " downloaded successfully!")
                    download = True
            except ValueError:
                print("file " + file_name + " not downloaded!")
            downloads = pd.concat([downloads, pd.DataFrame({
                    'file_name':file_name, 'download' : download})])
        return downloads
        
    def ftp_upload(self, file_name):
        ftp = self.ftp_connect()
        try: 
            ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))
            print('file ' + file_name + ' uploaded successfully!')
            return True
        except:
            print('file ' + file_name + ' not uploaded!')
        ftp.close()
        return False
        
    def ftp_disconnect(ftp):
        print('ftp connection closed!')