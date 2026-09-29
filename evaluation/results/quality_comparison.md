# YAAL vs Sarvam-1 Evaluation

## Evaluation Setup

- Evaluation prompts: **100**
- Judge model: **Qwen/Qwen2.5-3B-Instruct**
- Quality scale: **1–5**
- Quality criteria:
  - Tamil fluency
  - Instruction following
  - Factual accuracy
  - Relevance

## Inference Benchmark

| Metric | Sarvam-1 | YAAL |
|---|---:|---:|
| Successful prompts | 100/100 | 100/100 |
| Average generation time | 2.0002s | 3.0060s |
| Average generated tokens | 49.88 | 51.04 |
| Average tokens/sec | 24.90 | 16.89 |

## Automated Quality Evaluation

| Metric | Sarvam-1 | YAAL |
|---|---:|---:|
| Tamil fluency | 3.780 | 4.130 |
| Instruction following | 4.620 | 4.700 |
| Factual accuracy | 4.260 | 4.540 |
| Relevance | 4.120 | 4.440 |
| Overall quality | 4.195 | 4.453 |

## Methodology

The same 100 prompts were used for both models.

The base Sarvam-1 model and YAAL were evaluated separately using identical prompt inputs.

Quality was evaluated automatically using the separate
Qwen2.5-3B-Instruct judge model.

The judge assigned scores from 1 to 5 for Tamil fluency,
instruction following, factual accuracy, and relevance.

These results are benchmark-specific and should not be interpreted
as universal model rankings.
