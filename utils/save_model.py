from typing import Any
from pathlib import Path

from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "unitary/toxic-bert"
SAVE_DIR = Path("/app/model")

SAVE_DIR.mkdir(parents=True, exist_ok=True)

tokenizer: Any = AutoTokenizer.from_pretrained(MODEL_NAME)
model: Any = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

tokenizer.save_pretrained(SAVE_DIR)
model.save_pretrained(SAVE_DIR)

print(f"Saved model to {SAVE_DIR.resolve()}")
