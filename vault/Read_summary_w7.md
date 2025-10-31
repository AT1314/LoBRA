---
title: "Read_summary_w7"
date: "2025-02-24"
source: "inbox/Read_summary_w7.pdf"
format: "PDF Document"
pages: "6"
converted: "2025-10-31 10:24:36"
---

# Read_summary_w7

**Pages:** 6


## Page 1

Reading Summary Week 7
Angting Cai
Abstract
This reading summary covers the topics about Gpipe and Alpha.1
1 GPipe: Easy Scaling with Micro-Batch Pipeline Parallelism2
1.1 Abstract3
It is getting more and more critical to increase model capacity beyond the memory limit of a single4
accelerator in improve neural network model quality and efficiency. Instead of working on designing5
efficient algorithms or infrastructure, to address the need for scaling up capacity, GPipe, a pipeline6
parallelism library, is proposed to help scale any network that can be expressed as a sequence of7
layers. Utilizing a novel batch-splitting pipelining algorithm, it enables almost linear speedup when8
a model is partitioned across multiple accelerators. The author demonstrate the pros of GPipe by9
training on Image classification and Multilingual Neural Machine Translation.10
1.2 Introduction11
In both image classification and NLP, the accuracy(model quality) is proved to be increased with12
the increase of model capacity. Scaling Neural networks is challenging due to hardware constraints,13
memory limitations and communication bandwidths on accelerators - making it critical to work on14
dividing models into partitions. However, it is hard to design efficient algorithms specifically for15
different tasks.16
GPipe is introduced which is flexible enough for different training tasks. It first divides a sequence of17
layers in the model into cells. Then it uses the batch-splitting algorithm by split a mini-batch into18
smaller micro-batches and pipeline the execution of each set of micro-batches over cells. And finally19
do the update by accumulating the results(gradients) at the end of the mini-batch.20
1.3 The GPipe Library21
As shown in Figure 1 below, a model of a sequence of L layers can be first divided into K partitions,22
where each partition(cell) could be placed on a single accelerator. Each partition consists of more23
than one layer in the model, working on both multiple forward functions and backward propagation.24
It also have a parameter M which specifies the number of micro-batches in one mini-batch.25
The microbatch and pipeline mechanism reduces the idle time for each accelerator due to the26
dependency, generally improving the efficiency. Meanwhile, if using batch normalization, the27
statistics of inputs during training would be computed over micro-batch and over replicas if necessary.28
To further optimize the performance, one way is to reduce activation memory requirements. GPipe29
supports re-materialization, which is to only store output activations at the partition boundaries and30
do the recomputation during backward pass instead of keeping the data in memory all the time. It31
reduces the memory requirement from O(N × L) to O(N + L
K × N
M . As shown in Figure 1c, some32
idle time could still be observed for each accelerator - bubble overhead. But it gets negligible when33
M >= 4× K. Also, it is actually not a strong requirement to have high-speed interconnects when34
using GPipe.35

## Page 2

Figure 1: Working mechanism of GPipe
There is also a noticeable problem about the imbalanced memory requirements and computation flops36
at different layers. Further work could be done about having a better partitioning algorithm.37
1.4 Performance Analyses38
The author run experiments on AmoebaNet-D and Trandformer-48 using GPipe with different39
number of partitions and different numbers of micro-batches, with and without high speed inter-40
connects. The results show that when M is larger enough compared with K, we can get linear41
speedup when increasing the number of accelerators(K) if the computation is evenly distributed over42
layers(Transformers), regardless of the equipment of high-speed interconnects.43
1.5 Image Classification and Multilingual Machine Translation44
In this section, the author run experiments to prove the effectiveness of GPipe on improving the45
accuracy(quality) of the trained large models on the two real-world tasks.46
1.6 Design Features and Trade-offs47
Model parallelism involves partitioning a network into different computation units. But it may suffer48
from low hardware utilization and device comm bottlenecks.49
To solve this, Single Program Multiple Data(SPMD) and pipeline parallelism have been proposed. It50
• Extends data parallelism across additional tensor dimensions.51
• Enables scaling of individual layers (e.g., matrix multiplications) by splitting them across52
many devices.53
• Requires frequent inter-device communication (e.g., AllReduce operations), so it performs54
best with high-speed interconnects.55
• Limited flexibility, as some layer types (e.g., convolutions split along certain dimensions)56
are not efficient to parallelize.57
Another solution is to exploit the pipeline parallelism, which breaks the network into stages and58
processes mini-batches (or “micro-batches”) in a pipeline to reduce idle time. One real case is59
Pipeline Dream, which intersperses forward and backward passes but introduces weight staleness,60
requiring multiple parameter copies on each device.61
Compared with these, GPipe62
• Has A “batch-splitting” form of pipeline parallelism that divides a mini-batch into micro-63
batches, pipelines their forward passes, and applies a single synchronous gradient update64
afterward.65
• Avoids weight staleness and keeps communication overhead low (only at partition bound-66
aries).67
2

## Page 3

• Can scale model capacity linearly with available accelerators, even if interconnect speeds68
are modest.69
But it also has limitations about70
• Each layer must fit on a single accelerator71
• Certain layers (e.g., BatchNorm) need special treatment when split into micro-batches.72
1.7 Conclusion73
GPipe, a scalable model parallelism library for training giant neural networks, generally improves the74
efficiency, flexibility and reliability in Deep Neural Network training these days.75
2 Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed76
Deep Learning77
2.1 Abstract78
Alpa automates model-parallel training of large deep learning models, by generating execution79
plans that unify data, operator and pipeline parallelism. Different from existing ways of generating80
one manually or automatically from limited space of model parallelism configs, Alpa distributes81
the training by viewing parallelism as two hierarchical levels: inter-operator and intra-operator82
parallelisms, designing compilation passes and implementing an efficient runtime.83
2.2 Introduction84
Advances in DL is tightly related to the scaling language models. While it is challenging in the work85
about model definition and the cluster environment. It is important to correctly tune the parallelization86
strategy to improve the training performance. Definitely automating the parallelization of large-scale87
models could accelerate ML research and production. But recent work still has a lot of constraints.88
One way to organize things better when navigating the complex space of plans is to organize different89
parallelization techniques into a hierarchical space and do mappings. Observing the differences90
in bandwidth requirements and some cluster-specific restriction, as shown in Figure 2, we take91
intra-operator and inter-operator parallelism.92
Intra-operator parallelism indeed has better device utilization but requires frequent communications.93
While inter-operator parallelism only communicates between adjacent stages, but incurs device idle94
time due to scheduling constraints. One great strategy is to map intra-operator parallelism to devices95
connected with high communication bandwidth.96
Alpa, the first compiler that automatically generates parallel execution plans covering all data, operator97
and pipeline parallelisms, first do partitioning on the cluster into device meshes, each of which has98
high bandwidth connections. Different stages are assigned to device meshes then. The paper makes99
contributions:100
• Construct a two-level parallel execution plan space based on intra- and inter- operator101
parallelism.102
• Design optimization algorithms for each hierarchy level.103
• Implement Alpa, a compiler system for distributed DL on GPU clusters, to realize (1) a104
set of compilation passes that generate execution plans using the hierarchical optimization105
algorithms, (2) a new runtime architecture that orchestrates the inter-op parallelism between106
device meshes, and (3) a number of system optimizations that improve compilation and107
address cross-mesh communication.108
• Do evaluation on training large models with billions of parameters.109
3

## Page 4

Figure 2: Parallelization plans generated for a computational graph
2.3 Background110
Development of Distributed DL: model developers define the dataflow graph -> An execution engine111
optimizes and executes the graph on a compute device -> Large model hard to execute due to hardware112
constraints -> Seek parallelization113
• Data parallelism114
• Operator parallelism115
• Pipeline parallelism116
• Manual combination of parallelisms117
• Automatic combination of parallelisms118
Evolves to119
• Intra-operator parallelism - partition along dimensions120
• Inter-operator parallelism121
2.4 Overview122
Three compilation passes are implemented in Alpa as shown in Figure 3:123
• Inter-op Pass - Use DP algorithm to assign stage to meshes and invoke intra-op passes124
• Intra-op Pass - Use Integer Linear Programming(ILP) formulation and report the cost back125
to inter-op pass126
• Runtime Orchestration - Fulfill the communication requirement between stages, then gener-127
ates static instructions to each mesh and invokes the execution on all meshes128
2.5 Intra-Operator Parallelism129
Alpa exploits SPMD-style intra-op parallelism and data parallelism, with ILP used for formulation.130
4

## Page 5

Figure 3: Compiler passes and runtime architecture
2.5.1 The Space of Intra-op Parallelism131
• Device mesh132
• Sharding Spec133
• Resharding134
• Parallel algorithms of an operator135
2.5.2 ILP Formulation136
ILP is used to formulate the cost minimization as an ILP and solve it optimally with an off-the-shelf137
solver.138
2.6 Limitations and Discussions139
Alpa’s new way of viewing parallelisms has flexibilities:140
• pipeline stages can contain an uneven number of operators or layers141
• pipeline stages in Alpa might be mapped to device meshaes with different shapes142
• within each stage, the data and operator parallelism configuration is customized non-143
uniformly on an op-by-op basis144
Despite those, Alpa’s optimization algorithms still have limitations:145
• Not modeling the communication cost between stages considering the comparably small146
costs.147
• Inter-op pass still has an hyperparameter.148
• Inter-op pass models pipeline parallelism still has a static linear schedule.149
• Not optimizing for the best scheme of overlapping computation and communication - Only150
able to handle static graphs with all tensor shapes known at compilation time151
References152
[1] Yanping Huang, Youlong Cheng, Ankur Bapna, Orhan Firat, Dehao Chen, Mia Chen, HyoukJoong Lee,153
Jiquan Ngiam, Quoc V Le, Yonghui Wu, et al. Gpipe: Efficient training of giant neural networks using pipeline154
parallelism. Advances in neural information processing systems, 32:103–112, 2019.155
5

## Page 6

[2] Zheng, Lianmin, et al. "Alpa: Automating inter-and Intra-Operator parallelism for distributed deep learning."156
16th USENIX Symposium on Operating Systems Design and Implementation (OSDI 22). 2022.157
[3] ChatGPT: OpenAI. (2023). ChatGPT [Large language model]. Retrieved from https://chat.openai.com/158
6