---
title: "Read_summary_w1"
date: "2025-01-13"
source: "inbox/Read_summary_w1.pdf"
format: "PDF Document"
pages: "9"
converted: "2025-10-31 10:24:37"
---

# Read_summary_w1

**Pages:** 9


## Page 1

Reading Summary Week 1
Angting Cai
Abstract
This reading summary covers chapter 1 - MLSys: intro and chapter 4 - DNN1
Architecture. The different chapters will be separately summarized in different2
sections in this paper.3
1 Chapter 1 - MLSys : Intro4
1.1 AI is everywhere5
AI emerged as one of the most transformative forces in human history, just like the Industrial Revolu-6
tion and the Digital Revolution in the 18th and 19th centuries. AI systems shape our world everywhere,7
working alongside humanity, enhancing our problem-solving capabilities and accelerating scientific8
progress. It has great potential about expanding the boundaries of human knowledge and capability.9
Different from revolutions in the past centuries, AI capabilities are advancing at an extraordinary rate.10
It only takes several years for us to build AI systems that can understand human speech, generate11
novel ideas or make complex decisions. In this new era, we need to work on engineering systems that12
can acquire capabilities through learning - exceed human performance in specialized domains. It is13
also critical to ensure the systems’ reliability and scalability.14
1.2 AI & ML15
AI represents the systematic pursuit of understanding and replicating human intelligent behaviors.16
More specifically, AI is a field that explores the capabilities of recognizing patterns, learning from17
experience and adapt correspondingly to new information(prediction), to build systems that can18
think, reason and adapt. While Machine learning (ML) is to create systems to identifying potential19
patterns and relationships utilizing some optimization techniques. AI and ML are like theoretical20
understanding and practical engineering implementation observed in other scientific fields.21
1.3 The evolution of AI22
As shown in Figure 1, AI evolves slowly in the 1900s, starting from Alan Turing’s journal and having23
significant breakthroughs in 1997. Symbolic AI(1956-1974) only handles iputs that exactly matched24
their pre-programmed patterns and rules. It was a great start but would break down when faced with25
real-world complexity. Expert Systems(1970s-1980s) such as MYCIN was one of the first large-scale26
expert systems designed to diagnose blood infections. However, the information gathered from27
human doctors is usually uncertain and incomplete which makes it difficult to be used for ML.28
In 1990s, AI’s research direction moves to statistical learning. Three factors converged to make this29
shift possible: the availability of large datasets (due to the digital revolution), greater computational30
power (driven by Moore’s Law), and innovative algorithms (such as Support Vector Machines31
and improved neural networks). Together, these enabled machines to discover patterns from data32
instead of relying on pre-programmed rules. Figure 2 shows the evolution journey of AI approaches,33
highlighting the key strengths and capabilities that emerged with each new paradigm. "Shallow34
learning" in the 2000s is like a foundation of deep learning(2012-Present). It has just one or two35
levels of processing on data. Based on support vector machines and shallow learning, in 2012, a deep36
neural network called AlexNet achieved a breakthrough. It uses layers of artificial neurons to learn37

## Page 2

Figure 1: Milestones in AI from 1950 to 2020
hierarchical representations of data, allowing networks to automatically discover features from raw38
inputs.39
By the early 2010s, three factors converged to unlock deep learning’s full potential: massive datasets,40
powerful hardware (GPUs), and new algorithmic techniques for training deep networks. This41
convergence sparked explosive progress, including the creation of “foundation models” such as42
GPT-3, containing hundreds of billions of parameters. Such models can perform a range of complex43
tasks—from generating text and images to writing code—showing that ever-larger neural networks44
trained on vast datasets can tackle increasingly sophisticated problems.45
Yet, these successes introduced new challenges beyond just the algorithms: managing huge datasets,46
distributing computation across thousands of GPUs, and deploying models at scale. This prompted a47
growing focus on Machine Learning Systems Engineering, a field that addresses the full lifecycle of48
AI systems—spanning data collection, model training, infrastructure, and deployment—echoing the49
discipline’s evolution from symbolic reasoning toward robust, production-ready AI systems.50
1.4 The Rise of ML Systems Engineering51
Just like Computer Science and Electrical Engineering in the late 1960s, nowadays we need Machine52
Learning Systems Engineering like Computer Engineering to fill the gap between ML algorithms53
and AI hardware. A great ML system should not only have a brilliant algorithm but also be able54
to efficiently collect and process the data it needs, distribute its computation across hundreds of55
machines, serve it reliably to millions of users or monitor its performance in production.56
1.5 Definition of ML System57
A machine learning system is an integrated computing system consisting of components: (1) Data58
that guides algorithmic behavior, (2) Learning algorithm (Model), (3) Computing infrastructure that59
2

