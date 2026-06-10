import json
import os
from models.produto import Roupa, Calçado
from models.usuario import Cliente, Administrador
from models.pedido import Pedido
from models.carrinho import Carrinho

DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")

class Database:
    def __init__(self):
        self.produtos = {}  # {codigo_int: Produto}
        self.clientes = {}  # {email: Cliente}
        self.pedidos = {}   # {idPedido: Pedido}
        self.load_data()

    def load_data(self):
        if not os.path.exists(DB_FILE):
            self.create_default_data()
            return

        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Carregar Produtos
            for item in data.get("produtos", []):
                tipo = item.get("tipo")
                if tipo == "Roupa":
                    prod = Roupa(
                        codigo=item["codigo"],
                        nome=item["nome"],
                        preco=item["preco"],
                        estoque=item["estoque"],
                        tamanho=item["tamanho"],
                        cor=item["cor"],
                        tecido=item["tecido"]
                    )
                elif tipo == "Calçado":
                    prod = Calçado(
                        codigo=item["codigo"],
                        nome=item["nome"],
                        preco=item["preco"],
                        estoque=item["estoque"],
                        tamanho=item["tamanho"],
                        material=item["material"],
                        marca=item["marca"]
                    )
                else:
                    continue
                self.produtos[prod.codigo] = prod

            # Carregar Clientes / Usuários
            for item in data.get("clientes", []):
                tipo_u = item.get("tipo", "Cliente")
                if tipo_u == "Admin":
                    usuario = Administrador(
                        cpf=item["cpf"],
                        nome=item["nome"],
                        email=item["email"],
                        senha=item["senha"],
                        cargo=item.get("cargo", "Gerente")
                    )
                else:
                    usuario = Cliente(
                        cpf=item["cpf"],
                        nome=item["nome"],
                        email=item["email"],
                        senha=item["senha"],
                        endereco=item.get("endereco", "")
                    )
                self.clientes[usuario.email] = usuario

            # Carregar Pedidos
            for item in data.get("pedidos", []):
                cliente_email = item["cliente_email"]
                cliente = self.clientes.get(cliente_email)
                if not cliente:
                    continue
                
                produtos_pedidos = []
                for p_item in item["produtos"]:
                    prod_codigo = p_item["codigo"]
                    prod = self.produtos.get(prod_codigo)
                    if prod:
                        produtos_pedidos.append({
                            "produto": prod,
                            "quantidade": p_item["quantidade"]
                        })
                
                pedido = Pedido(
                    idPedido=item["idPedido"],
                    cliente=cliente,
                    produtosPedidos=produtos_pedidos,
                    status=item["status"]
                )
                self.pedidos[pedido.idPedido] = pedido

        except Exception as e:
            print(f"Erro ao carregar banco de dados: {e}. Criando dados padrão.")
            self.create_default_data()

    def save_data(self):
        try:
            data = {
                "produtos": [],
                "clientes": [],
                "pedidos": []
            }

            # Serializar Produtos
            for prod in self.produtos.values():
                detalhes = prod.exibirDetalhes()
                prod_dict = {
                    "codigo": prod.codigo,
                    "nome": prod.nome,
                    "preco": prod.preco,
                    "estoque": prod.estoque,
                    "tipo": detalhes["Tipo"]
                }
                if detalhes["Tipo"] == "Roupa":
                    prod_dict.update({
                        "tamanho": prod.tamanho,
                        "cor": prod.cor,
                        "tecido": prod.tecido
                    })
                elif detalhes["Tipo"] == "Calçado":
                    prod_dict.update({
                        "tamanho": prod.tamanho,
                        "material": prod.material,
                        "marca": prod.marca
                    })
                data["produtos"].append(prod_dict)

            # Serializar Clientes / Usuários
            for usuario in self.clientes.values():
                user_dict = {
                    "cpf": usuario.cpf,
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "senha": usuario.senha
                }
                if isinstance(usuario, Cliente):
                    user_dict.update({
                        "tipo": "Cliente",
                        "endereco": usuario.endereco
                    })
                elif isinstance(usuario, Administrador):
                    user_dict.update({
                        "tipo": "Admin",
                        "cargo": usuario.cargo
                    })
                data["clientes"].append(user_dict)

            # Serializar Pedidos
            for pedido in self.pedidos.values():
                produtos_list = []
                for item in pedido.produtosPedidos:
                    produtos_list.append({
                        "codigo": item["produto"].codigo,
                        "quantidade": item["quantidade"]
                    })
                data["pedidos"].append({
                    "idPedido": pedido.idPedido,
                    "cliente_email": pedido.cliente.email,
                    "produtos": produtos_list,
                    "status": pedido.status
                })

            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar banco de dados: {e}")

    def create_default_data(self):
        # Produtos Padrão
        p1 = Roupa(101, "Vestido Midi Floral", 129.90, 10, "M", "Azul", "Viscose")
        p2 = Roupa(102, "Blusa Cropped Linho", 79.90, 15, "P", "Cru", "Linho")
        p3 = Roupa(103, "Calça Alfaiataria", 159.90, 8, "G", "Preta", "Poliéster")
        
        p4 = Calçado(201, "Sandália Salto Bloco", 149.90, 5, 37, "Couro Sintético", "Vizzano")
        p5 = Calçado(202, "Tênis Casual Branco", 119.90, 12, 36, "Lona", "Via Marte")
        p6 = Calçado(203, "Scarpin Clássico", 199.90, 4, 38, "Camurça", "Arezzo")

        for p in [p1, p2, p3, p4, p5, p6]:
            self.produtos[p.codigo] = p

        # Usuários/Clientes/Admins Padrão
        c1 = Cliente("123.456.789-00", "Rafaela Linck", "rafaela@email.com", "123", "Rua das Flores, 123 - Centro")
        c2 = Cliente("987.654.321-11", "Natalia Maciel", "natalia@email.com", "123", "Av. Brasil, 456 - Bairro Lindo")
        adm = Administrador("000.000.000-99", "Natália Maciel (Admin)", "admin@email.com", "123", "Gerente Geral")

        for u in [c1, c2, adm]:
            self.clientes[u.email] = u

        self.save_data()
