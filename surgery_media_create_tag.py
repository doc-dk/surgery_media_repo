import re
from pccm_db_functions import AddUpdate as sql
from pccm_db_functions import AskYN as ask
from pccm_db_functions import SurgeryLists
from pccm_db_functions import PCCMNamesDict as names
import pandas as pd
import os

class SurgeryTable:

    def __init__(self, conn, user_name):
    # , key_dict_entry):
        self.conn = conn
        self.user_name = user_name
        # self.key_dict_entry = key_dict_entry
        # self.surgery_date = key_dict_entry.get('surgery_date')
        # self.file_number = key_dict_entry.get('file_number')
        # self.lesion_location = key_dict_entry.get(
        #     'surgery_lesion_location')


    def read_surgery_media_datasheet(self, data_sheet_name):
        df = pd.read_excel(os.path.join('tmp', 'input_docs', data_sheet_name))
        for row in df:
            sx_date = row.surgery_date
            img_date = row.image_date
            img_interval = ask.get_days_interval(sx_date, img)
            if abs(img_interval) > 329:
                image_label = str(
                    round(img_interval/365, ndigits=2)) +\
                    '_years_from_surgery'
            elif abs(img_interval) > 90:
                image_label = str(
                    round(img_interval/30, ndigits=1)) +\
                    '_months_from_surgery'
            else:
                image_label = str(img_interval) + '_days_from_surgery'
            surgery_media_tag = '|'.join([
                re.sub('/', '_', row.file_number),
                re.sub('\.', '_', row.surgery_date), row.surgery_media,
                row.surgery_media_type_detail,
                str(image_label)])
            return surgery_media_tag


    def create_db_entry(self, surgery_media_tag):
        det = str.split(surgery_media_tag, '\\|')
        file_number, surgery_date, surgery_media, surgery_media_type_detail, image_label = det
        surgery_date = re.sub('_', '\.', surgery_date)
        image_interval = str.split()
        dat_dict = dict(
            file_number = file_number,
            surgery_media_type=surgery_media,
            surgery_media_type_details=surgery_media_type_detail,
            image_date=image_date,
            image_interval=str(image_interval),
            image_label=image_label,
            surgery_media_name=surgery_media_name,
            primary_server_location=primary_server_location)
        check = sql.review_input_dict(self.file_number, dat_dict)
        sql.add_update(self.conn, table='surgery_media', key_dict_entry=key_dict_entry, col_dict=dat_dict,
                       user_name=self.user_name)
        surgery_media_detail = '; '.join([
            surgery_media_type_detail, surgery_media_tag])
        dat = dict(surgery_media=surgery_media_detail)


    def get_surgery_media(self, surgery_media, past_date_check):
        check = False
        while not check:
            image_date = self.surgery_date
            if surgery_media.startswith('post'):
                past_date_check = True
            elif surgery_media.startswith('pre'):
                past_date_check = False
            else:
                past_date_check = None
            if past_date_check is not None:
                image_date = ask.check_date_chron(
                    date_string='Enter date for ' + surgery_media + ': ',
                    date_ref=self.surgery_date,
                    date_ref_name='surgery_date',
                    past_date_check=past_date_check
                )
            surgery_media_type_detail = ask.ask_list(
                'Please entery type of ' + surgery_media + ': ',
                choices=SurgeryLists.media_types.get(surgery_media))
            image_interval = ask.get_days_interval(
                self.surgery_date, image_date)
            if image_interval == 'NA':
                image_label = re.sub(
                    '\.', '_', self.surgery_date) + '_surgery_date'
            elif isinstance(image_interval, str):
                image_label = re.sub(
                    '\.', '_', self.surgery_date) + '_surgery_date'
            elif abs(image_interval) > 329:
                image_label = str(
                    round(image_interval/365, ndigits=2)) +\
                    '_years_from_surgery'
            elif abs(image_interval) > 90:
                image_label = str(
                    round(image_interval/30, ndigits=1)) +\
                    '_months_from_surgery'
            else:
                image_label = str(image_interval) + '_days_from_surgery'
            primary_server_location = input('server_location: ')
            surgery_media_tag = '|'.join([
                re.sub('/', '_', self.file_number),
                re.sub('\.', '_', self.surgery_date), surgery_media,
                surgery_media_type_detail,
                str(image_label)])
            surgery_media_name = surgery_media_tag
            # number_files, server_location = copy_media()
            dat_dict = dict(
                surgery_media_type=surgery_media,
                surgery_media_type_details=surgery_media_type_detail,
                image_date=image_date,
                image_interval=str(image_interval),
                image_label=image_label,
                surgery_media_name=surgery_media_name,
                primary_server_location=primary_server_location)
            check = sql.review_input_dict(self.file_number, dat_dict)
        sql.add_update(self.conn, table='surgery_media', key_dict_entry=key_dict_entry, col_dict=dat_dict,
                       user_name=self.user_name)
        surgery_media_detail = '; '.join([
            surgery_media_type_detail, surgery_media_tag])
        dat = dict(surgery_media=surgery_media_detail)
        return dat