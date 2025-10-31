---
title: "Read_summary_w9"
date: "2025-10-09"
source: "inbox/Read_summary_w9.pdf"
format: "PDF Document"
pages: "4"
converted: "2025-10-31 10:24:35"
---

# Read_summary_w9

**Pages:** 4


## Page 1

Reading Summary Week 9
Angting Cai
Abstract
This reading summary covers the topics about Paged Attention and Flash Attention.1
1 Efficient Memory Management for Large Language Model Serving with2
PagedAttention3
1.1 Intro & Motivation4
Large Language Models(LLMs) like GPT is used today handling a high volume of requests, which is5
costly and challenging. One main problem is about the Key-Value Cache. When managed inefficiently,6
memory can be wasted by fragmentation and redundant duplication - limiting the batch size and7
capping the overall throughput. The paper proposes PagedAttention inspired by OS virtual memory8
and paging techniques. Meanwhile, an end-to-end LLM serving system(a high-throughput distributed9
LLM serving engine) - vLLM is built on top the attention algorithm to resolve critical issues and10
boost serving throughput. Overall it achieves:11
• near-zero waste in KV cache memory and12
• flexible sharing of KV cache within and across requests to further reduce memory usage.13
By examining the existing LLM serving systems, the authors find some problems:14
• Large and Dynamic Memory Footprint: A 13B-parameter LLM can use up to 30% of GPU15
memory just for the KV cache. Figure 1 compares the memory wastes.16
• Fragmentation & Duplication: Existing serving systems store the KV cache in contiguous17
memory chunks, which causes severe internal and external fragmentation.18
• Resulting Low Utilization: Often only 20–38% of the KV cache memory is used effectively.19
By dividing the KV cache into blocks and using virtual memory - no need to have contiguous space,20
the KV cache can be managed in a more flexible way and alleviates internal fragmentation and21
removes external fragmentation. Built on top of PagedAttention, vLLM uses block-level memory22
management and preemptive request scheduling that are co-designed with PagedAttention, supporting23
LLMs like GPT, OPT, LLaMA with various sizes, serving 2-4x throughput, outperforming the24
previous state-of-theart solutions such as FasterTransformer and Orca.25
1.2 Background26
1.2.1 Transformer-based models & LLM Service & Autoregressive Decoding27
Basically, LLMs generate text in an autoregressive manner. Specifically, each generated token28
depends on all previously generated tokens. And during inference, the model caches the KV vectors29
from previous tokens for fast lookup.30

## Page 2

Figure 1: Memory Waste
1.2.2 Batching Techniques for LLMs31
The batching technique is able to batch requests to increase the ultilization of GPU - Amortizing32
the cost of model weight accesses. Even though fine-grained scheduling can significantly improve33
efficiency, it still needs an efficient memory manager for the large and dynamically sized KV cache.34
1.3 Memory Challenges in LLM Serving35
When the LLM is serving, there are some challenges:36
• KV Cache usage grows overtime, as decoding proceeds.37
• Some techniques like beam search and multiple sampling per request would produce KV38
that share the cache.39
• Also, the input of the prompts are unknown - the memory usage is unmanageable.40
Another big problem existing in the current systems is: the allocation of the cache is contiguous - the41
allocation of buffer for each request’s maximum length is inefficient.42
• Reserved Space: Pre-allocating space for future tokens forces large memory holds.43
• Internal Fragmentation: Requests often end before hitting their maximum length, leaving44
large unused spaces.45
• External Fragmentation: If each request gets differently sized contiguous chunks, memory46
“holes” form over time.47
1.4 The PagedAttention Approach & vLLM System48
1.4.1 PagedAttention Algorithm49
The core concept of this algorithm is based on OS virtual memory paging. It partitions the KV cache50
for each sequence into fixed-size blocks. While the blocks don’t have to be stored contiguous in51
memory - improve the flexibility. During attention, the query vectors are multiplied with key/value52
blocks (pages) via a specialized kernel that accesses them non-contiguously.53
The algorithm manages to eliminate both internal and external fragmentation. Meanwhile, multiple54
sequences can reference shared blocks without duplicating memory.55
1.4.2 KV Cache Manager56
The manager for KV Cache manages the actual GPU memory for those blocks. It also maintains57
block tables that map each request’s “logical” blocks to the “physical” blocks actually allocated in58
2

