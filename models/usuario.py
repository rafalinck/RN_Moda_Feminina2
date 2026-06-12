# =====================================================================
# CLASSE MÃE (SUPERCLASSE): USUARIO
# =====================================================================
class Usuario:
    def __init__(self, cpf: str, nome: str, email: str, senha: str):
        self.cpf = str(cpf)
        self.nome = str(nome)
        self.email = str(email)
        self.senha = str(senha)

    def fazerLogin(self, email: str, senha: str) -> bool:
        return self.email == email and self.senha == senha


# =====================================================================
# CLASSE FILHA (SUBCLASSE): CLIENTE (Herda de Usuario)
# =====================================================================
class Cliente(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, senha: str, endereco: str, carrinho=None):
        super().__init__(cpf, nome, email, senha)
        self.endereco = str(endereco)
        
        from models.carrinho import Carrinho
        self.carrinho = carrinho if carrinho is not None else Carrinho()

    def adicionarAoCarrinho(self, produto, qtd: int = 1) -> bool:
        return self.carrinho.adicionarItem(produto, qtd)

    def finalizarCompra(self):
        if not self.carrinho.itens:
            return None
        
        from models.pedido import Pedido
        import random
        
        id_pedido = random.randint(1000, 9999)
        
        produtos_pedidos = []
        for item in self.carrinho.itens.values():
            produtos_pedidos.append({
                "produto": item["produto"],
                "quantidade": item["quantidade"]
            })
            
        pedido = Pedido(idPedido=id_pedido, cliente=self, produtosPedidos=produtos_pedidos)
        pedido.atualizarEstoque()
        self.carrinho.limpar()
        
        return pedido


# =====================================================================
# CLASSE FILHA (SUBCLASSE): ADMINISTRADOR (Herda de Usuario)
# =====================================================================
class Administrador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, senha: str, cargo: str = "Gerente"):
        super().__init__(cpf, nome, email, senha)
        self.cargo = str(cargo)
