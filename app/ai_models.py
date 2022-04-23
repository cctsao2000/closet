'''
This file contains all AI models and all relevant classes or methods.
'''

from pathlib import Path

import numpy as np
import tensorflow as tf

from django.conf import settings


def _load_pretrained_AI_model(pb_file_path):

    model = tf.keras.models.load_model(Path(settings.BASE_DIR, 'app', 'pretrained_ai_models', pb_file_path))

    return model


class Classifier():

    RESULT = {
        0 : "T-shirt/top",
        1 : "Trouser",
        2 : "Pullover",
        3 : "Dress",
        4 : "Coat",
        5 : "Sandal",
        6 : "Shirt",
        7 : "Sneaker",
        8 : "Bag",
        9 : "Ankle boot"
    }

    def __init__(self):
        self.model = _load_pretrained_AI_model('my_dnn_model')

    def predict(self, image_file_path):
        image = tf.keras.preprocessing.image.load_img(
            image_file_path,
            target_size=(28, 28),
            color_mode = "grayscale"
        )
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr /= 255
        input_arr = np.array([input_arr])  # Convert single image to a batch.
        predict = np.argmax(self.model.predict(input_arr), axis=-1)
        predict_result = self.RESULT[predict[0]]

        return predict_result

if __name__ == '__main__':
    #
    # import numpy as np
    # import matplotlib.pyplot as plt
    # import tensorflow as tf
    #
    # from tensorflow.keras.utils import to_categorical
    # from tensorflow.keras.models import Sequential
    # from tensorflow.keras.layers import Conv2D
    # from tensorflow.keras.layers import MaxPooling2D
    # from tensorflow.keras.layers import Dropout
    # from tensorflow.keras.layers import Dense
    # from tensorflow.keras.layers import Flatten
    # from tensorflow.keras.optimizers import SGD
    #
    # from tensorflow.keras.datasets import fashion_mnist
    # (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
    #
    # x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))/255
    # x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))/255
    # y_train = to_categorical(y_train)
    # y_test = to_categorical(y_test)
    #
    # model = Sequential()
    # model.add(
    #     Conv2D(
    #         32,
    #         kernel_size=(3, 3),
    #         activation="relu",
    #         kernel_initializer="he_normal",
    #         input_shape=(28,28,1),
    #     )
    # )
    # model.add(MaxPooling2D((2, 2)))
    # model.add(Dropout(0.25))
    # model.add(Conv2D(64, (3, 3), activation="relu"))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Dropout(0.25))
    # model.add(Conv2D(128, (3, 3), activation="relu"))
    # model.add(Dropout(0.4))
    # model.add(Flatten())
    # model.add(Dense(128, activation="relu"))
    # model.add(Dropout(0.3))
    # model.add(Dense(10, activation="softmax"))
    #
    # model.compile(
    #     loss=tf.keras.losses.categorical_crossentropy,
    #     optimizer=tf.keras.optimizers.Adam(),
    #     metrics=["accuracy"]
    # )
    #
    # model.fit(x_train, y_train, batch_size=256, epochs=10)
    #
    # model.save(Path('pretrained_ai_models', 'my_dnn_model'))

    model = tf.keras.models.load_model(Path('pretrained_ai_models', 'my_dnn_model'))
    model.summary()
    print('done')
    import sys
    sys.exit()


