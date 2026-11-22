# perguntas.py
# Banco de perguntas do quiz, organizado por livro da Bíblia.
#
# As perguntas ficam em quatro arquivos (perguntas_p1..p4.py). Cada pergunta é um dict:
#   - "pergunta": texto da pergunta
#   - "opcoes": lista com 4 alternativas
#   - "resposta_correta": ÍNDICE (0 a 3) da alternativa certa
#
# Para adicionar perguntas, edite o arquivo do livro correspondente.

from perguntas_p1 import PERGUNTAS as _P1
from perguntas_p2 import PERGUNTAS as _P2
from perguntas_p3 import PERGUNTAS as _P3
from perguntas_p4 import PERGUNTAS as _P4

_TODAS = {**_P1, **_P2, **_P3, **_P4}

# Ordem canônica dos livros (também define como a tela inicial os agrupa).
_ANTIGO = [
    "Gênesis", "Êxodo", "Levítico", "Números", "Deuteronômio", "Josué",
    "Juízes", "Rute", "1 Samuel", "2 Samuel", "1 Reis", "2 Reis",
    "1 Crônicas", "2 Crônicas", "Esdras", "Neemias", "Ester", "Jó",
    "Salmos", "Provérbios", "Eclesiastes", "Cantares", "Isaías", "Jeremias",
    "Lamentações", "Ezequiel", "Daniel", "Oseias", "Joel", "Amós", "Obadias",
    "Jonas", "Miqueias", "Naum", "Habacuque", "Sofonias", "Ageu", "Zacarias",
    "Malaquias",
]
_NOVO = [
    "Mateus", "Marcos", "Lucas", "João", "Atos", "Romanos", "1 Coríntios",
    "2 Coríntios", "Gálatas", "Efésios", "Filipenses", "Colossenses",
    "1 Tessalonicenses", "2 Tessalonicenses", "1 Timóteo", "2 Timóteo",
    "Tito", "Filemom", "Hebreus", "Tiago", "1 Pedro", "2 Pedro", "1 João",
    "2 João", "3 João", "Judas", "Apocalipse",
]

GRUPOS = [("Antigo Testamento", _ANTIGO), ("Novo Testamento", _NOVO)]

BANCO_DE_PERGUNTAS = {livro: _TODAS[livro] for livro in _ANTIGO + _NOVO}
