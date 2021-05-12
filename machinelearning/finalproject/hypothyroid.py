import pandas as pd
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model

from dsutils import DataDir
from typing import Any, Iterable, Tuple


class Hypothyroid:

    def __init__(self, csvfile: str = 'hypothyroid.csv') -> None:
        df = pd.read_csv(DataDir.join(csvfile), na_values='?',
                         keep_default_na=True)
        df.rocket.classcols = ['Class']
        df = df.rocket.nona.normalized.balanced
