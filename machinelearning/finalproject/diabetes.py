from __future__ import annotations

import pandas as pd
import numpy as np
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model
import imblearn

from dsutils import DataDir
from typing import Tuple, List, Union


@pd.api.extensions.register_dataframe_accessor("rocket")
class RocketFrame(DataDir):
    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__()
        self._data = data
        self._classnames = []

    def __str__(self) -> str:
        return str(self._data)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def classnames(self) -> List[str]:
        return self._classnames

    @classnames.setter
    def classnames(self, classnames: List[str]) -> None:
        for cls in classnames:
            if cls not in self._data.columns:
                raise ValueError(f"'{cls}' column must exist in the dataframe")
        self._classnames = classnames

    @property
    def classes(self) -> RocketFrame:
        return self.__class__(self.data[self.classnames])

    @property
    def instances(self) -> RocketFrame:
        return self.__class__(self.data.drop(columns=self.classnames))

    @property
    def numericals(self) -> RocketFrame:
        cls = self.classes.data
        num = self.data.select_dtypes(include=np.number)
        num = num.drop(columns=cls.columns, errors='ignore')
        num = num.join(cls)
        num = self.__class__(num)
        num.classnames = cls.columns
        return num

    @property
    def categoricals(self) -> RocketFrame:
        cls = self.classes.data
        cat = self.data.select_dtypes(include=object)
        cat = cat.drop(columns=cls.columns, errors='ignore')
        cat = cat.join(cls)
        cat = self.__class__(cat)
        cat.classnames = cls.columns
        return cat

    @property
    def normalized(self) -> RocketFrame:
        cls = self.classes.data

        num = self.numericals.instances.data
        num_normalizer = sklearn.preprocessing.MinMaxScaler()
        num_cols = num.columns

        num = num_normalizer.fit_transform(num)
        num = pd.DataFrame(num, columns=num_cols)

        cat = self.categoricals.instances.data
        cat = pd.get_dummies(cat) if cat.size > 0 else cat

        data = self.__class__(num.join(cat).join(cls))
        data.classnames = self.classnames
        return data

    @property
    def balanced(self) -> RocketFrame:
        balancer = imblearn.over_sampling.SMOTE()
        instances, classes = self.instances.data, self.classes.data
        instances, classes = balancer.fit_resample(instances, classes)

        data = self.__class__(instances.join(classes))
        data.classnames = self.classnames
        return data






class DiabetesData(DataDir):

    def __init__(self,
                 csvfile: str,
                 csvclasses: List[str] = None,
                 splitsize: float = 0.3) -> None:

        if splitsize > 1 or splitsize < 0:
            raise ValueError("'splitsize' deve ser entre 0 e 1")

        super().__init__()
        csvfile = self.datafilename(csvfile)
        self._data = pd.read_csv(csvfile)

        if csvclasses is None:
            csvclasses = ['class']

        for cls in csvclasses:
            if cls not in self._data.columns:
                raise ValueError(f"'{cls} class must exist in 'csvfile'")

        self.classnames = csvclasses

        self._splitsize = splitsize
        self._datatrain = None
        self._datatest = None
        # self.xtrain, self.xtest, self.ytrain, self.ytest = self.datasplit

        self.normalizer = sklearn.preprocessing.MinMaxScaler()
        self.balancer = imblearn.over_sampling.SMOTE()
        self.model = sklearn.ensemble.RandomForestClassifier()

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def classes(self) -> pd.DataFrame:
        return self.data[self.classnames]

    @property
    def instances(self) -> pd.DataFrame:
        return self.data.drop(columns=self.classnames)

    @property
    def numericals(self) -> pd.DataFrame:
        return self.instances.select_dtypes(include=np.number)

    @property
    def categoricals(self) -> pd.DataFrame:
        return self.instances.select_dtypes(include=object)

    def normalized(self, balance: bool = False) -> pd.DataFrame:
        num = self.numericals
        cat = self.categoricals

        if num.size > 0:
            columns = num.columns
            num = self.normalizer.fit_transform(num)
            num = pd.DataFrame(num, columns=columns)

        if cat.size > 0:
            cat = pd.get_dummies(cat)

        instances = num.join(cat)
        classes = self.classes

        if balance:
            instances, classes = self.balancer.fit_resample(instances, classes)

        return instances.join(classes)




    def numericals2(self,
                   normal: bool = False,
                   balance: bool = False) -> pd.DataFrame:
        data = self.instances.select_dtypes(include=np.number)

        if normal:
            normalizer = sklearn.preprocessing.MinMaxScaler()
            normal = normalizer.fit_transform(data)
            data = pd.DataFrame(normal, columns=data.columns)

        if balance:
            oversample = imblearn.over_sampling.SMOTE()
            x, y = oversample.fit_resample(data, self.classes)
            data = x.join(y)

        return data

    def categoricals2(self,
                     normal: bool = False,
                     balance: bool = False) -> pd.DataFrame:
        data = self.instances.select_dtypes(include=object)

        if normal and data.size > 0:
            data = pd.get_dummies(data)

        if balance and data.size > 0:
            oversample = imblearn.over_sampling.SMOTE()
            x, y = oversample.fit_resample(data, self.classes)
            data = x.join(y)

        return data

    @property
    def normalized2(self) -> pd.DataFrame:
        return self.numericals(normal=True).join(
            self.categoricals(normal=True)
        )

    @property
    def balanced2(self) -> pd.DataFrame:
        return self.numericals(balance=True).join(
            self.categoricals(balance=True)
        )

    @property
    def balancednormal2(self) -> pd.DataFrame:
        return self.numericals(balance=True, normal=True).join(
            self.categoricals(balance=True, normal=True)
        )

    @property
    def split(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if self._datatrain is None or self._datatest is None:
            pass

        balanced = self.balancednormal
        x = balanced.drop(columns=[self.classnames])
        y = balanced[[self.classnames]]

        xtrain, xtest, ytrain, ytest = sklearn.model_selection.train_test_split(
            self.balancednormal, 1, test_size=0.3
        )


class Diabetes(DiabetesData):

    def __init__(self):
        super().__init__('diabetes.csv')
        self.xtrain, self.xtest, self.ytrain, self.ytest = self.split
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
        instances[self.classnames] = result

        for i, name in enumerate(self.model.classes_):
            name = f'{name}_p'
            instances[name] = proba[i]

        self._predict = instances
        return self._predict

    def accuracy(self) -> float:
        return sklearn.metrics.accuracy_score(self.ytest,
                                              self._predict[self.classnames])






