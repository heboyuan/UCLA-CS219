from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import binascii


sc = SparkContext("spark://vagrant.vm:7077", "NetworkWordCount")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")
initialStateRDD = sc.parallelize([])


# stream_data = ssc.textFileStream("file:////home/vagrant/219/data")
stream_data = ssc.socketTextStream("172.18.0.4", 12345)


def decode_line(line):
    from decoder import mi_enb_decoder
    return [mi_enb_decoder(line).get_type_id()]


def message_count(m):
    return m, 1


def update_count(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)


stream_data = stream_data.flatMap(decode_line)
stream_data = stream_data.map(message_count)
stream_data = stream_data.updateStateByKey(
    update_count, initialRDD=initialStateRDD)

stream_data.pprint()

ssc.start()
ssc.awaitTermination()
