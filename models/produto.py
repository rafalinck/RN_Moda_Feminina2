# =====================================================================
# CLASSE MÃE (SUPERCLASSE): PRODUTO
# =====================================================================
# Esta é a classe base para todos os produtos da nossa loja.
# Ela define os atributos e comportamentos comuns que qualquer produto tem 
# (como código, nome, preço e estoque).
class Produto:
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int):
        # Construtor: Inicializa as variáveis do objeto (atributos)
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.preco = float(preco)
        self.estoque = int(estoque)

    def exibirDetalhes(self) -> dict:
        """
        Retorna as informações gerais do produto.
        [CONCEITO DE POO - POLIMORFISMO]:
        Este método será sobrescrito (modificado) nas classes filhas (Roupa e Calçado) 
        para incluir detalhes exclusivos de cada tipo de produto.
        """
        return {
            "Código": self.codigo,
            "Nome": self.nome,
            "Preço": f"R$ {self.preco:.2f}",
            "Estoque": self.estoque,
            "Tipo": "Produto Geral"
        }

    def diminuirEstoque(self, quantidade: int) -> bool:
        """
        Diminui a quantidade em estoque quando uma venda é realizada.
        Retorna True se deu certo (tem estoque suficiente) ou False se faltar estoque.
        """
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            return True
        return False

    def aumentarEstoque(self, quantidade: int):
        """
        Adiciona mais itens ao estoque (usado pela administradora).
        """
        self.estoque += quantidade


# =====================================================================
# CLASSE FILHA (SUBCLASSE): ROUPA (Herda de Produto)
# =====================================================================
# [CONCEITO DE POO - HERANÇA]:
# A classe 'Roupa' herda tudo que 'Produto' tem (código, nome, preço, estoque)
# e adiciona suas características próprias (tamanho, cor, tecido).
class Roupa(Produto):
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int, tamanho: str, cor: str, tecido: str):
        # super().__init__ chama o construtor da classe mãe (Produto) para inicializar a parte comum
        super().__init__(codigo, nome, preco, estoque)
        # Atributos específicos da Roupa:
        self.tamanho = str(tamanho)
        self.cor = str(cor)
        self.tecido = str(tecido)

    def exibirDetalhes(self) -> dict:
        """
        [CONCEITO DE POO - POLIMORFISMO]:
        Aqui nós sobrescrevemos o método 'exibirDetalhes' da classe mãe.
        Chamamos o método original com 'super().exibirDetalhes()' e adicionamos 
        as chaves específicas de Roupa (Tamanho, Cor e Tecido).
        """
        detalhes = super().exibirDetalhes()
        detalhes.update({
            "Tamanho": self.tamanho,
            "Cor": self.cor,
            "Tecido": self.tecido,
            "Tipo": "Roupa"
        })
        return detalhes


# =====================================================================
# CLASSE FILHA (SUBCLASSE): CALÇADO (Herda de Produto)
# =====================================================================
# [CONCEITO DE POO - HERANÇA]:
# Assim como Roupa, 'Calçado' herda de 'Produto', mas adiciona atributos 
# pertinentes a sapatos (como tamanho numérico, material e marca).
class Calçado(Produto):
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int, tamanho: int, material: str, marca: str):
        # super().__init__ chama o construtor da classe mãe (Produto)
        super().__init__(codigo, nome, preco, estoque)
        # Atributos específicos do Calçado:
        self.tamanho = int(tamanho)
        self.material = str(material)
        self.marca = str(marca)

    def exibirDetalhes(self) -> dict:
        """
        [CONCEITO DE POO - POLIMORFISMO]:
        Sobrescreve o método 'exibirDetalhes' para incluir informações de Calçado.
        """
        detalhes = super().exibirDetalhes()
        detalhes.update({
            "Tamanho": self.tamanho,
            "Material": self.material,
            "Marca": self.marca,
            "Tipo": "Calçado"
        })
        return detalhes
