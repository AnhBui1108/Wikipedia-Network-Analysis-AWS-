#!/usr/bin/env python
# coding: utf-8

# In[1]:


import unittest

import pyspark 
from pyspark.storagelevel import StorageLevel
from pyspark.sql import (
    functions as F, 
    types as T,
    SparkSession,
)


# In[2]:


from methods import create_mutual_links, connected_components


# In[3]:


class DataIOSynth:
    def __init__(self, spark):
        self.spark = spark
    def read(self, path):
        path = f"./TestData/{path}"
        return self.spark.read.json(path)
    def write(self, df, path):
        path = f"./TestData/{path}"
        df.coalesce(1).write.mode("OVERWRITE").json(path)

def read_json(spark, path):
    path=f"./TestData/{path}"
    return spark.read.json(path)


# In[4]:


exp_links= frozenset({
    frozenset([1,2]),
    frozenset([2, 8]),
    frozenset([4,5]),
    frozenset([4, 10])})
    


# In[5]:


exp_components = frozenset({
    frozenset([1, 2, 8]),
    frozenset([4, 5, 10])
})
    


# In[6]:


class TestMethods(unittest.TestCase):
    def test_create_links_and_component(self):
        spark=(
            SparkSession
            .builder
            .master("local")
            .appName("My app")
            .getOrCreate()
        )
        dataIO = DataIOSynth(spark)
        mutual_links = create_mutual_links(
            spark,
            read_json(spark, 'page.jsonl'),
            read_json(spark, 'pagelinks.jsonl'),
            read_json(spark, 'linktarget.jsonl'),
            read_json(spark, 'redirect.jsonl')
        )
        dataIO.write(mutual_links, "mutual_links")
        actual_link = frozenset(frozenset(r) for r in mutual_links.collect())
        self.assertEqual(actual_link, exp_links)

        checkpoint_path = f"./test_output/"
        cc = connected_components(spark, mutual_links, dataIO)
        cc = cc.select(F.col("src").alias("vertex_ID"),
               F.col("updated_component_ID").alias("component_ID"))
        dataIO.write(cc, "test_components")
        groups = frozenset(frozenset(c.members) for c in 
                           cc
                           .groupby("component_ID")
                           .agg(F.expr("collect_list(vertex_ID) as members"))
                           .collect()
                          )
        self.assertEqual(groups, exp_components)
        print("conected component stats")
        cc_stats = cc.groupBy("component_ID").agg(F.expr("count(*) as size"))
        cc_counts = cc_stats.count()
        print("The number of conected component: ", cc_counts)
        cc_stats.orderBy(F.desc("size")).show(truncate=False)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
            
            
        


# In[ ]:




