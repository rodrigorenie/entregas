import re

from typing import Optional
from pyspark import SparkContext, SparkConf, RDD


class Ex01:
    """
    Objetivo: Identificar quais palavras mais ocorrem no texto Passos:
        * Ler da pasta Dados\\E1\\texto.txt
        * Quebrar o texto em um array
        * Filtrar palavras maior que 2 caracteres
        * atribuir o valor 1 para cada item do array
        * Agrupar por chave
        * Ordenar por chave
        * Ordenar por valor
        * Serializar os resultados
    """

    def __init__(self, spark: SparkContext, fpath: Optional[str] = None) -> None:
        self.spark = spark
        self.rdd = spark.textFile(fpath if fpath else 'data/sparkdaml/ex01/texto.txt')

    @property
    def array(self) -> RDD:
        return self.rdd.flatMap(lambda s: re.split('\\W+', s))

    @property
    def over2chars(self) -> RDD:
        return self.array.filter(lambda s: len(s) > 2)

    @property
    def setone(self) -> RDD:
        return self.over2chars.map(lambda i: (i, 1))

    @property
    def groupbykey(self) -> RDD:
        return self.setone.reduceByKey(lambda v1, v2: v1 + v2)

    @property
    def orderbykey(self) -> RDD:
        return self.groupbykey.sortBy(lambda e: e[0])

    @property
    def orderbyvalue(self) -> RDD:
        return self.groupbykey.sortBy(lambda e: e[1])

    @staticmethod
    def run():
        conf = SparkConf()
        conf.setAppName('Pós DS - Spark - Exercício 01')
        ex = Ex01(SparkContext(conf=conf))
        for v in ex.orderbykey.collect():
            print(v)
