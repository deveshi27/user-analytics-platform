# Real-Time Analytics Platform

## Overview

This project is a production-grade, end-to-end real-time analytics platform built using modern data engineering and backend technologies.
It ingests streaming events, processes them in real time, stores raw and aggregated data, enables fast search and visualization, and exposes clean analytics APIs.

The architecture is modular, scalable, fault-tolerant, and aligned with industry best practices.

---

## High-Level Architecture

- Real-time path
Kafka → Spark → Elasticsearch → Kibana
↓
FastAPI

- Batch / analytical path
Kafka → Spark → S3 (Bronze / Silver) → Glue → Athena (optional)

---

## Tech Stack

- API: FastAPI – ingestion and analytics APIs
- Streaming: Kafka – event streaming and buffering
- Processing: Spark Structured Streaming – real-time processing and aggregation
- Storage: Amazon S3 – data lake (Bronze and Silver)
- Metadata: AWS Glue – schema and table catalog
- Search: Elasticsearch – low-latency analytics
- Visualization: Kibana – dashboards and monitoring
- Orchestration: Airflow – Monitoring and sceduling
- Infrastructure: Docker & Docker Compose – reproducible local setup

---

## Project Folder Structure

This repository follows a **service-oriented, production-style layout**.  
Each top-level directory represents a **clear responsibility boundary**.

```
├── analytics-api/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py              # Environment & service configuration
│   │   │   └── security.py            # API-key authentication logic
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py          # Service health check endpoint
│   │   │       └── metrics.py         # Analytics & metrics endpoints
│   │   ├── services/
│   │   │   └── elastic_client.py      # Elasticsearch REST client
│   │   ├── schemas/
│   │   │   └── responses.py           # API response models
│   │   └── main.py                    # FastAPI application entrypoint
│   ├── Dockerfile                     # Container definition
│   └── requirements.txt               # Python dependencies
│
├── ingestion-service/
│   ├── app/
│   │   ├── main.py                    # API entrypoint
│   │   ├── kafka_producer.py          # Kafka producer logic
│   │   ├── models/
│   │   │   └── event_schema.py        # Event validation schemas
│   │   └── routers/
│   │       └── events.py              # Event ingestion endpoints
│   ├── Dockerfile                     # Container definition
│   └── requirements.txt               # Python dependencies
│
├── spark-streaming/
│   ├── app/
│   │   ├── stream_processor.py        # Main Spark streaming job
│   │   ├── schemas.py                 # Event schemas
│   │   ├── aggregations.py            # Windowed aggregation logic
│   │   └── es_writer.py               # Elasticsearch REST writer
│   ├── config/
│   │   └── spark.conf                 # Spark, S3 & Elasticsearch configuration
│   ├── Dockerfile                     # Spark runtime container
│   └── requirements.txt               # Python dependencies
│
├── infra/
│   ├── docker-compose.yml             # All services wiring
│   └── .env                           # Runtime environment variables (gitignored)
│
├── airflow/
│   └── dags/
│       └── spark_streaming_dag.py     # DAG to trigger and monitor Spark jobs
│
├── docs/
│   ├── architecture.md                # System architecture and design decisions
│   └── data-flow.md                   # Step-by-step data flow explanation
│
└── README.md                           # Project overview, setup, and usage guide
```
---

### Why This Structure Works

- Clear separation of concerns  
- Independent service scaling  
- Easy onboarding  
- Mirrors real production repositories  
- Interviewer-friendly and readable  

---

## Data Lake Structure (S3)
```
s3://user-analytics-datalake/
bronze/
user_events/date=YYYY-MM-DD/
silver/
user_metrics/date=YYYY-MM-DD/
checkpoints/
```

Bronze contains raw, immutable events.
Silver contains aggregated, query-ready metrics.

---

## Key Features

- Real-time event ingestion
- Windowed aggregations
- Immutable raw data storage
- Searchable metrics in Elasticsearch
- Interactive dashboards in Kibana
- Read-only analytics APIs
- Secure, containerized setup
- Resume-grade system design

---

## How to Run (High Level)

```bash
cd infra
docker compose build
docker compose up -d
```
All services start together in a single network.

---

## Service Access

- FastAPI(analytics-api service): [http://localhost:9000](http://localhost:9000)
- FastAPI(ingestion-service): [http://localhost:8000](http://localhost:8000)
- Kibana: [http://localhost:5601](http://localhost:5601)
- Elasticsearch: [http://localhost:9200](http://localhost:9200)
- Airflow: [http://localhost:8080](http://localhost:8080)

---

## Analytics API (FastAPI)

All analytics APIs are read-only and backed by Elasticsearch.

Available endpoints:

- `GET /health`
- `GET /metrics/active-users`
- `GET /metrics/events-by-type`
- `GET /metrics/event-count`
- `GET /metrics/activity-window`

- Authentication is handled using an API key passed via the `x-api-key` header.

---

## Design Principles

- Loose coupling between services
- Clear separation of ingestion, processing, storage, and serving
- Immutable raw data for replayability
- Independent batch and real-time paths
- Docker-first development
- Cloud-ready (EC2 / EMR / EKS compatible)

---

## Project Phases

- Phase 1: Kafka setup
- Phase 2: Spark streaming
- Phase 3: Aggregations
- Phase 4: Airflow orchestration
- Phase 5: S3 data lake (Bronze / Silver)
- Phase 6: Glue and Athena
- Phase 7: Elasticsearch and Kibana
- Phase 8: FastAPI analytics service

---
