FROM apache/spark:3.5.1

USER root

ENV HOME=/opt/spark
ENV SPARK_USER=spark

WORKDIR /opt/spark/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -o /opt/spark/jars/hadoop-aws-3.3.4.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
 && curl -o /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

COPY app/ app/
COPY config/spark.conf /opt/spark/conf/spark-defaults.conf

RUN mkdir -p /opt/spark/logs \
    /opt/spark/checkpoints \
    /opt/spark/output \
    /opt/spark/.ivy2

ENTRYPOINT ["/opt/spark/bin/spark-submit"]
CMD ["--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1","app/stream_processor.py"]
