# System Architecture

## Overview

This project implements a **scalable, event-driven analytics platform** that supports **real-time ingestion, processing, search, and visualization**, along with **batch storage and analytics**.
The system is designed to handle high-volume event streams while keeping the architecture **modular, observable, and cloud-ready**.

The platform integrates:

* Streaming ingestion
* Distributed processing
* Search & analytics
* Workflow orchestration
* Cloud storage
* API-based access

All components are containerized and orchestrated using Docker Compose.

---

## High-Level Architecture

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ HTTP (Ingest / Query)
┌────▼─────┐
│ FastAPI  │
└────┬─────┘
     │ Events
┌────▼─────┐
│  Kafka   │
└────┬─────┘
     │ Stream
┌────▼─────────────────────┐
│Spark Structured Streaming│
└────┬──────────────┬──────┘
     │              │
 Raw Events      Aggregates
     │              │
┌────▼─────┐   ┌────▼────────┐
│    S3    │   │Elasticsearch│
└────┬─────┘   └────┬────────┘
     │              │
┌────▼─────┐   ┌────▼─────┐
│  AWS Glue│   │  Kibana  │
└──────────┘   └──────────┘

        ▲
        │
   ┌────┴────┐
   │ Airflow │
   └─────────┘
```

---

## Component Architecture

### FastAPI (API Layer)

**Role**

* Entry point for event ingestion
* Query layer on top of Elasticsearch
* Metrics and search endpoints

**Why FastAPI**

* Lightweight and fast
* Async-friendly
* Clean REST contracts

**Key Design Decision**
FastAPI is **additive**, not a replacement for Kibana.

* Kibana → visualization & exploration
* FastAPI → programmatic access & service-to-service queries

---

### Kafka (Event Streaming Layer)

**Role**

* Durable event buffer
* Decouples producers and consumers
* Enables horizontal scalability

**Why Kafka**

* High throughput
* Replayability
* Fault tolerance

Events are published by FastAPI and consumed by Spark in streaming mode.

---

### Spark Structured Streaming (Processing Layer)

**Role**

* Real-time event processing
* Windowed aggregations
* Data enrichment & validation

**Processing Outputs**

1. **Raw events** → S3
2. **Aggregated results** → Elasticsearch

**Key Design Decision**
Elasticsearch is accessed **via REST API**, not using a Spark connector, to:

* Reduce dependency coupling
* Improve security control
* Avoid connector version conflicts

---

### Amazon S3 (Data Lake)

**Role**

* Long-term storage for raw and aggregated data
* Source of truth for analytics

**Storage Strategy**

* Partitioned data
* Append-only writes
* Schema evolution supported

---

### AWS Glue (Metadata Layer)

**Role**

* Central schema registry
* Enables future querying via Athena or other engines

Glue catalogs datasets written by Spark into S3.

---

### Elasticsearch (Search & Analytics Engine)

**Role**

* Index aggregated event data
* Power fast search & metrics queries

**Security**

* Accessed using authenticated REST calls
* Credentials managed via environment variables

---

### Kibana (Visualization Layer)

**Role**

* Dashboards
* Real-time monitoring
* Exploratory analytics

Kibana remains the **primary visualization tool**, while APIs serve programmatic consumers.

---

### Airflow (Orchestration Layer)

**Role**

* Monitor Spark jobs
* Manage dependencies
* Retry & monitoring

**Used For**

* Batch reprocessing
* Backfills
* Controlled execution of pipelines

---

### Docker & Docker Compose (Infrastructure)

**Role**

* Local & reproducible environment
* Service isolation
* Simplified onboarding

**Characteristics**

* Containerized services
* Shared Docker network
* Persistent volumes for stateful components

---

## Deployment Architecture

* All services run in isolated containers
* Inter-service communication via Docker network
* Volumes mounted for:

  * Kafka data
  * Elasticsearch indices
  * Spark checkpoints
* Environment variables used for secrets and configs

---

## Architectural Principles

* **Decoupled components**
* **Scalable by design**
* **Failure-tolerant**
* **Cloud-portable**
* **Production-aligned**

---

## Why This Architecture Matters

* Supports **real-time + batch analytics**
* Aligns with **modern data engineering best practices**
* Mirrors **real production systems**
* Resume-ready and interview-strong

---