import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def _ensure_nltk():
    try:
        from nltk.corpus import stopwords  # noqa
        _ = stopwords.words("portuguese")
    except Exception:
        import nltk
        nltk.download("stopwords")

from app.services.nlp import preprocess_for_ml

# ✅ FUNÇÃO TOP-LEVEL (PICKLABLE) – substitui o lambda
def tfidf_preprocess(s: str) -> str:
    return preprocess_for_ml(s)

def train_and_save(model_path: str = "models/email_clf.joblib"):
    _ensure_nltk()

    df = pd.read_csv("data/sample_emails.csv")
    X = df["text"].astype(str).tolist()
    y = df["label"].astype(str).tolist()

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            preprocessor=tfidf_preprocess,   # ✅ aqui
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
        )),
        ("clf", LogisticRegression(max_iter=500))
    ])

    pipeline.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"✅ Modelo salvo em: {model_path}")

if __name__ == "__main__":
    out = os.getenv("MODEL_PATH", "models/email_clf.joblib")
    train_and_save(out)
