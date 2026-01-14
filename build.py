import os
import nltk

def main():
    # baixa stopwords dentro do projeto (vira parte do bundle)
    os.makedirs("nltk_data", exist_ok=True)
    nltk.download("stopwords", download_dir="nltk_data")

    # treina e salva modelo dentro do bundle
    import train
    out = os.getenv("MODEL_PATH", "models/email_clf.joblib")
    train.train_and_save(out)

if __name__ == "__main__":
    main()
