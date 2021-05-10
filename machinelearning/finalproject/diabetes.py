import pandas as pd
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model
import os

from dsutils import DataDir
from typing import Any, Iterable, Tuple


class Diabetes(DataDir):

    def __init__(self, csvfile: str = 'diabetes.csv') -> None:
        super().__init__()
        self.df = pd.read_csv(os.path.join(self.datadir, csvfile))
        self.df.rocket.classcols = ['class']
        self.train, self.test = self.df.rocket.normalized.balanced.split(0.7)

        self._model = None
        self._modellist = []
        self._predict = None

        self.registermodel(sklearn.ensemble.RandomForestClassifier)
        self.registermodel(sklearn.ensemble.AdaBoostClassifier)
        self.registermodel(sklearn.ensemble.ExtraTreesClassifier)
        self.registermodel(sklearn.ensemble.GradientBoostingClassifier)

    @staticmethod
    def validmodel(model: Any) -> None:
        methods = ['fit', 'predict', 'predict_proba']
        if not all(meth in dir(model) for meth in methods):
            raise ValueError(f'{model.__qualname__} deve conter os métodos '
                             f'{methods}')

    def registermodel(self, model: Any) -> None:
        Diabetes.validmodel(model)
        self._modellist.append(model)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: Any) -> None:
        Diabetes.validmodel(model)

        x = self.train.instances.df
        y = self.train.classes.df.values.ravel()

        self._model = model().fit(x, y)

    def predict(self, instances: pd.DataFrame = None) -> pd.DataFrame:
        if instances is None:
            instances = self.test.instances.df

        classcols = self.df.rocket.classcols
        predict = pd.DataFrame(self.model.predict(instances), columns=classcols)
        proba = self.model.predict_proba(instances).T
        instances = instances.join(predict)
        instances.rocket.classcols = self.df.rocket.classcols

        for i, name in enumerate(self.model.classes_):
            instances[f'{name}_p'] = proba[i]

        return instances

    def accuracy(self) -> Iterable[Tuple[str, float]]:
        x = self.test.instances.df
        y = self.test.classes.df

        for model in self._modellist:
            self.model = model
            yield self.model, self.model.score(x, y)








