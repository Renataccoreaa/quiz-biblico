# perguntas.py
# Aqui guardamos todas as perguntas do quiz, organizadas por livro da Bíblia.
#
# Cada pergunta é um dicionário (dict) com:
#   - "pergunta": o texto da pergunta
#   - "opcoes": uma lista com 4 alternativas possíveis
#   - "resposta_correta": o ÍNDICE (posição) da opção certa na lista "opcoes"
#     (lembrando que em Python a contagem começa do 0, não do 1!)
#
# Exemplo: se "resposta_correta" é 2, a opção certa é a de índice 2,
# ou seja, a TERCEIRA opção da lista (posições 0, 1, 2...).

BANCO_DE_PERGUNTAS = {
    "Gênesis": [
        {
            "pergunta": "Quem foi o primeiro homem criado por Deus?",
            "opcoes": ["Adão", "Noé", "Abraão", "Moisés"],
            "resposta_correta": 0
        },
        {
            "pergunta": "Quantos dias Deus levou para criar o mundo (incluindo o descanso)?",
            "opcoes": ["5 dias", "6 dias", "7 dias", "10 dias"],
            "resposta_correta": 2
        },
        {
            "pergunta": "Qual foi o nome da esposa de Adão?",
            "opcoes": ["Sara", "Eva", "Rebeca", "Raquel"],
            "resposta_correta": 1
        },
        {
            "pergunta": "Quem construiu uma arca para sobreviver ao Dilúvio?",
            "opcoes": ["Noé", "Jó", "Davi", "Jonas"],
            "resposta_correta": 0
        },
        {
            "pergunta": "Quais foram os dois filhos de Adão e Eva mencionados primeiro?",
            "opcoes": ["Esaú e Jacó", "Caim e Abel", "Isaque e Ismael", "Moisés e Arão"],
            "resposta_correta": 1
        },
        {
            "pergunta": "Em que cidade Deus destruiu por causa da maldade de seus habitantes, junto com Gomorra?",
            "opcoes": ["Babel", "Sodoma", "Nínive", "Jericó"],
            "resposta_correta": 1
        },
    ],

    "Êxodo": [
        {
            "pergunta": "Quem liderou o povo de Israel para fora do Egito?",
            "opcoes": ["Moisés", "Josué", "Arão", "Davi"],
            "resposta_correta": 0
        },
        {
            "pergunta": "Quantas pragas Deus enviou ao Egito?",
            "opcoes": ["7", "8", "10", "12"],
            "resposta_correta": 2
        },
        {
            "pergunta": "O que Moisés recebeu no Monte Sinai?",
            "opcoes": ["Os Dez Mandamentos", "A Arca da Aliança", "O Livro de Davi", "As chaves do templo"],
            "resposta_correta": 0
        },
        {
            "pergunta": "Qual mar foi aberto para o povo de Israel atravessar?",
            "opcoes": ["Mar Morto", "Mar da Galileia", "Mar Vermelho", "Mar Mediterrâneo"],
            "resposta_correta": 2
        },
        {
            "pergunta": "Quem era o faraó que perseguiu os israelitas (de forma genérica no relato)?",
            "opcoes": ["O faraó do Egito", "O rei da Babilônia", "O rei de Nínive", "O rei dos filisteus"],
            "resposta_correta": 0
        },
        {
            "pergunta": "O que o povo recebia diariamente no deserto para se alimentar?",
            "opcoes": ["Pão de trigo", "Maná", "Mel", "Leite e mel"],
            "resposta_correta": 1
        },
    ],

    "Salmos": [
        {
            "pergunta": "Quem é tradicionalmente apontado como autor da maioria dos Salmos?",
            "opcoes": ["Salomão", "Davi", "Moisés", "Isaías"],
            "resposta_correta": 1
        },
        {
            "pergunta": "Qual Salmo começa com 'O Senhor é o meu pastor'?",
            "opcoes": ["Salmo 1", "Salmo 23", "Salmo 91", "Salmo 119"],
            "resposta_correta": 1
        },
        {
            "pergunta": "Qual é o maior capítulo (Salmo) da Bíblia?",
            "opcoes": ["Salmo 100", "Salmo 119", "Salmo 150", "Salmo 23"],
            "resposta_correta": 1
        },
        {
            "pergunta": "Os Salmos são, em sua maioria, escritos em forma de quê?",
            "opcoes": ["Cartas", "Provérbios", "Poemas e cânticos", "Leis"],
            "resposta_correta": 2
        },
        {
            "pergunta": "Qual destas palavras aparece com frequência no final dos versículos dos Salmos como uma pausa ou exclamação?",
            "opcoes": ["Amém", "Selá", "Aleluia", "Hossana"],
            "resposta_correta": 1
        },
        {
            "pergunta": "O livro de Salmos faz parte de qual seção da Bíblia?",
            "opcoes": ["Novo Testamento", "Antigo Testamento", "Evangelhos", "Cartas Paulinas"],
            "resposta_correta": 1
        },
    ],

    "João": [
        {
            "pergunta": "Como começa o Evangelho de João?",
            "opcoes": [
                "'No princípio era o Verbo'",
                "'Bem-aventurados os pobres'",
                "'Naqueles dias apareceu João Batista'",
                "'Livro da geração de Jesus Cristo'"
            ],
            "resposta_correta": 0
        },
        {
            "pergunta": "Qual foi o primeiro milagre de Jesus relatado no Evangelho de João?",
            "opcoes": [
                "Multiplicação dos pães",
                "Curar um cego",
                "Transformar água em vinho",
                "Andar sobre as águas"
            ],
            "resposta_correta": 2
        },
        {
            "pergunta": "Quem era o discípulo que, segundo o livro, Jesus amava?",
            "opcoes": ["Pedro", "Tomé", "João", "André"],
            "resposta_correta": 2
        },
        {
            "pergunta": "Qual discípulo duvidou da ressurreição de Jesus até ver as marcas dos cravos?",
            "opcoes": ["Tomé", "Filipe", "Mateus", "Tiago"],
            "resposta_correta": 0
        },
        {
            "pergunta": "Em João 3:16, o que Deus deu ao mundo por amor?",
            "opcoes": ["A lei", "Seu filho unigênito", "Os profetas", "Os mandamentos"],
            "resposta_correta": 1
        },
        {
            "pergunta": "Quem Jesus ressuscitou dos mortos depois de 4 dias no túmulo, segundo João?",
            "opcoes": ["Lázaro", "Jairo", "O filho da viúva", "Zaqueu"],
            "resposta_correta": 0
        },
    ],
}
