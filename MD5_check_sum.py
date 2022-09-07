import hashlib
import os
import shutil

from PIL import Image

img_path = 'D:/Shweta/Surgery/surgery_media/tmp/12sep18 pre op & Sx/IMG_1998.jpg'
# hashlib.md5(img_path)

md5hash = hashlib.md5(Image.open(img_path).tobytes())
print(md5hash.hexdigest())


class Md5CheckSum():

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def get_file_names_list(self):
        files = os.listdir(self.source)
        return files

    def make_file_path(self, file_name):
        file_path = os.path.join(self.source, file_name)
        return file_path

    @staticmethod
    def get_hash_value_of_img(img_path):
        md5hash = hashlib.md5(Image.open(img_path).tobytes())
        return md5hash

    def copy_image_from_source_to_destination(self, img_name):
        source_img_path = os.path.join(self.source, img_name)
        destination_img_path = os.path.join(self.destination, img_name)
        shutil.copy(source_img_path, destination_img_path)

def get_unique_images():
    md5 = Md5CheckSum(source='D:/Shweta/Surgery/surgery_media/md5/source/trial',
                      destination='D:/Shweta/Surgery/surgery_media/md5/destination/md5_v1')

    files = md5.get_file_names_list()
    hash_value_list = []
    for file in files:
        file_path = md5.make_file_path(file_name=file)
        hash_value = md5.get_hash_value_of_img(file_path)
        if not hash_value in hash_value_list:
            hash_value_list.append(hash_value)





