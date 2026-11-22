# app.py
# Aplicação Flask do Quiz Bíblico.

import os
import random
import secrets

from dotenv import load_dotenv
from flask import (
    Flask, abort, redirect, render_template, request, session, url_for,
)

from perguntas import BANCO_DE_PERGUNTAS, GRUPOS

load_dotenv()  # lê o arquivo .env (se existir) para variáveis de ambiente

DEBUG = os.environ.get("FLASK_DEBUG") == "1"
NUMERO_DE_PERGUNTAS = 5

app = Flask(__name__)

# A chave secreta vem SEMPRE do ambiente (nunca fica no código).
# Em desenvolvimento (FLASK_DEBUG=1) geramos uma chave temporária; em
# produção, a ausência da variável impede a aplicação de subir.
_secret = os.environ.get("SECRET_KEY")
if not _secret:
    if DEBUG:
        _secret = secrets.token_hex(32)
    else:
        raise RuntimeError(
            "Defina a variável de ambiente SECRET_KEY (veja .env.example)."
        )
app.secret_key = _secret

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=not DEBUG,
)


@app.after_request
def cabecalhos_de_seguranca(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline'; "
        "script-src 'none'; frame-ancestors 'none'"
    )
    return resp


# ---------- CSRF simples baseado em token na sessão ----------

def _token_csrf():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = _token_csrf


@app.before_request
def verificar_csrf():
    if request.method == "POST":
        enviado = request.form.get("csrf", "")
        esperado = session.get("csrf", "")
        if not esperado or not secrets.compare_digest(enviado, esperado):
            abort(400)


# ---------- Rotas ----------

def _quiz_ativo():
    return "ids" in session and "livro" in session


@app.route("/")
def inicio():
    return render_template("inicio.html", grupos=GRUPOS)


@app.route("/comecar", methods=["POST"])
def comecar():
    livro = request.form.get("livro", "")
    if livro not in BANCO_DE_PERGUNTAS:
        abort(400)

    total = len(BANCO_DE_PERGUNTAS[livro])
    quantidade = min(NUMERO_DE_PERGUNTAS, total)

    # Evita repetir perguntas entre partidas: lembramos quais já saíram
    # para este livro e sorteamos primeiro entre as inéditas.
    vistas_por_livro = session.get("vistas", {})
    vistas = [i for i in vistas_por_livro.get(livro, []) if i < total]
    inéditas = [i for i in range(total) if i not in vistas]
    if len(inéditas) >= quantidade:
        ids = random.sample(inéditas, quantidade)
        vistas += ids
    else:  # acabaram as inéditas: completa com antigas e recomeça o ciclo
        antigas = [i for i in range(total) if i in vistas]
        ids = inéditas + random.sample(antigas, quantidade - len(inéditas))
        vistas = list(ids)
    vistas_por_livro.pop(livro, None)
    vistas_por_livro[livro] = vistas
    # mantém o cookie pequeno: só os 12 livros mais recentes
    vistas_por_livro = dict(list(vistas_por_livro.items())[-12:])

    # Embaralha a ordem das alternativas de cada pergunta (só guardamos
    # índices; as respostas corretas nunca vão para o cookie).
    ordens = [random.sample(range(4), 4) for _ in ids]

    csrf = _token_csrf()
    session.clear()
    session.update(csrf=csrf, livro=livro, ids=ids, ordens=ordens, atual=0,
                   pontos=0, feedback=None, vistas=vistas_por_livro)
    return redirect(url_for("pergunta"))


@app.route("/pergunta")
def pergunta():
    if not _quiz_ativo():
        return redirect(url_for("inicio"))

    atual, ids = session["atual"], session["ids"]
    if atual >= len(ids):
        return redirect(url_for("resultado"))

    livro = session["livro"]
    dados = BANCO_DE_PERGUNTAS[livro][ids[atual]]
    ordem = session["ordens"][atual]
    return render_template(
        "pergunta.html",
        pergunta=dados["pergunta"],
        opcoes=[dados["opcoes"][j] for j in ordem],
        numero=atual + 1,
        total=len(ids),
        livro=livro,
        feedback=session.get("feedback"),
        progresso=int(atual / len(ids) * 100),
    )


@app.route("/responder", methods=["POST"])
def responder():
    if not _quiz_ativo() or session.get("feedback"):
        return redirect(url_for("pergunta"))

    atual, ids = session["atual"], session["ids"]
    if atual >= len(ids):
        return redirect(url_for("resultado"))

    try:
        escolhida = int(request.form.get("opcao", ""))
    except ValueError:
        abort(400)

    dados = BANCO_DE_PERGUNTAS[session["livro"]][ids[atual]]
    ordem = session["ordens"][atual]
    if not 0 <= escolhida < len(ordem):
        abort(400)

    # posição da alternativa correta depois do embaralhamento
    correta = ordem.index(dados["resposta_correta"])
    if escolhida == correta:
        session["pontos"] += 1
    session["feedback"] = {"escolhida": escolhida, "correta": correta}
    return redirect(url_for("pergunta"))


@app.route("/proxima", methods=["POST"])
def proxima():
    if _quiz_ativo() and session.get("feedback"):
        session["atual"] += 1
        session["feedback"] = None
    return redirect(url_for("pergunta"))


@app.route("/resultado")
def resultado():
    if not _quiz_ativo() or session["atual"] < len(session["ids"]):
        return redirect(url_for("inicio"))
    return render_template(
        "resultado.html",
        pontuacao=session["pontos"],
        total=len(session["ids"]),
        livro=session["livro"],
    )


if __name__ == "__main__":
    app.run(debug=DEBUG)
