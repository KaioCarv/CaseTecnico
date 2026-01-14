# Email Classificador IA (Produtivo / Improdutivo)

Aplicação web para **automatizar a triagem de emails** em ambientes com alto volume (ex.: setor financeiro), classificando mensagens como **Produtivo** ou **Improdutivo** e sugerindo uma **resposta automática**.

> **Destaques**
- Upload ou colagem do conteúdo do email (`.txt` / `.pdf`)
- Classificação + confiança + método (LLM ou ML local)
- Sugestão de resposta pronta para copiar
- **LLM (OpenAI) opcional** para melhorar qualidade
- **Fallback automático** para modelo local (TF-IDF + Logistic Regression)
- Deploy simplificado via **Docker + Gunicorn**

---

## Demo rápida
1. Cole o texto do email **ou** envie um arquivo `.txt`/`.pdf`
2. Clique em **Processar email**
3. Veja a **categoria** e a **resposta sugerida**

---

## Stack
- **Backend:** Python + Flask
- **NLP/ML:** NLTK (stopwords), scikit-learn (TF-IDF + Logistic Regression), joblib
- **PDF:** PyPDF2
- **UI:** HTML + Bootstrap + JS
- **Deploy:** Docker + Gunicorn

---

## Requisitos
- Docker + Docker Compose (**recomendado**)  
  **ou**
- Python 3.10+ (para rodar sem Docker)

---

## Configuração de ambiente

Crie o arquivo `.env` na raiz do projeto (ou copie o exemplo):

```bash
cp .env.example .env
