from pathlib import Path
from typing import Any, cast

from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "unitary/toxic-bert"
SAVE_DIR = Path("/app/model")

SAVE_DIR.mkdir(parents=True, exist_ok=True)

tokenizer = cast(Any, AutoTokenizer.from_pretrained(MODEL_NAME))
model = cast(Any, AutoModelForSequenceClassification.from_pretrained(MODEL_NAME))

tokenizer.save_pretrained(SAVE_DIR)
model.save_pretrained(SAVE_DIR)

print(f"Saved model to {SAVE_DIR.resolve()}")