## Page 3

Figure 2: Evolution of AI
Figure 3: Machine Learning System Components
enables both the learning process and the application of learned knowledge. Just as shown in Figure 3,60
each of these components serves a distinct but interconnected purpose, creating a computing system61
capable of making predictions, generating content, or taking actions based on learned patterns.62
1.6 The ML Systems Lifecycle63
Traditional systems are usually deterministic based on the code base. However, ML systems derive64
their behavior from data rather than solely the code. As data changes, the systems must be retrained65
to maintain accuracy.66
As shown in Figure 4, Machine learning systems follow a dynamic lifecycle composed of multiple67
stages—data collection, model training, evaluation, deployment, and monitoring—connected through68
feedback loops. These stages must address both learning and infrastructure needs, as flaws in one area69
can undermine the entire system, creating a “vicious cycle.” Conversely, each component functioning70
well (e.g., robust data pipelines, efficient training infrastructure, and continuous monitoring) leads to71
a “virtuous cycle,” where improvements in one stage feed back into others.72
Finally, ML systems are not uniform. They span diverse settings—from large-scale cloud services73
handling millions of users to tiny embedded systems in IoT devices—underscoring the wide range of74
engineering challenges and the importance of a holistic approach that considers algorithms, data, and75
infrastructure together.76
3

## Page 4

Figure 4: Lifecycle of ML systems
1.7 The Spectrum of ML Systems77
ML systems exist at different scales and in diverse environments. from TinyML systems to cloud-78
based ML systems. They are adapted for different contexts. And in each context, we should maintain79
the balance between limited resources and capabilities of the ML systems.80
1.8 ML System Implications of the ML Lifecycle81
The diversity of ML systems across the spectrum represents the complex trade-offs. The decision82
making process are throughout the whole ML systems lifecycle. First, we should consider the83
application is latency-sensitive or computation-intensive. Second, resources management is vital84
for systems at different scales, such as cloud systems(optimized for cost efficiency at scale), Edge85
systems(Fixed resource limits), and mobile systems(Every piece of resources matters). Third,86
operational complexity increases with system distribution. Fourth, data considerations often introduce87
competing pressures. Last but not least, Evolution and maintenance requirements must be considered88
from the start.89
Emerging application-level trends include a shift toward agentic systems, which move beyond mere90
prediction and instead learn, act, and adapt in real time—often in multi-agent environments with91
dynamic interactions and objectives. These systems also incorporate advanced operational intelligence92
features, such as automated resource management and self-monitoring, further increasing complexity93
and requiring robust decision-making frameworks.94
Meanwhile, system architecture is also evolving to accommodate these advanced applications.95
Integration frameworks must now manage intricate, cross-organizational interactions, prompting96
innovative methods for handling diverse data sources and meeting operational requirements. In this97
landscape, resource efficiency has become a primary focus, driving interest in model compression98
techniques and specialized AI hardware—ranging from robust data center accelerators to low-power99
processors for edge devices and embedded/mobile systems. Overall, these developments herald an100
era of more adaptive, capable, and efficient machine learning systems, highlighting the importance of101
strategies that align application needs with the underlying infrastructure.102
1.9 Real-world applications and impact103
This chapter introduces some real-world applications to prove the ML systems’ abilities to operate104
effectively address practical challenges and drive innovations.105
1.10 Challenges and Considerations106
1.10.1 Data Challenges107
Data is the foundation of any ML systems. There exists many challenges from different aspects. First,108
the data quality from the real-world is not always that ideal. It is usually messy and inconsistent.109
Second, as ML systems grow, they should be able to deal with large amounts of data. They should110
learn to store, process and manage such large datasets efficiently. Third, data may change over time -111
"data drift". During the process of learning of a ML system, the patterns in new data may begin to112
differ from the patterns the system originally learned from.113
1.10.2 Model Challenges114
Some models like GPT-3 are hard to train due to the complexity, since they require enormous115
computing power to train and run, making it difficult to deploy them in situations with limited116
resources. So the first challenge is about how to train these models effectively. Another important117
4

## Page 5

