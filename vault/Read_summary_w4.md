---
title: "Read_summary_w4"
date: "2025-02-02"
source: "inbox/Read_summary_w4.pdf"
format: "PDF Document"
pages: "7"
converted: "2025-10-31 10:24:36"
---

# Read_summary_w4

**Pages:** 7


## Page 1

Reading Summary Week 4
Angting Cai
Abstract
This reading summary covers the topics about TVM and Triton.1
1 TVM2
1.1 Abstract3
The paper is aimed to address the challenges of deploying deep learning(DL) models across diverse4
hardware platforms efficiently. The writers propose a solution of TVM, an optimizing compiler that5
automates performance potability via graph-level and operator-level optimization, solves DL-specific6
challenges such as operator fusion and memory latency hiding, and uses learning-based cost modeling7
to rapidly explore hardware-specific code optimizations.8
As for the results, TVM matches or even outperforms hand-tuned libraries on CPUs, GPUs and9
other hardware. It also enables efficient deployment to new accelerators. Most importantly, it is10
open-sourced and has been adopted in industry. It bridges the gap between ML models and diverse11
hardware, reducing manual effort while achieving state-of-art performance.12
1.2 Introduction13
There is a growing demand that DL models need feployment across diverse hardware. But current14
frameworks, such as TensorFlow, MXNet, Caffe, and PyTorch, rely on a computational graph IR to15
implement optimizations. They focus on vendor-specific libraries optimized for server-class GPUs.16
Besides the hardware diversity, challenges like significant manual optimizations and the trade-offs17
between limiting optimizations or using unoptimized code.18
TVM builds a compiler stack that mainly solves:19
• Leveraging Specific Hardware Features and Abstractions.20
• Large Search Space for Optimization21
It addresses these challenges with three key modules: (1) Tensor Expression Language: Declarative22
operator definitions with hardware-agnostic transformations. (2) ML-Based Auto-Tuning: Learns23
cost models to efficiently explore optimization configurations. (3) Graph Rewriter: Jointly optimizes24
graph- and operator-level transformations.25
Based on these, TVM manages to perform joint high- and low-level optimizations and generate26
hardware-specific optimized code for diverse hardware backends.27
Conclusively, it has made contributions including:28
• Identifies optimization challenges for DL performance portability.29
• Introduces new schedule primitives for cross-thread memory reuse, hardware intrinsics, and30
latency hiding.31
• Proposes ML-guided auto-tuning to automate operator optimization.32
• Builds an end-to-end compiler(compilation and optimization stack) supporting major DL33
frameworks (TensorFlow, PyTorch) and hardware backends.34

## Page 2

1.3 Overview35
As shown in Figure 1, TVM accepts models from existing DL frameworks and converts them into a36
computational graph representation. Then, it performs high-level optimization by doing the graph-37
level optimizations to simplify the computation. After that, it starts the operator-level optimizations,38
which includes Declarative Tensor Expressions and Hardware-Aware Optimization Primitives(to do39
automated code generation using an ML-based cost model). Finally, it packages the optimized graph,40
generated operators(lib) and model parameters into a portable runtime module for deployment.41
Some key features of TVM:42
• End-Use Simplicity43
• Cross-Language Support44
• Extensibility45
Figure 1: System Overview of TVM
1.4 Optimizing Computational Graphs46
Computational Graphs represents DL models as dataflow graphs where nodes are tensor operations47
and edges are data dependencies. Here the paper focuses on optimizing large, multi-dimensional48
tensors, unlike low-level IRs like LLVM. TVM implements many graph-level optimizations including49
operator fusion, constant-folding, static memory planning, and data layout transformation.50
Operator fusion and constant-folding have been discussed in class. Static memory planning pre-51
allocates memory for intermediate tensors to avoid dynamic allocation overhead. While data layout52
transformation converts tensor layouts to match hardware preferences. During these implementations,53
we should notice that the existing frameworks require handcrafted implementations for fused operators54
which is unsustainable for diverse hardware.55
After discussing the high-level optimizations, TVM also automates code generation for operators,56
enabling flexible optimization across diverse backends, which will be discussed in the later sections.57
1.5 Generating Tensor Operations58
TVM produces efficient code for each operator by generating many valid implementations on each59
hardware backend and choosing an optimized version. The idea of decoupling descriptions from60
computation rules or schedule optimizations from Halide is used here.61
2

## Page 3

