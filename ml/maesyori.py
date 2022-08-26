import random

import numpy as np
import scipy
from librosa import amplitude_to_db, feature, note_to_hz

sr = 48000


def preprocess_input(onsei_data: np.ndarray) -> np.ndarray:
    slice_len = int(sr * 1.27)
    kiritori = random.randrange(0, max(1, len(onsei_data) - slice_len))
    sliced = np.resize(onsei_data[kiritori:kiritori+slice_len], slice_len)

    # プリエンファシスフィルタ:
    # y(t) = x(t) - p x(t - 1)
    p = 0.97
    pre_emphasis = scipy.signal.lfilter([1.0, -p], 1, sliced)

    hop_length = int(sr * 10e-3)
    win_length = int(sr / note_to_hz('C3'))
    mel_spectrogram = feature.melspectrogram(
        sr=sr, y=pre_emphasis, hop_length=hop_length, win_length=win_length)
    mel_non_zero = np.where(mel_spectrogram == 0,
                            np.finfo(float).eps, mel_spectrogram)
    common_logarithm = amplitude_to_db(mel_non_zero)
    max_value = common_logarithm.max()
    min_value = common_logarithm.min()
    return (common_logarithm - min_value) / (max_value - min_value)
