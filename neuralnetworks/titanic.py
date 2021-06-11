import dsutils
import pandas
import numpy
import tensorflow

from tensorflow import keras


class TitanicData:
    TrainData = tuple[numpy.array, numpy.array]
    TestData = tuple[numpy.array, numpy.array]

    @staticmethod
    def dataset_split() -> tuple[TrainData, TestData]:
        csv = dsutils.datadir.join('datasets', 'titanic.csv')
        df = pandas.read_csv(csv)
        df = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])

        df['Sex'] = pandas.Categorical(df['Sex']).codes
        df['Embarked'] = pandas.Categorical(df['Embarked']).codes
        df = df.titanic.nona

        dftrain, dftest = df.titanic.split()

        train_i = dftrain.titanic.instances.to_numpy()
        train_i = tensorflow.convert_to_tensor(train_i, dtype=tensorflow.int64)

        train_l = dftrain.titanic.classes.to_numpy()
        train_l = keras.utils.to_categorical(train_l)

        test_i = dftest.titanic.instances.to_numpy()
        test_i = tensorflow.convert_to_tensor(test_i, dtype=tensorflow.int64)

        test_l = dftest.titanic.classes.to_numpy()
        test_l = keras.utils.to_categorical(test_l)

        return (train_i, train_l), (test_i, test_l)

    (train_i, train_l), (test_i, test_l) = dataset_split.__func__()
    train = (train_i, train_l)
    test = (test_i, test_l)


class Titanic:

    def __init__(self):
        network = keras.models.Sequential()
        network.add(keras.layers.Dense(50, activation='relu', input_shape=(7,)))
        network.add(keras.layers.Dense(50, activation='relu'))
        network.add(keras.layers.Dense(2, activation='softmax'))
        network.summary()

        network.compile(optimizer='adam', loss='categorical_crossentropy',
                        metrics=['accuracy'])

        history = network.fit(TitanicData.train_i, TitanicData.train_l,
                              epochs=100,
                              batch_size=128,
                              validation_data=TitanicData.test)

        test_loss, test_acc = network.evaluate(TitanicData.test_i,
                                               TitanicData.test_l)
        print('test_loss: ', test_acc)
        print('test_acc: ', test_acc)
