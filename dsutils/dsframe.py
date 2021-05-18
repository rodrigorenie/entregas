import sklearn
import pandas
import numpy
import imblearn


@pandas.api.extensions.register_dataframe_accessor('ds')
class DSFrame:
    """Classe que extende a funcionalidade de um :class:`pandas.DataFrame`

    Adiciona uma propriedade nas instâncias da classe :class:`pandas.DataFrame`
    chamado ``ds``, a partir da onde é possível acessar todos os métodos
    implementados nesta classe.

    Exemplo:

    >>> import pandas
    >>> # Obrigatório importar o módulo para registrar a propriedade 'ds'
    >>> import dsutils
    >>> pd = pandas.DataFrame([[1, 2], [3, 4], [5, 6]], columns=[['i', 'c']])
    >>> pd.ds.classcols = ['c']
    >>> # Cópia do DataFrame contendo apenas as instâncias
    >>> pd.ds.instances
    >>> # Cópia do DataFrame contendo apenas as classes
    >>> pd.ds.classes
    >>> # Cópia do DataFrame com as instâncias normalizaas e balanceaas
    >>> pd.ds.normalized.ds.balanced.ds.instances
    """

    def __init__(self, df: pandas.DataFrame) -> None:
        self._df = df
        self._classcols = []
        self._train = None
        self._test = None

    @property
    def df(self) -> pandas.DataFrame:
        return self._df

    @property
    def classcols(self) -> list[str]:
        return self._classcols

    @classcols.setter
    def classcols(self, classcols: list[str]) -> None:
        for col in classcols:
            if col not in self.df.columns:
                raise ValueError(f"'{col}' column must exist in the dataframe")
        self._classcols = classcols

    @property
    def train(self) -> pandas.DataFrame:
        if self._train is None:
            self._train, self._test = self.split()
        return self._train

    def __str__(self) -> str:
        return str(self.df)

    @property
    def classes(self) -> pandas.DataFrame:
        cols = self.df.columns.difference(self.classcols)
        df = self.df.drop(cols, 1)
        return df

    @property
    def instances(self) -> pandas.DataFrame:
        df = self.df.drop(columns=self.classcols, errors='ignore')
        return df

    @property
    def nona(self) -> pandas.DataFrame:
        df = self.df
        df = df.drop(columns=df.columns[df.isna().all()])
        df = df.dropna()
        df = df.reset_index(drop=True)
        return df

    @property
    def numericals(self) -> pandas.DataFrame:
        df = self.df.drop(columns=self.classcols, errors='ignore')
        df = df.select_dtypes(include=numpy.number)
        df = df.join(self.classes)
        return df

    @property
    def categoricals(self) -> pandas.DataFrame:
        df = self.df.drop(columns=self.classcols, errors='ignore')
        df = df.select_dtypes(include=object)
        df = df.join(self.classes)
        return df

    @property
    def normalized(self) -> pandas.DataFrame:
        normalizer = sklearn.preprocessing.MinMaxScaler()

        dfcat = self.__class__(self.categoricals).instances
        dfnum = self.__class__(self.numericals).instances

        dfcat = pandas.get_dummies(dfcat) if dfcat.size > 0 else dfcat
        dfnum = pandas.DataFrame(normalizer.fit_transform(dfnum),
                                 columns=dfnum.columns)

        return dfcat.join(dfnum).join(self.classes)

    @property
    def balanced(self) -> pandas.DataFrame:
        balancer = imblearn.over_sampling.SMOTE()
        df = self.df.groupby(self.classcols).filter(lambda x: len(x) > 6)
        dfinst = self.__class__(df).instances
        dfclass = self.__class__(df).classes
        dfinst, dfclass = balancer.fit_resample(dfinst, dfclass)
        return dfinst.join(dfclass)

    @property
    def reduced(self) -> pandas.DataFrame:
        df, dfclass = self.instances, self.classes

        df = sklearn.decomposition.PCA(n_components=2).fit_transform(df)
        df = pandas.DataFrame(df, columns=['X', 'y'])
        df = df.join(dfclass.reset_index(drop=True))

        return df

    def split(self, size: float = 0.3) -> tuple[pandas.DataFrame,
                                                pandas.DataFrame]:
        x = self.instances
        y = self.classes

        split = sklearn.model_selection.train_test_split(x, y, test_size=size)
        x_train, x_test, y_train, y_test = split

        x = x_train.join(y_train).reset_index(drop=True)
        y = x_test.join(y_test).reset_index(drop=True)

        return x, y


@pandas.api.extensions.register_dataframe_accessor('hypo')
class DSHypoFrame(DSFrame):

    def __init__(self, df: pandas.DataFrame) -> None:
        df = df.replace('?', numpy.nan)
        super().__init__(df)
        self.classcols = ['Class']


@pandas.api.extensions.register_dataframe_accessor('diabetes')
class DSDiabetesFrame(DSFrame):

    def __init__(self, df: pandas.DataFrame) -> None:
        super().__init__(df)
        self.classcols = ['class']
