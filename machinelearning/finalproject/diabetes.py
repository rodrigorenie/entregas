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
class RocketFrame:
    def __init__(self, df: pd.DataFrame, classcols: List[str] = []) -> None:
        self._df = df
        self._dftrain = None
        self._dftest = None
        self._classcols = classcols

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def __str__(self) -> str:
        return str(self.df)

    @property
    def classcols(self) -> List[str]:
        return self._classcols

    @classcols.setter
    def classcols(self, classcols: List[str]) -> None:
        for col in classcols:
            if col not in self.df.columns:
                raise ValueError(f"'{col}' column must exist in the dataframe")
        self._classcols = classcols

    @property
    def classes(self) -> RocketFrame:
        cols = self.df.columns.difference(self.classcols)
        df = self.df.drop(cols, 1)
        return self.__class__(df, self.classcols)

    @property
    def instances(self) -> RocketFrame:
        df = self.df.drop(columns=self.classcols, errors='ignore')
        return self.__class__(df, self.classcols)

    @property
    def numericals(self) -> RocketFrame:
        df = self.df.select_dtypes(include=np.number)
        df = df.drop(columns=self.classcols, errors='ignore')
        df = df.join(self.classes.df)
        return self.__class__(df, self.classcols)

    @property
    def categoricals(self) -> RocketFrame:
        df = self.df.select_dtypes(include=object)
        df = df.drop(columns=self.classcols, errors='ignore')
        df = df.join(self.classes.df)
        return self.__class__(df, self.classcols)

    @property
    def normalized(self) -> RocketFrame:
        normalizer = sklearn.preprocessing.MinMaxScaler()

        dfcat = self.categoricals.instances.df
        dfcat = pd.get_dummies(dfcat) if dfcat.size > 0 else dfcat
        dfcat = dfcat.join(self.classes.df)

        df = self.numericals.instances.df
        df = pd.DataFrame(normalizer.fit_transform(df), columns=df.columns)

        return self.__class__(df.join(dfcat), self.classcols)

    @property
    def balanced(self) -> RocketFrame:
        balancer = imblearn.over_sampling.SMOTE()
        dfinst, dfclass = self.instances.df, self.classes.df
        dfinst, dfclass = balancer.fit_resample(dfinst, dfclass)
        return self.__class__(dfinst.join(dfclass), self.classcols)

    def split(self, size: float = 0.7) -> Tuple[RocketFrame, RocketFrame]:
        x = self.instances.df
        y = self.classes.df
        c = self.classcols

        split = sklearn.model_selection.train_test_split(x, y, test_size=size)
        x_train, x_test, y_train, y_test = split

        train = x_train.join(y_train).reset_index(drop=True)
        test = x_test.join(y_test).reset_index(drop=True)

        return self.__class__(train, c), self.__class__(test, c)




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


class Diabetes:

    def __init__(self, csvfile: str = 'diabetes.csv'):
        super().__init__()
        self.df = pd.read_csv(csvfile)
        self.df.rocket.classcols = ['class']
        self.train, self.test = self.df.rocket.normalized.balanced.split(0.3)

        self._model = None
        self._predict = None

    @property
    def model(self):
        if self._model is None:
            x = self.train.instances.df
            y = self.train.classes.df.values.ravel()

            # model = sklearn.ensemble.RandomForestClassifier()
            # model = sklearn.ensemble.AdaBoostClassifier()
            # model = sklearn.ensemble.BaggingClassifier()
            model = sklearn.ensemble.GradientBoostingClassifier()
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






