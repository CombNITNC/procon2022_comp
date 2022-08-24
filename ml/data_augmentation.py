import tensorflow as tf
from tf.keras import layers

factor_data = (-0.2, 0.2)


def data_augmentation():
    sample_data_augmentation = tf.keras.Sequential([
        layers.RandomTranslation(height_factor=(
            0, 0), width_factor=(-0.5, 0.5)),
        layers.RandomBrightness(value_range=(0.0, 1.0), factor=factor_data),
        layers.RandomContrast(factor=factor_data)
    ])
    return sample_data_augmentation
