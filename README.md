# microengine-io

## High-Throughput Limit Order Book Matching Engine & Microstructure Liquidity Monitor

MicroEngine.io is a performance-optimized, in-memory electronic trading matching engine simulation built to track market microstructure dynamics and compute liquidity volatility analytics in real-time. 

## Architecture & Performance Mechanics
* **$O(\log N)$ Matching Loop:** Uses `sortedcontainers.SortedDict` to bypass slow tabular databases, maintaining algorithmic price-time priority structures natively in-memory.
* **Quantitative Liquidity Metrics:** Real-time generation of Order Book Imbalance (OBI) skews to capture supply/demand manipulation.
* **Structural Liquidity Anomaly Engine:** Tracks structural rolling historical windows to monitor sudden drops in market depth, flashing immediate alerts if institutional order cancellations sweep out liquidity.

## Project Structure
```text
microengine-io/
├── engine/               # Core low-latency matching state machine
│   ├── order.py          # Data definitions using __slots__ optimization
│   ├── order_book.py     # O(log N) Sorted Dict Bid/Ask queues
│   └── matching_engine.py# Atomic execution loops
├── analytics/            # High-Frequency financial metric processors
│   └── anomaly_engine.py # Volatility scanners and OBI computation
├── data/                 # Systematic tick generators & shock simulators
│   └── market_simulator.py
└── app.py                # High-end operational cockpit UI panel
