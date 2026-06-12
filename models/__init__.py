# =====================================================================
# EXPOSIÇÃO PÚBLICA DE CLASSES DO PACOTE MODELS
# =====================================================================
from .produto import Produto, Roupa, Calçado
from .usuario import Usuario, Cliente, Administrador
from .carrinho import Carrinho
from .pedido import Pedido

__all__ = [
    "Produto",
    "Roupa",
    "Calçado",
    "Usuario",
    "Cliente",
    "Administrador",
    "Carrinho",
    "Pedido"
]
