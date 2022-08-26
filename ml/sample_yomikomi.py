import yaml
import os
import tensorflow as tf
from itertools import product
from maesyori import preprocess_input
from os.path import join
from scipy.io.wavfile import read
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def sample_data(question_sub_dir):

    with open(join("..", "sample", question_sub_dir, "information.txt"), encoding="utf-8") as sample_file:
        parsed = yaml.load(sample_file, Loader=Loader)
        seikai_parsed_split = parsed["speech"].split(",")
        nsplit = parsed["nsplit"]

    bunkatu_list = []

    for sample in range(1, nsplit+1):
        sample_bunkatu = join("..", "sample", question_sub_dir,
                              f"problem{sample}.wav")
        _rate, bunkatu_onsei = read(sample_bunkatu)
        bunkatu_graph = preprocess_input(bunkatu_onsei)
        bunkatu_list.append(bunkatu_graph)

    seikai_list = []

    for seikai_split in seikai_parsed_split:
        seikai_parsed_number = int(seikai_split[1:])
        seikai_list.append(seikai_parsed_number-1)

    seikai_tf = tf.keras.utils.to_categorical(seikai_list, num_classes=44)

    seikai_data = seikai_tf

    pair_data = list(product(bunkatu_list, seikai_data))

    return pair_data


def sample_all_data():

    sample_pair_data = []
    for sample_dir in os.listdir(join("..", "sample")):
        if os.path.isdir(join("..", "sample", sample_dir)):
            sample_pair_list = sample_data(sample_dir)

            sample_pair_data += sample_pair_list

    return sample_pair_data
