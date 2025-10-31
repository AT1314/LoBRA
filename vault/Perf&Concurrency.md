---
title: "Perf&Concurrency"
date: "2025-10-31"
source: "inbox/Perf&Concurrency.html"
format: "HTML"
converted: "2025-10-31 10:23:06"
---

# Perf and Concurrency

Performance Metrics

Problem of Tail-latency

Sources of latency variability

Software techniques to tame the tail

Memcached

**Network performance metrics**

# Performance Metrics

  * **Bandwidth [b/s]** – raw capacity of the link.

  * **Latency [s] = Propagation + Transmit + Queue + Overhead**.
    * Propagation = distance / speed-of-light in medium;
    * Transmit = object size (bits) / bandwidth;
    * Queue = time blocked behind other packets;
    * Overhead = CPU time to put a frame on the wire .

  * **Error-rate P** – probability a frame arrives corrupted .

Context| “Mega” means| Typical rate unit  
---|---|---  
Computer-architecture| 2²⁰ (1 048 576)| MB/s  
Computer-networks| 10⁶| Mb/s  
  
Remember: **Mbps (megabits/s)→network ≠ MBps (megabytes/s)→arch** ; throughput
< bandwidth because of headers, protocol overhead, etc.

  * **ping** → round-trip latency & liveness

  * **iperf3** → achievable bandwidth between two hosts & Times how long it takes to send N bytes to the other endpoint

# Problem of Tail-latency

  * Percentiles: p50 vs p90 vs p99 describe distribution tails .

  * **Amplification:** even if each server’s 99th-percentile is rare, a frontend waiting for many correlated sub-requests sees a _much_ higher chance one of them is slow, so user-level latency skews to the tail .

  * **Key observation:** ~5 % of hosts can contribute ~50 % of total latency

## Sources of latency variability

Shared local resources (CPU cores, caches, memory bw)

Global sharing (network switches, shared FS)

GC & background maintenance (log compaction, data rebuild)

Queueing in switches/servers

Power-limiting / DVFS transitions

Energy management

## Software techniques to tame the tail

Technique| Idea  
---|---  
**Hedged/tied requests**|  Send duplicate request to another server; keep
fastest, cancel the rest  
**Reduce head-of-line blocking**|  Split long ops into small ones  
**Synchronize disruption**|  Run background jobs all at once to confine impact  
**Service-class differentiation**|  Isolate latency-sensitive vs batch work  
**High-level queuing**|  Keep device-level queues short; prioritize early  
**Canary requests（Large IR Systems)**|  Probe a few “leaf” servers before
fanning out fully  
  
## Memcached

  * **Role:** in-memory key-value cache used to offload repeated DB queries (O(1) RAM lookup, LRU eviction) .

  * **Flow:** cache-hit returns immediately; cache-miss triggers DB query then stores result .

  * **Partition/aggregate risk:** a query that fans out to _S_ nodes must wait for the slowest; with μ = 90 µs, σ = 7 µs, increasing _S_ pushes user-visible latency into higher percentiles

