import re
from dataclasses import dataclass
from typing import Optional, Dict
from .llm import llm_classify_and_reply
from .nlp import normalize

@dataclass
class ClassificationResult:
    category: str
    confidence: int
    method: str
    hints: Optional[Dict] = None

def _heuristic_classify(text: str) -> ClassificationResult:
    t = normalize(text)

    productive_patterns = [
        r"\b(status|andamento|atualiza|previs[aã]o|prazo|follow[- ]?up)\b",
        r"\b(erro|bug|falha|problema|não funciona|nao funciona|instável|instavel)\b",
        r"\b(suporte|ajuda|chamado|ticket|requisi[cç][aã]o)\b",
        r"\b(anexo|arquivo|segue|documento|planilha)\b",
    ]
    unproductive_patterns = [
        r"\b(feliz natal|feliz ano|boas festas|parab[eé]ns|obrigad|valeu|agradec)\b",
        r"\b(bom dia|boa tarde|boa noite)\b",
    ]

    if any(re.search(p, t) for p in productive_patterns):
        return ClassificationResult("Produtivo", 75, "heuristic")

    if any(re.search(p, t) for p in unproductive_patterns):
        return ClassificationResult("Improdutivo", 75, "heuristic")

    # default conservador
    return ClassificationResult("Produtivo", 55, "heuristic")

def classify_email(email_text: str) -> ClassificationResult:
    raw = normalize(email_text)
    raw_for_llm = raw[:8000]  # evita PDF gigante

    llm_out = llm_classify_and_reply(raw_for_llm)
    if llm_out:
        cat = "Produtivo" if llm_out.get("category") == "Produtivo" else "Improdutivo"
        conf = int(max(0, min(100, llm_out.get("confidence", 75))))
        return ClassificationResult(category=cat, confidence=conf, method="llm", hints={"llm_reply": llm_out.get("reply", "")})

    return _heuristic_classify(raw)
