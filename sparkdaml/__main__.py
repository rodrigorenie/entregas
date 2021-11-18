from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

if __name__ == '__main__':
    # spark = SparkSession.builder.appName('Testing 123').getOrCreate()
    # rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 56])
    # count = rdd.count()
    # print(count)

    conf = SparkConf()
    conf.setAppName('testing 123 modafucka')
    conf.set('spark.sql.catalogImplementation', 'hive')
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 2, 3])
    count = rdd.count()

    print("count:", count)
