import re

import pyspark.sql
from pyspark.sql import SparkSession, functions
from dateutil import parser


class Ex01:
    """
    Objetivo: Identificar quais palavras mais ocorrem no texto.
    Passos:
        * Ler da pasta Dados/E1/texto.txt
        * Quebrar o texto em um array
        * Filtrar palavras maior que 2 caracteres
        * atribuir o valor 1 para cada item do array
        * Agrupar por chave
        * Ordenar por chave
        * Ordenar por valor
        * Serializar os resultados
    """

    def __init__(self) -> None:
        """Carrega o texto e imprime as 20 palavras mais frequentes"""
        spark = SparkSession.builder.getOrCreate()
        fpath = 'data/sparkdaml/ex01/texto.txt'
        self.rdd = spark.sparkContext.textFile(fpath)

        print('Exercício 01')
        for word, freq in self.top20:
            print(f'{freq:>5} : {word}')
        print('\n\n')

    @property
    def split(self) -> pyspark.RDD:
        """Separa o texto em palavras e transforma em um array"""
        return self.rdd.flatMap(lambda s: re.split(r'\W+', s))

    @property
    def filter(self) -> pyspark.RDD:
        """Do resultado de :attr:`split`, filtra por palavras com mais de 2 caracteres"""
        return self.split.filter(lambda w: len(w) > 2)

    @property
    def update(self) -> pyspark.RDD:
        """Do resultado de :attr:`filter`, transforma a palavra em chave com valor 1"""
        return self.filter.map(lambda w: (w, 1))

    @property
    def group(self) -> pyspark.RDD:
        """Do resultado de :attr:`update`, agrupa a chaves (palavras) únicas e soma seus valores, resultando na
        contagem de palavras únicas do texto"""
        return self.update.reduceByKey(lambda acc, cur: acc + cur)

    @property
    def order(self) -> pyspark.RDD:
        """Do resultado de :attr:`group`, ordena o array pelo valor (contagem)"""
        return self.group.sortBy(lambda kv: kv[1], ascending=False)

    @property
    def top20(self) -> list[tuple[str, int]]:
        """Do resultado de :attr:`order`, coleta as 30 palavras mais frequentes do texto"""
        return self.order.take(20)


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

    def __init__(self) -> None:
        """Carrega o texto e imprime os 20 erros mais frequentes"""
        spark = SparkSession.builder.getOrCreate()
        fpath = 'data/sparkdaml/ex02/logs.txt'
        self.rdd = spark.sparkContext.textFile(fpath)
        self.wordlist = None

        print('Exercício 02')
        for error, freq in self.top20:
            print(f'{freq:>5} : {error}')
        print('\n\n')

    @property
    def lower(self) -> pyspark.RDD:
        """Transforma todas as linhas do texto em minúscula"""
        return self.rdd.map(lambda s: str(s).lower())

    @property
    def filter(self) -> pyspark.RDD:
        """Do resultado de :attr:`lower`, filtra por linhas que contém a palavra 'erro'"""
        return self.lower.filter(lambda s: re.match(r'erro\b', s) is not None)

    @property
    def split(self) -> pyspark.RDD:
        """Do resultado de :attr:`filter`, separa o texto em palavras e transforma em um array"""
        return self.filter.flatMap(lambda s: re.split(r'\W+', s))

    @property
    def count(self) -> pyspark.RDD:
        """Do resultado de :attr:`split`, contabiliza a quantidade de cada palavra única"""
        return self.split.map(lambda w: (w, 1)).reduceByKey(lambda acc, cur: acc + cur)

    @property
    def sort(self) -> pyspark.RDD:
        """Do resultado de :attr:`count`, ordena o array pelo valor (contagem)"""
        return self.count.sortBy(lambda kv: kv[1], ascending=False)

    def save(self):
        """Salva o resultado de :attr:`sort` em uma variável da classe"""
        self.wordlist = self.sort.collect()

    @property
    def top20(self) -> list[tuple[str, int]]:
        """Do resultado de :attr:`filter`, trata os dados conforme formato do texto, contabiliza cada erro único e
        coleta os 20 mais frequentes"""
        tmp = self.filter.map(lambda s: re.split(r'\t', s))
        tmp = tmp.filter(lambda v: len(v) == 6)
        tmp = tmp.map(lambda v: (v[5], 1))
        tmp = tmp.reduceByKey(lambda acc, cur: acc + cur)
        tmp = tmp.sortBy(lambda kv: kv[1], ascending=False)
        return tmp.take(20)


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

    def __init__(self) -> None:
        """Carrega os dados do arquivo logs.txt"""
        spark = SparkSession.builder.getOrCreate()
        fpath = 'data/sparkdaml/ex02/logs.txt'
        self.rdd = spark.sparkContext.textFile(fpath)
        self.digitlist = None

        print('Exercício 02b')
        for error, freq in self.top20:
            print(f'{freq:>5} : {error}')
        print('\n\n')

    @property
    def lower(self) -> pyspark.RDD:
        """Converte todas as linhas do arquivo carregado para minúsculo"""
        return self.rdd.map(lambda s: str(s).lower())

    @property
    def filter(self) -> pyspark.RDD:
        """Do resultado de :attr:`lower`, filtra por linhas que começam com 'erro'"""
        return self.lower.filter(lambda s: re.match(r'^erro\b', s) is not None)

    @property
    def split(self) -> pyspark.RDD:
        """Do resultado de :attr:`filter`, cria um vetor com as palavras do texto
        e filtra por palavras que contém apenas dígitos"""
        tmp = self.filter.flatMap(lambda s: re.split(r'\W+', s))
        return tmp.filter(lambda w: re.fullmatch(r'[0-9]+', w) is not None)

    @property
    def count(self) -> pyspark.RDD:
        """Do resultado de :attr:`split`, contabiliza a frequência de cada palavra única"""
        tmp = self.split.map(lambda w: (w, 1))
        return tmp.reduceByKey(lambda acc, cur: acc + cur)

    @property
    def sort(self) -> pyspark.RDD:
        """Do resultado de :attr:`count`, ordene pela frequência"""
        return self.count.sortBy(lambda kv: kv[1], ascending=False)

    def save(self):
        """Salva o resultado de :attr:`sort` em uma variável"""
        self.digitlist = self.sort.collect()

    @property
    def top20(self) -> list[tuple[str, int]]:
        """Do resultado de :attr:`sort`, retorne os 20 primeiros elementos"""
        return self.sort.take(20)


