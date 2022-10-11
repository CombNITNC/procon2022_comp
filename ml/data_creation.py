from shuffle_number import waveform_sample_data
import idx2numpy
import numpy as np
from os.path import join

train_label_list = []
train_image_list = []
for train_data in range(5000):
    train_image, train_label = waveform_sample_data()
    train_label_list.append(np.array(train_label))
    train_image_list.append(train_image)
processing_train_label = np.array(train_label_list)
processing_train_image = np.array(train_image_list)
idx2numpy.convert_to_file(
    join("..", "dataset", "train_label.idx"), processing_train_label)
idx2numpy.convert_to_file(
    join("..", "dataset", "train_image.idx"), processing_train_image)

test_label_list = []
test_image_list = []
for test_data in range(1000):
    test_image, test_label = waveform_sample_data()
    test_label_list.append(test_label)
    test_image_list.append(test_image)
processing_test_label = np.array(test_label_list)
processing_test_image = np.array(test_image_list)
idx2numpy.convert_to_file(
    join("..", "dataset", "test_label.idx"), processing_test_label)
idx2numpy.convert_to_file(
    join("..", "dataset", "test_image.idx"), processing_test_image)

validation_label_list = []
validation_image_list = []
for validation_data in range(1000):
    validation_image, validation_label = waveform_sample_data()
    validation_label_list.append(validation_label)
    validation_image_list.append(validation_image)
processing_validation_label = np.array(validation_label_list)
processing_validation_image = np.array(validation_image_list)
idx2numpy.convert_to_file(
    join("..", "dataset", "validation_label.idx"), processing_validation_label)
idx2numpy.convert_to_file(
    join("..", "dataset", "validation_image.idx"), processing_validation_image)
