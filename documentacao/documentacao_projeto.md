# Documentação do Projeto: R&N Moda Feminina

**Disciplina**: Programação Orientada a Objetos (POO)  
**Trabalho de G2 – Implementação**  
**Integrantes**: Rafaela Linck e Natalia Maciel  

---

## 1. Introdução

Este projeto consiste na implementação de um sistema de e-commerce e retaguarda para a loja virtual **R&N Moda Feminina**. O sistema foi desenvolvido em Python utilizando o paradigma de Orientação a Objetos, com uma interface gráfica rica em **Tkinter** que simula os fluxos de login, navegação de produtos, gerenciamento de carrinho, finalização de compra com geração de nota fiscal e um painel de controle administrativo.

O projeto atende integralmente a todos os requisitos solicitados na disciplina:
- Mínimo de 5 classes (foram desenvolvidas 7 classes centrais de modelo: `Produto`, `Roupa`, `Calçado`, `Usuario`, `Cliente`, `Carrinho` e `Pedido`).
- Utilização de **Associação**, **Herança** e **Polimorfismo**.
- Interação por parte do usuário (dados digitados na interface).
- Criação de diagramas de classe e objetos (disponibilizados em formato Mermaid no diretório).

---

## 2. Estrutura e Modelagem do Sistema (POO)

