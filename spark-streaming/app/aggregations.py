from pyspark.sql.functions import col, window, count

def aggregate_events(df):
    """
    Aggregates events per event_type in 1-minute windows
    """
    return (
        df
        .withWatermark("event_time", "2 minutes")
        .groupBy(
            window(col("event_time"), "1 minute"),
            col("event_type")
        )
        .agg(count("*").alias("event_count"))
    )
