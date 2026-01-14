import os
from dataclasses import dataclass
from typing import Optional, Dict

import joblib

from .nlp import normalize, preprocess_for_ml
from .llm import llm_classify_and_reply

MODEL_PATH = os.getenv("MODEL_PATH", "models/email_clf.joblib")

@dataclass
class ClassificationResult:
    category: str               # "Produtivo" | "Improdutivo"
    confidence: int             # 0-100
    method: str                 # "llm" | "ml"
    hints: Optional[Dict] = None


def _ensure_nltk():
    """
    Garante stopwords no runtime (especialmente em deploy).
    """
    try:
        import nltk
        from nltk.corpus import stopwords  # noqa
        _ = stopwords.words("portuguese")
    except Exception:
        import nltk
        nltk.download("stopwords")


def _load_or_train_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass  # modelo inválido/corrompido -> re-treina

    from train import train_and_save
    train_and_save(MODEL_PATH)
    return joblib.load(MODEL_PATH)



def classify_email(email_text: str) -> ClassificationResult:
    _ensure_nltk()
    raw = normalize(email_text)

    # 1) Tenta LLM (se houver chave)
    llm_out = llm_classify_and_reply(raw)
    if llm_out:
        cat = "Produtivo" if llm_out.get("category") == "Produtivo" else "Improdutivo"
        conf = int(max(0, min(100, llm_out.get("confidence", 75))))
        return ClassificationResult(category=cat, confidence=conf, method="llm", hints={"llm_reply": llm_out.get("reply", "")})

    # 2) Fallback ML local
    model = _load_or_train_model()
    x = preprocess_for_ml(raw)

    proba = model.predict_proba([x])[0]
    # Classes ordenadas conforme model.classes_
    classes = list(model.classes_)
    idx_prod = classes.index("Produtivo") if "Produtivo" in classes else 0

    p_prod = float(proba[idx_prod])
    category = "Produtivo" if p_prod >= 0.5 else "Improdutivo"
    confidence = int(round(max(p_prod, 1 - p_prod) * 100))

    return ClassificationResult(category=category, confidence=confidence, method="ml")
