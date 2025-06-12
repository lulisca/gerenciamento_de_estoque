class Produto:
    def __init__(self, codigo, nome, peso, validade, preco_compra, preco_venda, engradado, lote, fornecedor, categoria, fabricante, data_fabricacao=None, tamanho_engradado=None, data_cadastro=None):
        self.codigo = codigo  # Código do produto
        self.nome = nome  # Nome do produto
        self.peso = peso  # Peso do produto
        self.validade = validade  # Data de validade
        self.preco_compra = preco_compra  # Preço de compra
        self.preco_venda = preco_venda  # Preço de venda
        self.engradado = engradado  # Identificação do engradado
        self.lote = lote  # Número do lote
        self.fornecedor = fornecedor  # Fornecedor
        self.categoria = categoria  # Categoria
        self.fabricante = fabricante  # Fabricante
        self.data_fabricacao = data_fabricacao  # Data de fabricação
        self.tamanho_engradado = tamanho_engradado  # Tamanho do engradado
        self.data_cadastro = data_cadastro  # Data e hora do cadastro

    def __str__(self):
        # Retorna uma string representando o produto com todos os campos principais
        return f"{self.nome} (Código: {self.codigo}, Engradado: {self.engradado}, Lote: {self.lote}, Fornecedor: {self.fornecedor}, Categoria: {self.categoria}, Fabricante: {self.fabricante}, Fabricação: {self.data_fabricacao}, Tam. Engradado: {self.tamanho_engradado}, Cadastro: {self.data_cadastro})"
