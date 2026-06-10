from models.produto import Produto

# =====================================================================
# CLASSE: CARRINHO (Associação)
# =====================================================================
# O Carrinho atua como um agregador de itens temporários antes da compra.
# [CONCEITO DE POO - ASSOCIAÇÃO]:
# A classe Carrinho mantém referências a objetos do tipo 'Produto' dentro de 
# um dicionário. Ela calcula subtotais e totais dinamicamente interagindo com os produtos.
class Carrinho:
    def __init__(self):
        # self.itens armazena: {codigo_do_produto: {"produto": objeto_Produto, "quantidade": int}}
        self.itens = {}  
        self.valorTotal = 0.0

    def adicionarItem(self, produto: Produto, qtd: int) -> bool:
        """
        Adiciona um produto ao carrinho. 
        Garante que a quantidade solicitada não exceda o estoque disponível.
        Retorna True se adicionou com sucesso, False se o estoque for insuficiente.
        """
        if qtd <= 0:
            return False
            
        # Verifica a quantidade que o usuário já tem no carrinho
        qtd_atual_carrinho = self.itens.get(produto.codigo, {}).get("quantidade", 0)
        total_desejado = qtd_atual_carrinho + qtd
        
        # Verifica se o estoque da loja suporta o total desejado
        if total_desejado > produto.estoque:
            return False
            
        # Se o produto já estava no carrinho, apenas soma a nova quantidade
        if produto.codigo in self.itens:
            self.itens[produto.codigo]["quantidade"] += qtd
        else:
            # Caso contrário, insere uma nova entrada associando o objeto Produto
            self.itens[produto.codigo] = {
                "produto": produto,
                "quantidade": qtd
            }
        
        # Recalcula o valor total do carrinho
        self.calcularTotal()
        return True

    def removerItem(self, idProduto: int) -> bool:
        """
        Remove um produto completamente do carrinho com base no seu código de identificação.
        """
        idProduto = int(idProduto)
        if idProduto in self.itens:
            del self.itens[idProduto]
            self.calcularTotal()
            return True
        return False

    def calcularTotal(self) -> float:
        """
        Calcula a soma total do carrinho multiplicando o preço de cada produto
        pela quantidade adicionada.
        """
        total = 0.0
        for item in self.itens.values():
            # item["produto"] é uma instância de Produto (ou de suas subclasses Roupa/Calçado)
            total += item["produto"].preco * item["quantidade"]
        self.valorTotal = total
        return self.valorTotal

    def limpar(self):
        """
        Limpa todos os itens do carrinho (usado após a finalização da compra).
        """
        self.itens.clear()
        self.valorTotal = 0.0
