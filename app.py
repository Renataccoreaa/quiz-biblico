# app.py
# Este é o "cérebro" da aplicação. Aqui usamos o Flask para criar rotas,
# ou seja, "endereços" do site (como /inicio, /pergunta, etc).

from flask import Flask, render_template, request, session, redirect, url_for
import random

from perguntas import BANCO_DE_PERGUNTAS

# Cria a aplicação Flask
app = Flask(__name__)

# A "secret_key" é necessária para o Flask poder usar "session".
# Session é uma forma de guardar informações do usuário enquanto ele
# navega pelo site (tipo: "qual pergunta ele está agora", "quantos pontos tem").
# Em produção isso deveria ser uma chave secreta de verdade, mas para
# aprendizado, qualquer texto serve.
app.secret_key = "minha_chave_secreta_para_o_quiz_biblico"

NUMERO_DE_PERGUNTAS = 5


@app.route("/")
def inicio():
    """
    Rota da página inicial.
    Aqui mostramos a lista de livros da Bíblia disponíveis para o usuário escolher.
    """
    livros_disponiveis = list(BANCO_DE_PERGUNTAS.keys())
    return render_template("inicio.html", livros=livros_disponiveis)


@app.route("/comecar", methods=["POST"])
def comecar():
    """
    Esta rota é chamada quando o usuário clica em "Começar Quiz" na tela inicial.
    Ela recebe o livro escolhido, sorteia 5 perguntas, e guarda tudo na sessão.
    """
    livro_escolhido = request.form.get("livro")

    # Pega todas as perguntas daquele livro
    todas_perguntas = BANCO_DE_PERGUNTAS.get(livro_escolhido, [])

    # Sorteia 5 perguntas aleatórias (sem repetir) daquele livro.
    # Se o livro tiver menos de 5 perguntas cadastradas, pega todas que existem.
    quantidade = min(NUMERO_DE_PERGUNTAS, len(todas_perguntas))
    perguntas_sorteadas = random.sample(todas_perguntas, quantidade)

    # Guardamos na "session" (memória temporária do usuário):
    session["livro"] = livro_escolhido
    session["perguntas"] = perguntas_sorteadas
    session["pergunta_atual"] = 0   # começamos na pergunta de índice 0
    session["pontuacao"] = 0

    return redirect(url_for("pergunta"))


@app.route("/pergunta", methods=["GET", "POST"])
def pergunta():
    """
    Esta rota mostra a pergunta atual e também processa a resposta
    que o usuário enviou (quando ele clica numa opção).
    """

    # Se o método for POST, significa que o usuário ACABOU de responder
    # a pergunta anterior. Então primeiro processamos essa resposta.
    if request.method == "POST":
        resposta_escolhida = int(request.form.get("opcao"))
        indice_atual = session["pergunta_atual"]
        pergunta_respondida = session["perguntas"][indice_atual]

        if resposta_escolhida == pergunta_respondida["resposta_correta"]:
            session["pontuacao"] += 1

        # Avança para a próxima pergunta
        session["pergunta_atual"] += 1

    indice_atual = session["pergunta_atual"]
    perguntas = session["perguntas"]

    # Se já passou da última pergunta, vai para a tela de resultado
    if indice_atual >= len(perguntas):
        return redirect(url_for("resultado"))

    pergunta_atual = perguntas[indice_atual]

    return render_template(
        "pergunta.html",
        pergunta=pergunta_atual,
        numero=indice_atual + 1,
        total=len(perguntas),
        livro=session["livro"],
    )


@app.route("/resultado")
def resultado():
    """
    Mostra a pontuação final do usuário.
    """
    pontuacao = session.get("pontuacao", 0)
    total = len(session.get("perguntas", []))
    livro = session.get("livro", "")

    return render_template(
        "resultado.html",
        pontuacao=pontuacao,
        total=total,
        livro=livro,
    )


# Este bloco só executa quando rodamos "python app.py" diretamente
# (e não quando o arquivo é importado por outro script).
if __name__ == "__main__":
    app.run(debug=True)