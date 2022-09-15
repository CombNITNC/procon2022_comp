import random
from os.path import join
from scipy.io.wavfile import read
import numpy as np
from maesyori import preprocess_input


def waveform_sample_data():
    list_number = list(range(1, 44+1))
    shuffle_list = random.sample(list_number, k=random.randint(3, 5))
    yomidata_list = []
    for use_number in shuffle_list:
        nihongo_use = random.getrandbits(1) == 1
        if nihongo_use:
            yomidata_list.append(f"J{use_number:02}")
        else:
            yomidata_list.append(f"E{use_number:02}")

    waveform_path = []
    for sample in yomidata_list:
        waveform_path.append(join("..", "jk", f"{sample}.wav"))

    waveform_loading = []
    for path in waveform_path:
        waveform_sample, waveform_onsei = read(path)
        waveform_loading.append(waveform_onsei)

    sample_length = 96000
    test_sample = np.zeros(sample_length)
    for waveform_data in waveform_loading:
        cut = random.randrange(0, max(1, len(waveform_data)))
        sliced = np.resize(
            waveform_data[cut:cut + sample_length], sample_length)
        test_sample += sliced
    neural_input_data = preprocess_input(test_sample)

    neural_output = [0.0]*44
    for use_number in shuffle_list:
        neural_output[use_number-1] = 1.0

    return (neural_input_data, neural_output)
