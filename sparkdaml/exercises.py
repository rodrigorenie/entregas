import re

from typing import Optional
from pyspark import SparkContext, SparkConf, RDD


class Ex01:
    """
    Objetivo: Identificar quais palavras mais ocorrem no texto. Passos:
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
    def split(self) -> RDD:
        return self.rdd.flatMap(lambda s: re.split('\\W+', s))

    @property
    def filter(self) -> RDD:
        return self.split.filter(lambda w: len(w) > 2)

    @property
    def update(self) -> RDD:
        return self.filter.map(lambda w: (w, 1))

    @property
    def group(self) -> RDD:
        return self.update.reduceByKey(lambda acc, cur: acc + cur)

    @property
    def order(self) -> RDD:
        return self.group.sortBy(lambda kv: kv[1], ascending=False)

    @property
    def top50(self) -> list[tuple[str, int]]:
        return self.order.take(50)

    @staticmethod
    def run() -> None:
        ex = Ex01(SparkContext.getOrCreate(conf=SparkConf()))
        print('Exercício 01')
        for word, freq in ex.top50:
            print(f'{freq:>5} : {word}')
        print('\n\n')


class Ex02:
    """
    Objetivo: Identificar os logs em com erro
        - Ler da pasta /content/drive/MyDrive/AulaSpark/Dados/E2/logs.txt
        - Passar todas palavras para minúsculas
        - Pegar apenas as linhas que contém a palavra “erro”
         - Dica: Utilize
            - import re
            - re.match(pattern, string)
        - Contar as palavras
        - Ordenar pelas palavras que mais se repetem
        - Salvar os resultados
        - Exibir os 20 primeiros erros que mais ocorrem
    """

    def __init__(self, spark: SparkContext, fpath: Optional[str] = None) -> None:
        self.spark = spark
        self.rdd = spark.textFile(fpath if fpath else 'data/sparkdaml/ex02/logs.txt')
        self.wordlist = None

    @property
    def lower(self) -> RDD:
        return self.rdd.map(lambda s: str(s).lower())

    @property
    def filter(self) -> RDD:
        return self.lower.filter(lambda s: re.match(r'erro\b', s) is not None)

    @property
    def split(self) -> RDD:
        return self.filter.flatMap(lambda s: re.split(r'\W+', s))

    @property
    def count(self) -> RDD:
        return self.split.map(lambda w: (w, 1)).reduceByKey(lambda acc, cur: acc + cur)

    @property
    def sort(self) -> RDD:
        return self.count.sortBy(lambda kv: kv[1], ascending=False)

    def save(self):
        self.wordlist = self.sort.collect()

    @property
    def top20(self) -> list[tuple[str, int]]:
        return self.filter.map(
            lambda s: re.split(r'\t', s)
        ).filter(
            lambda v: len(v) == 6
        ).map(
            lambda v: (v[5], 1)
        ).reduceByKey(
            lambda acc, cur: acc + cur
        ).sortBy(
            lambda kv: kv[1], ascending=False
        ).take(20)

    @staticmethod
    def run() -> None:
        ex = Ex02(SparkContext.getOrCreate(conf=SparkConf()))
        ex.save()

        print('Exercício 02')
        for error, freq in ex.top20:
            print(f'{freq:>5} : {error}')
        print('\n\n')


class Ex02b:
    """
    Objetivo: Identificar os logs em com erro
        - Ler da pasta /content/drive/MyDrive/AulaSpark/Dados/E2/logs.txt
        - Passar todas palavras para minúsculas
        - Pegar apenas as linhas que Iniciam a palavra “erro”
        - Dica: Utilize
            import re
            re.match(pattern, string)
        - Filtrar apenas os dígitos (não palavras)
        - Contar
        - Ordenar pelas palavras que mais se repetem
        - Salvar os resultados
        - Exibir os 20 primeiros erros que mais ocorrem
    """

    def __init__(self, spark: SparkContext, fpath: Optional[str] = None) -> None:
        """Carrega do arquivo logs.txt"""
        self.spark = spark
        self.rdd = spark.textFile(fpath if fpath else 'data/sparkdaml/ex02/logs.txt')
        self.digitlist = None

    @property
    def lower(self) -> RDD:
        """Converte todas as linhas "s" para minúsculas"""
        return self.rdd.map(lambda s: str(s).lower())

    @property
    def filter(self) -> RDD:
        return self.lower.filter(lambda s: re.match(r'^erro\b', s) is not None)

    @property
    def split(self) -> RDD:
        return self.filter.flatMap(
            lambda s: re.split(r'\W+', s)
        ).filter(
            lambda w: re.fullmatch(r'[0-9]+', w) is not None
        )

    @property
    def count(self) -> RDD:
        return self.split.map(
            lambda w: (w, 1)
        ).reduceByKey(
            lambda acc, cur: acc + cur
        )

    @property
    def sort(self) -> RDD:
        return self.count.sortBy(lambda kv: kv[1], ascending=False)

    def save(self):
        self.digitlist = self.sort.collect()

    @property
    def top20(self) -> list[tuple[str, int]]:
        return self.sort.take(20)

    @staticmethod
    def run() -> None:
        ex = Ex02b(SparkContext.getOrCreate(conf=SparkConf()))
        ex.save()

        print('Exercício 02b')
        for error, freq in ex.top20:
            print(f'{freq:>5} : {error}')
        print('\n\n')


class Ex03:
    """
    Objetivo: Identificar os logs em com erro
        * Ler da pasta /content/drive/MyDrive/AulaSpark/Dados/E2/logs.txt
        * Passar todas palavras para minúsculas
        * Pegar apenas as linhas que Iniciam a palavra “erro”
            Dica: Utilize
                import re
                re.match(pattern, string)
        * Filtrar apenas os dígitos (não palavras)
        * Contar
        * Ordenar pelas palavras que mais se repetem
        * Salvar os resultados
        * Exibir os 20 primeiros erros que mais ocorrem
    """