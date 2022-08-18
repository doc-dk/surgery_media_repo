import cv2
from PIL import Image
import fitz
import os
import cv2
import pyqrcode

scanned_file_path = 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/path_reports/surgery_histopah/98_19/prem_sharma_2019_05_01_radical.pdf'
qr_path = 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/path_reports/qr_codes/98_19_Surgery Pathology.png'

# img = Image.open(qr_path)
# pdf = img.convert('RGB')
# pdf.save('D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_codes/07_19_Patient_File_Data.pdf')
#
# rgba = Image.open(qr_path)
# rgb = Image.new('RGB', rgba.size, (255, 255, 255))
# rgb.paste(rgba)
# rgb.save(scanned_file_path, 'PDF', resoultion=100.0)

# add_pdf_to_pdf('07_19', scanned_file_path, 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_codes/07_19_Patient File Data.pdf',
#                 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_codes/added_qr_code')

# add_png_to_doc_convert_to_pdf('07_19_Patient File Data.png', 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_codes',
#                                'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_codes')
##


input_pdf = 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_on_the_first_page/surgery_histopath/prem_sharma_2019_05_01_radical.pdf'
output_file = 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_on_the_first_page/added_qr_code/2022_07_16_98_19_location_trial.pdf'
qr_code = 'D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_on_the_first_page/qr_codes/98_19_Surgery Pathology.png'

# image_rectangle = fitz.Rect(21,20,121,120)
# image_rectangle.is_empty
# # image_rectangle = fitz.Rect(450,20,550,120)
# file_handle = fitz.open(input_pdf)
# first_page = file_handle[0]
# qr_code = open(qr_code)
# first_page.insert_image(image_rectangle, filename=qr_code)
# file_handle.save(output_file)

##

# image_rectangle = fitz.Rect(1,2,101,102)
# image_rectangle.is_empty
# # image_rectangle = fitz.Rect(450,20,550,120)
# file_handle = fitz.open(input_pdf)
# first_page = file_handle[0]
# qr_code = open(qr_code)
# qr_code = qr_code.resize((50, 50))
# qr_code.save('D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_on_the_first_page/qr_codes/98_19_Surgery Pathology_resized.png')
# qr_code = open('D:/Shweta/data_digitization/adding_qr_code_in_pdf/qr_on_the_first_page/qr_codes/98_19_Surgery Pathology_resized.png')

# first_page.insert_image(image_rectangle, filename=qr_code)
# file_handle.save(output_file)

def make_qr_code(file_number, id_data, qr_dir):
    file_number_str = file_number.replace("/", "_")
    # qr_code_dat = str(file_number_str) + '_' + '_'.join(str(id_text) for id_text in (id_dat[0:1] + folder))
    qr_code_lst = [file_number_str] + id_data
    qr_code_dat = ' '.join(str(id_text) for id_text in qr_code_lst)
    qr_img = pyqrcode.create(qr_code_dat)
    qr_img_path = os.path.join(qr_dir, 'qr_img.png')
    qr_img.png((qr_img_path), scale=4)
    return qr_img_path, qr_code_lst

def add_the_qr_code_at_top(input_pdf_path, qr_path, output_pdf_path):
    image_rectangle = fitz.Rect(10, 20, 110, 120)
    # image_rectangle = fitz.Rect(450,20,550,120)
    file_handle = fitz.open(input_pdf_path)
    first_page = file_handle[0]
    qr_code = open(qr_path)
    first_page.insert_image(image_rectangle, filename=qr_code)
    file_handle.save(output_pdf_path)
    print('added_qr_code_at_the_top_of_the_pdf')

def attach_qr_code_on_scanned_file(scanned_file_folder, qr_code_folder, added_qr_code_folder):
    qr_file_lst = os.listdir(qr_code_folder)
    for file in qr_file_lst:
        scanned_file_path = os.path.join(scanned_file_folder, file + '.pdf')
        qr_folder = os.path.join(qr_code_folder, file)
        file_dat_qr = os.path.join(qr_folder, file+'_Patient File Data.png')
        output_file = os.path.join(added_qr_code_folder, file + '.pdf')
        add_the_qr_code_at_top(scanned_file_path, file_dat_qr, output_file)

def read_qr_code_data(qr_path):
    qr_img = cv2.imread(qr_path)
    detect = cv2.QRCodeDetector()
    value, points, qr_code = detect.detectAndDecode(qr_img)
    return value


read_qr_code_data(qr_code)
