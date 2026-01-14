import re
from typing import List
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

_PT = set(stopwords.words("portuguese"))
_EN = set(stopwords.words("english"))
_STOP = _PT | _EN

_stem_pt = SnowballStemmer("portuguese")
_stem_en = SnowballStemmer("english")


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    # mantém letras/números, corta pontuação
    return re.findall(r"[a-zà-ú0-9]+", text.lower())


def preprocess_for_ml(text: str) -> str:
    """
    Retorna string "limpa" (tokens filtrados) para vetorização.
    """
    toks = tokenize(text)
    toks = [t for t in toks if t not in _STOP and len(t) >= 2]

    # Stemming “leve” (melhora generalização no dataset pequeno)
    stemmed = []
    for t in toks:
        # heurística simples: se tiver acento/ç, tende a pt; senão tenta pt e en igual
        if re.search(r"[à-úç]", t):
            stemmed.append(_stem_pt.stem(t))
        else:
            stemmed.append(_stem_pt.stem(t))
    return " ".join(stemmed)
