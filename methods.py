
import pyspark 
from pyspark.storagelevel import StorageLevel
from pyspark.sql import (
    functions as F, 
    types as T,
    SparkSession,
)
import os
from datetime import datetime


spark = (
    SparkSession.builder
    .appName("My App")
    .getOrCreate()
)


def parquet(prefix):
    files= spark.read.parquet(f"s3://bsu-c535-fall2024-commons/arjun-workspace/{prefix}/")
    files.save(prefix)
    return files

def save(self, name):
    t = datetime.now()
    (self
     .persist(StorageLevel.MEMORY_AND_DISK)
     .createOrReplaceTempView(name)
    )
    rows = spark.table(name).count()
    print(f"{name} -{rows} rows - elapsed {datetime.now() -t}")
    spark.table(name).printSchema()
    

pyspark.sql.DataFrame.save = save


def create_mutual_links(spark, page, pagelinks, linktarget, redirect):
    (
        page
        .filter(F.col('page_namespace')==0)
        .join(
            redirect,
            (F.col('page_id') == F.col('rd_from')),
            'left'
        )
         .join(
            linktarget,
            (F.col('page_title') == F.col('lt_title')) & (F.col('page_namespace') == F.col('lt_namespace')),
            'inner',
        )
        .select('lt_id',
                F.when(F.col('page_is_redirect') == False, F.col("page_title"))
                .otherwise(F.col("rd_title"))
                .alias('lt_title_updated'),
                'lt_namespace')
        .join(
            page,
            (F.col('lt_title_updated') == F.col('page_title')) & (F.col('page_namespace') == F.col('lt_namespace')),
            'left',
        )
        .select('lt_id','lt_title_updated','page_id')
        .join(
            pagelinks,
            (F.col('pl_target_id') == F.col('lt_id')),
            'inner',
        )
        .select(
            F.col('pl_from').alias('page_a'),
            F.col('page_id').alias('page_b')
        )
        .distinct()
        .withColumn( 
            'sorted_pair',
            F.array_sort(F.array(F.col('page_a'), F.col('page_b')))
        )
  
        .groupBy('sorted_pair')
        .agg(F.count('*').alias('frequency'))
        .filter(F.col('frequency') > 1)
        .select(
            F.col('sorted_pair')[0].alias('src'),
            F.col('sorted_pair')[1].alias('dst')
        )
        .persist(StorageLevel.MEMORY_AND_DISK)
        .createOrReplaceTempView('mutual_links')
    )
    
    return spark.table('mutual_links')



class DataIO:
    def __init__(self, spark):
        self.spark = spark
        
    def read(self, path):
        path = f"{os.environ['CS535_S3_WORKSPACE']}{path}"
        return self.spark.read.json(path)
        
    def write(self, df, path):
        path = f"{os.environ['CS535_S3_WORKSPACE']}{path}"
        df.write.mode("OVERWRITE").json(path)
        


def connected_components(spark, mutual_links, dataIO, path):
    t1= datetime.now()
    
    bidirectional_edge = (
        mutual_links
        .union(mutual_links.select(F.col("dst").alias("src"), F.col("src").alias("dst")))
        .persist(StorageLevel.MEMORY_AND_DISK)
    )
    bidirectional_edge.count()

    
    t2 = datetime.now()
    iteration_0 = (
        bidirectional_edge
        .groupBy("src")
        .agg(F.min(F.col('dst')).alias('component_ID'))
        .select(F.col("src").alias("vertex_ID"),
                F.least('vertex_ID', 'component_ID').alias('component_ID'))
        .persist(StorageLevel.MEMORY_AND_DISK)
     )
    
    print("vertex list size:", iteration_0.count())
    print("elapse time: ", datetime.now() - t2)
    print("Start iteration")
    
    iteration_count = 0
    iteration_prev = iteration_0
    iteration_prev.show()
    
    print("iteration setup running tine", datetime.now() - t1)
    while True:
        t3= datetime.now()
        iteration_count += 1
        print(f"Iteration {iteration_count}")
    
        iteration_curr =(
            bidirectional_edge
            .join(iteration_prev, 
                  F.col("dst") == F.col("vertex_ID"), 
                  "inner")
            .groupBy('src')
            .agg(F.min("component_ID").alias("curr_component_ID"))
            .select("src", "curr_component_ID")
            .join(
                iteration_prev, F.col('src')==F.col('vertex_ID'), 'inner')
            .select('src',
                    F.least(F.col('curr_component_ID'), F.col('component_ID')).alias('updated_component_ID'))
            .persist(StorageLevel.MEMORY_AND_DISK)
        )
        print("vertex count:", iteration_curr.count())   
        
       
        num_changed = (
            iteration_curr
            .join(iteration_prev, 
                  F.col("vertex_ID")==F.col("src"),
                  "inner")
            .filter(F.col("updated_component_ID") != F.col("component_ID"))
            .count()
        )
        print(f"Number of vertex changed: {num_changed}")
        print("iteration time:", datetime.now() - t3)
    
        
        if num_changed == 0:
            print("Finish")
            break
    
        
        if iteration_count % 3 == 0:
            checkpoint_path = f"{path}/iter_{iteration_count}"
            dataIO.write(iteration_curr,checkpoint_path)
            print("Succesfully write checkpoint to S3 bucket")
            print("-----------------")
            print("Checkpoint", iteration_count/3)
            iteration_curr = dataIO.read(checkpoint_path)
            print("Read checkpoint from S3 bucket")
        
        iteration_prev = iteration_curr.select(F.col("src").alias('vertex_ID'),F.col("updated_component_ID").alias("component_ID"))

    return iteration_curr 







