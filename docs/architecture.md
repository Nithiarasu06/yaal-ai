# YAAL Architecture

```mermaid
flowchart TB

    U["👤 User"]

    F["🖥️ YAAL Frontend<br/>React + TypeScript + Vite"]

    API["⚡ FastAPI Backend<br/>Python"]

    T["🔤 Tokenizer<br/>Sarvam Tokenizer"]

    M["🧠 Sarvam-1<br/>Base Language Model"]

    L["🔗 Tamil LoRA<br/>Fine-tuned Adapter"]

    G["🎮 GPU Inference<br/>NVIDIA RTX 3050"]

    R["💬 Tamil Response"]

    U --> F
    F -->|"HTTP POST /generate"| API
    API --> T
    T --> M
    L --> M
    M --> G
    G --> R
    R --> F
    F --> U