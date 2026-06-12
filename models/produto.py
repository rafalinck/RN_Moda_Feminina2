# =====================================================================
# CLASSE MÃE (SUPERCLASSE): PRODUTO
# =====================================================================
class Produto:
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.preco = float(preco)
        self.estoque = int(estoque)

    def exibirDetalhes(self) -> dict:
        return {
            "Código": self.codigo,
            "Nome": self.nome,
            "Preço": f"R$ {self.preco:.2f}",
            "Estoque": self.estoque,
            "Tipo": "Produto Geral"
        }

    def diminuirEstoque(self, quantidade: int) -> bool:
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            return True
        return False

    def aumentarEstoque(self, quantidade: int):
        self.estoque += quantidade


# =====================================================================
# CLASSE FILHA (SUBCLASSE): ROUPA (Herda de Produto)
# =====================================================================
class Roupa(Produto):
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int, tamanho: str, cor: str, tecido: str):
        super().__init__(codigo, nome, preco, estoque)
        self.tamanho = str(tamanho)
        self.cor = str(cor)
        self.tecido = str(tecido)

    def exibirDetalhes(self) -> dict:
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
class Calçado(Produto):
    def __init__(self, codigo: int, nome: str, preco: float, estoque: int, tamanho: int, material: str, marca: str):
        super().__init__(codigo, nome, preco, estoque)
        self.tamanho = int(tamanho)
        self.material = str(material)
        self.marca = str(marca)

    def exibirDetalhes(self) -> dict:
        detalhes = super().exibirDetalhes()
        detalhes.update({
            "Tamanho": self.tamanho,
            "Material": self.material,
            "Marca": self.marca,
            "Tipo": "Calçado"
        })
        return detalhes
