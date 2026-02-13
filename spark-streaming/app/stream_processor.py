from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from schemas import event_schema
from aggregations import aggregate_events

KAFKA_BROKER = "kafka:9092"
TOPIC = "user_events_raw"

spark = (
    SparkSession.builder
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("INFO")

# 1️⃣ Read from Kafka
raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BROKER)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)

# 2️⃣ Convert Kafka value from bytes → JSON
json_df = (
    raw_df
    .selectExpr("CAST(value AS STRING) as json")
    .select(from_json(col("json"), event_schema).alias("data"))
    .select("data.*")
)

# 3️⃣ Apply transformations
aggregated_df = aggregate_events(json_df)

# 4️⃣ Write output to files (Parquet)
query = (
    aggregated_df
    .writeStream
    .format("parquet")
    .option("path", "/opt/spark/output")
    .option("checkpointLocation", "/opt/spark/checkpoints")
    .outputMode("append")
    .start()
)

query.awaitTermination()
