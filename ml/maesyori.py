import cv2
import numpy as np
import scipy
from librosa import amplitude_to_db, feature, note_to_hz

sr = 48000


def preprocess_input(onsei_data: np.ndarray) -> np.ndarray:

    # プリエンファシスフィルタ:
    # y(t) = x(t) - p x(t - 1)
    p = 0.97
    pre_emphasis = scipy.signal.lfilter([1.0, -p], 1, onsei_data)

    hop_length = int(sr * 10e-3)
    win_length = int(sr / note_to_hz('C3'))
    mel_spectrogram = feature.melspectrogram(
        sr=sr, y=pre_emphasis, hop_length=hop_length, win_length=win_length)
    shrink = cv2.resize(mel_spectrogram, (128, 128))
    mel_non_zero = np.where(shrink == 0,
                            np.finfo(float).eps, shrink)
    common_logarithm = amplitude_to_db(mel_non_zero)
    max_value = common_logarithm.max()
    min_value = common_logarithm.min()
    return (common_logarithm - min_value) / (max_value - min_value)
