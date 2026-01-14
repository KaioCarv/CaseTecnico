# Email Classificador IA (Produtivo / Improdutivo)

Aplicação web simples que:
- faz upload/paste de email (.txt/.pdf)
- classifica em Produtivo/Improdutivo
- sugere resposta automática

## Rodando local (sem Docker)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

python train.py
gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app

#Pelo docker:
docker compose up --build