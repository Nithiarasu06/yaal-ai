# YAAL Training Pipeline

YAAL uses a Tamil-focused fine-tuning pipeline built on top of the Sarvam-1
base language model.

```mermaid
flowchart LR

    A["Tamil Datasets"]
    B["Data Collection"]
    C["Cleaning & Filtering"]
    D["Tamil SFT Dataset"]
    E["Train / Validation / Test"]
    F["Sarvam-1 Base Model"]
    G["LoRA / PEFT"]
    H["Fine-Tuning"]
    I["Tamil LoRA Adapter"]
    J["Hugging Face Hub"]
    K["YAAL Backend"]
    L["Local GPU Inference"]

    A --> B
    B --> C
    C --> D
    D --> E

    F --> G
    E --> H
    G --> H

    H --> I
    I --> J
    J --> K
    K --> L