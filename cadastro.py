from infoproduto import Produto  # Importa a classe Produto definida em infoproduto.py
from json_utils import salvar_produtos, salvar_estoque, carregar_produtos, carregar_estoque  # Funções utilitárias para manipulação de arquivos JSON
from collections import deque  # Estrutura de dados fila
from datetime import datetime, timedelta  # Manipulação de datas

def cadastrar_produto():
    print("\n___ Cadastro de Produto ___")  
    nome = input("Nome: ")  
    codigo = input("Código: ")  
    peso = float(input("Peso (gramas): "))  
    data_fabricacao = input("Data de fabricação (DIA-MÊS-ANO) (DD-MM-AAAA): ")  
    validade = input("Data de validade (DIA-MÊS-ANO) (DD-MM-AAAA): ")  
    tamanho_engradado = input("Tamanho do engradado: ")  
    preco_compra = float(input("Preço de compra: "))  
    preco_venda = float(input("Preço de venda: "))  
    engradado = input("Identificação do engradado: ")  
    lote = int(input("Lote: "))  
    fornecedor = input("Fornecedor: ")  
    categoria = input("Categoria: ") 
    fabricante = input("Fabricante: ")  
    data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M")  
    print(f"Produto cadastrado em: {data_cadastro}")  
    # instancia e retorna c as propriedades
    return Produto(codigo, nome, peso, validade, preco_compra, preco_venda, engradado, lote, fornecedor, categoria, fabricante, data_fabricacao, tamanho_engradado, data_cadastro=data_cadastro)

def remover_produto(produtos, estoque):
    engradado_codigo = input("Digite o código do engradado a remover: ")  
    encontrado = False  # Flag para saber se encontrou o engradado
    for linha in estoque:  # Percorre as prateleiras
        for pilha in linha:  # Percorre as pilhas de cada prateleira
            if engradado_codigo in pilha:  # Se o engradado está na pilha
                pilha.remove(engradado_codigo)  # Remove o engradado da pilha
                encontrado = True # quer dizer que encontrou então  
    for i, produto in enumerate(produtos):  # Percorre a lista de produtos
        if produto.engradado == engradado_codigo:  # Se encontrou o produto pelo engradado
            del produtos[i]  # Remove o produto da lista
            salvar_produtos(produtos)  # Salva a lista de produtos
            salvar_estoque(estoque)  # Salva o estoque
            print(f"Produto e engradado '{engradado_codigo}' removidos com sucesso do estoque.")
            return
    if not encontrado:
        print(f"Engradado '{engradado_codigo}' não encontrado no estoque.")  # Mensagem se não encontrou
    else:
        print(f"Engradado '{engradado_codigo}' removido da pilha, mas produto não encontrado na lista.")  # Mensagem se só removeu da pilha

def inicializar_estoque():
    # Cria uma matriz 8x5, cada posição é uma pilha (lista)
    return [[[] for _ in range(5)] for _ in range(8)]

def adicionar_engradado(estoque, coluna, linha, engradado):
    pilha = estoque[linha][coluna]  # Seleciona a pilha
    if len(pilha) < 5:  # Se a pilha tem espaço
        pilha.append(engradado)  # Adiciona o engradado
        return True
    else:
        print("Pilha cheia! Não é possível adicionar mais engradados nesta posição.")  # Mensagem de erro
        return False

def remover_engradado(estoque, coluna, linha):
    pilha = estoque[linha][coluna]  # Seleciona a pilha
    if pilha:  # Se a pilha não está vazia
        return pilha.pop()  # Remove e retorna o topo
    else:
        print("Pilha vazia! Não há engradados para remover nesta posição.")  # Mensagem de erro
        return None

def consultar_topo(estoque, coluna, linha):
    pilha = estoque[linha][coluna]  # Seleciona a pilha
    if pilha:  # Se a pilha não está vazia
        return pilha[-1]  # Retorna o topo
    else:
        return None

def visualizar_estoque(estoque):
    print("\n=== Estoque (8 Prateleiras x 5 lugares, pilha máx 5) ===") 
    for i, linha in enumerate(estoque):  # Para cada prateleira
        lugares = []  # Lista para armazenar as pilhas
        for j in range(5):  # Para cada pilha
            pilha = linha[j] if j < len(linha) and isinstance(linha[j], list) else []  # S
            pilha_estatica = pilha.copy()[:5] + ['-'] * (5 - len(pilha))  # Garante 5 posições
            lugares.append(pilha_estatica)  # Adiciona à lista
        print(f"Prateleira {i+1}:", lugares)  # Exibe a prateleira

def encontrar_posicao_livre(estoque):
    # Procura a próxima posição livre na matriz
    for linha in range(8):
        for coluna in range(5):
            if len(estoque[linha][coluna]) < 5:
                return coluna, linha  # Retorna a posição livre
    return None  # Se não houver posição livre

class ItemPedido:
    def __init__(self, codigo_produto, quantidade, data_solicitacao, nome_solicitante):
        self.codigo_produto = codigo_produto  # Código do produto
        self.quantidade = quantidade  # Quantidade solicitada
        self.data_solicitacao = data_solicitacao  # Data do pedido
        self.nome_solicitante = nome_solicitante  # Nome de quem solicitou
    def __str__(self):
        return f"Produto: {self.codigo_produto}, Quantidade: {self.quantidade}, Data: {self.data_solicitacao}, Solicitante: {self.nome_solicitante}"