Tensor Expression Language is used to automatically generate low-level codes.. Operations are62
defined as index formulae and each tensor operation specifies the output shape and the computation63
pattern for clear DL work. Also, the decoupling of computation enables flexibility and easy integration64
of hardware-specific optimizations.65
As for schedule space, a schedule maps a tensor expression to low-level code through a series of66
basic transformation primitives, which maintain the logical equivalence of the program. Figure
Figure 2: TVM scheduling and schedule primitives
67
2 summarizes the operation code generation process and schedule primitives that TVM supports.68
TVM’s scheduling infrastructure, inspired by Halide, is extended with new primitives that support69
advanced optimizations such as nested parallelism, cooperative data fetching, and explicit latency70
hiding. The concept of memory scopes is introduced when discussing the cooperative data fetching.71
While Latency hiding refers to the process of overlapping memory operations with computation to72
maximize utilization of memory and compute resources. And it requires different strategies depending73
on the target hardware back-end.74
For Tensorization, analogous to vertorization for SIMD, tensorization replaces tensor computations75
with tensor hardware intrinsics. It is made extensible by using the tensor expression language to76
declare both the behavior of each new hardware intrinsic and the associated lowering rule. With77
tensorize schedule primive, this decoupling from fixed primitives ensures that the system can easily78
integrate new accelerators and benefit from handcrafted micro-kernels when necessary.79
1.6 Automating Optimization80
Considering the large search space of operator implementations for each hardware backend, an81
automated schedule optimizer is designed: consisting of a schedule explorer and a ML-based cost82
model responsible for prediction.83
TVM provides a template API where developers can specify the configurable "knobs" in the schedul-84
ing space. Base on it, the optimizer can start to search over the billions of possible configs.85
Instead of using blackbox optimization or predefined analytical models, TVM employs a statistical86
ML approach - a cost model that is trained on runtime measurement data to predict the relative87
performance of different schedule configurations. By using a ranking objective rather than absolute88
time predictions, the model efficiently guides the search for optimal configurations. This ML model89
is periodically updated with new data, improving its accuracy over time.90
In the schedule explorer, instead of exhaustively evaluating every possibility, a parallel simulated91
annealing algorithm is employed. Starting by a random walk in the config space, based on the92
performance data the future iterations will favor moves predicted to lower the cost(A kind of93
convergence). The models get refined continuously in this process.94
To scale the optimization process, TVM builds a distributed device pool with RPC(s).95
1.7 Evaluation96
TVM’s core is implemented in C++. Bindings are provided to Python and Java. The evaluations are97
run on Server-Class GPU, embedded CPU, embedded GPU and FPGA Accelerator.98
3

## Page 4

1.8 Related-work & Conclusion99
TVM is a great end-to-end optimization stack to realize automated end-to-end optimization in Deep100
learning.101
2 Triton102
2.1 Abstract103
The motivation of Triton is: The need for efficient compute kernels in deep learning, especially for104
operations that cannot leverage existing vendor libraries such as cuBLAS and cuDNN, which are105
suffering from poor device utilization without custom implementations written by experts. New106
abstractions for specifying custom DL workloads at a minimal performance cost are needed.107
Triton, a language and compiler centered around the concept of tile is presented. It employs:108
• A C-based language coupled with an LLVM-based intermediate representation (IR) that109
allows tensor programs to be expressed in terms of operations on parametric tile variables.110
• Novel tile-level optimization passes that compile these programs into efficient GPU code.111
With Triton, developers can build portable and high-performance implementations of crucial DL112
primitives like Matmul and Convolution kernels. It is also competitive with hand-tuned vendor113
libraries and are flexible enough to support recent research like shift convolutions.114
2.2 Introduction115
Motivation: The development of Deep Neural Networks(DNNs) is due to high-performance, pro-116
grammable parallel computing architectures like GPUs and vendor libraries like cuBLAS. But these117
libraries cover only a restricted set of tensor operations, leaving the implementation of novel primi-118
tives to expert. Existing Domain-Specific Languages(DSLs) and loop synthesis tools do generally119
perform well in some cases but areslower than vendor librariesin practice, and lack the expressivity120
necessary to build structured sparsity patterns as well.121
Previous trials: One of the trials is to use micro-kernels. But it requires much manual effort and122
lacks portability. Besides that, although recent high-level tiling abstractions have emerged, underlying123
compiler backends still struggle to support tile-level operations and optimizations.124
Hence, Triton, an open-source itermediate language and compiler specifying and compiling tile125
programs into efficient GPU code, is proposed.126
Overview of Triton and the evaluation part is shown in Figure 1 and summarized as below:
Figure 3: Overview
127
4

## Page 5

