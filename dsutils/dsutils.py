from __future__ import annotations

import os
import sklearn
import inspect
import pandas
import numpy
import imblearn

from typing import Tuple, List
from rich import box
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.rule import Rule


class DataDir:

    datadir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'data')
    )

    @staticmethod
    def join(*args):
        caller = inspect.getmodule(inspect.currentframe().f_back).__package__
        path = os.path.join(DataDir.datadir, caller)
        for arg in args:
            arg = os.path.basename(arg)
            path = os.path.join(path, arg)
        return path


@pandas.api.extensions.register_dataframe_accessor("rocket")
class RocketFrame:
    """Classe que extende a funcionalidade de um :class:`pandas.DataFrame`

    Adiciona uma propriedade nas instâncias da classe :class:`pandas.DataFrame`
    chamado ``rocket``, a partir da onde é possível acessar todos os métodos
    implementados nesta classe.

    Exemplo:

    >>> import pandas
    >>> # Obrigatório importar o módulo para registrar a propriedade 'rocket'
    >>> import dsutils
    >>> pd = pandas.DataFrame([[1, 2], [3, 4], [5, 6]], columns=[['i', 'c']])
    >>> pd.rocket.classcols = ['c']
    >>> # Cópia do DataFrame contendo apenas as instâncias
    >>> pd.rocket.instances.df
    >>> # Cópia do DataFrame contendo apenas as classes
    >>> pd.rocket.classes.df
    """
    def __init__(self,
                 df: pandas.DataFrame,
                 classcols: List[str] = None) -> None:
        self._df = df
        self._classcols = classcols if classcols is not None else []
        self._train = None
        self._test = None

    @property
    def df(self) -> pandas.DataFrame:
        return self._df

    @property
    def train(self) -> RocketFrame:
        if self._train is None:
            self._train, self._test = self.split()
        return self._train

    @property
    def test(self) -> RocketFrame:
        if self._test is None:
            self._train, self._test = self.split()
        return self._test

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
    def nona(self) -> RocketFrame:
        df = self.df
        df = df.drop(columns=df.columns[df.isna().all()])
        df = df.dropna()
        df = df.reset_index(drop=True)
        return self.__class__(df, self.classcols)

    @property
    def numericals(self) -> RocketFrame:
        df = self.df.select_dtypes(include=numpy.number)
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
        dfcat = pandas.get_dummies(dfcat) if dfcat.size > 0 else dfcat
        dfcat = dfcat.join(self.classes.df)

        df = self.numericals.instances.df
        df = pandas.DataFrame(normalizer.fit_transform(df), columns=df.columns)

        return self.__class__(df.join(dfcat), self.classcols)

    @property
    def balanced(self) -> RocketFrame:
        balancer = imblearn.over_sampling.SMOTE()
        dfinst, dfclass = self.instances.df, self.classes.df
        dfinst, dfclass = balancer.fit_resample(dfinst, dfclass)
        return self.__class__(dfinst.join(dfclass), self.classcols)

    def split(self, size: float = 0.3) -> Tuple[RocketFrame, RocketFrame]:
        x = self.instances.df
        y = self.classes.df
        c = self.classcols

        split = sklearn.model_selection.train_test_split(x, y, test_size=size)
        x_train, x_test, y_train, y_test = split

        train = x_train.join(y_train).reset_index(drop=True)
        test = x_test.join(y_test).reset_index(drop=True)

        return self.__class__(train, c), self.__class__(test, c)


class Exercise:

    def __init__(self, title):
        self._title = title
        self._items = {}

    @staticmethod
    def text(*args, **kwargs):
        return Text(*args, **kwargs)

    def __iter__(self):
        for number, (item, resolution) in enumerate(self._items.items()):
            yield f'{number+1:02}', item, resolution

    def item(self, item, *resolutions):
        self._items[item] = resolutions

    def print(self):
        console = Console(width=80)
        console.print(Panel(Text(self._title, justify='center')))

        for number, item, resolutions in self:
            console.print(Columns([
                Panel(number, width=6, box=box.SIMPLE),
                Panel(item, width=73, box=box.SIMPLE)
            ]))
            console.print(*resolutions, sep='\n')
            console.print()
            console.print(Rule(characters='-'))
