# Data Flow Documentation

## Purpose

This document explains **how data moves through the system**, step by step, from ingestion to analytics and visualization.  
It focuses on **runtime behavior**, not implementation details.

---

## 1️⃣ Event Ingestion Flow (Real-Time)

### Step 1: Event Creation
- Client applications generate user events (e.g., login, click, purchase).
- Events are sent as JSON payloads.

### Step 2: FastAPI Ingestion
- FastAPI receives events via HTTP endpoints.
- Basic validation is applied.
- Events are forwarded to Kafka.

**Why**
- Stateless
- Scales horizontally
- Clean API boundary

---

## 2️⃣ Streaming Layer (Kafka)

### Step 3: Kafka Buffering
- Events are published to Kafka topics.
- Kafka ensures:
  - Durability
  - Backpressure handling
  - Event replay

**Key Benefit**
Producers and consumers are fully decoupled.

---

## 3️⃣ Stream Processing (Spark)

### Step 4: Spark Reads from Kafka
- Spark Structured Streaming consumes Kafka topics.
- Events are read in micro-batches.
- JSON is parsed into structured columns.

---

### Step 5: Bronze Zone Write (Raw Events)

**What Happens**
- Raw events are written directly to S3.
- Data is:
  - Immutable
  - Append-only
  - Partitioned by date

**Purpose**
- Debugging
- Reprocessing
- Auditing

---

### Step 6: Silver Zone Processing (Aggregations)

**What Happens**
- Spark performs:
  - Windowed aggregations
  - Event counts
  - User activity metrics

**Output**
- Clean, aggregated datasets
- Written back to S3 (Silver zone)
- Also streamed to Elasticsearch

---

## 4️⃣ Storage & Analytics Flow (Batch)

### Step 7: S3 as Data Lake
- S3 holds:
  - Bronze (raw events)
  - Silver (aggregated metrics)

**Characteristics**
- Cheap storage
- Infinite scalability
- Source of truth

---

### Step 8: AWS Glue Catalog
- Glue crawlers scan S3 paths.
- Schemas are inferred automatically.
- Tables are registered in the Data Catalog.

**Result**
- Data becomes queryable
- Schema evolution supported

---

## 5️⃣ Search & Visualization Flow

### Step 9: Elasticsearch Indexing
- Aggregated metrics are indexed via REST API.
- Each batch is written using bulk indexing.
- Index mappings are auto-created.

**Why Elasticsearch**
- Low-latency queries
- Aggregations
- Full-text search

---

### Step 10: Kibana Dashboards
- Kibana reads from Elasticsearch.
- Dashboards show:
  - Active users
  - Event trends
  - Time-based metrics

---

## 6️⃣ Orchestration Flow (Airflow)

### Step 11: Airflow Scheduling
- Airflow DAGs:
  - Trigger Spark jobs
  - Handle retries
  - Manage dependencies

**Important**
Airflow orchestrates — it does not process data.

---

## 7️⃣ Query Flow (FastAPI Analytics)

### Step 12: Analytics Queries
- FastAPI exposes read-only APIs.
- Queries Elasticsearch only.
- API-key based authentication.

**Example Endpoints**
- `/metrics/active-users`
- `/metrics/events-by-type`
- `/metrics/event-count`
- `/metrics/activity-window`

---

## Failure & Recovery Handling

### Kafka Failure
- Events remain in topic
- Consumers resume from offsets

### Spark Failure
- Checkpoints ensure exactly-once semantics
- Job resumes without data loss

### Elasticsearch Failure
- Spark retries indexing
- Data still safely stored in S3

---

## Key Design Guarantees

- At-least-once ingestion
- Exactly-once Spark processing
- Immutable raw data
- Reprocessable pipeline
- Independent read & write paths

---

## Summary

This data flow ensures:
- Real-time insights
- Reliable storage
- Debuggable pipelines
- Production-grade analytics

The system cleanly separates **ingestion**, **processing**, **storage**, **search**, and **serving** layers.