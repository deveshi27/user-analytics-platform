from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json,
    col,
    to_date,
    lit
)
from schemas import event_schema
from aggregations import aggregate_events
from es_writer import write_to_es
# -----------------------------
# Kafka config
# -----------------------------
KAFKA_BROKER = "kafka:9092"
TOPIC = "user_events_raw"

# -----------------------------
# S3 paths (FINAL STRUCTURE)
# -----------------------------
BRONZE_PATH = "s3a://user-analytics-datalake-dev/bronze/user_events/"
SILVER_PATH = "s3a://user-analytics-datalake-dev/silver/user_metrics/"

CHECKPOINT_BRONZE = "s3a://user-analytics-datalake-dev/checkpoints/spark/bronze/"
CHECKPOINT_SILVER = "s3a://user-analytics-datalake-dev/checkpoints/spark/silver/"

# -----------------------------
# Elasticsearch config
# -----------------------------
ES_HOST = "http://elasticsearch:9200"
ES_INDEX = "user_metrics_silver"

# -----------------------------
# Spark session
# -----------------------------
spark = (
    SparkSession.builder
    .appName("SparkKafkaStreaming-Bronze-Silver")
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("INFO")

# -----------------------------
# 1️⃣ Read from Kafka
# -----------------------------
raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BROKER)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)

# -----------------------------
# 2️⃣ Parse JSON (RAW EVENTS)
# -----------------------------
parsed_df = (
    raw_df
    .selectExpr("CAST(value AS STRING) as json")
    .select(from_json(col("json"), event_schema).alias("data"))
    .select("data.*")
)
# -----------------------------
# 3️⃣ BRONZE — Raw events (partitioned)
# -----------------------------
bronze_df = parsed_df.withColumn(
    "date",
    to_date(col("event_time"))
)
bronze_query = (
    bronze_df
    .writeStream
    .format("parquet")
    .partitionBy("date")  # creates date=YYYY-MM-DD
    .option("path", BRONZE_PATH)
    .option("checkpointLocation", CHECKPOINT_BRONZE)
    .outputMode("append")
    .start()
)
# -----------------------------
# 4️⃣ SILVER — Aggregated events
# -----------------------------
aggregated_df = aggregate_events(parsed_df)

silver_df = aggregated_df.withColumn(
    "date",
    col("window").getField("start").cast("date")
)

silver_query = (
    silver_df
    .writeStream
    .format("parquet")
    .partitionBy("date")
    .option("path", SILVER_PATH)
    .option("checkpointLocation", CHECKPOINT_SILVER)
    .outputMode("append")
    .start()
)
# -----------------------------
# 5️⃣ ELASTICSEARCH — Silver indexing (REST)
# -----------------------------

def write_batch_to_es(batch_df, batch_id):
    es_df = (
        batch_df
        .withColumn("window_start", col("window").getField("start"))
        .withColumn("window_end", col("window").getField("end"))
        .drop("window")
    )

    records = [row.asDict() for row in es_df.collect()]
    write_to_es("user_metrics_silver", records)

es_query = (
    silver_df
    .writeStream
    .foreachBatch(write_batch_to_es)
    .outputMode("update")
    .option(
        "checkpointLocation",
        "s3a://user-analytics-datalake-dev/checkpoints/spark/es/"
    )
    .start()
)

spark.streams.awaitAnyTermination()
