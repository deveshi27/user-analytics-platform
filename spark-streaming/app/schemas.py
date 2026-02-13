from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    MapType
)

event_schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("source", StringType(), True),
    StructField("event_time", TimestampType(), True),
    StructField("metadata", MapType(StringType(), StringType()), True)
])
