import random
import scipy.signal
from librosa import cqt, feature
import numpy as np


def preprocess_input(onsei_data):
    kiritori = random.randrange(0, len(onsei_data),)
    slice_len = 1800
    sliced = onsei_data[kiritori:kiritori+slice_len]
    sliced.resize(slice_len)

    # プリエンファシスフィルタの数式
    # y(t) = x(t) - p x(t - 1)
    p = 0.97
    pre_emphasis = (scipy.signal.lfilter([1.0, -p], 1, sliced), p)

    sr = 48000
    hop_length = sr*10e-3
    fmin = 1/10e-3
    spectrum = cqt(pre_emphasis, sr=sr, fmin=fmin, hop_length=hop_length)
    mel_spectrogram = feature.melspectrogram(sr=sr, S=spectrum)
    mel_non_zero = np.where(mel_spectrogram == 0,
                            np.finfo(float).eps, mel_spectrogram)
    common_logarithm = np.log10(mel_non_zero)*20
    average = np.mean(common_logarithm, axis=0)
    average_eps = average + np.finfo(float).eps
    return mel_non_zero - average_eps
