# YAAL — Yet Another AI Language Model

<p align="center">
  <img src="frontend/public/yaal.svg" width="120" alt="YAAL Logo">
</p>

<h3 align="center">
  Tamil-Focused Language Model Adaptation using LoRA
</h3>

<p align="center">
  <b>YAAL explores Tamil language adaptation, instruction following, local inference, and automated LLM evaluation.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Tamil-8B5CF6?style=for-the-badge">
  <img src="https://img.shields.io/badge/Base%20Model-Sarvam--1-6366F1?style=for-the-badge">
  <img src="https://img.shields.io/badge/Fine--Tuning-LoRA%20%2F%20PEFT-06B6D4?style=for-the-badge">
  <img src="https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=for-the-badge">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

---

## 🌐 Overview

**YAAL (Yet Another AI Language Model)** is an experimental Tamil-focused language model project built by adapting **Sarvam-1** using **LoRA-based Parameter-Efficient Fine-Tuning (PEFT)**.

The project investigates whether targeted Tamil instruction and conversational data can improve model behavior across:

- Tamil language fluency
- Instruction following
- Factual response generation
- Relevance
- Tamil knowledge tasks
- Conversational interactions

YAAL also includes a web interface and an automated evaluation pipeline for comparing the adapted model with the base Sarvam-1 model.

---

## ✨ Key Features

- 🇮🇳 Tamil-focused language adaptation
- 🧠 Sarvam-1 as the base model
- ⚡ LoRA / PEFT fine-tuning
- 📚 Tamil instruction and conversational datasets
- 💬 Interactive web-based chat interface
- 🚀 FastAPI backend
- ⚛️ React + TypeScript + Vite frontend
- 💻 Local GPU inference
- 📊 100-prompt controlled benchmark
- 🤖 Automated quality evaluation using Qwen2.5-3B-Instruct
- 📈 Inference and quality comparison between Sarvam-1 and YAAL
- 🧪 Reproducible evaluation scripts and results

---

# 🖥️ Web Application

YAAL includes a custom web interface designed for interacting with the model.

## 🏠 Home

<p align="center">
  <img src="docs/screenshots/home.png" width="900" alt="YAAL Home Interface">
</p>

## 💬 Chat Interface

<p align="center">
  <img src="docs/screenshots/chat.png" width="900" alt="YAAL Chat Interface">
</p>

## 🔌 API Interface

<p align="center">
  <img src="docs/screenshots/api.png" width="900" alt="YAAL API Interface">
</p>

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    React + Vite      │
                         │      Frontend        │
                         └──────────┬───────────┘
                                    │
                              HTTP / API
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │        YAAL          │
                         │   Sarvam-1 + LoRA    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Tamil Response     │
                         └──────────────────────┘

Detailed architecture:

docs/architecture.md
🧠 Model Architecture & Fine-Tuning

YAAL uses Sarvam-1 as its base model and applies parameter-efficient fine-tuning using LoRA / PEFT.

Instead of updating the entire model, LoRA trains a relatively small set of additional parameters while keeping the base model largely frozen.

This allows experimentation with Tamil adaptation using significantly fewer trainable parameters.

Model Statistics
Property	YAAL
Base model	Sarvam-1
Total parameters	2,549,057,536
Trainable parameters	23,969,792
Trainable percentage	0.9403%
Fine-tuning method	LoRA / PEFT
Maximum sequence length	768 tokens
Parameter Distribution
Total Parameters
2,549,057,536
        │
        ├── Frozen Base Model
        │
        └── Trainable LoRA Parameters
            23,969,792
            0.9403%
📚 Training Dataset

The training corpus was assembled from Tamil-oriented instruction and conversational resources.

Dataset Composition
Dataset	Samples
Indic SFT Mini — Tamil	7,935
VAZHI after safety filtering	3,698
Combined dataset	11,633
Dataset Split
Split	Samples
Training	9,306
Validation	1,163
Test	1,164
Total	11,633

The dataset split uses a fixed random seed of 42.

Task Categories

The processed dataset contains multiple task styles, including:

Chat
Instruction following
How-to tasks
Tamil conversational examples
Tamil knowledge-oriented examples

Detailed training documentation:

docs/training-pipeline.md
⚙️ Technology Stack
Machine Learning
Python
PyTorch
Hugging Face Transformers
PEFT
LoRA
TRL
BitsAndBytes
NumPy
Pandas
Scikit-learn
Frontend
React
TypeScript
Vite
CSS
Backend
Python
FastAPI
Uvicorn
Development Hardware

Local evaluation was performed using:

GPU: NVIDIA GeForce RTX 3050 Laptop GPU
VRAM: 6 GB
📊 YAAL vs Sarvam-1 Benchmark

