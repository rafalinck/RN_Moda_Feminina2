# Script de Teste Puro do Modelo POO (Console)
from models.produto import Roupa, Calçado
from models.usuario import Cliente
from models.carrinho import Carrinho
from models.pedido import Pedido

def testar_sistema_poo():
    print("=== INICIANDO TESTE DE POO (R&N Moda Feminina) ===")
    
    # 1. Demonstração de Herança e Instanciação de Objetos
    print("\n--- 1. Instanciação e Herança ---")
    vestido = Roupa(101, "Vestido Midi Floral", 129.90, 10, "M", "Azul", "Viscose")
    sapato = Calçado(201, "Sandália Salto Bloco", 149.90, 5, 37, "Couro Sintético", "Vizzano")
    
    print(f"Objeto 'vestido' é instância de Roupa? {isinstance(vestido, Roupa)}")
    print(f"Objeto 'vestido' herda de Produto? {isinstance(vestido, Roupa.__base__)}")
    print(f"Objeto 'sapato' é instância de Calçado? {isinstance(sapato, Calçado)}")
    print(f"Objeto 'sapato' herda de Produto? {isinstance(sapato, Calçado.__base__)}")
    
    # 2. Demonstração de Polimorfismo
    print("\n--- 2. Demonstração de Polimorfismo (exibirDetalhes) ---")
    print("Detalhes da Roupa (sobrescrito):")
    for chave, valor in vestido.exibirDetalhes().items():
        print(f"  {chave}: {valor}")
        
    print("\nDetalhes do Calçado (sobrescrito):")
    for chave, valor in sapato.exibirDetalhes().items():
        print(f"  {chave}: {valor}")
        
    # 3. Associação: Cliente e Carrinho
    print("\n--- 3. Associação: Cliente -> Carrinho -> Produtos ---")
    cliente = Cliente("123.456.789-00", "Rafaela Linck", "rafaela@email.com", "123", "Rua das Flores, 123 - Centro")
    print(f"Cliente instanciado: {cliente.nome}")
    print(f"Carrinho associado automaticamente ao cliente? {cliente.carrinho is not None}")
    
    # Adicionando itens ao carrinho
    print("\nAdicionando itens ao carrinho do Cliente...")
    sucesso_vestido = cliente.adicionarAoCarrinho(vestido, 2)
    sucesso_sapato = cliente.adicionarAoCarrinho(sapato, 1)
    
    print(f"Adicionou 2 Vestidos (Estoque original: 10)? {sucesso_vestido}. Estoque atual: {vestido.estoque}")
    print(f"Adicionou 1 Sandália (Estoque original: 5)? {sucesso_sapato}. Estoque atual: {sapato.estoque}")
    
    print("\nVerificando itens no carrinho:")
    for codigo, item in cliente.carrinho.itens.items():
        prod = item["produto"]
        qtd = item["quantidade"]
        print(f"  - {prod.nome} | Qtd: {qtd} | Preço Unit.: R$ {prod.preco:.2f} | Subtotal: R$ {prod.preco * qtd:.2f}")
        
    print(f"Valor total do carrinho calculado: R$ {cliente.carrinho.valorTotal:.2f}")
    
    # 4. Finalizando compra, gerando Pedido e Nota Fiscal (Polimorfismo e Associação)
    print("\n--- 4. Finalização de Compra (Carrinho -> Pedido e Baixa de Estoque) ---")
    pedido = cliente.finalizarCompra()
    print(f"Pedido gerado com ID: {pedido.idPedido}")
    print(f"Status do pedido: {pedido.status}")
    print(f"Estoque do Vestido após finalizar compra (deve ser 8): {vestido.estoque}")
    print(f"Estoque da Sandália após finalizar compra (deve ser 4): {sapato.estoque}")
    print(f"Itens no carrinho do cliente após finalizar (deve estar limpo): {len(cliente.carrinho.itens)}")
    
    # 5. Geração de Nota Fiscal
    print("\n--- 5. Geração e Impressão da Nota Fiscal ---")
    pedido.gerarNotaFiscal()
    
    print("\n=== FIM DO TESTE DE POO COM SUCESSO ===")

if __name__ == "__main__":
    testar_sistema_poo()
