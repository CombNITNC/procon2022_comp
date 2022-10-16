from data_augmentation import data_augmentation
from tensorflow.data import Dataset, AUTOTUNE
import tensorflow
import numpy as np


def twenty_times_more_data(image, label):
    image_processor = data_augmentation()
    expanded_image = image[np.newaxis, :, :]
    expanded_label = label[np.newaxis, :]
    cast_image = tensorflow.cast(expanded_image, tensorflow.float32)
    cast_label = tensorflow.cast(expanded_label, tensorflow.float32)
    image_list = []
    label_list = [cast_label]*20
    for _ in range(20):
        image_processed = image_processor(cast_image)
        image_list.append((image_processed))
    image_label_dataset = Dataset.from_tensor_slices((image_list, label_list))
    image_label_dataset.batch(200)
    image_label_dataset.prefetch(AUTOTUNE)

    return image_label_dataset
