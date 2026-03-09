from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class ToxicClassifier:
    def __init__(self, model_name: str = "unitary/toxic-bert") -> None:
        self._tokenizer: Any = AutoTokenizer.from_pretrained(model_name)
        self._model: Any = AutoModelForSequenceClassification.from_pretrained(
            model_name
        )
        self._model.eval()

    def predict_proba(self, text: str) -> float:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        inputs = self._tokenizer(
            text,
            truncation=True,
            padding=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            logits = self._model(**inputs).logits
            probs = torch.sigmoid(logits)

        return float(probs[0][0].item())

    def predict(self, text: str, threshold: float = 0.5) -> bool:
        return self.predict_proba(text) >= threshold
