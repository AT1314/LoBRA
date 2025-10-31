---
title: "Read_summary_w8"
date: "2025-03-04"
source: "inbox/Read_summary_w8.pdf"
format: "PDF Document"
pages: "4"
converted: "2025-10-31 10:24:35"
---

# Read_summary_w8

**Pages:** 4


## Page 1

Reading Summary Week 8
Angting Cai
Abstract
This reading summary covers the topics about GPT-3 and Chinchilla Scaling Law.1
1 Language Models are Few-Shot Learners (GPT-32
1.1 Abstract3
Work on NLP tasks and benchmarks highly depend on pretraining on text followed by task-specific4
fine-tuning. To make things simpler, the paper introduces GPT-3, an autoregressive language model5
with 175 billion parameters, which is applied without any gradient updates or fine-tuning. Purely6
with text interaction, GPT-3 achieves strong performance on many NLP datasets. But still, it has7
some issues when dealing with some other datasets.8
1.2 Introduction9
Recent advances in NLP highly relied on large transformer based language models pre-trained and10
fine-tuned on specific tasks. However, fine-tuning does require a great number of labeled examples11
for each task, and the performance gains usually come from exploiting correlations instead of12
understanding. The author wants llm to be able to do like a human - learn a new task from just a13
description or a handful of example, which has greater flexibility.14
The author presents GPT-3 with 175B parameters, focusing on how language models can learn15
tasks with zero, one or only a few example provided just the text prompts. And it is proved that16
GPT-3 performs well on many benchmarks, without task-specific fine-tuning data, and explore the17
performance of the model under zero/one/few-shot scenarios. The results can be learned from Figure18
1 and 2.19
Figure 1: Large models make effcient use of in-context information

## Page 2

Figure 2: Aggregate performance for all 42 accuracy-denominated benchmarks
GPT-3 achieves competitive performance in tasks like question answering, translation, cloze tasks20
and certain reading comprehension datasets. It is able to do basic arithmetic, word unscrambling and21
using novel words correctly from a single demonstration. Meanwhile, there are still some challenging22
tasks that require the model to further improve to deal with.23
GPT-3 can generate new articles from real ones. But the issues about bias and fairness are discussed24
as well. The authors appeal for thoughtful usage and further research into safe deployment.25
1.3 Approach26
Some task settings are given:27
• Fine-Tuning: classical approach - using many labeled examples to update a model (Not used28
in GPT-3).29
• Few-Shot: Give the model K labeled examples as context at inference time without any30
parameter updates31
• One-Shot: Give only one single example with an instruction32
• Zero-Shot: Give only a natural language instruction describing the task33
As for the model and architecture for GPT-3, it is built on the same Transformer architecture as GPT-234
but scaled vastly. The model sizes scale from 125M to 175B parameters, with 96 transformer layers35
and a 12288-dimensional hidden size in the largest model. Meanwhile, the context window is 204836
tokens, while the attention layers alternate between dense and locally banded sparse patterns.37
Regarding the training dataset, GPT-3 mainly rely on filtered Common Crawl, WebText2, books38
corpora and English Wikipedia. There are about 300 billion tokens in total during training and some39
datasets are repeatedly used during the procedure. The training process also does filtering to remove40
low-quality text as much as possible.41
Figure 3: dataset
For the training setup, GPT-3 is trained on a cluster of V100 GPUs using model and pipeline42
parallelism. Large models uses bigger batch sizes but apply smaller learning rates.43
2

## Page 3

The authors do the evaluation by running benchmarks under zero/one/few-shot scenarios and do some44
multiple-choice tasks and open-ended tasks.45
1.4 Results & Discussion46
The results are based on the evaluation contents discussed above. Here we will only focus on the47
discussion on the results.48
The author did some contamination analysis to reduce the overlap of the dataset as much as possible,49
to make the evaluation with the benchmarks and datasets more reliable.50
However, GPT-3 still has some limitations. It is likely to fail on some tasks:51
• Narrow tasks like RACE reading comprehension and multi-step reasoning.52
• Structured reasoning like ceratin arithmetic and logic-based tasks.53
• Comparing two complex pieces of text.54
Also, the training costs are very high due to the scale of the model the parallelism requirement. It is55
unclear how to best control GPT-3’s outputs as well.56
In general, scaling up language models can really improves "few-shot" performance on a wide range57
of NLP tasks. It doesn’t need fine-tuning which is more practical in our daily life for humans. What58
needs further work is how to improve accuracy the remove some bias and unsafe usage cases as much59
as possible.60
2 Training Compute-Optimal Large Language Models61
2.1 Abstract62
The paper investigates how to optimize the allocation of the compute resources when training large63
Transformer-based language models(LLMs). The authors point out that today’s LLMs are often64
undertrained - trained on fewer tokens than optimal for their sizes, which means the performance65
could be further improved given the size of those models.66
2.2 Introduction67
Many recent LLMs such as GPT-3 has scaled up the size of parameters. But the number of tokens are68
still around 300B, as shown in Figure 4. One question is about: what is the best trade-off between69
model size and the number of training tokens?70
Figure 4: Number of tokens in LLMs today
The paper claims that for a given fixed compute budget, model size and training token counts should71
grow in roughly equal proportion, in contrast to previous study that claims that model size should72
grow much faster.73
2.3 Estimate optimal parameter/training tokens allocation74
The author presents three different approach the estimate the optimal allocation - Given a fixed75
compute budget C, find the ideal proportion of N(Number of parameters) vs. D(Training token76
counts).77
3

## Page 4

• Minimum Over Training Curves: For fixed model sizes, train each for different number of78
training tokens. Find the optimal N vs. D by checking the loss curves for a give FLOP79
• IsoFLOP Profiles: For different FLOP adjust the N vs. D to get the same total compute. Fit80
curves to see which model size yields the lowest final loss on each “isoFLOP” line.81
• Parametric Loss Function: Assume a function82
L(N, D) ≈ E + A
Nα + B
Dβ .
, fit α and β, and solve for N and D to minimize the loss under the constraint that FLOP(N,83
D) = C.84
All three methods indicate that N and D should scale nearly equally.85
2.4 Chinchilla: A Practical Validation86
Figure 5: Chinchilla vs. Gopher
Figure 5 shows the architectural setup of Chinchilla and Gopher. Chinchilla has 70B parameters87
and 1.4 trillion tokens in total while Gopher has about 280B parameters(4x vs. Chinchilla) and 1/4x88
tokens vs. Chinchilla using the same compute budget.89
Despite having only one-quarter the parameters of Gopher, Chinchilla outperforms Gopher—and90
even larger models—on a wide variety of NLP tasks, including:91
• Language Modeling92
• MMLU (Massive Multitask Language Understanding)93
• Reading Comprehension94
• BIG-bench95
• Closed-Book QA96
Besides, Chinchilla’s training costs are lower than a 200B+ parameter model.97
2.5 Discussion98
With the validation by Chinchilla, it is proved that current LLMs are overly large in their (parameter)99
size compared to the training data size. It should be paid attention to try to use smaller model to train100
more data. Meanwhile, it is getting more important to deal with the bias/toxicity in the dataset to101
improve the dataset quality so as to increase the number of training tokens. It is always critical in102
general to determine the optimal ratio between the model capacity vs. training data.103
Conclusively, LLM development should not only focus on scaling the model size but also important104
to scale the training data. Equally scaling both model capacity and dataset size yields more powerful105
and more efficient models. "Bigger is not always better" if the training data size is fixed.106
References107
[1] Brown, Tom, et al. "Language models are few-shot learners." Advances in neural information processing108
systems 33 (2020): 1877-1901.109
[2] Hoffmann, Jordan, et al. "Training compute-optimal large language models." arXiv preprint arXiv:2203.15556110
(2022).111
[3] ChatGPT: OpenAI. (2023). ChatGPT [Large language model]. Retrieved from https://chat.openai.com/112
4