Figure 5: Overview of the five fundamental system pillars of ML Sys Engineering
challenge is to ensure that models can work well in real-world conditions. For critical applications118
like autonomous vehicles or medical systems this challenge is vital.119
1.10.3 System Challenges120
It is important as well to make sure the reliability of the whole pipeline of the ML System. Both the121
training systems and the serving systems should be maintained correctly, especially for ML Systems122
that serve millions of users.123
1.10.4 Ethical and Social Considerations124
ML Systems should guarantee fairness. Any discrimination is not allowed regardless of whether it is125
intentional. Besides, transparency and privacy are critical if we want to approach ML system design126
and deployment better.127
1.11 Future Directions128
Looking to the future of ML Systems, one significant trends is the democratization of AI technology.129
Everyone should be able to use or build ML system(platform) to solve problems. Also, there is130
still much work that can be done to reduce computational costs and make systems more efficient.131
This can also help make sophisticated AI capabilities available on more tiny devices. Moreover,132
autonomous ML Systems are an important trend which can adapt and improve themselves. They133
can also dramatically reduce operational overhead of running ML systems while improving their134
reliability.135
Though trends are promising, we should also take a look at the limitations of the field. Truly artificial136
general intelligence, more flexible AI, less bias, more transparency and privacy are all vital problems137
that can be worked on.138
1.12 Learning Path and Book Structure139
As shown in Figure 5,the five pillars central to the framework are Data, Training, Deployment,140
Operations and Ethics & Governance.141
2 Chapter 4 - DNN Architectures142
2.1 Purpose143
The purpose of this chapter is to explore how fundamental patterns in deep learning architec-144
tures—such as dense layers, convolutions, temporal mechanisms, and attention—form systematic145
building blocks for modern AI. By understanding these recurring structures, we can design more146
flexible, efficient, and scalable systems that balance computational needs with real-world constraints.147
This insight helps us map neural network concepts to practical architectures, optimize hardware148
usage, and make informed trade-offs between model complexity and system performance.149
5

## Page 6

2.2 Overview150
Neural network architectures have evolved to address specific pattern processing challenges. This151
chapter will discuss a fundamental approach by examining how ML systems’ computational patterns152
map to hardware resources. The mapping from algorithmic requirements to computer system design153
involves several key considerations:154
1. Memory access patterns: How data moves through the memory hierarchy. 2. Computation charac-155
teristics: The nature and organization of arithmetic operations. 3. Data movement: Requirements for156
on-chip and off-chip data transfer 4. Resource utilization: How computational and memory resources157
are allocated158
This chapter will discuss on algorithmic structures like MLPs, CNNs, RNNs, Transformers.159
2.3 Multi-layer Perceptrons: Dense Pattern Processing160
MLPs extend basic neural networks into deeper structures, getting a universal algorithm for mapping161
inputs to outputs. This architecture process each feature equally, based on the Universal Approxima-162
tion Theorem(UAT).163
Deep learning systems require dense pattern processing to learn arbitrary relationships across all164
input features. MLPs’ algorithm is to connect everything to everything to address our need for165
arbitrary feature relationships but creates specific computational patterns that must be handled166
efficiently by computer systems. Memory requirements for dense pattern processing stem from167
storing and accessing weights, inputs, and intermediate results. But deep learning framework abstract168
the hardware-specific details(CPU, GPU) through optimized matrix multiplication implementations.169
For the computational needs, the dense matrix multiplication can be efficiently parallelized across170
multiple units. Meanwhile, deep learning frameworks orchestrate the data movements through171
optimized memory management systems.172
2.4 CNN: Spatial Pattern Processing173
Different from MLPs to treat every input feature equally, architecture like Convolutional Neural174
Networks(CNN )employ spatial pattern processing to exploit the spatial relationships in many real-175
world data types, serving real-world cases like image processing. CNNs use a local connection176
pattern where each output connects only to a small, spatially contiguous region of the input.177
This local receptive field moves across the input space, applying the same set of weights at each178
position—a process known as convolution. For memory requirement, deep learning frameworks179
typically implement this through specialized memory layouts that optimize for both filter reuse and180
spatial locality in feature map access. For computational needs, structured parallelism is utilized181
for the repeated nature of convolution. And deep learning frameworks optimize it by designing182
specialized convolution algorithms. For data movement, besides the hardware utilization, deep183
learning frameworks orchestrate these movements by organizing computations to maximize filter184
weight reuse and minimize redundant feature map accesses.185
2.5 RNN: Sequential Pattern Processing186
Different from MLPs and CNNs, Recurrent Neural Networks(RNN) is used to deal with real-world187
data that the order and relationship between elements over time matters, like text processing, speech188
recognition and time-series analysis. Pattern processing in this architecture needs to maintain and189
update relevant context overtime. Sequential processing must handle variable-length sequences while190
maintaining computational efficiency.191
Instead of just mapping inputs to outputs, RNNs maintain an internal state that is updated at each192
time step. RNNs require storing two sets of weights along with the hidden state. Unlike CNNs where193
weights are reused across spatial positions, RNN weights are reused across time steps. Additionally,194
the system must maintain the hidden state, which becomes a critical factor in memory usage and195
access patterns. For computational needs, the core computation in RNNs involves repeatedly applying196
weight matrices across time steps.197
6

## Page 7

