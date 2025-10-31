---
title: "Read_summary_w3"
date: "2025-01-27"
source: "inbox/Read_summary_w3.pdf"
format: "PDF Document"
pages: "4"
converted: "2025-10-31 10:24:37"
---

# Read_summary_w3

**Pages:** 4


## Page 1

Reading Summary Week 3
Angting Cai
Abstract
This reading summary covers the topics about GPU Performance from Nvidia and1
MI300X vs H100.2
1 GPU Performance Background User’s Guide3
1.1 Abstract4
This guide provides background on the structure of a GPU, how operations are executed, and common5
limitations with deep learning operations.6
1.2 Overview7
This guide covers the GPU Architecture Fundamentals, GPU Execution Model, Understanding8
performance, and DNN Operation Categories.9
1.3 GPU Architecture Fundamentals10
GPU is highly parallel which is composed of processing elements and a memory hierarchy. As shown11
in Figure 1, NVIDIA GPUs at a high level consist of a number of Streaming Multiprocessors(SMs),12
on-chip L2 cache and high-bandwidth DRAM. Each SM has its own instruction schedulers and13
various instruction execution pipelines.14
Different from NVIDIA CUDA cores, Tensor Cores were introduced in the NVIDIA V olta GPU15
architecture to accelerate matrix multiply and accumulate operations for machine learning and16
scientific applications. Tensor cores can compute and accumulate products in higher precision than17
the inputs. But it is restricted that the math operations should be able to be formulated in terms of18
matrix blocks.19
Figure 1: Simplified view of the GPU architecture

## Page 2

1.4 GPU Execution Model20
Threads are the smallest units of executing instructions in GPU. To utilize the parallel resources, GPU21
execute functions by first grouping threads into equally-sized thread blocks then launch the thread22
blocks. Also, to hide dependent instruction latency, GPU occasionally switch to the execution of23
other threads to effectively make use of each core.24
An SM is mapped from a thread block, which means that all threads within the same block work in25
the same SM and they can use the share memory resource in SM to cooperate. The number of thread26
blocks is usually set higher than the number of SMs to minimize the "tail" effect, which refers to the27
effect that at the end of the function execution only a few active thread blocks remain.28
1.4.1 Understanding Performance29
Performance of a function on a give processor is limited by one of the following three factors: memory30
bandwidth, math bandwidth, and latency.31
Assuming the memory access and math operations can be overlapped, the bottleneck is either the32
mem access or math operations. We can get the conclusion that on a given processor a given algorithm33
is math limited if34
#ops
#bytes > BWmath
BWmem
(1)
On the left hand side, it is known as the algorithm’s arithmetic intensity(AI). On the right hand side35
the ratio of a processor’s math and memory bandwidths is sometimes called ops:byte ratio. If only36
considering the arithmetic operations, most common operations have low AI. However, in practice37
we should consider other instructions such as memory access, address calculation and control flow38
instructions.39
The AI and ops:byte analysis assumes that a workload is sufficiently large to saturate a given40
processor’s math and memory pipelines. But if not, the processor will be under-utilized and the41
bottleneck will be the latency instead. Besides, the arithmetic intensity(AI) calculation assumes that42
inputs and outputs are accessed from memory only once but actually it is normal to read input elements43
multiple times, which will reduce AI to some degree. AI is more like a first-order approximation but44
not accurate enough in later investigation.45
1.4.2 DNN Operation Categories46
While modern NN are built from a variety of layers, their operations fall into three main categories47
Element-wise Operations, Reduction Operations, Dot-product Operations.48
1.4.3 Element-wise Operations49
Elementwise operations can be unary of binary operations. Layers in this category perform mathe-50
matical operations on each element independently of all other elements in the tensor.51
1.4.4 Reduction Operations52
Reduction operations produce values computed over a range of input tensor values.53
1.4.5 Dot-Product Operations54
Operations in this category can be expressed as dot-products of elements from two tensors, usually a55
weight tensor and an activation tensor. Convolution can be expressed as collections of dot-products56
as well. Meanwhile, operations in this category can be math-limited if the matrices are large enough.57
2 MI300X vs H10058
This passage talks about an independent analysis and training-focused benchmarking of the MI300X,59
the H100 and the H200 engaging with both NVIDIA and AMD, offering some suggestions to AMD60
to help them make some improvements in related fields.61
2

## Page 3

