import re
from typing import Optional
from .classifier import ClassificationResult
from .llm import llm_classify_and_reply
from .nlp import normalize

def _detect_intent(text: str) -> str:
    t = normalize(text)

    if re.search(r"\b(status|andamento|atualiza|previs[aã]o|prazo|follow[- ]?up)\b", t):
        return "status"
    if re.search(r"\b(erro|bug|falha|problema|não funciona|nao funciona|instável|instavel)\b", t):
        return "suporte"
    if re.search(r"\b(anexo|anexei|arquivo|pdf|planilha|documento|segue)\b", t):
        return "arquivo"
    if re.search(r"\b(obrigad|valeu|parab[eé]ns|feliz natal|feliz ano|bom dia|boa tarde|boa noite)\b", t):
        return "cumprimento"
    return "geral"


def suggest_reply(email_text: str, result: ClassificationResult) -> str:
    raw = normalize(email_text)

    # Se veio de LLM, usa a resposta sugerida dele (quando existir)
    if result.method == "llm" and result.hints and result.hints.get("llm_reply"):
        return result.hints["llm_reply"].strip()

    intent = _detect_intent(raw)

    if result.category == "Improdutivo":
        if intent == "cumprimento":
            return (
                "Obrigado pela mensagem! 😊\n"
                "Desejamos o mesmo a você. Qualquer necessidade, estamos à disposição."
            )
        return (
            "Obrigado pelo contato!\n"
            "Mensagem recebida. Se houver alguma solicitação específica, pode nos enviar que ajudamos."
        )

    # Produtivo
    if intent == "status":
        return (
            "Olá! Obrigado pelo contato.\n"
            "Estamos verificando o status da sua solicitação e retornaremos com uma atualização em breve.\n"
            "Se puder, informe o número do chamado/requisição para agilizar."
        )
    if intent == "suporte":
        return (
            "Olá! Entendi o problema.\n"
            "Para avançarmos, poderia enviar:\n"
            "1) passo a passo para reproduzir,\n"
            "2) prints/erro exibido,\n"
            "3) data/horário aproximado.\n"
            "Assim que recebermos, seguimos com a análise."
        )
    if intent == "arquivo":
        return (
            "Olá! Arquivo recebido.\n"
            "Vamos analisar o conteúdo e retornaremos com os próximos passos ou confirmação de recebimento."
        )

    return (
        "Olá! Obrigado pelo email.\n"
        "Para que possamos ajudar mais rápido, poderia detalhar o que você precisa (e informar o ID do caso/chamado, se houver)?"
    )