Abaixo está o detalhamento de como os conceitos de Programação Orientada a Objetos foram implementados nas classes de modelo (disponíveis na pasta [`models/`](file:///C:/Users/rafaela.gotardo/.gemini/antigravity-ide/scratch/rn_moda_feminina/models/)):

### A. Herança (Inheritance)
A herança é utilizada para reaproveitar propriedades e comportamentos comuns entre entidades parecidas.

1. **Produtos**:
   - `Produto` ([produto.py](file:///C:/Users/rafaela.gotardo/.gemini/antigravity-ide/scratch/rn_moda_feminina/models/produto.py)) é a superclasse que define atributos básicos como `codigo`, `nome`, `preco` e `estoque`.
   - `Roupa` e `Calçado` herdam de `Produto` utilizando `super().__init__(...)` e acrescentam seus próprios atributos específicos:
     - `Roupa` adiciona: `tamanho: str`, `cor: str`, `tecido: str`.
     - `Calçado` adiciona: `tamanho: int`, `material: str`, `marca: str`.

2. **Usuários**:
   - `Usuario` ([usuario.py](file:///C:/Users/rafaela.gotardo/.gemini/antigravity-ide/scratch/rn_moda_feminina/models/usuario.py)) é a superclasse de autenticação contendo `cpf`, `nome`, `email`, `senha` e o método `fazerLogin()`.
   - `Cliente` herda de `Usuario` e expande o modelo adicionando um `endereco` de entrega e associando a ele um objeto de `Carrinho`.
   - `Administrador` herda de `Usuario` e expande o modelo adicionando um `cargo` administrativo. Apenas usuários do tipo administrador possuem acesso ao painel de gerenciamento no sistema.

### B. Polimorfismo (Polymorphism)
O polimorfismo permite que métodos com a mesma assinatura tenham comportamentos diferentes dependendo da classe que os executa.

- O método `exibirDetalhes()` está definido na classe base `Produto`.
- As subclasses `Roupa` e `Calçado` sobrescrevem (override) esse método:
  - `Roupa.exibirDetalhes()` chama o método da classe pai com `super().exibirDetalhes()` e injeta o tamanho, cor e tecido no dicionário de retorno.
  - `Calçado.exibirDetalhes()` faz o mesmo, inserindo tamanho numérico, material e marca.
- Na **Vitrine de Produtos** (`gui/app.py`), o sistema itera por uma lista genérica de objetos do tipo `Produto`. Ao chamar `prod.exibirDetalhes()`, o Python executa dinamicamente o método correto de acordo com o tipo do objeto instanciado (Roupa ou Calçado), exibindo as especificações corretas no card de cada produto sem que a vitrine precise conhecer explicitamente os detalhes internos de cada subclasse.

### C. Associação e Agregação (Association & Aggregation)
As associações definem os relacionamentos e a dependência de ciclo de vida entre as classes.

1. **Cliente e Carrinho**:
   - A classe `Cliente` possui um atributo `carrinho` que armazena uma instância da classe `Carrinho` (`Cliente` "tem um" `Carrinho`).
2. **Carrinho e Produto**:
   - O `Carrinho` armazena uma agregação de produtos dentro de um dicionário (`self.itens`), vinculando instâncias de `Produto` (ou suas subclasses) às suas respectivas quantidades.
3. **Pedido, Cliente e Produtos**:
   - A classe `Pedido` possui uma associação direta com o `Cliente` (para saber quem comprou e qual o endereço de entrega) e uma lista de referências aos `Produtos` adquiridos, unindo as diferentes entidades para consolidação da compra.

---

## 3. Descrição das Classes e Métodos

### `Produto` (Classe Mãe)
- **Atributos**: `codigo` (int), `nome` (str), `preco` (float), `estoque` (int).
- **Métodos**:
  - `exibirDetalhes() -> dict`: Retorna os dados cadastrais básicos.
  - `diminuirEstoque(quantidade: int) -> bool`: Deduz o estoque do produto se houver quantidade disponível.
  - `aumentarEstoque(quantidade: int) -> void`: Adiciona itens ao estoque.

### `Roupa` (Subclasse)
- **Atributos**: Herda `Produto`, mais `tamanho` (str), `cor` (str), `tecido` (str).
- **Métodos**:
  - `exibirDetalhes() -> dict` (Sobrescrito/Polimórfico).

### `Calçado` (Subclasse)
- **Atributos**: Herda `Produto`, mais `tamanho` (int), `material` (str), `marca` (str).
- **Métodos**:
  - `exibirDetalhes() -> dict` (Sobrescrito/Polimórfico).

### `Usuario` (Classe Mãe)
- **Atributos**: `cpf` (str), `nome` (str), `email` (str), `senha` (str).
- **Métodos**:
  - `fazerLogin(email: str, senha: str) -> bool`: Valida as credenciais.

### `Cliente` (Subclasse)
- **Atributos**: Herda `Usuario`, mais `endereco` (str), `carrinho` (Carrinho).
- **Métodos**:
- `adicionarAoCarrinho(produto: Produto, qtd: int) -> bool`: Adiciona item ao carrinho.
- `finalizarCompra() -> Pedido`: Transforma os itens do carrinho em um pedido de compra, atualiza o estoque e limpa o carrinho.

### `Administrador` (Subclasse)
- **Atributos**: Herda `Usuario`, mais `cargo` (str).
- **Métodos**: Herda todos os métodos de `Usuario` (como `fazerLogin`). Permite acesso administrativo para cadastrar novos produtos e gerenciar o status de pedidos de clientes.

### `Carrinho`
- **Atributos**: `itens` (dict), `valorTotal` (float).
- **Métodos**:
  - `adicionarItem(produto: Produto, qtd: int) -> bool`: Valida estoque e insere o produto.
  - `removerItem(idProduto: int) -> bool`: Remove o produto do carrinho.
  - `calcularTotal() -> float`: Soma o valor de todos os itens baseados no preço.
  - `limpar() -> void`: Esvazia o carrinho.

### `Pedido`
- **Atributos**: `idPedido` (int), `cliente` (Cliente), `produtosPedidos` (list), `status` (str).
- **Métodos**:
  - `alterarStatus(novoStatus: str)`: Altera a situação da entrega (ex: Pendente -> Enviado -> Entregue).
  - `atualizarEstoque(quantidade: int)`: Dá baixa no estoque de cada produto associado ao pedido.
  - `gerarNotaFiscal() -> str`: Formata uma nota fiscal eletrônica em string detalhada e imprime no console do Python.

---

## 4. Como Executar a Aplicação

### Pré-requisitos
A aplicação foi projetada para ter **zero dependências externas**, necessitando apenas de uma instalação padrão do Python 3 (que já inclui a biblioteca gráfica `tkinter`).

### Execução via Terminal
Abra o prompt de comando ou terminal na pasta raiz do projeto (`rn_moda_feminina/`) e execute:

```bash
python main.py
```

### Script de Teste do Modelo POO (Sem Interface Gráfica)
Se você ou a professora desejarem testar apenas as classes Python de POO puras no console para comprovar a lógica de herança e polimorfismo, execute:

```bash
python test_oop.py
```

---

## 5. Roteiro de Demonstração (Uso Prático)

Para a gravação do vídeo ou apresentação em aula, siga este roteiro:

1. **Apresentação dos Diagramas**:
   - Mostre os arquivos [`diagrama_classes.mermaid`](file:///C:/Users/rafaela.gotardo/.gemini/antigravity-ide/scratch/rn_moda_feminina/documentacao/diagrama_classes.mermaid) e [`diagrama_objetos.mermaid`](file:///C:/Users/rafaela.gotardo/.gemini/antigravity-ide/scratch/rn_moda_feminina/documentacao/diagrama_objetos.mermaid) (pode abri-los em um visualizador Markdown ou no editor).
2. **Login e Cadastro**:
   - Abra o sistema (`main.py`). Ele iniciará na tela de Login.
   - Faça login com as credenciais padrão de testes que já vêm pré-carregadas (`rafaela@email.com` / `123`).
   - *Alternativa*: Vá na aba "Cadastrar-se" e crie uma nova usuária cliente.
3. **Navegação e Vitrine**:
   - Apresente a vitrine. Mostre o uso dos filtros dinâmicos de categoria ("Todos", "Roupas", "Calçados") e a barra de busca de produtos.
   - Destaque que os cards de roupas exibem cor/tecido, enquanto os de calçados exibem material/marca (Polimorfismo).
4. **Carrinho de Compras**:
   - Adicione 2 unidades do "Vestido Midi Floral" e 1 unidade da "Sandália Salto Bloco" na vitrine.
   - Navegue até a aba "Meu Carrinho".
   - Remova um item ou finalize a compra.
   - Mostre o popup contendo a **Nota Fiscal** gerada e gerida pela classe `Pedido`.
5. **Painel do Administrador**:
   - Acesse a aba "Painel Admin".
   - Mostre que o estoque do produto comprado diminuiu automaticamente.
   - Use o formulário à esquerda para cadastrar um novo produto (ex: uma Roupa ou Calçado).
   - Volte à vitrine e mostre o produto recém-criado disponível para compra imediata!
   - No painel admin à direita, avance o status do pedido de "Pendente" para "Preparando" -> "Enviado" -> "Entregue".
