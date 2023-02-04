from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import os, sys, time

hdfs_path = "hdfs://192.168.0.1:9000/data/"

#create spark session
spark = SparkSession.builder.master("spark://192.168.0.1:7077").getOrCreate()
print("Spark Session Started")

#spark.conf.set("spark.executor.instances", 1)

#initialize dataset
#q2=spark.read.parquet("./data/yellow_tripdata_2022-prwtoi6.parquet")
q4 = spark.read.option("header", "true").option("inferSchema", "true").parquet(hdfs_path + "yellow_tripdata_2022-prwtoi6.parquet")
q4=q4.filter((month(col("tpep_pickup_datetime")) >= 1) & (month(col("tpep_pickup_datetime")) <= 6))

#add column for month
q4new = q4.withColumn("weekday", dayofweek(col("tpep_pickup_datetime")))
q4new = q4.withColumn("timezone", hour(col("tpep_pickup_datetime")))

#sql query
q4new.createOrReplaceTempView("data")
query_help = spark.sql("""SELECT weekday, timezone, row_number() OVER (PARTITION BY weekday, timezone ORDER BY AVG(Passenger_count)) as row_nr
FROM data""")
query_help.createOrReplaceTempView("newdata")
query4 = spark.sql(""" SELECT *
FROM newdata
WHERE row_nr <= 3""")

start = time.time()
query4.show()
time_elapsed = time.time() - start

print("Time elapsed: ", time_elapsed) 

spark.stop()