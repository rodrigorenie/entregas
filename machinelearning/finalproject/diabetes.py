import pandas as pd
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model

from dsutils import DataDir
from typing import Any, Iterable, Tuple


class Diabetes:

    def __init__(self, csvfile: str = 'diabetes.csv') -> None:
        self._df = pd.read_csv(DataDir.join(csvfile))
        self._df.rocket.classcols = ['class']
        self._supported_models = []

        self.model = sklearn.ensemble.RandomForestClassifier
        self.registermodel(sklearn.ensemble.ExtraTreesClassifier)
        self.registermodel(sklearn.ensemble.AdaBoostClassifier)
        self.registermodel(sklearn.ensemble.GradientBoostingClassifier)

    @staticmethod
    def validmodel(model: Any) -> None:
        methods = ['fit', 'predict', 'predict_proba']
        if not all(meth in dir(model) for meth in methods):
            raise ValueError(f'{model.__qualname__} deve conter os métodos '
                             f'{methods}')

    @property
    def df(self):
        return self._df

    @property
    def testdf(self):
        return self.df.rocket

    @property
    def model(self) -> Any:
        return self._model

    @model.setter
    def model(self, model: Any) -> None:
        Diabetes.validmodel(model)
        if model not in self._supported_models:
            self._supported_models.append(model)

        x = self.df.rocket.train.instances.df
        y = self.df.rocket.train.classes.df.values.ravel()
        self._model = model().fit(x, y)

    def __str__(self):
        name = self.__class__.__qualname__
        model = self.model.__class__.__qualname__
        return f'Classe {name}() <Modelo {model}()>'

    def registermodel(self, model: Any) -> None:
        Diabetes.validmodel(model)
        if model not in self._supported_models:
            self._supported_models.append(model)

    def predict(self, instances: pd.DataFrame) -> pd.DataFrame:
        classcols = self.df.rocket.classcols
        predict = pd.DataFrame(self.model.predict(instances), columns=classcols)
        proba = self.model.predict_proba(instances).T

        instances = instances.join(predict)
        instances.rocket.classcols = self.df.rocket.classcols

        for i, name in enumerate(self.model.classes_):
            instances[f'{name}_p'] = proba[i]

        return instances

    def accuracy(self) -> Iterable[Tuple[str, float]]:
        x = self.df.rocket.test.instances.df
        y = self.df.rocket.test.classes.df

        for model in self._supported_models:
            self.model = model
            yield self.model, self.model.score(x, y)








