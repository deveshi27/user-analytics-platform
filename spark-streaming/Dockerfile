FROM apache/spark:3.5.1

USER root

ENV HOME=/opt/spark
ENV SPARK_USER=spark

WORKDIR /opt/spark/app

# -----------------------------
# Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# App code & Spark config
# -----------------------------
COPY app/ app/
COPY config/spark.conf /opt/spark/conf/spark-defaults.conf

# -----------------------------
# Runtime directories
# -----------------------------
RUN mkdir -p \
    /opt/spark/logs \
    /opt/spark/checkpoints \
    /opt/spark/output \
    /opt/spark/.ivy2

# -----------------------------
# Run Spark Streaming job
# -----------------------------
ENTRYPOINT ["/opt/spark/bin/spark-submit"]
CMD ["--packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.4","--conf","spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem","app/stream_processor.py"]

