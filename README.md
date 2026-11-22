# 📖 Quiz Bíblico

Quiz em Flask com os 66 livros da Bíblia (752 perguntas). Cada partida sorteia 5 perguntas do livro escolhido, mostra se a resposta foi certa ou errada e, no final, a pontuação.

- **Site no ar:** https://quiz-biblico-ymz7.onrender.com (Render, plano gratuito: a primeira abertura depois de um tempo parado pode levar uns 50 segundos)
- **Código:** https://github.com/Renataccoreaa/quiz-biblico

## Como funciona

- As perguntas **não se repetem entre partidas** do mesmo livro: o app lembra, no cookie do navegador, quais já saíram e só repete quando as inéditas acabam.
- A **ordem das alternativas é embaralhada** a cada partida.
- A tela inicial agrupa os livros em Antigo e Novo Testamento.

## Estrutura do projeto

| Arquivo | Para que serve |
|---|---|
| `app.py` | Aplicação Flask: rotas, sessão, CSRF, cabeçalhos de segurança |
| `perguntas.py` | Junta os arquivos de perguntas e define a ordem dos livros |
| `perguntas_p1.py` … `p4.py` | As perguntas (p1: Gênesis–Ester, p2: Jó–Malaquias, p3: Mateus–Colossenses, p4: 1 Tessalonicenses–Apocalipse) |
| `templates/` | Páginas HTML (`base`, `inicio`, `pergunta`, `resultado`) |
| `static/style.css` | Visual do site |
| `.env.example` | Modelo das variáveis de ambiente |
| `.env` | Suas variáveis reais. **Fica só na sua máquina** (está no `.gitignore`) |
| `requirements.txt` | Dependências Python |
| `Procfile` | Comando de inicialização (`gunicorn app:app`) |

## Rodar no seu computador

Requisitos: Python 3.10 ou mais novo.

1. Abra um terminal na pasta do projeto.
2. Crie o ambiente virtual e instale as dependências:
   ```
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   ```
   Se o comando `python` não funcionar no Windows, use `py` no lugar.
3. Crie o arquivo `.env` a partir do modelo (`copy .env.example .env`) e preencha:
   ```
   SECRET_KEY=<chave gerada no próximo passo>
   FLASK_DEBUG=1
   ```
4. Gere uma chave secreta e cole no `.env`:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
5. Inicie o app:
   ```
   .venv\Scripts\python app.py
   ```
6. Abra http://127.0.0.1:5000

> Com `FLASK_DEBUG=1` o app recarrega sozinho quando você edita arquivos e usa cookies sem a marca Secure, o que permite testar em `http://`. **Nunca use `FLASK_DEBUG=1` em produção.**

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | Sim (em produção) | Chave que assina o cookie de sessão. Sem ela, o app se recusa a iniciar (de propósito). Use uma chave diferente em cada ambiente. |
| `FLASK_DEBUG` | Não | `1` só em desenvolvimento local. Em produção, não defina ou deixe `0`. |

## Publicar no Render

O deploy é automático: cada push na branch `main` gera um novo deploy.

**Configuração do serviço (já feita)**
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Variável `SECRET_KEY` definida em **Environment** do serviço

**Para definir ou trocar a `SECRET_KEY` no Render**
1. Gere uma chave nova (comando acima). Não reutilize a do seu `.env`.
2. No painel do Render, abra o serviço **quiz-biblico**.
3. No menu lateral, na seção **MANAGE**, clique em **Environment**. (Atenção: a seta "← Environment" no topo do menu só volta para a lista de serviços, e o menu **New → Env Group** não é o certo.)
4. Clique em **+ Add Environment Variable**, preencha Key `SECRET_KEY` e o Value com a chave.
5. Salve com **Save and deploy**.
6. Em **Deploys**, acompanhe até o status ficar **Live**.

> Trocar a `SECRET_KEY` invalida os cookies existentes: quem estiver no meio de um quiz volta para o início. Não há outro efeito.

**Se o deploy falhar:** o Render mantém a versão anterior no ar. Abra **Logs** e leia a mensagem de erro. O erro `Defina a variável de ambiente SECRET_KEY` significa que a variável não está definida no serviço.

## Adicionar ou editar perguntas

1. Abra o arquivo do livro (veja a tabela de estrutura) e adicione um item no formato:
   ```python
   {"pergunta": "Quem construiu a arca?", "opcoes": ["Moisés", "Noé", "Abraão", "Davi"], "resposta_correta": 1},
   ```
   - Sempre **4 alternativas, todas diferentes**.
   - `resposta_correta` é o **índice** da alternativa certa, **começando em 0** (0 = primeira, 3 = quarta).
   - Não precisa embaralhar as alternativas na mão: o app embaralha.
2. Evite perguntas cuja resposta aparece no próprio enunciado ou que tenham mais de uma resposta defensável. Confira o texto bíblico (Almeida) quando tiver dúvida.
3. Teste localmente e publique:
   ```
   git add -A
   git commit -m "Descreva a mudança"
   git push origin main
   ```
   O Render publica sozinho.

Para adicionar um **livro novo** (ex.: um deuterocanônico), crie a lista no arquivo de perguntas e inclua o nome na lista `_ANTIGO` ou `_NOVO` de `perguntas.py`. A tela inicial monta os botões a partir dessas listas.

## Segurança

- A chave secreta vem do ambiente e nunca fica no código nem no GitHub.
- O cookie de sessão tem `HttpOnly`, `SameSite=Lax` e `Secure` (fora do modo debug).
- Todas as rotas POST exigem token CSRF; livro e opção escolhida são validados no servidor.
- A sessão guarda só índices de perguntas, nunca o texto das respostas corretas.
- Cabeçalhos: CSP restritiva (sem scripts), `X-Frame-Options`, `nosniff` e `Referrer-Policy`.
- Limitação conhecida: o cookie é assinado, mas não criptografado. Quem decodificá-lo e cruzar com as perguntas (que estão no GitHub público) consegue descobrir as respostas. Isso afeta apenas o placar.
- Nunca faça commit do `.env`. Se uma chave vazar, gere outra e atualize no Render.

## Problemas comuns

| Sintoma | Causa e solução |
|---|---|
| `RuntimeError: Defina a variável de ambiente SECRET_KEY` | Falta a `SECRET_KEY` no `.env` (local) ou em Environment (Render). |
| Site abre muito devagar na primeira vez | Plano gratuito do Render desliga a instância por inatividade. Aguarde cerca de 50 segundos. |
| Deploy no Render falhou | Veja **Logs**. A versão anterior continua no ar até um deploy dar certo. |
| O quiz volta sempre para a tela inicial | O navegador está bloqueando cookies, ou a `SECRET_KEY` mudou no meio do quiz. |
| Localmente o quiz volta para o início | Verifique se o `.env` tem `FLASK_DEBUG=1` (sem isso o cookie Secure não funciona em `http://`). |
