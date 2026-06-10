import tkinter as tk
from tkinter import messagebox, ttk
from gui.styles import *
from gui.components import ScrollableFrame, CardProduto
from models.produto import Roupa, Calçado
from models.usuario import Cliente, Administrador
from models.carrinho import Carrinho
from models.pedido import Pedido
from database import Database

class RnModaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("R&N Moda Feminina - Sistema de E-Commerce")
        self.geometry("1100x700")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Banco de Dados Simulado
        self.db = Database()
        
        # Estado do Sistema
        self.current_user = None  # Objeto Cliente logado
        
        # Fontes personalizadas no Tkinter
        self.option_add("*Font", FONT_BODY)

        # Container Principal
        self.main_container = tk.Frame(self, bg=BG_DARK)
        self.main_container.pack(fill="both", expand=True)

        # Inicia na Tela de Login
        self.mostrar_tela_login()

    def limpar_container_principal(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # =========================================================================
    # TELA DE LOGIN / REGISTRO
    # =========================================================================
    def mostrar_tela_login(self):
        self.limpar_container_principal()
        self.current_user = None

        # Frame Centralizado
        frame_central = tk.Frame(self.main_container, bg=BG_DARK)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")

        # Logo / Título
        lbl_logo = tk.Label(frame_central, text="R&N Moda Feminina", font=(FONT_FAMILY, 28, "bold"), fg=COLOR_PRIMARY, bg=BG_DARK)
        lbl_logo.pack(pady=(0, 5))
        lbl_sub = tk.Label(frame_central, text="De mulher para mulher!", font=FONT_BODY, fg=TEXT_SECONDARY, bg=BG_DARK)
        lbl_sub.pack(pady=(0, 30))

        # Notebook (Abas) para Login e Cadastro
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_CARD, foreground=TEXT_PRIMARY, font=FONT_TITLE_SMALL, borderwidth=0, padding=[20, 8])
        style.map("TNotebook.Tab", background=[("selected", COLOR_PRIMARY)], foreground=[("selected", BG_DARK)])

        self.tab_control = ttk.Notebook(frame_central, style="TNotebook")
        
        # Aba Entrar
        tab_login = tk.Frame(self.tab_control, bg=BG_CARD, padx=30, pady=30, bd=1, relief="solid", highlightcolor=COLOR_BORDER, highlightbackground=COLOR_BORDER)
        self.tab_control.add(tab_login, text="  Entrar  ")
        self.setup_aba_login(tab_login)

        # Aba Cadastrar-se
        tab_cadastro = tk.Frame(self.tab_control, bg=BG_CARD, padx=30, pady=25, bd=1, relief="solid", highlightcolor=COLOR_BORDER, highlightbackground=COLOR_BORDER)
        self.tab_control.add(tab_cadastro, text=" Cadastrar-se ")
        self.setup_aba_cadastro(tab_cadastro)

        self.tab_control.pack()

    def setup_aba_login(self, container):
        # Email
        lbl_email = tk.Label(container, text="E-mail:")
        aplicar_estilo_label(lbl_email, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_email.pack(anchor="w", pady=(0, 5))
        
        ent_email = tk.Entry(container, width=35)
        aplicar_estilo_entrada(ent_email)
        ent_email.pack(ipady=6, pady=(0, 15))
        # Dado padrão para testes rápidos
        ent_email.insert(0, "rafaela@email.com")

        # Senha
        lbl_senha = tk.Label(container, text="Senha:")
        aplicar_estilo_label(lbl_senha, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_senha.pack(anchor="w", pady=(0, 5))
        
        ent_senha = tk.Entry(container, width=35, show="*")
        aplicar_estilo_entrada(ent_senha)
        ent_senha.pack(ipady=6, pady=(0, 25))
        # Dado padrão para testes rápidos
        ent_senha.insert(0, "123")

        # Botão Acessar
        btn_acessar = tk.Button(
            container, 
            text="Entrar no Sistema", 
            command=lambda: self.processar_login(ent_email.get(), ent_senha.get())
        )
        aplicar_estilo_botao(btn_acessar, bg=COLOR_PRIMARY, fg="#FFFFFF")
        btn_acessar.pack(fill="x", ipady=5)

    def setup_aba_cadastro(self, container):
        # CPF
        lbl_cpf = tk.Label(container, text="CPF:")
        aplicar_estilo_label(lbl_cpf, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_cpf.pack(anchor="w", pady=(0, 2))
        ent_cpf = tk.Entry(container, width=35)
        aplicar_estilo_entrada(ent_cpf)
        ent_cpf.pack(ipady=4, pady=(0, 10))

        # Nome
        lbl_nome = tk.Label(container, text="Nome Completo:")
        aplicar_estilo_label(lbl_nome, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_nome.pack(anchor="w", pady=(0, 2))
        ent_nome = tk.Entry(container, width=35)
        aplicar_estilo_entrada(ent_nome)
        ent_nome.pack(ipady=4, pady=(0, 10))

        # Email
        lbl_email = tk.Label(container, text="E-mail:")
        aplicar_estilo_label(lbl_email, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_email.pack(anchor="w", pady=(0, 2))
        ent_email = tk.Entry(container, width=35)
        aplicar_estilo_entrada(ent_email)
        ent_email.pack(ipady=4, pady=(0, 10))

        # Senha
        lbl_senha = tk.Label(container, text="Senha:")
        aplicar_estilo_label(lbl_senha, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_senha.pack(anchor="w", pady=(0, 2))
        ent_senha = tk.Entry(container, width=35, show="*")
        aplicar_estilo_entrada(ent_senha)
        ent_senha.pack(ipady=4, pady=(0, 10))

        # Seleção de Tipo de Conta
        self.tipo_user_cad_var = tk.StringVar(value="Cliente")
        frame_tipo_u = tk.Frame(container, bg=BG_CARD)
        frame_tipo_u.pack(fill="x", pady=(0, 5))
        
        lbl_tipo_u = tk.Label(frame_tipo_u, text="Tipo de Conta:")
        aplicar_estilo_label(lbl_tipo_u, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_tipo_u.pack(side="left")
        
        def atualizar_campo_dinamico():
            if self.tipo_user_cad_var.get() == "Cliente":
                self.lbl_din_user.configure(text="Endereço de Entrega:")
            else:
                self.lbl_din_user.configure(text="Cargo / Função (Ex: Gerente):")
        
        r_cli = tk.Radiobutton(
            frame_tipo_u, 
            text="Cliente", 
            variable=self.tipo_user_cad_var, 
            value="Cliente", 
            bg=BG_CARD, 
            fg=TEXT_PRIMARY, 
            selectcolor=BG_CARD, 
            activebackground=BG_CARD,
            activeforeground=TEXT_PRIMARY,
            command=atualizar_campo_dinamico
        )
        r_cli.pack(side="left", padx=10)
        
        r_adm = tk.Radiobutton(
            frame_tipo_u, 
            text="Admin", 
            variable=self.tipo_user_cad_var, 
            value="Admin", 
            bg=BG_CARD, 
            fg=TEXT_PRIMARY, 
            selectcolor=BG_CARD, 
            activebackground=BG_CARD,
            activeforeground=TEXT_PRIMARY,
            command=atualizar_campo_dinamico
        )
        r_adm.pack(side="left", padx=10)

        # Campo Dinâmico (Endereço para Cliente / Cargo para Admin)
        self.lbl_din_user = tk.Label(container, text="Endereço de Entrega:")
        aplicar_estilo_label(self.lbl_din_user, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        self.lbl_din_user.pack(anchor="w", pady=(0, 2))
        ent_din_user = tk.Entry(container, width=35)
        aplicar_estilo_entrada(ent_din_user)
        ent_din_user.pack(ipady=4, pady=(0, 15))

        # Botão Criar Conta
        btn_criar = tk.Button(
            container, 
            text="Criar Conta", 
            command=lambda: self.processar_cadastro(
                ent_cpf.get(), ent_nome.get(), ent_email.get(), ent_senha.get(), ent_din_user.get(), self.tipo_user_cad_var.get()
            )
        )
        aplicar_estilo_botao(btn_criar, bg=COLOR_PRIMARY, fg="#FFFFFF")
        btn_criar.pack(fill="x", ipady=4)

    def processar_login(self, email, senha):
        if not email or not senha:
            messagebox.showerror("Campos Vazios", "Por favor, digite seu e-mail e senha.")
            return

        cliente = self.db.clientes.get(email)
        # Executa método fazerLogin da classe base Usuario (Demonstração do Login)
        if cliente and cliente.fazerLogin(email, senha):
            self.current_user = cliente
            # Limpa carrinho anterior, se for Cliente
            if isinstance(self.current_user, Cliente):
                self.current_user.carrinho.limpar()
            messagebox.showinfo("Sucesso", f"Bem-vinda de volta, {cliente.nome}!")
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Erro de Login", "Credenciais incorretas. Tente novamente.")

    def processar_cadastro(self, cpf, nome, email, senha, endereco_ou_cargo, tipo_user):
        if not all([cpf, nome, email, senha, endereco_ou_cargo]):
            messagebox.showerror("Campos Vazios", "Por favor, preencha todos os campos do cadastro.")
            return

        if email in self.db.clientes:
            messagebox.showerror("Cadastro Duplicado", "Este e-mail já está cadastrado no sistema.")
            return

        # Instanciação polimórfica com base no tipo escolhido
        if tipo_user == "Admin":
            novo_usuario = Administrador(cpf=cpf, nome=nome, email=email, senha=senha, cargo=endereco_ou_cargo)
        else:
            novo_usuario = Cliente(cpf=cpf, nome=nome, email=email, senha=senha, endereco=endereco_ou_cargo)
            
        self.db.clientes[email] = novo_usuario
        self.db.save_data()
        
        messagebox.showinfo("Sucesso", f"Conta de {tipo_user} criada com sucesso! Faça login na aba ao lado.")
        self.tab_control.select(0)  # Volta para aba login

    # =========================================================================
    # DASHBOARD PRINCIPAL (SISTEMA LOGADO)
    # =========================================================================
    def mostrar_dashboard(self):
        self.limpar_container_principal()

        # Layout Split: Sidebar (Menu Lateral) + Main Panel (Painel de Conteúdo)
        self.sidebar = tk.Frame(self.main_container, bg=BG_NAV, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.conteudo = tk.Frame(self.main_container, bg=BG_DARK)
        self.conteudo.pack(side="right", fill="both", expand=True)

        self.setup_sidebar()
        self.abrir_vitrine()

    def setup_sidebar(self):
        is_admin = isinstance(self.current_user, Administrador)
        is_cliente = isinstance(self.current_user, Cliente)

        # Título / Logo
        lbl_titulo = tk.Label(self.sidebar, text="R&N Moda", font=(FONT_FAMILY, 20, "bold"), fg=COLOR_PRIMARY, bg=BG_NAV)
        lbl_titulo.pack(pady=(30, 2), anchor="w", padx=20)
        lbl_sub = tk.Label(self.sidebar, text="Feminina Online", font=FONT_BODY_SMALL, fg=TEXT_SECONDARY, bg=BG_NAV)
        lbl_sub.pack(pady=(0, 40), anchor="w", padx=20)

        # Botões de Navegação (visibilidade baseada no tipo de usuário)
        self.btn_vitrine = self.criar_item_menu("🛍️  Vitrine", self.abrir_vitrine)

        # Carrinho e Pedidos: somente para Clientes
        self.btn_carrinho = None
        self.btn_pedidos = None
        if is_cliente:
            self.btn_carrinho = self.criar_item_menu("🛒  Meu Carrinho (0)", self.abrir_carrinho)
            self.btn_pedidos = self.criar_item_menu("📦  Meus Pedidos", self.abrir_pedidos)
            self.atualizar_contador_carrinho()

        # Painel Admin: somente para Administradores
        self.btn_admin = None
        if is_admin:
            self.btn_admin = self.criar_item_menu("⚙️  Painel Admin", self.abrir_admin)

        # Separador inferior
        tk.Frame(self.sidebar, height=1, bg=COLOR_BORDER).pack(fill="x", padx=10, side="bottom", pady=(10, 15))

        # Usuário Logado
        frame_user = tk.Frame(self.sidebar, bg=BG_NAV)
        frame_user.pack(fill="x", padx=15, side="bottom", pady=10)

        # Indica o tipo de conta
        tipo_txt = "Administradora" if is_admin else "Cliente"
        lbl_tipo = tk.Label(frame_user, text=tipo_txt, font=FONT_BODY_SMALL, fg=COLOR_PRIMARY, bg=BG_NAV)
        lbl_tipo.pack(anchor="w")

        lbl_logado = tk.Label(frame_user, text="Olá,", font=FONT_BODY_SMALL, fg=TEXT_SECONDARY, bg=BG_NAV)
        lbl_logado.pack(anchor="w")
        lbl_nome = tk.Label(frame_user, text=self.current_user.nome, font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_NAV, wraplength=180, justify="left")
        lbl_nome.pack(anchor="w", pady=(0, 10))

        btn_logout = tk.Button(frame_user, text="Sair / Logout", font=FONT_BODY_SMALL, fg=COLOR_DANGER, bg=BG_NAV, bd=0, activebackground=BG_NAV, activeforeground=COLOR_DANGER, cursor="hand2")
        btn_logout.configure(command=self.mostrar_tela_login)
        btn_logout.pack(anchor="w")

    def criar_item_menu(self, text, command):
        btn = tk.Button(
            self.sidebar,
            text=text,
            font=FONT_BODY_BOLD,
            fg=TEXT_SECONDARY,
            bg=BG_NAV,
            activebackground=BG_CARD,
            activeforeground=COLOR_PRIMARY,
            bd=0,
            anchor="w",
            padx=20,
            pady=12,
            cursor="hand2",
            command=command
        )
        btn.pack(fill="x")
        return btn

    def reset_botoes_menu(self):
        botoes = [self.btn_vitrine, self.btn_carrinho, self.btn_pedidos, self.btn_admin]
        for btn in botoes:
            if btn is not None:
                btn.configure(fg=TEXT_SECONDARY, bg=BG_NAV)

    def marcar_menu_ativo(self, btn_ativo):
        self.reset_botoes_menu()
        if btn_ativo is not None:
            btn_ativo.configure(fg=COLOR_PRIMARY, bg=BG_CARD)

    def limpar_painel_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def atualizar_contador_carrinho(self):
        if not isinstance(self.current_user, Cliente) or self.btn_carrinho is None:
            return
        qtd_itens = sum(item["quantidade"] for item in self.current_user.carrinho.itens.values())
        self.btn_carrinho.configure(text=f"🛒  Meu Carrinho ({qtd_itens})")

    # =========================================================================
    # ABA: VITRINE DE PRODUTOS
    # =========================================================================
    def abrir_vitrine(self, filtro="Todos", busca=""):
        self.marcar_menu_ativo(self.btn_vitrine)
        self.limpar_painel_conteudo()

        # Cabeçalho da Aba
        header = tk.Frame(self.conteudo, bg=BG_DARK, pady=20, padx=25)
        header.pack(fill="x")

        lbl_titulo = tk.Label(header, text="Vitrine de Produtos", font=FONT_TITLE_LARGE, fg=TEXT_PRIMARY, bg=BG_DARK)
        lbl_titulo.pack(side="left")

        # Filtro de Busca
        frame_filtro_busca = tk.Frame(header, bg=BG_DARK)
        frame_filtro_busca.pack(side="right")

        ent_busca = tk.Entry(frame_filtro_busca, width=20)
        aplicar_estilo_entrada(ent_busca)
        ent_busca.insert(0, busca)
        ent_busca.pack(side="left", ipady=4, padx=5)

        # Botão de Busca
        btn_buscar = tk.Button(
            frame_filtro_busca, 
            text="Buscar", 
            command=lambda: self.abrir_vitrine(filtro, ent_busca.get())
        )
        aplicar_estilo_botao(btn_buscar, bg=COLOR_BORDER, fg=TEXT_PRIMARY)
        btn_buscar.pack(side="left")

        # Filtros rápidos (Botões Roupas, Calçados, Todos)
        frame_filtros = tk.Frame(self.conteudo, bg=BG_DARK, padx=25, pady=0)
        frame_filtros.pack(fill="x", pady=(0, 10))

        filtros_nomes = ["Todos", "Roupas", "Calçados"]
        for f in filtros_nomes:
            bg_f = COLOR_PRIMARY if filtro == f else BG_CARD
            fg_f = "#FFFFFF" if filtro == f else TEXT_PRIMARY
            btn_f = tk.Button(
                frame_filtros, 
                text=f, 
                command=lambda tipo=f: self.abrir_vitrine(tipo, ent_busca.get())
            )
            aplicar_estilo_botao(btn_f, bg=bg_f, fg=fg_f)
            btn_f.pack(side="left", padx=(0, 10))

        # Divisor
        tk.Frame(self.conteudo, height=1, bg=COLOR_BORDER).pack(fill="x", padx=25)

        # Frame Principal com Scroll
        scroll_frame = ScrollableFrame(self.conteudo, bg=BG_DARK)
        scroll_frame.pack(fill="both", expand=True, padx=25, pady=15)

        # Grid de produtos
        grid_produtos = scroll_frame.scrollable_frame
        
        # Filtra os produtos com base na seleção
        produtos_filtrados = []
        for p in self.db.produtos.values():
            detalhes = p.exibirDetalhes()
            tipo = detalhes["Tipo"]
            
            # Aplica busca de texto
            if busca and busca.lower() not in p.nome.lower():
                continue
                
            # Aplica filtro de categoria
            if filtro == "Roupas" and tipo != "Roupa":
                continue
            if filtro == "Calçados" and tipo != "Calçado":
                continue
                
            produtos_filtrados.append(p)

        if not produtos_filtrados:
            lbl_nada = tk.Label(grid_produtos, text="Nenhum produto encontrado.", bg=BG_DARK, fg=TEXT_SECONDARY, font=FONT_TITLE_SMALL)
            lbl_nada.pack(pady=40)
            return

        # Popula o grid (2 colunas)
        row = 0
        col = 0
        grid_produtos.columnconfigure(0, weight=1, uniform="equal")
        grid_produtos.columnconfigure(1, weight=1, uniform="equal")

        for prod in produtos_filtrados:
            card = CardProduto(grid_produtos, prod, self.adicionar_produto_ao_carrinho)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col > 1:
                col = 0
                row += 1

    def adicionar_produto_ao_carrinho(self, produto, qtd):
        # Verifica se é Cliente (Admin não pode comprar)
        if not isinstance(self.current_user, Cliente):
            messagebox.showinfo("Acesso Restrito", "Administradores não podem comprar produtos. Faça login como Cliente.")
            return
        # Chama a associação da classe Cliente
        sucesso = self.current_user.adicionarAoCarrinho(produto, qtd)
        if sucesso:
            self.atualizar_contador_carrinho()
            messagebox.showinfo("Adicionado!", f"{qtd}x '{produto.nome}' adicionado ao carrinho com sucesso!")
            # Recarrega a vitrine para mostrar os estoques atualizados em tempo real se necessário
            self.abrir_vitrine()
        else:
            messagebox.showerror("Erro de Estoque", f"Desculpe, quantidade indisponível. Estoque disponível: {produto.estoque}")

    # =========================================================================
    # ABA: MEU CARRINHO DE COMPRAS
    # =========================================================================
    def abrir_carrinho(self):
        self.marcar_menu_ativo(self.btn_carrinho)
        self.limpar_painel_conteudo()

        header = tk.Frame(self.conteudo, bg=BG_DARK, pady=20, padx=25)
        header.pack(fill="x")

        lbl_titulo = tk.Label(header, text="Meu Carrinho", font=FONT_TITLE_LARGE, fg=TEXT_PRIMARY, bg=BG_DARK)
        lbl_titulo.pack(side="left")

        # Divisor
        tk.Frame(self.conteudo, height=1, bg=COLOR_BORDER).pack(fill="x", padx=25)

        # Se carrinho estiver vazio
        if not self.current_user.carrinho.itens:
            lbl_vazio = tk.Label(self.conteudo, text="🛒 Seu carrinho está vazio.", bg=BG_DARK, fg=TEXT_SECONDARY, font=FONT_TITLE_MED)
            lbl_vazio.pack(pady=100)
            return

        # Frame Principal com Scroll
        scroll_frame = ScrollableFrame(self.conteudo, bg=BG_DARK)
        scroll_frame.pack(fill="both", expand=True, padx=25, pady=15)
        container_itens = scroll_frame.scrollable_frame

        # Lista de itens
        for codigo, item in list(self.current_user.carrinho.itens.items()):
            prod = item["produto"]
            qtd = item["quantidade"]
            subtotal = prod.preco * qtd

            detalhes = prod.exibirDetalhes()

            frame_item = tk.Frame(container_itens, bg=BG_CARD, bd=1, highlightthickness=0, highlightbackground=COLOR_BORDER)
            frame_item.pack(fill="x", pady=5, padx=10)

            # Detalhes do Produto
            frame_detalhes = tk.Frame(frame_item, bg=BG_CARD)
            frame_detalhes.pack(side="left", padx=15, pady=15)

            lbl_tipo = tk.Label(frame_detalhes, text=detalhes["Tipo"].upper(), font=FONT_BODY_SMALL, fg=COLOR_PRIMARY, bg=BG_CARD)
            lbl_tipo.pack(anchor="w")

            lbl_nome = tk.Label(frame_detalhes, text=prod.nome, font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_CARD)
            lbl_nome.pack(anchor="w")

            if detalhes["Tipo"] == "Roupa":
                specs = f"Tamanho: {detalhes['Tamanho']} | Cor: {detalhes['Cor']} | Tecido: {detalhes['Tecido']}"
            else:
                specs = f"Tamanho: {detalhes['Tamanho']} | Material: {detalhes['Material']} | Marca: {detalhes['Marca']}"

            lbl_specs = tk.Label(frame_detalhes, text=specs, font=FONT_BODY_SMALL, fg=TEXT_SECONDARY, bg=BG_CARD)
            lbl_specs.pack(anchor="w")

            # Remocao / Quantidade / Subtotal
            frame_valores = tk.Frame(frame_item, bg=BG_CARD)
            frame_valores.pack(side="right", padx=15, pady=15)

            lbl_val_unit = tk.Label(frame_valores, text=f"Unit: R$ {prod.preco:.2f}", font=FONT_BODY_SMALL, fg=TEXT_SECONDARY, bg=BG_CARD)
            lbl_val_unit.pack(side="left", padx=10)

            lbl_qtd = tk.Label(frame_valores, text=f"Qtd: {qtd}", font=FONT_BODY, fg=TEXT_PRIMARY, bg=BG_CARD)
            lbl_qtd.pack(side="left", padx=10)

            lbl_subtotal = tk.Label(frame_valores, text=f"R$ {subtotal:.2f}", font=FONT_TITLE_SMALL, fg=COLOR_PRIMARY, bg=BG_CARD)
            lbl_subtotal.pack(side="left", padx=15)

            btn_remover = tk.Button(
                frame_valores, 
                text="Remover", 
                command=lambda c=codigo: self.remover_do_carrinho(c)
            )
            aplicar_estilo_botao(btn_remover, bg=COLOR_DANGER, fg="#FFFFFF")
            btn_remover.pack(side="left")

        # Checkout Bar (Total e Finalizar)
        checkout_bar = tk.Frame(self.conteudo, bg=BG_CARD, bd=1, highlightthickness=0, highlightbackground=COLOR_BORDER)
        checkout_bar.pack(fill="x", side="bottom", padx=25, pady=20)

        frame_total = tk.Frame(checkout_bar, bg=BG_CARD)
        frame_total.pack(side="left", padx=20, pady=15)

        lbl_total_txt = tk.Label(frame_total, text="Valor Total:", font=FONT_BODY, fg=TEXT_SECONDARY, bg=BG_CARD)
        lbl_total_txt.pack(anchor="w")

        lbl_total_val = tk.Label(frame_total, text=f"R$ {self.current_user.carrinho.valorTotal:.2f}", font=FONT_TITLE_LARGE, fg=COLOR_PRIMARY, bg=BG_CARD)
        lbl_total_val.pack(anchor="w")

        btn_comprar = tk.Button(checkout_bar, text="Finalizar Compra", command=self.finalizar_compra)
        aplicar_estilo_botao(btn_comprar, bg=COLOR_SUCCESS, fg="#FFFFFF")
        btn_comprar.pack(side="right", padx=20, pady=15, ipadx=10, ipady=5)

    def remover_do_carrinho(self, codigo_produto):
        if self.current_user.carrinho.removerItem(codigo_produto):
            self.atualizar_contador_carrinho()
            self.abrir_carrinho()

    def finalizar_compra(self):
        if not self.current_user.carrinho.itens:
            return

        # Criação de Pedido, Atualização de estoque e Limpeza do carrinho
        # Chamando método finalizarCompra da classe Cliente
        pedido = self.current_user.finalizarCompra()
        
        if pedido:
            # Salva o pedido no BD simulado
            self.db.pedidos[pedido.idPedido] = pedido
            self.db.save_data()
            
            # Geração da Nota Fiscal
            nota_fiscal = pedido.gerarNotaFiscal()
            
            # Mostra a Nota Fiscal na Tela (Popup Premium)
            self.mostrar_modal_nota_fiscal(nota_fiscal)
            
            # Atualiza o contador de itens na tela e redireciona
            self.atualizar_contador_carrinho()
            self.abrir_pedidos()

    def mostrar_modal_nota_fiscal(self, texto_nota):
        modal = tk.Toplevel(self)
        modal.title("Nota Fiscal Eletrônica - R&N Moda")
        modal.geometry("550x600")
        modal.configure(bg=BG_DARK)
        modal.grab_set()  # Bloqueia interação com a janela de trás
        modal.transient(self)

        lbl_header = tk.Label(modal, text="Compra Realizada com Sucesso!", font=FONT_TITLE_MED, fg=COLOR_SUCCESS, bg=BG_DARK)
        lbl_header.pack(pady=15)

        # Campo de texto para exibir a nota com scrollbar
        frame_texto = tk.Frame(modal, bg=BG_DARK)
        frame_texto.pack(fill="both", expand=True, padx=20, pady=5)

        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side="right", fill="y")

        # Usar Courier para a nota fiscal alinhar perfeitamente
        txt_nota = tk.Text(frame_texto, wrap="word", yscrollcommand=scrollbar.set, bg=BG_CARD, fg=TEXT_PRIMARY, bd=1, relief="solid", font=("Courier", 10))
        txt_nota.insert("1.0", texto_nota)
        txt_nota.configure(state="disabled") # Somente leitura
        txt_nota.pack(fill="both", expand=True)

        scrollbar.config(command=txt_nota.yview)

        btn_fechar = tk.Button(modal, text="Fechar e Voltar", command=modal.destroy)
        aplicar_estilo_botao(btn_fechar, bg=COLOR_PRIMARY, fg="#FFFFFF")
        btn_fechar.pack(pady=15, ipadx=10)

    # =========================================================================
    # ABA: MEUS PEDIDOS
    # =========================================================================
    def abrir_pedidos(self):
        self.marcar_menu_ativo(self.btn_pedidos)
        self.limpar_painel_conteudo()

        header = tk.Frame(self.conteudo, bg=BG_DARK, pady=20, padx=25)
        header.pack(fill="x")

        lbl_titulo = tk.Label(header, text="Histórico de Pedidos", font=FONT_TITLE_LARGE, fg=TEXT_PRIMARY, bg=BG_DARK)
        lbl_titulo.pack(side="left")

        # Divisor
        tk.Frame(self.conteudo, height=1, bg=COLOR_BORDER).pack(fill="x", padx=25)

        # Filtrar apenas os pedidos deste cliente
        pedidos_usuario = [p for p in self.db.pedidos.values() if p.cliente.email == self.current_user.email]

        if not pedidos_usuario:
            lbl_nada = tk.Label(self.conteudo, text="📦 Você ainda não realizou nenhum pedido.", bg=BG_DARK, fg=TEXT_SECONDARY, font=FONT_TITLE_MED)
            lbl_nada.pack(pady=100)
            return

        scroll_frame = ScrollableFrame(self.conteudo, bg=BG_DARK)
        scroll_frame.pack(fill="both", expand=True, padx=25, pady=15)
        container_pedidos = scroll_frame.scrollable_frame

        # Exibir em ordem reversa (mais recentes primeiro)
        for pedido in reversed(pedidos_usuario):
            # Calcula valor do pedido
            total_pedido = sum(item["produto"].preco * item["quantidade"] for item in pedido.produtosPedidos)

            frame_ped = tk.Frame(container_pedidos, bg=BG_CARD, bd=1, highlightthickness=0, highlightbackground=COLOR_BORDER)
            frame_ped.pack(fill="x", pady=6, padx=10)

            frame_info = tk.Frame(frame_ped, bg=BG_CARD)
            frame_info.pack(side="left", padx=15, pady=15)

            lbl_id = tk.Label(frame_info, text=f"Pedido #{pedido.idPedido}", font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=BG_CARD)
            lbl_id.pack(anchor="w")

            status_colors = {
                "Pendente": COLOR_PRIMARY,
                "Preparando": "#F59E0B",
                "Enviado": "#3B82F6",
                "Entregue": COLOR_SUCCESS
            }
            color_s = status_colors.get(pedido.status, TEXT_SECONDARY)
            lbl_status = tk.Label(frame_info, text=f"Status: {pedido.status}", font=FONT_BODY, fg=color_s, bg=BG_CARD)
            lbl_status.pack(anchor="w")

            lbl_total = tk.Label(frame_info, text=f"Total: R$ {total_pedido:.2f} | {len(pedido.produtosPedidos)} item(ns)", font=FONT_BODY_SMALL, fg=TEXT_SECONDARY, bg=BG_CARD)
            lbl_total.pack(anchor="w")

            # Botão para reinspecionar nota fiscal
            btn_nota = tk.Button(
                frame_ped, 
                text="Nota Fiscal", 
                command=lambda p=pedido: self.mostrar_modal_nota_fiscal(p.gerarNotaFiscal())
            )
            aplicar_estilo_botao(btn_nota, bg=COLOR_BORDER, fg=TEXT_PRIMARY)
            btn_nota.pack(side="right", padx=15, pady=15)

    # =========================================================================
    # ABA: PAINEL ADMINISTRATIVO
    # =========================================================================
    def abrir_admin(self):
        self.marcar_menu_ativo(self.btn_admin)
        self.limpar_painel_conteudo()

        header = tk.Frame(self.conteudo, bg=BG_DARK, pady=15, padx=25)
        header.pack(fill="x")

        lbl_titulo = tk.Label(header, text="Painel do Administrador", font=FONT_TITLE_LARGE, fg=TEXT_PRIMARY, bg=BG_DARK)
        lbl_titulo.pack(side="left")

        lbl_desc = tk.Label(header, text="(Modo Simulado de Administração de Vendas)", font=FONT_BODY_SMALL, fg=TEXT_SECONDARY, bg=BG_DARK)
        lbl_desc.pack(side="left", padx=15, pady=(10, 0))

        # Divisor
        tk.Frame(self.conteudo, height=1, bg=COLOR_BORDER).pack(fill="x", padx=25)

        # Layout Split: Lado Esquerdo (Cadastrar Produto) | Lado Direito (Gerenciar Pedidos e Estoque)
        frame_corpo = tk.Frame(self.conteudo, bg=BG_DARK)
        frame_corpo.pack(fill="both", expand=True, padx=25, pady=15)

        frame_esquerdo = tk.Frame(frame_corpo, bg=BG_CARD, bd=1, highlightthickness=0, highlightbackground=COLOR_BORDER)
        frame_esquerdo.pack(side="left", fill="both", expand=True, padx=(0, 10))

        frame_direito = tk.Frame(frame_corpo, bg=BG_DARK)
        frame_direito.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.setup_cadastro_produto_admin(frame_esquerdo)
        self.setup_gerenciamento_pedidos_admin(frame_direito)

    def setup_cadastro_produto_admin(self, container):
        # Título
        lbl_c_titulo = tk.Label(container, text="Cadastrar Novo Produto", font=FONT_TITLE_MED, fg=COLOR_PRIMARY, bg=BG_CARD)
        lbl_c_titulo.pack(anchor="w", padx=20, pady=(20, 15))

        # Tipo de Produto (Roupa vs Calçado)
        self.tipo_prod_var = tk.StringVar(value="Roupa")
        
        frame_tipo = tk.Frame(container, bg=BG_CARD)
        frame_tipo.pack(fill="x", padx=20, pady=(0, 10))

        lbl_tipo = tk.Label(frame_tipo, text="Tipo:")
        aplicar_estilo_label(lbl_tipo, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_tipo.pack(side="left")

        r_roupa = tk.Radiobutton(
            frame_tipo, 
            text="Roupa", 
            variable=self.tipo_prod_var, 
            value="Roupa", 
            bg=BG_CARD, 
            fg=TEXT_PRIMARY, 
            selectcolor=BG_CARD, 
            activebackground=BG_CARD,
            activeforeground=TEXT_PRIMARY,
            command=self.toggle_admin_fields
        )
        r_roupa.pack(side="left", padx=10)

        r_calcado = tk.Radiobutton(
            frame_tipo, 
            text="Calçado", 
            variable=self.tipo_prod_var, 
            value="Calçado", 
            bg=BG_CARD, 
            fg=TEXT_PRIMARY, 
            selectcolor=BG_CARD, 
            activebackground=BG_CARD,
            activeforeground=TEXT_PRIMARY,
            command=self.toggle_admin_fields
        )
        r_calcado.pack(side="left", padx=10)

        # Formulário em Grid
        form_grid = tk.Frame(container, bg=BG_CARD)
        form_grid.pack(fill="both", expand=True, padx=20)
        form_grid.columnconfigure(1, weight=1)

        # Campos Comuns
        lbl_cod = tk.Label(form_grid, text="Código:")
        aplicar_estilo_label(lbl_cod, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_cod.grid(row=0, column=0, sticky="w", pady=4)
        self.ent_cod = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_cod)
        self.ent_cod.grid(row=0, column=1, sticky="ew", pady=4, ipady=3)

        lbl_nome = tk.Label(form_grid, text="Nome:")
        aplicar_estilo_label(lbl_nome, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_nome.grid(row=1, column=0, sticky="w", pady=4)
        self.ent_nome_p = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_nome_p)
        self.ent_nome_p.grid(row=1, column=1, sticky="ew", pady=4, ipady=3)

        lbl_preco = tk.Label(form_grid, text="Preço:")
        aplicar_estilo_label(lbl_preco, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_preco.grid(row=2, column=0, sticky="w", pady=4)
        self.ent_preco = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_preco)
        self.ent_preco.grid(row=2, column=1, sticky="ew", pady=4, ipady=3)

        lbl_estoque = tk.Label(form_grid, text="Estoque Inicial:")
        aplicar_estilo_label(lbl_estoque, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        lbl_estoque.grid(row=3, column=0, sticky="w", pady=4)
        self.ent_estoque = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_estoque)
        self.ent_estoque.grid(row=3, column=1, sticky="ew", pady=4, ipady=3)

        # Campos Dinâmicos (Roupa)
        self.lbl_din1 = tk.Label(form_grid, text="Tamanho (S/M/L):")
        aplicar_estilo_label(self.lbl_din1, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        self.lbl_din1.grid(row=4, column=0, sticky="w", pady=4)
        self.ent_din1 = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_din1)
        self.ent_din1.grid(row=4, column=1, sticky="ew", pady=4, ipady=3)

        self.lbl_din2 = tk.Label(form_grid, text="Cor:")
        aplicar_estilo_label(self.lbl_din2, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        self.lbl_din2.grid(row=5, column=0, sticky="w", pady=4)
        self.ent_din2 = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_din2)
        self.ent_din2.grid(row=5, column=1, sticky="ew", pady=4, ipady=3)

        self.lbl_din3 = tk.Label(form_grid, text="Tecido:")
        aplicar_estilo_label(self.lbl_din3, font=FONT_BODY_BOLD, fg=TEXT_SECONDARY)
        self.lbl_din3.grid(row=6, column=0, sticky="w", pady=4)
        self.ent_din3 = tk.Entry(form_grid)
        aplicar_estilo_entrada(self.ent_din3)
        self.ent_din3.grid(row=6, column=1, sticky="ew", pady=4, ipady=3)

        # Botão cadastrar
        btn_cad = tk.Button(container, text="Cadastrar Produto", command=self.gravar_produto_admin)
        aplicar_estilo_botao(btn_cad, bg=COLOR_PRIMARY, fg="#FFFFFF")
        btn_cad.pack(fill="x", padx=20, pady=20)

    def toggle_admin_fields(self):
        tipo = self.tipo_prod_var.get()
        if tipo == "Roupa":
            self.lbl_din1.configure(text="Tamanho (Ex: M):")
            self.lbl_din2.configure(text="Cor:")
            self.lbl_din3.configure(text="Tecido:")
        else:
            self.lbl_din1.configure(text="Tamanho (Ex: 38):")
            self.lbl_din2.configure(text="Material:")
            self.lbl_din3.configure(text="Marca:")

    def gravar_produto_admin(self):
        tipo = self.tipo_prod_var.get()
        try:
            codigo = int(self.ent_cod.get())
            nome = self.ent_nome_p.get()
            preco = float(self.ent_preco.get())
            estoque = int(self.ent_estoque.get())
            
            if codigo in self.db.produtos:
                messagebox.showerror("Erro de Cadastro", f"O código {codigo} já está em uso por outro produto.")
                return

            if not nome:
                messagebox.showerror("Erro", "O nome do produto não pode ser vazio.")
                return

            if tipo == "Roupa":
                tamanho = self.ent_din1.get()
                cor = self.ent_din2.get()
                tecido = self.ent_din3.get()
                
                if not all([tamanho, cor, tecido]):
                    messagebox.showerror("Erro", "Preencha todos os campos da Roupa.")
                    return
                # Herança e instanciação
                novo_prod = Roupa(codigo, nome, preco, estoque, tamanho, cor, tecido)
            else:
                try:
                    tamanho = int(self.ent_din1.get())
                except ValueError:
                    messagebox.showerror("Erro de Tipo", "Para Calçados, o tamanho deve ser um número inteiro (ex: 37).")
                    return
                material = self.ent_din2.get()
                marca = self.ent_din3.get()

                if not all([material, marca]):
                    messagebox.showerror("Erro", "Preencha todos os campos do Calçado.")
                    return
                # Herança e instanciação
                novo_prod = Calçado(codigo, nome, preco, estoque, tamanho, material, marca)

            # Salva
            self.db.produtos[codigo] = novo_prod
            self.db.save_data()
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
            
            # Limpa campos
            self.ent_cod.delete(0, tk.END)
            self.ent_nome_p.delete(0, tk.END)
            self.ent_preco.delete(0, tk.END)
            self.ent_estoque.delete(0, tk.END)
            self.ent_din1.delete(0, tk.END)
            self.ent_din2.delete(0, tk.END)
            self.ent_din3.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro de Conversão", "Código e Estoque devem ser INTEIROS. Preço deve ser FLOAT (ex: 120.50).")

    def setup_gerenciamento_pedidos_admin(self, container):
        # Frame superior para listagem de pedidos
        frame_pedidos = tk.Frame(container, bg=BG_CARD, bd=1, highlightthickness=0, highlightbackground=COLOR_BORDER)
        frame_pedidos.pack(fill="both", expand=True, pady=(0, 10))

        lbl_tit_ped = tk.Label(frame_pedidos, text="Gerenciamento de Pedidos (Todos os Clientes)", font=FONT_TITLE_MED, fg=COLOR_PRIMARY, bg=BG_CARD)
        lbl_tit_ped.pack(anchor="w", padx=20, pady=(15, 10))

        scroll_ped = ScrollableFrame(frame_pedidos, bg=BG_CARD)
        scroll_ped.pack(fill="both", expand=True, padx=15, pady=5)
        lista_ped = scroll_ped.scrollable_frame

        if not self.db.pedidos:
            lbl_nada = tk.Label(lista_ped, text="Nenhum pedido no sistema.", bg=BG_CARD, fg=TEXT_SECONDARY)
            lbl_nada.pack(pady=20)
        else:
            for pedido in list(self.db.pedidos.values()):
                frame_lin = tk.Frame(lista_ped, bg=BG_CARD, pady=5)
                frame_lin.pack(fill="x", pady=2)
                
                # Detalhes do pedido
                txt_ped = f"Pedido #{pedido.idPedido} - {pedido.cliente.nome}\nStatus Atual: {pedido.status}"
                lbl_lin = tk.Label(frame_lin, text=txt_ped, font=FONT_BODY_SMALL, justify="left", anchor="w")
                aplicar_estilo_label(lbl_lin, font=FONT_BODY_SMALL, fg=TEXT_PRIMARY, bg=BG_CARD)
                lbl_lin.pack(side="left", padx=10)

                # Ação de Alterar Status
                btn_status = tk.Button(
                    frame_lin, 
                    text="Avançar Status", 
                    command=lambda p=pedido: self.avancar_status_pedido(p)
                )
                aplicar_estilo_botao(btn_status, bg=COLOR_BORDER, fg=TEXT_PRIMARY)
                btn_status.pack(side="right", padx=5)

                # Ação de Ver Nota Fiscal
                btn_ver = tk.Button(
                    frame_lin, 
                    text="Ver Nota", 
                    command=lambda p=pedido: self.mostrar_modal_nota_fiscal(p.gerarNotaFiscal())
                )
                aplicar_estilo_botao(btn_ver, bg=COLOR_BORDER, fg=TEXT_PRIMARY)
                btn_ver.pack(side="right", padx=5)

                tk.Frame(lista_ped, height=1, bg=COLOR_BORDER).pack(fill="x", padx=10, pady=2)

    def avancar_status_pedido(self, pedido):
        # Fluxo de status
        fluxo = ["Pendente", "Preparando", "Enviado", "Entregue"]
        try:
            idx = fluxo.index(pedido.status)
            if idx < len(fluxo) - 1:
                novo_status = fluxo[idx + 1]
                # Executa alterarStatus do modelo Pedido
                pedido.alterarStatus(novo_status)
                self.db.save_data()
                messagebox.showinfo("Status Atualizado", f"Pedido #{pedido.idPedido} avançou para '{novo_status}'.")
                self.abrir_admin()  # Recarrega tela
            else:
                messagebox.showinfo("Status Final", f"Pedido #{pedido.idPedido} já está no status final ('Entregue').")
        except ValueError:
            # Caso seja um status desconhecido, reseta para Pendente
            pedido.alterarStatus("Pendente")
            self.db.save_data()
            self.abrir_admin()