class FilaPedidos:
    def __init__(self):
        self.fila = deque()  # Inicializa a fila
    def adicionar_pedido(self, item_pedido):
        self.fila.append(item_pedido)  # Adiciona pedido à fila
    def processar_pedido(self):
        if self.fila:
            return self.fila.popleft()  # Remove e retorna o primeiro pedido
        else:
            print("Nenhum pedido na fila.")
            return None
    def visualizar_fila(self):
        if not self.fila:
            print("Fila de pedidos vazia.")
        else:
            print("\n=== Fila de Pedidos ===")
            for i, pedido in enumerate(self.fila, 1):
                print(f"{i}. {pedido}")

def produtos_proximos_vencimento(produtos, dias=30, idx=0, resultado=None):
    if resultado is None:
        resultado = []
    if idx >= len(produtos):
        # Ordena pelo vencimento mais próximo
        def get_data_validade(prod):
            validade = prod.validade
            try:
                return datetime.strptime(validade, "%d-%m-%Y")
            except ValueError:
                try:
                    return datetime.strptime(validade, "%Y-%m-%d")
                except Exception:
                    return datetime.max
        return sorted(resultado, key=get_data_validade)
    try:
        validade = produtos[idx].validade
        # Aceita formatos DD-MM-AAAA ou YYYY-MM-DD
        try:
            data_validade = datetime.strptime(validade, "%d-%m-%Y")
        except ValueError:
            data_validade = datetime.strptime(validade, "%Y-%m-%d")
        if data_validade <= datetime.now() + timedelta(days=dias):
            resultado.append(produtos[idx])
    except Exception as e:
        pass  # Ignora produtos com data inválida
    return produtos_proximos_vencimento(produtos, dias, idx+1, resultado)

def carregar_produtos_na_matriz(produtos, estoque): # ele corre pelos espaços da matriz até achar um espaço livre p encaixar o produto
    alterado = False  
    for produto in produtos:  
        encontrado = False
        for linha in estoque:
            for pilha in linha:
                if produto.engradado in pilha:
                    encontrado = True
                    break
            if encontrado:
                break
        if not encontrado:
            pos = encontrar_posicao_livre(estoque)
            if pos:
                coluna, linha = pos
                adicionar_engradado(estoque, coluna, linha, produto.engradado)
                alterado = True
    if alterado:
        salvar_estoque(estoque)
    return estoque

def menu():
    produtos = carregar_produtos()  
    estoque = carregar_estoque()  
    estoque = carregar_produtos_na_matriz(produtos, estoque)  
    salvar_estoque(estoque)  
    fila_pedidos = FilaPedidos()  #carrega os metodos 
    while True:
        print("\n=== Gerenciamento de Estoque ===")  # Menu principal
        print("1. Cadastrar produto e adicionar engradado em pilha")
        print("2. Visualizar produtos")
        print("3. Remover produto e engradado pelo código do engradado")
        print("4. Visualizar estoque (matriz de pilhas)")
        print("5. Adicionar pedido à fila")
        print("6. Processar próximo pedido")
        print("7. Visualizar fila de pedidos")
        print("8. Relatório de produtos próximos ao vencimento")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")  # Solicita a opção do usuário
        if opcao == "1":
            produto = cadastrar_produto()  # Cadastra novo produto
            pos = encontrar_posicao_livre(estoque)  # Encontra posição livre
            if pos:
                coluna, linha = pos
                if adicionar_engradado(estoque, coluna, linha, produto.engradado):
                    produtos.append(produto)
                    salvar_produtos(produtos)
                    salvar_estoque(estoque)
                    print(f"Produto cadastrado e engradado '{produto.engradado}' adicionado automaticamente na pilha ({linha}, {coluna}).")
            else:
                print("Estoque cheio! Não é possível cadastrar mais engradados.")
        elif opcao == "2":
            if not produtos:
                print("Nenhum produto cadastrado.")
            else:
                print("\n___ Produtos Cadastrados ___")
                for i, p in enumerate(produtos, 1):
                    print(f"{i}. {p}")
        elif opcao == "3":
            engradado_codigo = input("Digite o código do engradado a remover: ")
            encontrado = False
            for linha in estoque:
                for pilha in linha:
                    if engradado_codigo in pilha:
                        pilha.remove(engradado_codigo)
                        encontrado = True
            for i, produto in enumerate(produtos):
                if produto.engradado == engradado_codigo:
                    del produtos[i]
                    salvar_produtos(produtos)
                    salvar_estoque(estoque)
                    print(f"Produto e engradado '{engradado_codigo}' removidos com sucesso do estoque.")
                    break
            else:
                if not encontrado:
                    print(f"Engradado '{engradado_codigo}' não encontrado no estoque.")
                else:
                    print(f"Engradado '{engradado_codigo}' removido da pilha, mas produto não encontrado na lista.")
        elif opcao == "4":
            visualizar_estoque(estoque)
        elif opcao == "5":
            codigo_produto = input("Código do produto: ")
            quantidade = int(input("Quantidade: "))
            data_solicitacao = datetime.now().strftime("%d/%m/%Y %H:%M")
            nome_solicitante = input("Nome do solicitante: ")
            item = ItemPedido(codigo_produto, quantidade, data_solicitacao, nome_solicitante)
            fila_pedidos.adicionar_pedido(item)
            print("Pedido adicionado à fila.")
        elif opcao == "6":
            pedido = fila_pedidos.processar_pedido()
            if pedido:
                print(f"Processando pedido: {pedido}")
                # Aqui você pode implementar a lógica para retirar os engradados do estoque
        elif opcao == "7":
            fila_pedidos.visualizar_fila()
        elif opcao == "8":
            proximos = produtos_proximos_vencimento(produtos)
            if not proximos:
                print("Nenhum produto próximo ao vencimento (30 dias).")
            else:
                print("\nProdutos próximos ao vencimento:")
                for p in proximos:
                    print(p)
        elif opcao == "9":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()  # Inicia o menu principal