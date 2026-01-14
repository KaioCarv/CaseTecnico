import os
import json
from typing import Optional, Dict

def llm_enabled() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))

def llm_classify_and_reply(email_text: str) -> Optional[Dict]:
    """
    Retorna dict com:
      {
        "category": "Produtivo" | "Improdutivo",
        "confidence": 0-100,
        "reply": "..."
      }
    Se não houver chave, retorna None.
    """
    if not llm_enabled():
        return None

    # Import local para não exigir pacote se você não usar LLM
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    system = (
        "Você é um assistente que classifica emails e sugere respostas curtas e profissionais. "
        "Categorias: Produtivo (precisa ação/resposta específica) e Improdutivo (sem ação imediata). "
        "Responda SOMENTE em JSON válido no formato: "
        '{"category":"Produtivo|Improdutivo","confidence":0-100,"reply":"..."}'
    )

    user = (
        "Classifique e sugira resposta. Email:\n"
        "-----\n"
        f"{email_text}\n"
        "-----"
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )

    content = resp.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        if "category" in data and "reply" in data:
            return data
    except Exception:
        return None

    return None
