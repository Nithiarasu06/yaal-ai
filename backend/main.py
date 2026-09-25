import os
import re
import time

import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


# ============================================================
# CONFIGURATION
# ============================================================

BASE_MODEL = "sarvamai/sarvam-1"
LORA_MODEL = "Nithiarasu/sarvam-tamil-lora"

HOST = "127.0.0.1"
PORT = 8000

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Tamil AI API",
    description="Tamil AI Assistant powered by Sarvam-1 + Tamil LoRA",
    version="1.0.0",
)

# Allow React/Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_new_tokens: int = Field(
        default=150,
        ge=1,
        le=512
    )


# ============================================================
# GLOBAL MODEL VARIABLES
# ============================================================

tokenizer = None
base_model = None
model = None


# ============================================================
# GPU INFORMATION
# ============================================================

def get_gpu_info():
    if not torch.cuda.is_available():
        return {
            "available": False,
            "device": "cpu",
            "gpu": "NONE",
            "allocated_gb": 0,
            "reserved_gb": 0,
        }

    allocated = torch.cuda.memory_allocated() / (1024 ** 3)
    reserved = torch.cuda.memory_reserved() / (1024 ** 3)

    return {
        "available": True,
        "device": DEVICE,
        "gpu": torch.cuda.get_device_name(0),
        "allocated_gb": round(allocated, 2),
        "reserved_gb": round(reserved, 2),
    }


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    global tokenizer
    global base_model
    global model

    print("=" * 70)
    print("TAMIL AI BACKEND")
    print("=" * 70)

    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("GPU: NONE")

    # --------------------------------------------------------
    # TOKENIZER
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("LOADING TOKENIZER")
    print("=" * 70)

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Tokenizer loaded!")
    print(f"Vocabulary size: {len(tokenizer)}")

    # --------------------------------------------------------
    # BASE MODEL
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("LOADING SARVAM-1")
    print("=" * 70)

    if torch.cuda.is_available():

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16,
            device_map={"": 0},
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

    else:

        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float32,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

    print("Sarvam-1 loaded successfully!")
    print(f"Device: {DEVICE}")

    if torch.cuda.is_available():
        print(
            f"GPU allocated: "
            f"{torch.cuda.memory_allocated() / (1024 ** 3):.2f} GB"
        )

    # --------------------------------------------------------
    # LOAD LORA
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("LOADING TAMIL LoRA")
    print("=" * 70)

    model = PeftModel.from_pretrained(
        base_model,
        LORA_MODEL,
    )

    # Inference mode
    model.eval()

    # Disable cache if necessary only during training.
    # For inference we want cache enabled.
    model.config.use_cache = True

    print("Tamil LoRA loaded successfully!")

    if torch.cuda.is_available():
        print(
            f"GPU allocated: "
            f"{torch.cuda.memory_allocated() / (1024 ** 3):.2f} GB"
        )

    print()
    print("=" * 70)
    print("MODEL READY")
    print("=" * 70)


# ============================================================
# PROMPT FORMAT
# ============================================================

def build_prompt(user_prompt: str) -> str:
    """
    Format the prompt similarly to the training/evaluation
    format used for the Tamil SFT data.
    """

    user_prompt = user_prompt.strip()

    prompt = (
        "<s>[INST] "
        f"{user_prompt}"
        " [/INST]"
    )

    return prompt


# ============================================================
# CLEAN MODEL OUTPUT
# ============================================================

def clean_response(text: str, original_prompt: str) -> str:

    text = text.strip()

    # Remove special instruction markers
    text = text.replace("</s>", "")
    text = text.replace("<s>", "")
    text = text.replace("[/INST]", "")
    text = text.replace("[INST]", "")

    # Sometimes the model may generate another instruction turn
    if "[INST]" in text:
        text = text.split("[INST]")[0]

    # Remove accidental prompt echo
    if text.startswith(original_prompt):
        text = text[len(original_prompt):].strip()

    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(
    prompt: str,
    max_new_tokens: int = 150,
):

    if model is None or tokenizer is None:
        raise RuntimeError("Model is not loaded")

    formatted_prompt = build_prompt(prompt)

    # --------------------------------------------------------
    # TOKENIZE
    # --------------------------------------------------------

    inputs = tokenizer(
        formatted_prompt,
        return_tensors="pt",
        truncation=True,
        max_length=2048,
    )

    # Move tensors to model device
    if torch.cuda.is_available():
        inputs = {
            key: value.to(DEVICE)
            for key, value in inputs.items()
        }
    else:
        inputs = {
            key: value.to("cpu")
            for key, value in inputs.items()
        }

    input_length = inputs["input_ids"].shape[1]

    # --------------------------------------------------------
    # GENERATION
    # --------------------------------------------------------

    start_time = time.time()

    with torch.no_grad():

        outputs = model.generate(
            **inputs,

            # Maximum response length
            max_new_tokens=max_new_tokens,

            # Deterministic generation
            do_sample=False,

            # Greedy decoding
            num_beams=1,

            # Prevent excessive repetition
            repetition_penalty=1.05,

            # Stop at EOS
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,

            # Don't use generation length based on prompt
            use_cache=True,
        )

    generation_time = time.time() - start_time

    # --------------------------------------------------------
    # ONLY TAKE NEW TOKENS
    # --------------------------------------------------------

    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    # --------------------------------------------------------
    # CLEAN
    # --------------------------------------------------------

    response = clean_response(
        response,
        prompt,
    )

    return response, generation_time, len(generated_tokens)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    gpu = get_gpu_info()

    return {
        "status": "online",
        "message": "Tamil AI Assistant is running",
        "base_model": BASE_MODEL,
        "adapter": LORA_MODEL,
        "gpu": gpu["gpu"],
        "device": gpu["device"],
    }


# ============================================================
# HEALTH ENDPOINT
# ============================================================

@app.get("/health")
def health():

    gpu = get_gpu_info()

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "tokenizer_loaded": tokenizer is not None,
        "cuda": torch.cuda.is_available(),
        "gpu": gpu,
    }


# ============================================================
# GENERATE ENDPOINT
# ============================================================

@app.post("/generate")
def generate(request: GenerateRequest):

    try:

        print()
        print("=" * 70)
        print("NEW REQUEST")
        print("=" * 70)

        print(f"Prompt: {request.prompt}")
        print(f"Max new tokens: {request.max_new_tokens}")

        response, generation_time, generated_tokens = generate_response(
            request.prompt,
            request.max_new_tokens,
        )

        print()
        print("MODEL RESPONSE")
        print("=" * 70)
        print(response)
        print("=" * 70)

        print(
            f"Generation time: {generation_time:.2f}s"
        )

        print(
            f"Generated tokens: {generated_tokens}"
        )

        if torch.cuda.is_available():
            print(
                f"GPU allocated: "
                f"{torch.cuda.memory_allocated() / (1024 ** 3):.2f} GB"
            )

        return {
            "prompt": request.prompt,
            "response": response,
            "generation_time": round(generation_time, 2),
            "generated_tokens": generated_tokens,
        }

    except Exception as e:

        print()
        print("=" * 70)
        print("GENERATION ERROR")
        print("=" * 70)
        print(str(e))

        return {
            "error": True,
            "message": str(e),
        }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    try:
        load_model()

        print()
        print("=" * 70)
        print("STARTING SERVER")
        print("=" * 70)

    except Exception as e:

        print()
        print("=" * 70)
        print("MODEL LOADING FAILED")
        print("=" * 70)
        print(str(e))

        raise


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
    )