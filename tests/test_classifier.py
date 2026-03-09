import pytest
import torch

from toxic_service.classifier import ToxicClassifier


class FakeTokenizer:
    def __call__(self, text, truncation, padding, return_tensors):
        return {"input_ids": torch.tensor([[1, 2, 3]])}


class FakeOutput:
    def __init__(self, logits):
        self.logits = logits


class FakeModel:
    def __init__(self, logits):
        self.logits = logits
        self.eval_called = False

    def eval(self):
        self.eval_called = True

    def __call__(self, **kwargs):
        return FakeOutput(self.logits)


def test_init_loads_tokenizer_and_model(monkeypatch):
    tokenizer = FakeTokenizer()
    model = FakeModel(torch.tensor([[0.0]]))

    monkeypatch.setattr(
        "toxic_service.classifier.AutoTokenizer.from_pretrained",
        lambda _: tokenizer,
    )
    monkeypatch.setattr(
        "toxic_service.classifier.AutoModelForSequenceClassification.from_pretrained",
        lambda _: model,
    )

    classifier = ToxicClassifier("dummy-model")

    assert classifier._tokenizer is tokenizer
    assert classifier._model is model
    assert model.eval_called is True


def test_predict_proba_raises_for_non_string():
    classifier = ToxicClassifier.__new__(ToxicClassifier)
    classifier._tokenizer = FakeTokenizer()
    classifier._model = FakeModel(torch.tensor([[0.0]]))

    with pytest.raises(TypeError):
        classifier.predict_proba(123)


def test_predict_proba_returns_probability():
    classifier = ToxicClassifier.__new__(ToxicClassifier)
    classifier._tokenizer = FakeTokenizer()
    classifier._model = FakeModel(torch.tensor([[0.0]]))

    proba = classifier.predict_proba("hello")

    assert isinstance(proba, float)
    assert 0.49 < proba < 0.51


def test_predict_respects_threshold():
    classifier = ToxicClassifier.__new__(ToxicClassifier)
    classifier._tokenizer = FakeTokenizer()
    classifier._model = FakeModel(torch.tensor([[2.0]]))
    assert classifier.predict("toxic") is True

    classifier._model = FakeModel(torch.tensor([[-2.0]]))
    assert classifier.predict("clean") is False
