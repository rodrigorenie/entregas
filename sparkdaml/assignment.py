import pyspark.sql

from pyspark.sql import SparkSession, functions


class Assignment:
    """Com os arquivos contidos em Dados/ETrabalho descritos abaixo:

        cities.csv          id
        lines.csv           city_id
        station_lines.csv   line_id, station_id
        station.csv         city_id

    Responder:
        * Qual país possui cidades?
        * Qual cidade possui linhas?
        * Quais são 10 linhas que passam por mais cidades?
        * Qual é o país que tem mais linhas?
        * A linha que tem mais estações em seu percurso?
        * Quais são as 10 cidades que possuem as linhas com mais estações?
        * Qual país são os mais presentes entre essas 10 cidades?
        * O país que tem a maior média de estações?
    """

    def __init__(self):
        """Carrega os dados dos arquivos na pasta de dados e imprime o solicitado"""
        spark = SparkSession.builder.getOrCreate()
        dpath = 'data/sparkdaml/assignment'

        self.cities = spark.read.csv(f'{dpath}/cities.csv', header=True, inferSchema=True)
        self.lines = spark.read.csv(f'{dpath}/lines.csv', header=True, inferSchema=True)
        self.station_lines = spark.read.csv(f'{dpath}/station_lines.csv', header=True, inferSchema=True)
        self.stations = spark.read.csv(f'{dpath}/stations.csv', header=True, inferSchema=True)

        print('Trabalho - Qual país possui cidades?')
        self.countries.show(self.countries.count(), False)

        print('Trabalho - Qual cidade possui linhas?')
        self.lines_per_city.show(self.lines_per_city.count(), False)

        print('Trabalho - Quais são 10 linhas que passam por mais cidades?')
        self.cities_per_line.show()

        print('Trabalho - Qual é o país que tem mais linhas?')
        self.lines_per_country.show()

        print('Trabalho - A linha que tem mais estações em seu percurso?')
        self.stations_per_line.show()

        print('Trabalho - Quais são as 10 cidades que possuem as linhas com mais estações?')
        self.stations_with_lines_per_city.show()

        print('Trabalho - Qual país são os mais presentes entre essas 10 cidades?')
        self.countries_of_stations_with_lines_per_city.show()

        print('Trabalho - O país que tem a maior média de estações?')
        self.avg_stations_per_country.show()

    @property
    def countries(self) -> pyspark.sql.DataFrame:
        city = self.cities
        tmp = self.cities.groupby(city['country'])
        return tmp.agg(functions.countDistinct(city['name']).name('# cities'))

    @property
    def lines_per_city(self) -> pyspark.sql.DataFrame:
        stationline, city = self.station_lines, self.cities
        tmp = stationline.join(city, stationline['city_id'] == city['id'], how='inner').groupby(city['name'])
        return tmp.agg(functions.count(city['name']).name('lines'))

    @property
    def cities_per_line(self) -> pyspark.sql.DataFrame:
        line, stationline = self.lines, self.station_lines
        tmp = stationline.join(line, stationline['line_id'] == line['id'], how='inner')
        tmp = tmp.groupby(line['name'])
        tmp = tmp.agg(functions.countDistinct(stationline['city_id']).name('# cities'))
        return tmp.sort(tmp['# cities'], ascending=False).limit(10)

    @property
    def lines_per_country(self) -> pyspark.sql.DataFrame:
        stationline, city = self.station_lines, self.cities
        tmp = stationline.join(city, stationline['city_id'] == city['id'], how='inner')
        tmp = tmp.groupby(city['country'])
        tmp = tmp.agg(functions.countDistinct(stationline['line_id']).name('# lines'))
        return tmp.sort(city['country']).limit(10)

    @property
    def stations_per_line(self) -> pyspark.sql.DataFrame:
        stationline, line = self.station_lines, self.lines
        tmp = stationline.join(line, stationline['line_id'] == line['id'], how='inner')
        tmp = tmp.groupby(line['name'].name('line name'), line['id'].name('line id'))
        tmp = tmp.agg(functions.countDistinct(stationline['station_id']).name('# stations'))
        return tmp.sort(tmp['# stations'], ascending=False).limit(10)

    @property
    def stations_with_lines_per_city(self) -> pyspark.sql.DataFrame:
        stationline, line, city = self.station_lines, self.lines, self.cities

        tmp = stationline.join(line, stationline['line_id'] == line['id'], how='inner')
        tmp = tmp.groupby(line['name'], line['id'])
        tmp = tmp.agg(functions.countDistinct(stationline['station_id']).name('# stations per line'),
                      functions.first(line['city_id']).name('city_id'))

        tmp = tmp.join(city, tmp['city_id'] == city['id'], how='left')
        tmp = tmp.groupby(city['name'], city['country'])
        tmp = tmp.agg(functions.sum('# stations per line').name('# stations per line'))
        return tmp.sort(tmp['# stations per line'], ascending=False).limit(10)

    @property
    def countries_of_stations_with_lines_per_city(self) -> pyspark.sql.DataFrame:
        tmp = self.stations_with_lines_per_city
        tmp = tmp.groupby('country')
        return tmp.agg(functions.count('country').name('count'))

    @property
    def avg_stations_per_country(self) -> pyspark.sql.DataFrame:
        station, city = self.stations, self.cities

        tmp = station.join(city, station['city_id'] == city['id'], how='inner')
        tmp = tmp.groupby(city['country'], city['name'])
        tmp = tmp.agg(functions.countDistinct(station['id']).name('# stations'))
        tmp = tmp.groupby('country')
        tmp = tmp.agg(functions.avg('# stations').name('# avg stations per city'))
        return tmp.sort(tmp['# avg stations per city'], ascending=False).limit(10)
