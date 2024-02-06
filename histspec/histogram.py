import numpy as np

def normalize_histogram(hist):
    '''
    Normalisasikan histogram. Hasil fungsi ini adalah histogram
    dengan nilai rentang 0 hingga 1.

    Argumen:
        hist (numpy.ndarray): Histogram citra
    Hasil:
        Histogram yang dinormalisasikan
    '''
    return np.asarray(hist) / np.sum(hist)

def create_transformer_histogram(hist, L=256):
    '''
    Membuat fungsi transformasi untuk ekualisasi histogram.

    Argumen:
        hist (numpy.ndarray): Histogram citra
    Hasil:
        s (numpy.ndarray): Transformer nilai piksel
    '''
    norm_hist = normalize_histogram(hist)
    s = (L - 1) * np.cumsum(norm_hist)
    
    return s.round().astype(int)

def create_histogram_matching(in_hist, out_hist, L=256):
    '''
    Buat fungsi transformasi dari histogram masukan dengan histogram
    yang diinginkan.

    Argumen:
        in_hist (numpy.ndarray): Histogram citra masukkan
        out_hist (numpy.ndarray): Histogram citra yang diinginkan
        L (int): Tingkat intentitas piksel
    Hasil:
        Transformer nilai piksel
    '''
    s = create_transformer_histogram(in_hist, L)
    G = create_transformer_histogram(out_hist, L)

    diff = np.abs(s[:, np.newaxis] - G)

    return np.argmin(diff, axis=1)