To solve the problem in AMD’s ecosystem about poor public software stack, the author’s team have62
open-sourced many of the benchmarks and created some one-liner commands to reproduce them.63
2.1 Key Findings64
H100/200 from Nvidia performs well and don’t need much support. While MI300X has a lot of bugs65
and with the support of AMD engineers the performance on the benchmarks are not falling to far66
away behind Nvidia’s. MI300X has a lower total cost of ownership(TCO) compared to H100/200, but67
training performance per TCO is worse on MI300X on public stable releases of AMD software. The68
benchmarking results on AMD are worse overall, due to some reasons like weaker ROCm Compute69
Communication Library(RCCL) and AMD’s lower degree of vertical integration with Networking70
and switching hardware compared to Nvidia’s NCCL and etc. Besides, many of AMD AI Libraries71
are forks of NVIDIA AI Libraries, leading to suboptimal outcomes and compatibility issues. And72
AMD’s products have worse flexity compared to Nvidia’s.73
2.2 Executive Recommendation to AMD74
First, AMD should offer their engineers more available compute and engineering resources. Second,75
more MI300X should be put into use to Pytorch CI/CD for automated testing. Third, focus more on76
testing products for the public. Fourth, cooperate more about Meta to get production LLM training77
workloads working. Besides, give a try on GPT-3 175B and do corresponding tests.78
2.3 A Summary of the AMD vs Nvidia Narrative79
MI300X, launched in late 2023, boasts superior on-paper specifications with 1,307 TFLOP/s of FP1680
compute, which outperforms Nvidia’s H100 and H200. One reason is that MI300X rely less on81
expensive Ethernet-based networking.82
The main disconnect between on-paper promise and market uptake came down to software and83
ecosystem readiness. Despite the MI300X’s compelling hardware profile and cost advantages, AMD’s84
software stack—and broader support for AI workloads—lagged Nvidia’s. This gap undermined the85
MI300X’s deployment traction and constrained AMD’s overall share gains in the data center GPU86
space.87
2.4 General Matrix Multiply (GEMM) Performance88
General Matrix Multiplication(GEMMs) is one of the most common operations. The performance on89
GEMMs is a good proxy for how well frontier transformers will train on the hardware.90
The BF16 benchmark results reveal that despite higher theoretical peak throughput, the MI300X is91
about 14% slower than H100/H200. For FP8 tests, MI300X is slower as well. Some software bugs92
and library choices are potentially the reason for the gap.93
2.5 Popular GEMM Benchmark Isn’t Accurate94
The popular GEMM Benchmark isn’t that accurate. One reason is that it didn’t carry out L295
Cache clearing between iterations. Another is that it only took the max performance instead of the96
median/mean.97
2.6 HBM Memory Bandwidth Performance98
Improving the HBM memory bandwidth can help set a larger batch size but it will hurt time to99
convergence.100
2.7 AMD Hand-Crafted VIP Custom Builds and WIP Development Builds101
During the process of testing with AMD, a lot of Docker images have been built to ensure the102
environments, which is different from Nvidia that can provide pre-built stable release. The version of103
PyTorch that AMD engineers are working with are still a bit lagging.104
3

## Page 4

2.8 Training Testing Methodology105
The most accurate method is to take a medium-sized AI startup model’s internal codebases and run106
them on a 512-1024 GPU cluster. MLPerf GPT3 175B Training is also a good proxy to measure the107
time it takes to train to a specific convergence. The design of SemiAnalysis benchmark involves:108
model choices (GPT 1.5B DDP, Mistral 7B, etc), simplicity, reproducibility, batch size differences109
and parallelism.110
2.9 Single Node Training111
MI300X doesn’t perform well on smaller models like GPT 1.5B or any model that uses a non-casual112
attention layer, like Mistral 7B v0.1. Overall MI300X doesn’t perform well against H100/200 before113
applying many (bug) fixes. But it should be remembered not to use MI300X for non-casual attention114
layer.115
2.10 Multi-Node Training116
H100 wins MI300X. And this gap widens as you add more nodes working together into a single117
training workload.118
2.11 AMD PYTORCH_TUNABLE_OPS FLAG is a Bad User Experience119
The required feature PYTORCH_TUNABLE_OPS makes the user experience poor because it is a120
new feature that has a lot of potential bugs. Besides the bugs, the tool is still hard to use and especially121
time-consuming which make things annoying.122
2.12 Scale Up NVLink/xGMI Topology123
Considering the Scale up fabric, the MI300X’s xGMI can’t actually provide 448GBytes/s because it124
is a point-to-point fabric. While Nvidia uses a switched topography ensuring the high bandwidth per125
GPU.126
2.13 Exploring Ideas for Better Performance on AMD127
It is recommended that AMD should partner with Docker and ensure that Docker can autodetect128
GPUs for AMD as well, making the workflow as streamlined as when working with Nvidia GPUs.129
2.14 AMD’s Forked Libraries130
AMD builds a translation tool called Hipify to translate Nvidia CUDA to AMD HIP. After all CUDA131
is built on the Nvidia ecosystem which is not always proper for the AMD ecosystem. AMD should132
try to build their own software.133
References134
[1] https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/135
index.html136
[2] https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/137
#scale-up-nvlinkxgmitopology138
[3] Chatgpt O1139
4