• Triton-C: A C-like language that expresses tensor programs using parametric tile variables,128
offering a familiar interface for CUDA programmers and integration with existing DNN129
transcompilers.130
• Triton-IR: An LLVM-based intermediate representation tailored for tile-level analysis,131
transformation, and optimization.132
• Triton-JIT: A Just-In-Time compiler that converts Triton-IR into efficient LLVM bitcode133
through a series of tile-level machine-independent and machine-dependent optimization134
passes, including an auto-tuner for meta-parameter optimization.135
The authors do Numerical Experiments - Evaluations demonstrating that Triton can match or136
exceed the performance of established libraries (such as cuBLAS and cuDNN) for tasks like matrix137
multiplication and convolution, and can effectively implement novel research ideas (e.g., shift138
convolutions).139
2.3 Related Works140
Some related work in DL compilation can be grouped into mainly three approaches:141
• Tensor-level IRs142
• Polyhedral Model143
• Loop Synthesizers144
By contrast, Triton introduces tile-level operations and optimizations within the traditional com-145
pilation pipeline, offering pros including flexibility, support for non-affine indices, and automatic146
schedule inference.147
2.4 Triton-C148
The Triton-C language is a C-based, CUDA-like frontend for DNN transcompiler and programmers149
familiar with low-level GPU programming.150
2.4.1 Enhanced Syntax151
This part introduces the syntax about tile declarations, built-in function, broadcasting and predication.152
2.4.2 Semantics153
Tile Semantics: Triton-C integrates built-in tile types and operations to abstract complex performance154
details like memory coalescing, cache management, and specialized hardware utilization. This155
abstraction also allows the compiler to automatically optimize these aspects.156
Broadcasting Semantics: It provides a set of rules to perform the conversions implicitly(to let operands157
obey strict shape constraints).158
2.4.3 Programming Model159
Triton-C uses SPMD Model - Single Program, Multiple Data. Each kernel is written as a single160
threaded program but is automatically parallelized, which simplifies the kernel design because there161
is no need for explicit concurrency mechanisms.162
Meanwhile, as shown in Figure 4, kernels are associated with global ranges which allows them to163
operate over varying data dimensions.164
2.5 Triton-IR165
Triton-IR is an LLVM-based Intermediate Representation(IR) for tile-level program analysis, trans-166
formation and optimization. Triton-IR extends from LLVM-IR to include tile-level dataflow and167
control flow analysis.168
5

## Page 6

Figure 4: Difference between the CUDA and the Triton pro- gramming model
2.5.1 Structure169
Triton-IR programs are organized into independent modules. Functions are defined and consist of170
basic blocks that form the control flow graph(CFG). Basic blocks are straight-line code sequences171
that only contained terminator. Triton-IR uses Static Single Assignment (SSA) form. So each basic172
block defines a Data-Flow Graph(DFG).173
2.5.2 Support for Tile-Level Data-Flow Analysis174
Traditional scalar instructions are extended to support element-wise operations on tiles, along with175
specialized instructions for operations like transposition and matrix multiplication.176
2.5.3 Support for Tile-Level Control-Flow Analysis177
Triton-IR uses Predicated SSA(PSSA) and ϕ function to manage divergent control flow within tiles.178
Some new instructions like cmpp and psi enable safe handling of control-flow conditions in tile-level179
operations.180
Overall, Triton-IR bridges the gap between high-level tensor programming and low-level optimization,181
providing the necessary constructs to effectively manage and optimize tiled computations on GPUs.182
2.6 Triton-JIT183
Triton-JIT compiles Triton-IR programs via a machine-independent and machine-dependent opti-184
mization passes backed by an auto-tuning engine.185
2.6.1 Machine-Independent Passes186
Pre-fetching is employed to mitigate latency from tile-level memory operations(inside loops or187
something). Meanwhile, Tile-Level Peephole Optimization is used to simplify tile operations.188
2.6.2 Machine-Dependent Passes189
Some optimizations are used here:190
• Hierarchical Tiling191
• Memory Coalescing192
• Shared Memory Allocation193
• Shared Memory Synchronization194
6

## Page 7

2.6.3 Auto-Tuner195
Triton-IR can extract optimization paras directly from Triton-IR programs for hierarchical tiling.196
Also, it will do exhaustive search over predefined ranges to get the optimal configurations. Further197
improvements about auto-tuning can be done in the future.198
2.7 Numerical Experiments199
Experiments on Matmul and convolutions are done on an NVIDIA GeForce GTX1070 to be compared200
with the vendor libraries.201
2.8 Conclusion202
The paper introduces Triton, an open-source language and compiler that translates tiled neural203
network computations into efficient machine code. By incorporating targeted data- and control-204
flow extensions into LLVM-IR, Triton supports tile-level optimizations that achieve performance205
comparable to vendor libraries. Additionally, the authors present Triton-C, a high-level language that206
enables concise implementation of efficient kernels for novel CNN architectures[3].207
References208
[1] TVM: An Automated End-to-End Optimizing Compiler for Deep Learning . Chen, T., Moreau, T., Jiang, Z.,209
Zheng, L., Yan, E., Shen, H., . . . & Guestrin, C. (2018). TVM: An automated end-to-end optimizing compiler210
for deep learning (arXiv:1802.04799). https://arxiv.org/abs/1802.04799211
[2] Triton: An Intermediate Language and Compiler for Tiled Neural Network Computation. Kung, H. T., &212
Cox, D. (2019). Triton: An intermediate language and compiler for tiled neural network computations. Retrieved213
from https://www.eecs.harvard.edu/ htk/publication/2019-mapl-tillet-kung-cox.pdf214
[3] ChatGPT: OpenAI. (2023). ChatGPT [Large language model]. Retrieved from https://chat.openai.com/215
7