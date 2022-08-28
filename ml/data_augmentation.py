import tensorflow as tf
from keras import layers


def data_augmentation():
    sample_data_augmentation = tf.keras.Sequential([
        layers.RandomTranslation(height_factor=(
            0, 0), width_factor=(-0.5, 0.5)),
        layers.RandomContrast(factor=0.2)
    ])
    return sample_data_augmentation
