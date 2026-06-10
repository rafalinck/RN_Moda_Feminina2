# Configurações de Estilo da Interface R&N Moda Feminina

# Cores
BG_DARK = "#FFFFFF"          # Fundo principal claro
BG_CARD = "#FFFFFF"          # Fundo de cards e seções
BG_NAV = "#FFFFFF"           # Fundo do menu de navegação
TEXT_PRIMARY = "#000000"     # Texto principal preto
TEXT_SECONDARY = "#111111"   # Texto secundário/cinza escuro
TEXT_MUTED = "#666666"       # Texto desabilitado
COLOR_PRIMARY = "#C59B27"    # Amarelo Dourado R&N (Principal)
COLOR_SECONDARY = "#DFB74B"  # Dourado Claro
COLOR_SUCCESS = "#2E7D32"    # Verde de Sucesso
COLOR_DANGER = "#C62828"     # Vermelho de Perigo
COLOR_BORDER = "#EAEAEA"     # Cor das bordas cinza claro
COLOR_HOVER = "#A37B1A"      # Cor de hover para botões (dourado mais escuro)

# Fontes
FONT_FAMILY = "Segoe UI"
FONT_TITLE_LARGE = (FONT_FAMILY, 24, "bold")
FONT_TITLE_MED = (FONT_FAMILY, 16, "bold")
FONT_TITLE_SMALL = (FONT_FAMILY, 12, "bold")
FONT_BODY = (FONT_FAMILY, 10)
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_BODY_SMALL = (FONT_FAMILY, 9)
FONT_BUTTON = (FONT_FAMILY, 10, "bold")

# Funções auxiliares para estilização de widgets do Tkinter
def aplicar_estilo_painel(widget, bg=BG_CARD):
    widget.configure(bg=bg, bd=0, highlightthickness=0)

def aplicar_estilo_botao(widget, bg=COLOR_PRIMARY, fg="#FFFFFF", activebackground=COLOR_SECONDARY, activeforeground="#FFFFFF"):
    widget.configure(
        bg=bg,
        fg=fg,
        activebackground=activebackground,
        activeforeground=activeforeground,
        font=FONT_BUTTON,
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        relief="flat"
    )

def aplicar_estilo_entrada(widget):
    widget.configure(
        bg="#FFFFFF",
        fg=TEXT_PRIMARY,
        insertbackground=TEXT_PRIMARY,
        font=FONT_BODY,
        bd=0,
        highlightthickness=1,
        highlightbackground=COLOR_BORDER,
        highlightcolor=COLOR_PRIMARY
    )

def aplicar_estilo_label(widget, font=FONT_BODY, fg=TEXT_PRIMARY, bg=BG_CARD):
    widget.configure(
        font=font,
        fg=fg,
        bg=bg
    )
