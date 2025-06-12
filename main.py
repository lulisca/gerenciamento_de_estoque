from infoproduto import Produto
from json_utils import carregar_produtos, salvar_produtos
from cadastro import cadastrar_produto

produtos = carregar_produtos()

while True:
    novo = input("Deseja cadastrar um novo produto? (s/n): ")  # Pergunta ao usuário se deseja cadastrar
    if novo.lower() != 's':  # Se não for 's', sai do loop
        break
    produto = cadastrar_produto()  # Chama o cadastro
    produtos.append(produto)  # Adiciona à lista
    salvar_produtos(produtos)  # Salva no JSON

print("\nProdutos cadastrados:")
for p in produtos:
    print(f"- {p}")