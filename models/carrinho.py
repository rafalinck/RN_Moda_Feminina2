from models.produto import Produto

# =====================================================================
# CLASSE: CARRINHO
# =====================================================================
class Carrinho:
    def __init__(self):
        self.itens = {}  
        self.valorTotal = 0.0

    def adicionarItem(self, produto: Produto, qtd: int) -> bool:
        if qtd <= 0:
            return False
            
        qtd_atual_carrinho = self.itens.get(produto.codigo, {}).get("quantidade", 0)
        total_desejado = qtd_atual_carrinho + qtd
        
        if total_desejado > produto.estoque:
            return False
            
        if produto.codigo in self.itens:
            self.itens[produto.codigo]["quantidade"] += qtd
        else:
            self.itens[produto.codigo] = {
                "produto": produto,
                "quantidade": qtd
            }
        
        self.calcularTotal()
        return True

    def removerItem(self, idProduto: int) -> bool:
        idProduto = int(idProduto)
        if idProduto in self.itens:
            del self.itens[idProduto]
            self.calcularTotal()
            return True
        return False

    def calcularTotal(self) -> float:
        total = 0.0
        for item in self.itens.values():
            total += item["produto"].preco * item["quantidade"]
        self.valorTotal = total
        return self.valorTotal

    def limpar(self):
        self.itens.clear()
        self.valorTotal = 0.0