A controlled benchmark was conducted using 100 Tamil-language prompts.

The same prompt set was evaluated independently on both models.

⚡ Inference Performance
Metric	Sarvam-1	YAAL
Successful prompts	100/100	100/100
Average generation time	2.0002 s	3.0060 s
Average generated tokens	49.88	51.04
Average tokens/sec	24.90	16.89

The measurements above represent the observed performance under the local evaluation configuration used for this experiment.

🤖 Automated Quality Evaluation

Response quality was evaluated using Qwen2.5-3B-Instruct as a separate automated judge model.

Each response was evaluated on a 1–5 scale across four criteria:

Tamil fluency
Instruction following
Factual accuracy
Relevance
Quality Results
Metric	Sarvam-1	YAAL
Tamil fluency	3.780 / 5	4.130 / 5
Instruction following	4.620 / 5	4.700 / 5
Factual accuracy	4.260 / 5	4.540 / 5
Relevance	4.120 / 5	4.440 / 5
Overall quality	4.195 / 5	4.453 / 5
Evaluation Configuration
Property	Configuration
Evaluation prompts	100
Models compared	Sarvam-1, YAAL
Quality judge	Qwen2.5-3B-Instruct
Quality scale	1–5
Evaluation type	Controlled local benchmark
Hardware	RTX 3050 6 GB
Metrics	Quality + inference performance

Important: These measurements are specific to the selected 100-prompt dataset, hardware, inference configuration, and automated judge. They should not be interpreted as universal model rankings or general performance claims.

🔬 Evaluation Pipeline
                 ┌─────────────────────┐
                 │ 100 Tamil Prompts   │
                 └─────────┬───────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        ┌───────────────┐     ┌───────────────┐
        │   Sarvam-1    │     │     YAAL      │
        └───────┬───────┘     └───────┬───────┘
                │                     │
                └──────────┬──────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Response Collection │
                 └─────────┬───────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Qwen2.5-3B-Instruct │
                 │    Quality Judge    │
                 └─────────┬───────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Automated Scoring  │
                 └─────────┬───────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Comparison Reports │
                 └─────────────────────┘
Generated Evaluation Files
evaluation/results/
│
├── yaal_results.json
├── sarvam_results.json
├── quality_evaluation.json
├── quality_summary.json
└── quality_comparison.md
📁 Project Structure
Tamil_AI/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ├── yaal.svg
│   │   ├── favicon.svg
│   │   └── icons.svg
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── package-lock.json
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
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/Nithiarasu06/yaal-ai.git
cd yaal-ai
💻 Frontend Setup

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

For a production build:

npm run build
⚡ Backend Setup

Navigate to the backend:

cd backend

Install Python dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn main:app --reload
🧪 Running the Evaluation

Navigate to:

cd evaluation
Evaluate YAAL
python evaluate_yaal.py
Evaluate Sarvam-1
python evaluate_sarvam.py
Run Quality Judge
python judge_quality.py

Evaluation results are generated inside:

evaluation/results/
📖 Documentation
Document	Purpose
docs/architecture.md	System architecture and components
docs/training-pipeline.md	Dataset preparation and fine-tuning workflow
evaluation/results/quality_comparison.md	YAAL vs Sarvam-1 benchmark
evaluation/results/quality_summary.json	Machine-readable benchmark summary
evaluation/results/quality_evaluation.json	Prompt-level quality evaluations
🎯 Project Objectives

YAAL was developed to explore practical Tamil language-model development through:

Tamil-specific model adaptation
Parameter-efficient fine-tuning
Instruction tuning
Local model inference
Tamil conversational AI
Automated model evaluation
Model quality analysis
Web-based AI interaction
🔭 Future Work

Planned improvements include:

Larger and more diverse Tamil datasets
More comprehensive Tamil benchmarks
Human evaluation alongside automated judging
Hallucination analysis
Long-context evaluation
Safety evaluation
Quantized inference
Faster local inference
Improved Tamil tokenizer analysis
Edge and mobile deployment experiments
Expanded Tamil knowledge evaluation
Additional model comparisons
⚠️ Limitations

YAAL is an experimental research and development project.

The current benchmark is limited by:

100 evaluation prompts
Local hardware constraints
Automated quality judging
A single judge model
Specific generation settings
Limited evaluation categories

The quality scores therefore represent the behavior observed under this particular experimental setup rather than a comprehensive evaluation of either model.

👨‍💻 Author
Nithiarasu

AI & Data Science Student

YAAL is developed as an exploration of Tamil NLP, language-model adaptation, and practical generative AI systems.

📜 License

This project is released under the MIT License.

<p align="center"> <b>YAAL — Exploring Tamil Language AI</b> <br><br> Built with curiosity • Fine-tuned for Tamil • Evaluated with data </p>