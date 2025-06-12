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
        json.dump(dados, f, indent=4)  # Salva a lista de dicionários no arquivo

# Função para salvar a matriz de estoque em um arquivo JSON
def salvar_estoque(estoque, caminho='estoque.json'):
    # Converte tudo pra lista 
    matriz_serializavel = [[list(pilha) for pilha in linha] for linha in estoque]
    with open(caminho, 'w') as f:  # Abre o arquivo JSON para escrita
        json.dump(matriz_serializavel, f)  # Salva a matriz no arquivo

# Função p carregar a matriz 
def carregar_estoque(caminho='estoque.json'):
    try:
        with open(caminho, 'r') as f:  # Abre o arquivo JSON para leitura
            matriz = json.load(f)  # Carrega a matriz do arquivo
            matriz_corrigida = []
            for linha in matriz[:8]:  # ajeita p os tamanhos de 8 linhas e 5 colunas 
                nova_linha = []
                for pilha in linha[:5]:  # mostra as prateleiras 
                    # Garante que cada pilha caiba 5 engradados 
                    nova_linha.append(list(pilha)[:5])
                # Preenche com pilhas vazias se faltar
                while len(nova_linha) < 5:
                    nova_linha.append([])
                matriz_corrigida.append(nova_linha)
            # enquanto a linha for menor q 5 coloca naquela linha _
            while len(matriz_corrigida) < 8:
                matriz_corrigida.append([[] for _ in range(5)])
            return matriz_corrigida  # Retorna a matriz corrigida
    except FileNotFoundError:
        return [[[] for _ in range(5)] for _ in range(8)]  # Retorna matriz vazia se não existir