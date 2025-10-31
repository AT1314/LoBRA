---
title: "GPU"
date: "2025-10-31"
source: "inbox/GPU.md"
format: "Markdown"
processed: "2025-10-31 10:24:36"
---

# 1.21

# GPU hierarchy

Kernel → Threads → Blocks → Grids

More cores → More streaming multiprocessor(SM) → More Powerful → More Flops

![image.png](1%2021/image.png)

- A **GPU core** executes instructions for **CUDA threads**, but it cannot execute all threads simultaneously.
- Threads are executed in **warps** (groups of 32 threads in NVIDIA GPUs). A warp of threads is scheduled to run on a group of cores in a streaming multiprocessor (SM).
- Over time, the GPU's cores time-slice through the massive number of threads, giving the impression of running all threads simultaneously.

Threads are software abstractions

Sync CPU and GPU if needed

**Threads is Explicit and Static in Programs**

**Checkboundaryconditions**

- Handling Control Flow: Masking
- Coherent vs. Divergent(Should be minimized)
**Language model masking, sliding window attention**
- HBM → GPU memory   DRAM → CPU memory

![image.png](1%2021/image%201.png)

**cudaMemcpy**

**Pinned Memory**

![image.png](1%2021/image%202.png)

![image.png](1%2021/image%203.png)

→ Use of shared memory

## Synchronization primitives

![image.png](1%2021/image%204.png)

**Oversubscription**

DEEP DIVE OF CUDA scheduling

SRAM in GPU is critical (SM’s shared memory)