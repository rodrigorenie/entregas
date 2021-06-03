import numpy

from tensorflow import keras


class MnistData:
    TrainData = tuple[numpy.array, numpy.array]
    TestData = tuple[numpy.array, numpy.array]

    @staticmethod
    def dataset_split() -> tuple[TrainData, TestData]:
        dataset = keras.datasets.mnist.load_data()
        (train_i, train_l), (test_i, test_l) = dataset

        train_i = train_i.reshape((60000, 28 * 28))
        train_i = train_i.astype('float32') / 255
        train_l = keras.utils.to_categorical(train_l)

        test_i = test_i.reshape((10000, 28 * 28))
        test_i = test_i.astype('float32') / 255
        test_l = keras.utils.to_categorical(test_l)

        return (train_i, train_l), (test_i, test_l)

    (train_i, train_l), (test_i, test_l) = dataset_split.__func__()
    train = (train_i, train_l)
    test = (test_i, test_l)
