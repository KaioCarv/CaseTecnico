import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

from .services.extractor import extract_text_from_upload
from .services.classifier import classify_email
from .services.responder import suggest_reply

bp = Blueprint("main", __name__)

ALLOWED_EXT = {"txt", "pdf"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@bp.get("/")
def index():
    return render_template("index.html")


@bp.post("/process")
def process():
    email_text = (request.form.get("email_text") or "").strip()
    uploaded = request.files.get("email_file")

    # Se veio arquivo, ele prevalece.
    if uploaded and uploaded.filename:
        if not _allowed(uploaded.filename):
            return render_template(
                "index.html",
                error="Formato inválido. Envie .txt ou .pdf, ou cole o texto do email.",
                prev_text=email_text,
            )

        filename = secure_filename(uploaded.filename)
        email_text = extract_text_from_upload(uploaded, filename)

    if not email_text:
        return render_template(
            "index.html",
            error="Envie um arquivo ou cole o texto do email antes de processar.",
            prev_text="",
        )

    result = classify_email(email_text)
    reply = suggest_reply(email_text, result)

    return render_template(
        "index.html",
        result=result,
        reply=reply,
        prev_text=email_text[:8000],  # mantém UX sem estourar html
    )