Figure 6: The interaction between Query, Key, and Value components
2.6 Attention Mechanisms: Dynamic Pattern Processing198
It is important to build an architecture that can adaptively change its processing patterns based on the199
data. Transformer architecture implement these capabilities through attention mechanisms.200
For a sequence of length N with dimension d, this operation creates an N ×N attention matrix,201
determining how each position should attend to all others. As illustrated in Figure 6, the attention202
operation first computes query, key, and value projections for each position in the sequence. Next, it203
generates an N×N attention matrix through query-key interactions. Finally, it uses these attention204
weights to combine value vectors, producing the output. Here the attention weights are computed205
dynamically for each input, allowing the model to adapt its processing based on the dynamic content206
at hand. For system implications, in terms of memory requirements, attention mechanisms necessitate207
storage for attention weights, key-query-value projections, and intermediate feature representations.208
Computation needs in attention mechanisms center around two main phases: generating attention209
weights and applying them to values. While for data movement, the intermediate attention weights210
become a major factor in system bandwidth requirements.211
Transformer extend the basic attention mechanism by applying attention within a single sequence,212
enabling each element to attend to all other elements including itself(self-attention).213
2.7 Architectural Building Block214
Deep learning architecture can be seen as compositions of fundamental building blocks that evolved215
overtime. As shown in Figure 7, this table encapsulates the major shifts in deep learning architecture216
design and the corresponding changes in system-level considerations.217
MLPs indicated the shift from Perceptron to Multi-layer Networks. CNNs marked the innovation218
from Dense to Spatial Processing. While RNNs brings the evolution of sequential processing.219
Then it comes to the modern architecture - transformers, representing a sophisticated synthesis of220
these fundamental building blocks. Consider the Transformer architecture: at its core, we find MLP-221
style feedforward networks processing features between attention layers. The attention mechanism222
itself builds on ideas from sequence models but removes the recurrent connection, instead using223
position embeddings inspired by CNN intuitions. Skip connections, inherited from ResNets, appear224
throughout the architecture, while layer normalization, evolved from CNN’s batch normalization,225
stabilizes training.226
7

## Page 8

Figure 7: Evolution of deep learning architectures and their system implications
Figure 8: Comparison of primitive utilization across neural network architectures.
Even recent innovations in vision and language models follow this pattern of recombining fundamental227
building blocks.228
2.8 System-level Building Blocks229
This section explores how deep learning architectures map onto hardware and software through230
fundamental primitives—the irreducible operations that define both computation and data handling in231
modern AI systems.232
2.8.1 Core Computational Primitives233
1. Matrix Multiplication: Central to nearly all deep learning models (e.g., MLPs, CNNs, Transform-234
ers), often accelerated by specialized tensor cores. 2. Sliding Window Operations: Used for local235
filtering (like convolutions), optimized via memory tiling and specialized datapaths. 3. Dynamic236
Computation: Seen in attention mechanisms where runtime decisions dictate data flow, requiring237
flexible hardware routing and dynamic execution in software.238
2.8.2 Memory Access Primitives239
1. Sequential Access: Highly efficient; exploited by batching and careful data layout. 2. Strided Ac-240
cess: Common in convolutions, addressed by transformations like im2col and caching optimizations.241
3. Random Access: Occurs in attention mechanisms and leads to cache misses; tackled by large242
caches and scheduling strategies.243
2.8.3 Data Movement Primitives244
1. Broadcast: Sending the same data to multiple destinations in parallel. 2. Gather/Scatter: Distribut-245
ing or collecting different parts of data across processing units. 3. Reduction: Aggregating partial246
results (e.g., summations) for final outputs.247
8

## Page 9

2.8.4 System Design Impact248
1. Specialized Hardware: Tensor cores, high-bandwidth memory (HBM), and networks-on-chip249
arise to handle dense matrix ops, dynamic access, and high-volume data movement. 2. Memory250
Bottlenecks: Large, frequent data transfers can stall compute units; deeper caching hierarchies and251
efficient data layouts aim to alleviate this. 3. Trade-Offs: Optimizing for dense operations may252
reduce flexibility for dynamic patterns, while supporting large working sets for complex models may253
increase energy and latency overhead.254
2.9 Conclusion255
As the field of deep learning to evolve, it is important to efficiently support and optimize the256
fundamental building blocks so as to develop more powerful and scalable systems. Last but not least,257
while understanding the mapping between neural architectures and their computational requirements258
is vital for pushing the boundaries of what’s possible in, the interplay between algorithm innovation259
and systems optimization will drive the progress of this field in the future as well.260
References261
[1] https://mlsysbook.ai/contents/core/dnn_architectures/dnn_architectures.html#262
architectural-building-blocks263
[2] Chatgpt o1264
9