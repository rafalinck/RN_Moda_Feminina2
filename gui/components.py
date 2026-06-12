import tkinter as tk
from tkinter import ttk
from gui.styles import *

# =====================================================================
# CLASSE: SCROLLABLEFRAME
# =====================================================================
class ScrollableFrame(tk.Frame):
    def __init__(self, container, bg=BG_DARK, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.configure(bg=bg)
        
        self.canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg, bd=0)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# =====================================================================
# CLASSE: CARDPRODUTO
# =====================================================================
class CardProduto(tk.Frame):
    def __init__(self, parent, produto, on_adicionar_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.produto = produto
        self.on_adicionar = on_adicionar_callback
        
        self.configure(bg=BG_CARD, bd=1, highlightthickness=0, highlightbackground=COLOR_BORDER)
        
        detalhes = produto.exibirDetalhes()
        
        lbl_tipo = tk.Label(self, text=detalhes["Tipo"].upper(), fg=COLOR_PRIMARY, font=FONT_BODY_SMALL)
        aplicar_estilo_label(lbl_tipo, font=FONT_BODY_SMALL, fg=COLOR_PRIMARY)
        lbl_tipo.pack(anchor="w", padx=15, pady=(15, 2))
        
        lbl_nome = tk.Label(self, text=produto.nome, fg=TEXT_PRIMARY, font=FONT_TITLE_SMALL, wraplength=220, justify="left")
        aplicar_estilo_label(lbl_nome, font=FONT_TITLE_SMALL)
        lbl_nome.pack(anchor="w", padx=15, pady=(0, 10))
        
        frame_specs = tk.Frame(self, bg=BG_CARD)
        frame_specs.pack(fill="x", padx=15, pady=5)
        
        if detalhes["Tipo"] == "Roupa":
            specs_text = f"Tamanho: {detalhes['Tamanho']}  |  Cor: {detalhes['Cor']}\nTecido: {detalhes['Tecido']}"
        else:
            specs_text = f"Tamanho: {detalhes['Tamanho']}  |  Material: {detalhes['Material']}\nMarca: {detalhes['Marca']}"
            
        lbl_specs = tk.Label(frame_specs, text=specs_text, justify="left", anchor="w")
        aplicar_estilo_label(lbl_specs, font=FONT_BODY_SMALL, fg=TEXT_SECONDARY)
        lbl_specs.pack(anchor="w")

        div = tk.Frame(self, height=1, bg=COLOR_BORDER)
        div.pack(fill="x", padx=15, pady=10)

        frame_rodape = tk.Frame(self, bg=BG_CARD)
        frame_rodape.pack(fill="x", padx=15, pady=(0, 15))
        
        frame_preco_estoque = tk.Frame(frame_rodape, bg=BG_CARD)
        frame_preco_estoque.pack(side="left", fill="y")
        
        lbl_preco = tk.Label(frame_preco_estoque, text=f"R$ {produto.preco:.2f}")
        aplicar_estilo_label(lbl_preco, font=FONT_TITLE_MED, fg=COLOR_PRIMARY)
        lbl_preco.pack(anchor="w")
        
        txt_estoque = f"{produto.estoque} disponíveis" if produto.estoque > 0 else "Sem estoque"
        fg_estoque = COLOR_SUCCESS if produto.estoque > 0 else COLOR_DANGER
        lbl_estoque = tk.Label(frame_preco_estoque, text=txt_estoque)
        aplicar_estilo_label(lbl_estoque, font=FONT_BODY_SMALL, fg=fg_estoque)
        lbl_estoque.pack(anchor="w")
        
        if produto.estoque > 0:
            frame_compra = tk.Frame(frame_rodape, bg=BG_CARD)
            frame_compra.pack(side="right", fill="y")
            
            lbl_qtd = tk.Label(frame_compra, text="Qtd:")
            aplicar_estilo_label(lbl_qtd, font=FONT_BODY_SMALL, fg=TEXT_SECONDARY)
            lbl_qtd.pack(side="left", padx=(0, 2))
            
            self.spin_qtd = tk.Spinbox(
                frame_compra, 
                from_=1, 
                to=produto.estoque, 
                width=3, 
                bg="#FFFFFF", 
                fg=TEXT_PRIMARY, 
                buttonbackground=BG_CARD, 
                bd=0,
                highlightthickness=1,
                highlightbackground=COLOR_BORDER,
                highlightcolor=COLOR_PRIMARY
            )
            self.spin_qtd.pack(side="left", padx=(0, 8), ipady=2)
            
            btn_add = tk.Button(
                frame_compra,
                text="Comprar",
                command=lambda: self.on_adicionar(self.produto, int(self.spin_qtd.get()))
            )
            aplicar_estilo_botao(btn_add, bg=COLOR_PRIMARY, fg="#FFFFFF")
            btn_add.pack(side="left")
        else:
            lbl_esgotado = tk.Label(frame_rodape, text="Esgotado")
            aplicar_estilo_label(lbl_esgotado, font=FONT_BODY_BOLD, fg=COLOR_DANGER)
            lbl_esgotado.pack(side="right", padx=5)
