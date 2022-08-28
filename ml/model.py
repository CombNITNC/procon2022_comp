from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from data_augmentation import data_augmentation


def neural_voice_judgment_model():
    model = Sequential()

    model.add(data_augmentation())
    model.add(Conv2D(8, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(16, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(100, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(200, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(17424, activation='relu'))
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(500, activation='relu'))
    model.add(Dense(44, activation='softmax'))

    return model
