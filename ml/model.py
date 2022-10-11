from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, BatchNormalization


def neural_voice_judgment_model():
    model = Sequential()

    model.add(BatchNormalization())
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
    model.add(Dense(44))

    return model
