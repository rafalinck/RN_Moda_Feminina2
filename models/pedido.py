from models.produto import Produto

# =====================================================================
# CLASSE: PEDIDO
# =====================================================================
class Pedido:
    def __init__(self, idPedido: int, cliente, produtosPedidos: list, status: str = "Pendente"):
        self.idPedido = int(idPedido)
        self.cliente = cliente  
        self.produtosPedidos = produtosPedidos  
        self.status = str(status)

    def alterarStatus(self, novoStatus: str):
        self.status = str(novoStatus)

    def atualizarEstoque(self, quantidade: int = None):
        for item in self.produtosPedidos:
            prod = item["produto"]
            qtd_comprada = item["quantidade"]
            qtd_para_reduzir = quantidade if quantidade is not None else qtd_comprada
            prod.diminuirEstoque(qtd_para_reduzir)

    def gerarNotaFiscal(self) -> str:
        linhas = []
        linhas.append("==================================================")
        linhas.append("             R&N MODA FEMININA - NOTA FISCAL       ")
        linhas.append("==================================================")
        linhas.append(f"Pedido ID: {self.idPedido}")
        linhas.append(f"Status: {self.status.upper()}")
        linhas.append("--------------------------------------------------")
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
            
            detalhes = prod.exibirDetalhes()
            nome_exibicao = prod.nome
            if detalhes["Tipo"] == "Roupa":
                nome_exibicao += f" ({detalhes['Tamanho']}/{detalhes['Cor']})"
            elif detalhes["Tipo"] == "Calçado":
                nome_exibicao += f" (Tam: {detalhes['Tamanho']})"
                
            if len(nome_exibicao) > 22:
                nome_exibicao = nome_exibicao[:19] + "..."
                
            linhas.append(f"{nome_exibicao:<22} | {qtd:<3} | R${prod.preco:<6.2f} | R${subtotal:<6.2f}")
            
        linhas.append("--------------------------------------------------")
        linhas.append(f"VALOR TOTAL DO PEDIDO: R$ {total_pedido:.2f}")
        linhas.append("==================================================")
        linhas.append("         Obrigado por comprar na R&N Moda!        ")
        linhas.append("==================================================")
        
        nota = "\n".join(linhas)
        print(nota)
        return nota
