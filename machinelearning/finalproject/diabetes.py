import pandas as pd
import numpy as np
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model
import imblearn

from dsutils import DataDir
from typing import Tuple


class DiabetesData(DataDir):

    def __init__(self, csvfile: str, classname: str = 'class') -> None:
        super().__init__()
        csvfile = self.datafilename(csvfile)
        self._fulldata = pd.read_csv(csvfile)

        if classname not in self._fulldata.columns:
            raise ValueError(f"'{classname}' must exist in '{csvfile}'")

        self.classname = classname

    @property
    def datafull(self) -> pd.DataFrame:
        return self._fulldata

    @property
    def data(self) -> pd.DataFrame:
        return self.datafull.drop(columns=[self.classname])

    @property
    def dataclass(self) -> pd.DataFrame:
        return self.datafull[[self.classname]]

    @property
    def datanum(self) -> pd.DataFrame:
        normalizer = sklearn.preprocessing.MinMaxScaler()
        data = self.data.select_dtypes(include=np.number)
        normal = normalizer.fit_transform(data)
        return pd.DataFrame(normal, columns=data.columns)

    @property
    def datacat(self) -> pd.DataFrame:
        data = self.data.select_dtypes(include=object)
        data = pd.get_dummies(data) if data.size > 0 else data
        return data

    @property
    def datanormal(self) -> pd.DataFrame:
        return self.datanum.join(self.datacat)

    @property
    def datafullbalanced(self) -> pd.DataFrame:
        oversample = imblearn.over_sampling.SMOTE()
        x, y = oversample.fit_resample(self.datanormal, self.dataclass)
        return x.join(y)

    @property
    def datasplit(self) -> Tuple[pd.DataFrame, pd.DataFrame,
                                 pd.DataFrame, pd.DataFrame]:
        balanced = self.datafullbalanced
        x = balanced.drop(columns=[self.classname])
        y = balanced[[self.classname]]
        return sklearn.model_selection.train_test_split(x, y, test_size=0.3)


class Diabetes(DiabetesData):

    def __init__(self):
        super().__init__('diabetes.csv')
        self.xtrain, self.xtest, self.ytrain, self.ytest = self.datasplit
        self.ytrain = self.ytrain.values.ravel()

        self._model = None
        self._predict = None

        print(self.predict().iloc[:, -4:])

    @property
    def model(self):
        if self._model is None:
            # model = sklearn.ensemble.RandomForestClassifier()
            model = sklearn.ensemble.AdaBoostClassifier()
            # model = sklearn.ensemble.BaggingClassifier()
            # model = sklearn.ensemble.GradientBoostingClassifier()
            # model = sklearn.linear_model.LogisticRegression()
            # model = sklearn.linear_model.LogisticRegressionCV()
            model.fit(self.xtrain, self.ytrain)
            self._model = model
        return self._model

    def predict(self, instances: pd.DataFrame = None) -> pd.DataFrame:
        if instances is None:
            instances = self.xtest

        result = self.model.predict(instances)
        proba = self.model.predict_proba(instances)
        proba = proba.T
        instances[self.classname] = result

        for i, name in enumerate(self.model.classes_):
            name = f'{name}_p'
            instances[name] = proba[i]

        self._predict = instances
        return self._predict

    def accuracy(self) -> float:
        return sklearn.metrics.accuracy_score(self.ytest,
                                              self._predict[self.classname])






