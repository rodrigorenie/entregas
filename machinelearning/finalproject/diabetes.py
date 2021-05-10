import pandas as pd
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model
import os

from dsutils import DataDir


class Diabetes(DataDir):

    def __init__(self, csvfile: str = 'diabetes.csv') -> None:
        super().__init__()
        self.df = pd.read_csv(os.path.join(self.datadir, csvfile))
        self.df.rocket.classcols = ['class']
        self.train, self.test = self.df.rocket.normalized.balanced.split(0.3)

        self._model = None
        self._predict = None

    @property
    def model(self):
        if self._model is None:
            x = self.train.instances.df
            y = self.train.classes.df.values.ravel()

            model = sklearn.ensemble.RandomForestClassifier()
            # model = sklearn.ensemble.AdaBoostClassifier()
            # model = sklearn.ensemble.BaggingClassifier()
            # model = sklearn.ensemble.GradientBoostingClassifier()
            # model = sklearn.linear_model.LogisticRegression()
            # model = sklearn.linear_model.LogisticRegressionCV()

            self._model = model.fit(x, y)

        return self._model

    def predict(self, instances: pd.DataFrame = None) -> pd.DataFrame:
        if instances is None:
            instances = self.test.instances.df

        classcols = self.df.rocket.classcols
        predict = pd.DataFrame(self.model.predict(instances), columns=classcols)
        proba = self.model.predict_proba(instances).T
        instances = instances.join(predict)

        for i, name in enumerate(self.model.classes_):
            instances[f'{name}_p'] = proba[i]

        return instances

    def accuracy(self) -> float:
        return sklearn.metrics.accuracy_score(self.ytest,
                                              self._predict[self.classnames])