class Ex03:
    """Objetivo: identificar os veículos.
    Utilizando as informações do arquivo "registrosPlacas.txt", levantar as seguintes informações:
        * Preparar os dados
        * Identificar o veículo que tem mais registros
        * Identificar qual veículo teve a maior velocidade
        * Identificar qual veículo teve a maior velocidade média
    """

    def __init__(self) -> None:
        """Carrega os dados do arquivo registrosPlacas.txt e imprime o solicitado"""
        spark = SparkSession.builder.getOrCreate()
        fpath = 'data/sparkdaml/ex03/registrosPlacas.txt'
        rdd = spark.sparkContext.textFile(fpath).map(Ex03.prepare)
        self.df = spark.createDataFrame(rdd, ['Placa', 'Num', 'Cidade', 'Data', 'km/h'])

        print('Exercício 03 - Veículos com maior número de registros')
        self.mostrecords.show()

        print('Exercício 03 - Veículos com as maiores velocidades registradas')
        self.fastest.show()

        print('Exercício 03 - Veículos com as maiores velocidades médias registradas')
        self.fastestavg.show()

    @staticmethod
    def prepare(line: str) -> list:
        """Método auxiliar para converter as linhas do arquivo em colunas com a tipagem adequada"""
        line = line.replace('\t', ',').split(',')
        line[1] = int(line[1])
        line[4] = line[4].split(' ')[0]
        line[3] = parser.parse(line[3], tzinfos={"BRST": "UTC-2"})
        return line

    @property
    def grp(self) -> pyspark.sql.GroupedData:
        """Retorna o DataFrame agrupado por placa, utilizado como base por todos os outros métodos"""
        return self.df.groupby('Placa')

    @property
    def mostrecords(self) -> pyspark.sql.DataFrame:
        """Retorna os 10 veículos com mais registros"""
        tmp = self.grp.agg(functions.count('Placa').name('Registros'))
        return tmp.sort('Registros', ascending=False).limit(10)

    @property
    def fastest(self) -> pyspark.sql.DataFrame:
        """Retorna os 10 veículos com maior velocidade máxima"""
        tmp = self.grp.agg(functions.max('km/h').name('km/h max'))
        return tmp.sort('km/h max', ascending=False).limit(10)

    @property
    def fastestavg(self) -> pyspark.sql.DataFrame:
        """Retorna os 10 veículos com maior velocidade média"""
        tmp = self.grp.agg(functions.avg('km/h').name('km/h avg'))
        return tmp.sort('km/h avg', ascending=False).limit(10)
