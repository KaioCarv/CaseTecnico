import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from app.services.nlp import preprocess_for_ml


def _ensure_nltk():
    """
    No Vercel/serverless, use /tmp para guardar nltk_data.
    Local/Docker também funciona.
    """
    import nltk
    from nltk.corpus import stopwords

    nltk_data_dir = os.environ.get("NLTK_DATA", "/tmp/nltk_data")
    os.makedirs(nltk_data_dir, exist_ok=True)

    if nltk_data_dir not in nltk.data.path:
        nltk.data.path.append(nltk_data_dir)

    try:
        _ = stopwords.words("portuguese")
    except LookupError:
        nltk.download("stopwords", download_dir=nltk_data_dir)


# ✅ FUNÇÃO TOP-LEVEL (PICKLABLE)
def tfidf_preprocess(s: str) -> str:
    return preprocess_for_ml(s)


def train_and_save(model_path: str | None = "models/email_clf.joblib"):
    """
    - Se model_path for string: tenta salvar em disco (local/Docker).
    - Se model_path for None: não salva, retorna o pipeline (serverless-friendly).
    """
    _ensure_nltk()

    df = pd.read_csv("data/sample_emails.csv")
    X = df["text"].astype(str).tolist()
    y = df["label"].astype(str).tolist()

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            preprocessor=tfidf_preprocess,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
        )),
        ("clf", LogisticRegression(max_iter=500))
    ])

    pipeline.fit(X, y)

    if model_path:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(pipeline, model_path)
        print(f"✅ Modelo salvo em: {model_path}")

    return pipeline


if __name__ == "__main__":
    out = os.getenv("MODEL_PATH", "models/email_clf.joblib")
    train_and_save(out)
