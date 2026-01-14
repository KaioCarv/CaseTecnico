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
    import os
    import nltk
    from nltk.corpus import stopwords

    # guarda dados em /tmp (local gravável no serverless)
    nltk_data_dir = os.environ.get("NLTK_DATA", "/tmp/nltk_data")
    os.makedirs(nltk_data_dir, exist_ok=True)

    if nltk_data_dir not in nltk.data.path:
        nltk.data.path.append(nltk_data_dir)

    try:
        _ = stopwords.words("portuguese")
    except LookupError:
        nltk.download("stopwords", download_dir=nltk_data_dir)


_model_cache = None

def _load_or_train_model():
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    # tenta carregar se existir
    if os.path.exists(MODEL_PATH):
        try:
            _model_cache = joblib.load(MODEL_PATH)
            return _model_cache
        except Exception:
            pass

    # treina em runtime e usa cache em memória
    from train import train_and_save
    try:
        train_and_save(MODEL_PATH)          # tenta salvar se der
        _model_cache = joblib.load(MODEL_PATH)
    except Exception:
        # se não conseguir salvar (serverless), treina e retorna o pipeline direto
        _model_cache = train_and_save(None)  # vou te mostrar abaixo

    return _model_cache




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
