# YAAL

<p align="center">
  <img src="frontend/public/yaal.svg" width="110" alt="YAAL">
</p>

<p align="center">
  <strong>Yet Another AI Language Model</strong><br>
  A Tamil-focused language model adapted from Sarvam-1 using LoRA
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tamil-Focused-7C3AED?style=flat-square">
  <img src="https://img.shields.io/badge/Base%20Model-Sarvam--1-2563EB?style=flat-square">
  <img src="https://img.shields.io/badge/Fine--Tuning-LoRA-0891B2?style=flat-square">
  <img src="https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=flat-square">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square">
</p>

---

## About

**YAAL (Yet Another AI Language Model)** is an experimental Tamil-focused language model project built by adapting **Sarvam-1** with **LoRA-based Parameter-Efficient Fine-Tuning (PEFT)**.

The project combines model fine-tuning, a web-based chat interface, local inference, and an automated evaluation pipeline to study Tamil language-model behaviour.

### What YAAL focuses on

- Tamil language understanding and generation
- Tamil instruction following
- Tamil conversational responses
- Tamil knowledge-oriented questions
- Parameter-efficient model adaptation
- Local inference and evaluation

---

## Web Interface

### Home

<p align="center">
  <img src="docs/screenshots/home.png" width="850" alt="YAAL Home">
</p>

### Chat

<p align="center">
  <img src="docs/screenshots/chat.png" width="850" alt="YAAL Chat">
</p>

### API

<p align="center">
  <img src="docs/screenshots/api.png" width="850" alt="YAAL API">
</p>

---

## Model

YAAL uses **Sarvam-1** as its base model and applies LoRA/PEFT fine-tuning.

| Property | YAAL |
|---|---:|
| Base model | Sarvam-1 |
| Total parameters | 2,549,057,536 |
| Trainable parameters | 23,969,792 |
| Trainable percentage | 0.9403% |
| Fine-tuning | LoRA / PEFT |
| Maximum sequence length | 768 tokens |

Only a small portion of the model parameters are trained during adaptation.

---

## Dataset

The current training data combines Tamil-oriented instruction and conversational resources.

| Dataset | Samples |
|---|---:|
| Indic SFT Mini — Tamil | 7,935 |
| VAZHI after safety filtering | 3,698 |
| **Combined dataset** | **11,633** |

### Dataset Split

| Split | Samples |
|---|---:|
| Training | 9,306 |
| Validation | 1,163 |
| Test | 1,164 |
| **Total** | **11,633** |

Random seed: **42**

The dataset contains chat, instruction, how-to, conversational, and Tamil knowledge-oriented examples.

More details:

`docs/training-pipeline.md`

---

## Technology Stack

**Model & Training**

- Python
- PyTorch
- Transformers
- PEFT
- LoRA
- TRL
- BitsAndBytes
- NumPy
- Pandas
- Scikit-learn

**Frontend**

- React
- TypeScript
- Vite
- CSS

**Backend**

- FastAPI
- Uvicorn

**Local Evaluation Hardware**

- NVIDIA GeForce RTX 3050 Laptop GPU
- 6 GB VRAM

---

# Benchmark

YAAL was compared with the base **Sarvam-1** model using the same **100 Tamil prompts**.

## Inference

| Metric | Sarvam-1 | YAAL |
|---|---:|---:|
| Successful prompts | 100/100 | 100/100 |
| Average generation time | 2.0002 s | 3.0060 s |
| Average generated tokens | 49.88 | 51.04 |
| Average tokens/sec | 24.90 | 16.89 |

## Quality Evaluation

Responses were evaluated using **Qwen2.5-3B-Instruct** as an automated judge.

Scale: **1–5**

| Metric | Sarvam-1 | YAAL |
|---|---:|---:|
| Tamil fluency | 3.780 | **4.130** |
| Instruction following | 4.620 | **4.700** |
| Factual accuracy | 4.260 | **4.540** |
| Relevance | 4.120 | **4.440** |
| **Overall quality** | **4.195** | **4.453** |

The benchmark uses the same 100 prompts for both models.

> **Benchmark note:** Results are specific to this prompt set, hardware, inference configuration, and automated judge. They should not be interpreted as universal model rankings.

Detailed results:

`evaluation/results/quality_comparison.md`

---

## Evaluation Pipeline

```text
              100 Tamil Prompts
                     │
            ┌────────┴────────┐
            ▼                 ▼
        Sarvam-1            YAAL
            │                 │
            └────────┬────────┘
                     ▼
             Response Collection
                     │
                     ▼
             Qwen2.5-3B-Instruct
                  Judge
                     │
                     ▼
             Quality + Speed
                Metrics
                     │
                     ▼
              Final Comparison
```

Generated results:

```text
evaluation/results/
├── yaal_results.json
├── sarvam_results.json
├── quality_evaluation.json
├── quality_summary.json
└── quality_comparison.md
```

---

## Project Structure

```text
yaal-ai/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│   ├── architecture.md
│   ├── training-pipeline.md
│   └── screenshots/
│       ├── home.png
│       ├── chat.png
│       └── api.png
│
├── evaluation/
│   ├── test_prompts.json
│   ├── evaluate_yaal.py
│   ├── evaluate_sarvam.py
│   ├── judge_quality.py
│   └── results/
│
├── README.md
├── package.json
└── package-lock.json
```

---

## Run Locally

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Production build:

```bash
npm run build
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## Evaluation

From the `evaluation` directory:

```bash
python evaluate_yaal.py
```

```bash
python evaluate_sarvam.py
```

```bash
python judge_quality.py
```

Results are saved to:

```text
evaluation/results/
```

---

## Documentation

| File | Description |
|---|---|
| `docs/architecture.md` | System architecture |
| `docs/training-pipeline.md` | Training and dataset pipeline |
| `evaluation/results/quality_comparison.md` | Benchmark comparison |
| `evaluation/results/quality_summary.json` | Evaluation summary |
| `evaluation/results/quality_evaluation.json` | Detailed evaluations |

---

## Future Work

- Larger Tamil datasets
- Human evaluation
- More Tamil benchmark categories
- Hallucination evaluation
- Safety evaluation
- Long-context evaluation
- Quantized inference
- Faster local inference
- Additional Tamil model comparisons
- Edge and mobile deployment

---

## Limitations

YAAL is an experimental project. The current evaluation is based on 100 prompts, local hardware, a specific inference configuration, and an automated judge model.

The reported results therefore represent this particular experimental setup rather than a comprehensive evaluation of either model.

---

## Author

**Nithiarasu**  
AI & Data Science Student

---

<p align="center">
  <strong>YAAL</strong><br>
  Tamil Language AI • Fine-Tuning • Evaluation
</p>

