from models.produto import Produto

# =====================================================================
# CLASSE: PEDIDO (Associação)
# =====================================================================
# [CONCEITO DE POO - ASSOCIAÇÃO]:
# A classe 'Pedido' realiza a associação entre:
# 1. Um objeto 'Cliente' (quem fez a compra).
# 2. Vários objetos 'Produto' (os itens que foram comprados).
class Pedido:
    def __init__(self, idPedido: int, cliente, produtosPedidos: list, status: str = "Pendente"):
        self.idPedido = int(idPedido)
        # Associação direta com a classe Cliente
        self.cliente = cliente  
        # Associação: Lista de dicionários [{"produto": objeto_Produto, "quantidade": int}]
        self.produtosPedidos = produtosPedidos  
        # Situação do pedido (ex: Pendente, Preparando, Enviado, Entregue)
        self.status = str(status)

    def alterarStatus(self, novoStatus: str):
        """
        Permite que a administradora atualize o status logístico do pedido.
        """
        self.status = str(novoStatus)

    def atualizarEstoque(self, quantidade: int = None):
        """
        Deduz as quantidades compradas do estoque disponível de cada produto.
        """
        for item in self.produtosPedidos:
            prod = item["produto"]
            qtd_comprada = item["quantidade"]
            
            # Subtrai a quantidade comprada do estoque físico do produto
            qtd_para_reduzir = quantidade if quantidade is not None else qtd_comprada
            prod.diminuirEstoque(qtd_para_reduzir)

    def gerarNotaFiscal(self) -> str:
        """
        Gera e formata o recibo/Nota Fiscal da compra.
        [CONCEITO DE POO - POLIMORFISMO E ASSOCIAÇÃO]:
        Este método acessa informações de cada produto utilizando o polimorfismo do método 
        'exibirDetalhes()', garantindo que Roupas exibam tamanho/cor e Calçados exibam tamanho numérico.
        """
        linhas = []
        linhas.append("==================================================")
        linhas.append("             R&N MODA FEMININA - NOTA FISCAL       ")
        linhas.append("==================================================")
        linhas.append(f"Pedido ID: {self.idPedido}")
        linhas.append(f"Status: {self.status.upper()}")
        linhas.append("--------------------------------------------------")
        # Acessa os atributos do objeto Cliente associado
        linhas.append(f"Cliente: {self.cliente.nome}")
        linhas.append(f"CPF: {self.cliente.cpf}")
        linhas.append(f"E-mail: {self.cliente.email}")
        linhas.append(f"Endereço de Entrega: {self.cliente.endereco}")
        linhas.append("--------------------------------------------------")
        linhas.append(f"{'Item':<22} | {'Qtd':<3} | {'Unit.':<8} | {'Total':<8}")
        linhas.append("--------------------------------------------------")
        
        total_pedido = 0.0
        for item in self.produtosPedidos:
            prod = item["produto"]
            qtd = item["quantidade"]
            subtotal = prod.preco * qtd
            total_pedido += subtotal
            
            # [POLIMORFISMO]: Dependendo se 'prod' é Roupa ou Calçado, 
            # exibirDetalhes() retornará chaves diferentes. Tratamos isso dinamicamente!
            detalhes = prod.exibirDetalhes()
            nome_exibicao = prod.nome
            if detalhes["Tipo"] == "Roupa":
                nome_exibicao += f" ({detalhes['Tamanho']}/{detalhes['Cor']})"
            elif detalhes["Tipo"] == "Calçado":
                nome_exibicao += f" (Tam: {detalhes['Tamanho']})"
                
            # Limita o tamanho do texto para caber no leiaute do recibo
            if len(nome_exibicao) > 22:
                nome_exibicao = nome_exibicao[:19] + "..."
                
            linhas.append(f"{nome_exibicao:<22} | {qtd:<3} | R${prod.preco:<6.2f} | R${subtotal:<6.2f}")
            
        linhas.append("--------------------------------------------------")
        linhas.append(f"VALOR TOTAL DO PEDIDO: R$ {total_pedido:.2f}")
        linhas.append("==================================================")
        linhas.append("         Obrigado por comprar na R&N Moda!        ")
        linhas.append("==================================================")
        
        nota = "\n".join(linhas)
        print(nota)  # Imprime no terminal para verificação
        return nota
