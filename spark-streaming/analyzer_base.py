from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import binascii
import sys
import importlib

udf_module = importlib.import_module(sys.argv[1])
flatmap_udf_names = sys.argv[2].split(",")
flatmap_udf = [getattr(udf_module, udf_name) for udf_name in flatmap_udf_names]
map_udf_names = sys.argv[3].split(",")
map_udf = [getattr(udf_module, udf_name) for udf_name in map_udf_names]
state_update_udf_names = sys.argv[4].split(",")
state_update_udf = [getattr(udf_module, udf_name)
                    for udf_name in state_update_udf_names]


sc = SparkContext("spark://vagrant.vm:7077", "MobileDataAnalytics")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")
initialStateRDD = sc.parallelize([])


# stream_data = ssc.textFileStream("file:////home/vagrant/219/data")
stream_data = ssc.socketTextStream("172.18.0.4", 12345)

for f in flatmap_udf:
    stream_data = stream_data.flatMap(f)
for f in map_udf:
    stream_data = stream_data.map(f)
for f in state_update_udf:
    stream_data = stream_data.updateStateByKey(f, initialRDD=initialStateRDD)

stream_data.pprint()

ssc.start()
ssc.awaitTermination()
