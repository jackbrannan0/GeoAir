GeoAir is a real-time system that tracks aircraft and flags potential risks based on live geopolitical events and environmental factors. It combines fast data ingestion with spatial analysis to predict when a flight might intersect with a developing risk zone.
How it works
The system runs as a single backend with shared state, designed for speed and simplicity.
Flight data ingestion (Rust)
A Rust layer pulls aircraft data every ~10 seconds and processes it efficiently without Python’s performance limits.
Analysis layer (Python)
Python handles the higher-level logic—processing news, extracting relevant events, and turning them into geographic risk zones.
Storage (PostgreSQL + extensions)
Flight and event data are stored in a time-series setup, with spatial indexing to make location-based queries fast.
Prediction engine
The system projects aircraft paths forward and checks if they’re likely to intersect with active risk zones.
Live updates
Results are pushed to a frontend map in real time.
Tech stack
Rust (Tokio, Serde) for high-speed ingestion
Python (FastAPI, Shapely) for analysis and APIs
PostgreSQL with TimescaleDB + PostGIS for storage and spatial queries
JavaScript / React + Leaflet for the frontend
What makes it interesting
Uses Rust where performance actually matters
Handles both time-series and spatial data efficiently
Moves beyond tracking to predicting potential conflicts
Mixes real-world data sources (aviation + geopolitics) into one system
