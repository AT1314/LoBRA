---
title: "Attention Mechanism and Transformers"
date: 2025-10-28
tags: [deep-learning, nlp, transformers, attention]
course: CS224N
project: "NLP-Research"
summary: "Key concepts from the attention mechanism and transformer architecture"
---

# Attention Mechanism and Transformers

## Introduction

The attention mechanism revolutionized deep learning, particularly in NLP. Instead of compressing all information into a fixed-size vector, attention allows models to focus on relevant parts of the input.

## Self-Attention

Self-attention computes attention scores between all positions in a sequence.

### Key Components

1. **Query (Q)**: What we're looking for
2. **Key (K)**: What we're matching against
3. **Value (V)**: The information we want to retrieve

### Formula

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

Where:
- `d_k` is the dimension of the key vectors
- The division by `√d_k` prevents gradients from becoming too small

## Multi-Head Attention

Instead of performing a single attention function, multi-head attention:
1. Projects Q, K, V into multiple subspaces
2. Applies attention in parallel
3. Concatenates results
4. Projects back to original dimension

**Benefits:**
- Captures different types of relationships
- Allows attending to information from different representation subspaces
- More expressive than single-head attention

## Transformer Architecture

### Encoder
- Stack of N identical layers (typically N=6)
- Each layer has two sub-layers:
  1. Multi-head self-attention
  2. Position-wise feed-forward network
- Residual connections around each sub-layer
- Layer normalization

### Decoder
- Also N identical layers
- Three sub-layers:
  1. Masked multi-head self-attention
  2. Multi-head attention over encoder output
  3. Position-wise feed-forward network
- Masking prevents positions from attending to future positions

## Positional Encoding

Since transformers have no recurrence, positional encodings are added to give the model information about position:

```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

## Key Advantages

1. **Parallelization**: Unlike RNNs, all positions can be processed simultaneously
2. **Long-range dependencies**: Direct connections between any two positions
3. **Interpretability**: Attention weights can be visualized
4. **Flexibility**: Can be adapted for various tasks

## Applications

- Machine Translation (original use case)
- Text Summarization
- Question Answering
- Language Modeling (GPT series)
- Vision Tasks (Vision Transformers)

## Important Papers

1. **"Attention Is All You Need"** (Vaswani et al., 2017)
   - Introduced the Transformer architecture
   - Showed self-attention alone is sufficient

2. **"BERT: Pre-training of Deep Bidirectional Transformers"** (Devlin et al., 2018)
   - Bidirectional training of Transformers
   - Masked language modeling

3. **"Language Models are Few-Shot Learners"** (Brown et al., 2020)
   - GPT-3: scaling transformers to 175B parameters
   - Demonstrated few-shot learning capabilities

## Implementation Tips

### Computational Complexity
- Self-attention: O(n²d), where n is sequence length, d is dimension
- For long sequences, consider:
  - Sparse attention patterns
  - Sliding window attention
  - Memory-efficient attention variants

### Training Considerations
1. **Warmup**: Gradually increase learning rate
2. **Label Smoothing**: Regularization technique
3. **Dropout**: Applied to attention weights and residuals
4. **Batch Size**: Larger batches often help

## Common Variations

- **BERT**: Bidirectional encoder
- **GPT**: Decoder-only (autoregressive)
- **T5**: Unified text-to-text format
- **Vision Transformer (ViT)**: Images as sequences of patches
- **CLIP**: Vision and language alignment

## Resources

- Original paper: arXiv:1706.03762
- Annotated Transformer: http://nlp.seas.harvard.edu/annotated-transformer/
- HuggingFace Transformers library

## Key Takeaways

1. Attention provides a flexible way to aggregate information
2. Transformers parallelize better than RNNs
3. Pre-training + fine-tuning is a powerful paradigm
4. Scaling up (parameters, data, compute) continues to improve performance

