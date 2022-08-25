from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten


def neural_voice_judgment_model():
    model = Sequential()

    model.add(Conv2D(8, (5, 5), activation='relu', input_shape=(
        128, 128, 1), output_shape=(124, 124, 8)))
    model.add(MaxPooling2D(pool_size=(2, 2), output_shape=(62, 62, 8)))
    model.add(Conv2D(16, (5, 5), activation='relu', output_shape=(58, 58, 16)))
    model.add(MaxPooling2D(pool_size=(2, 2), output_shape=(29, 29, 16)))
    model.add(Conv2D(100, (5, 5), activation='relu', output_shape=(25, 25, 100)))
    model.add(MaxPooling2D(pool_size=(2, 2), output_shape=(12, 12, 100)))
    model.add(Conv2D(200, (5, 5), activation='relu', output_shape=(8, 8, 200)))
    model.add(MaxPooling2D(pool_size=(2, 2), output_shape=(4, 4, 200)))
    model.add(Flatten())
    model.add(Dense(17424), activation='relu')
    model.add(Dense(1024), activation='relu')
    model.add(Dense(500), activation='relu')
    model.add(Dense(44), activation='softmax')

    return model
