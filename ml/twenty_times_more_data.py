from data_augmentation import data_augmentation
from tensorflow.data import Dataset, AUTOTUNE


def twenty_times_more_data(image, label):
    image_list = []
    for _ in range(20):
        image_processor = data_augmentation()
        image_processed = image_processor(image)
        image_list.append((image_processed, label))
    image_dataset = Dataset.from_tensor_slices(image_list)
    image_dataset.batch(32)
    image_dataset.prefetch(AUTOTUNE)

    return image_dataset
