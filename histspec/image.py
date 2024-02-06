import io

import numpy as np
from PIL import Image

from . import histogram

def match_histogram_image(input_img, hist_spec, L=256):
    '''
    Memcocokkan histogram dari citra masukkan dengan histogram yang
    diinginkan.

    Argumen:
        input_img (PIL.Image): Citra masukkan
        hist_spec (numpy.ndarray): Histogram yang diinginkan
        L (int): Tingkat intentitas piksel
    Hasil:
        matched_img (numpy.ndarray): Citra yang sudah dicocokkan
    '''
    mapper = histogram.create_histogram_matching(input_img.histogram(), hist_spec, L)
    
    matched_img = mapper[input_img]

    return matched_img

def create_image(file_bytes):
    '''
    Membuat citra dari nilai bita.

    Argumen:
        file_bytes (bytes): Nilai bita dari file
    Hasil:
        img (PIL.Image): Citra
    '''
    file = io.BytesIO(file_bytes)
    img = Image.open(file)
    return img

def process_image(img, desired_img):
    '''
    Memproses citra masukkan dengan citra yang ingin dicocokkan histogramnya.

    Argumen:
        img (PIL.Image): Citra masukkan
        desired_img (PIL.Image): Citra yang ingin dicocokkan histogramnya
    Hasil:
        result_mem (io.BytesIO): Objek bita.
    '''
    channels = ['R', 'G', 'B']
    rgb_matching_img = []

    for channel in channels:
        rgb_matching_img.append((img.getchannel(channel), desired_img.getchannel(channel).histogram()))

    matched_rgb_img = np.array([match_histogram_image(img, target_hist).T for img, target_hist in rgb_matching_img]).T

    img.close()
    desired_img.close()

    result_mem = io.BytesIO()
    result = Image.fromarray(matched_rgb_img.astype('uint8'), 'RGB')
    result.save(result_mem, format='png')

    return result_mem
