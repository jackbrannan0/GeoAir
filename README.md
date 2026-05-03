GeoAir Intelligence Platform
GeoAir is a high-performance, real-time predictive alerting system designed to track aviation assets against dynamic geopolitical and environmental risk zones. By leveraging low-level systems programming in Rust and asynchronous spatial processing in Python, GeoAir identifies direct and projected trajectory risks as geopolitical events unfold globally.

🔑 Core Architecture Highlights
The platform uses a Layered Shared-State Monolith architecture to ensure high concurrency, low latency, and efficient resource allocation:

High-Frequency Ingestion: Built in Asynchronous Rust (Tokio, Reqwest) to ingest and serialize raw aircraft state vectors at 10-second intervals completely outside the Python Global Interpreter Lock (GIL).

Cross-Language Interop: Employs PyO3 and Maturin to expose the high-speed Rust parsing layer natively to the Python ecosystem.

Time-Series Persistence: Uses TimescaleDB on top of PostgreSQL for compressed, high-throughput hypertable storage and optimized spatial PostGIS indexing.

Spatiotemporal Predictive Engine: An analytics layer written in Python using Shapely that converts unstructured geopolitical news alerts (GDELT/NewsAPI) into geocoded risk zones, projecting aircraft convex hulls to predict intersection trajectories.

🏗️ System Design
The diagram below outlines the end-to-end data processing pipeline, showcasing how data flows continuously from upstream APIs through the low-latency processing layer to the client dashboard:

Ingest: Rust workers poll the OpenSky Network REST API and stream flight state vectors into local memory.

Process: The Python engine evaluates sentiment and geocodes geopolitical risks via NLP.

Correlate: PostGIS handles spatial queries to compute current and 30-minute predictive flight trajectory intersections with active risk zones.

Publish: Spatial updates and trajectory alerts are pushed instantly to the client-facing map using WebSockets.

🛠️ Tech Stack
Low-Level Execution: Rust (Tokio, Serde, PyO3)

Backend & Analytics: Python 3.11+ (FastAPI, Pydantic, Shapely, HuggingFace Transformers)

Database: PostgreSQL with TimescaleDB & PostGIS extensions

Frontend: Vanilla JavaScript / React, Leaflet.js

Infrastructure: Docker Compose

🚀 Key Learning Objectives & Challenges Solved
Solving the GIL bottleneck: Offloaded CPU-heavy network parsing to native Rust code.

Efficient Spatiotemporal Queries: Implemented ST_DWithin and specialized GIST indexes in PostGIS to perform real-time proximity lookups over millions of time-series points.

Predictive Risk Modeling: Moving beyond simple location tracking to construct dynamic Convex Hulls based on velocity, heading, and timing constraints.