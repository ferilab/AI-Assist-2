
from llama_cpp import Llama
from backend.config import MODEL_PATH
import os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print('Base_dir:        ', BASE_DIR)

llm = Llama(
    model_path=os.path.join(BASE_DIR, MODEL_PATH),
    n_ctx=1024,
    n_threads=6,      # i7 safe value
    n_gpu_layers=1,    # Metal acceleration
    verbose=False
)

def generate(prompt: str) -> str:
    output = llm(prompt, max_tokens=128, temperature=0.1, top_p=0.9, stop=["</s>"])
    return output["choices"][0]["text"].strip()