## Page 3

GPU memory. It allocates new blocks on demand as tokens are generated, rather than reserving them59
ahead of time.60
1.4.3 Decoding with PagedAttention & vLLM61
The entire procedure of decoding LLM prompt with PagedAttention & vLLM are in mainly three62
phases:63
• Prompt Phase: Process the initial user prompt and store the resulting KV in the cache’s64
blocks.65
• Autoregressive Phase: Tokens are generated one-by-one. And if the last block is full it66
will allocate a new one. Meanwhile, vLLM updates the block table accordingly. The67
PagedAttention kernel queries all relevant blocks for the self-attention computation.68
• Completion Phase: Once the sequence ends, the blocks are freed for use by other requests.69
During this procedure, because blocks are uniform and only partially allocated at runtime, KV cache70
usage is nearly perfectly matched to a sequence’s actual length.71
1.4.4 Complex Decoding Scenarios72
For parallel sampling and Beam search, the system tracks the blocks references carefully so that73
common parts are not necessarily duplicated.74
1.4.5 Scheduling & Handling Variable-Length Requests75
The system do iteration-level scheduling, improving the throughput by letting new requests in after76
each generation step. Meanwhile, the memory & swapping is dynamic - the system can swap blocks77
to CPU RAM and bring them later is the usage of GPU is tight, minimizing overhead.78
1.4.6 Distributed Setting79
The vLLM applies sharded GPU usage and work. And it has a central scheduler to coordinate with80
GPU workers. Also, the KV cache manager works on ensuring consistent block allocations across81
GPUs.82
2 FlashAttention: Fast and Memory-Efficient Exact Attention with83
IO-Awareness84
2.1 Motivation & Background85
Current attention mechanisms used in Transformer usually requires storing large intermediate tensors,86
which also lead to high memory bandwidth usage. Much work have been done about the trade-off in87
attention:88
• Exact vs. Approximate: Approximate attention aims to reduce the model complexity by89
approximations, but it leads to low accuracy.90
• Memory vs. Time: Other methods reduce memory usage by recomputing some parts of91
attention on the fly, which increases computation time.92
The paper proposes FLASH Attention, an exact, low-memory, and fast attention method that does not93
compromise on model quality or require large recomputation overhead.94
2.2 Core Idea of FlashAttention95
FlashAttention is based on the insight that I/O dominates runtime when sequence lengths are large.96
The authors propose to restructure attention computation to minimize these costly memory opera-97
tions—particularly reading/writing large intermediate matrices—from GPU DRAM.98
3

## Page 4

2.2.1 Chunked, Tile-based Attention99
Rather than computing the entire matrix at one time, the queries and keys are processed in blocks.100
Instead of read/write from GPU DRAM, it uses GPU SRAM(Shared Memory) which is faster and101
more bandwidth-efficient. Meanwhile, it carries out streaming Softmax Computation, reducing102
intermediate memory storage. Finally, it only writes out the final Attention weighted matrix, instead103
of also keeping the intermediates in DRAM.104
2.3 Technical Highlights105
The FlashAttention manages to provide great:106
• Memory Efficiency107
• Speedups108
• Exactness109
• Scalability110
• Usage of half-precision floating points111
References112
[1] Kwon, Woosuk, et al. "Efficient memory management for large language model serving with pagedattention."113
Proceedings of the 29th Symposium on Operating Systems Principles. 2023.114
[2] Dao, Tri, et al. "Flashattention: Fast and memory-efficient exact attention with io-awareness." Advances in115
neural information processing systems 35 (2022): 16344-16359.116
[3] ChatGPT: OpenAI. (2023). ChatGPT [Large language model]. Retrieved from https://chat.openai.com/117
4