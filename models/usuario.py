# =====================================================================
# CLASSE MÃE (SUPERCLASSE): USUARIO
# =====================================================================
# Representa qualquer pessoa com acesso ao sistema (Cliente ou Administrador).
class Usuario:
    def __init__(self, cpf: str, nome: str, email: str, senha: str):
        # Atributos básicos de cadastro comuns a todos os usuários
        self.cpf = str(cpf)
        self.nome = str(nome)
        self.email = str(email)
        self.senha = str(senha)

    def fazerLogin(self, email: str, senha: str) -> bool:
        """
        Método de autenticação simples: compara o e-mail e a senha informados
        com os dados armazenados no próprio objeto.
        """
        return self.email == email and self.senha == senha


# =====================================================================
# CLASSE FILHA (SUBCLASSE): CLIENTE (Herda de Usuario)
# =====================================================================
# [CONCEITO DE POO - HERANÇA]:
# A classe 'Cliente' herda todos os atributos e métodos de 'Usuario'
# e acrescenta um endereço e um Carrinho de compras.
class Cliente(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, senha: str, endereco: str, carrinho=None):
        # Inicializa a classe base (Usuario)
        super().__init__(cpf, nome, email, senha)
        self.endereco = str(endereco)
        
        # [CONCEITO DE POO - ASSOCIAÇÃO]:
        # Um Cliente "tem um" Carrinho de compras. Isso é uma relação de associação 
        # entre duas classes distintas (Cliente e Carrinho).
        from models.carrinho import Carrinho
        self.carrinho = carrinho if carrinho is not None else Carrinho()

    def adicionarAoCarrinho(self, produto, qtd: int = 1) -> bool:
        """
        Associação em ação: delega a tarefa de adicionar o item diretamente 
        para o objeto 'Carrinho' que pertence a este cliente.
        """
        return self.carrinho.adicionarItem(produto, qtd)

    def finalizarCompra(self):
        """
        Cria um Pedido a partir dos itens do carrinho e retorna o objeto gerado.
        Limpa o carrinho após finalizar e desconta do estoque físico.
        """
        if not self.carrinho.itens:
            return None
        
        from models.pedido import Pedido
        import random
        
        # Gera um número aleatório como ID do Pedido
        id_pedido = random.randint(1000, 9999)
        
        # Transforma o dicionário do Carrinho em uma lista simples de itens para o Pedido
        produtos_pedidos = []
        for item in self.carrinho.itens.values():
            produtos_pedidos.append({
                "produto": item["produto"],
                "quantidade": item["quantidade"]
            })
            
        # Criação da Instância de Pedido (associação entre Pedido, Cliente e Produtos)
        pedido = Pedido(idPedido=id_pedido, cliente=self, produtosPedidos=produtos_pedidos)
        
        # Atualiza o estoque físico de cada produto envolvido
        pedido.atualizarEstoque()
        
        # Esvazia o carrinho de compras do cliente
        self.carrinho.limpar()
        
        return pedido


# =====================================================================
# CLASSE FILHA (SUBCLASSE): ADMINISTRADOR (Herda de Usuario)
# =====================================================================
# [CONCEITO DE POO - HERANÇA]:
# Representa a administradora da loja, que herda os dados de 'Usuario'
# e ganha um cargo/função para identificação interna.
class Administrador(Usuario):
    def __init__(self, cpf: str, nome: str, email: str, senha: str, cargo: str = "Gerente"):
        # Inicializa a classe base (Usuario)
        super().__init__(cpf, nome, email, senha)
        self.cargo = str(cargo)

