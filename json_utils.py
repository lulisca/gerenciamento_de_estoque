import json  # Importa o módulo json para manipulação de arquivos JSON
from infoproduto import Produto  # Importa a classe Produto definida em infoproduto.py

# Função para carregar produtos de um arquivo JSON
def carregar_produtos(caminho='produtos.json'):
    produtos = []  # Lista que armazenará os objetos Produto carregados
    try:
        with open(caminho, 'r') as f:  # Abre o arquivo JSON para leitura
            dados = json.load(f)  # Carrega os dados do arquivo em formato de lista de dicionários
            for p in dados:  # Para cada dicionário na lista
                produtos.append(Produto(**p))  # Cria um objeto Produto usando os dados e adiciona à lista
    except FileNotFoundError:  # Caso o arquivo não exista
        print("Arquivo de produtos não encontrado.")  # Exibe mensagem de erro
    return produtos  # Retorna a lista de produtos carregados

# Função para salvar produtos em um arquivo JSON
def salvar_produtos(produtos, caminho='produtos.json'):
    dados = [vars(p) for p in produtos]  # Converte cada Produto em dicionário
    with open(caminho, 'w') as f:  # Abre o arquivo JSON para escrita
        json.dump(dados, f, indent=4)  # Salva a lista de dicionários no arquivo, formatando com indentação

# Função para salvar a matriz de estoque em um arquivo JSON
def salvar_estoque(estoque, caminho='estoque.json'):
    # Converte todos os elementos para listas para garantir compatibilidade com JSON
    matriz_serializavel = [[list(pilha) for pilha in linha] for linha in estoque]
    with open(caminho, 'w') as f:  # Abre o arquivo JSON para escrita
        json.dump(matriz_serializavel, f)  # Salva a matriz no arquivo

# Função para carregar a matriz de estoque de um arquivo JSON
def carregar_estoque(caminho='estoque.json'):
    try:
        with open(caminho, 'r') as f:  # Abre o arquivo JSON para leitura
            matriz = json.load(f)  # Carrega a matriz do arquivo
            # Garante que cada posição seja uma lista (pilha) de tamanho máximo 5
            matriz_corrigida = []
            for linha in matriz[:8]:  # Considera apenas as primeiras 8 linhas
                nova_linha = []
                for pilha in linha[:5]:  # Considera apenas as primeiras 5 pilhas
                    # Garante que cada pilha tenha no máximo 5 elementos
                    nova_linha.append(list(pilha)[:5])
                # Preenche com pilhas vazias se faltar
                while len(nova_linha) < 5:
                    nova_linha.append([])
                matriz_corrigida.append(nova_linha)
            # Preenche com linhas de pilhas vazias se faltar
            while len(matriz_corrigida) < 8:
                matriz_corrigida.append([[] for _ in range(5)])
            return matriz_corrigida  # Retorna a matriz corrigida
    except FileNotFoundError:
        return [[[] for _ in range(5)] for _ in range(8)]  # Retorna matriz vazia se não existir