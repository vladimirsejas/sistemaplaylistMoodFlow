import os
from src.interface import Interface


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO: aponte para a pasta que contém a subpasta "playlist/"
#
# Exemplos:
#   Windows : r"C:\Users\SeuNome\Music"
#   Linux   : "/home/seuNome/Música"
#   macOS   : "/Users/seuNome/Music"
#
# A estrutura esperada é:
#   <PASTA_MUSICAS>/
#   └── playlist/
#       ├── adele/
#       │     ├── Send My Love.mp4
#       │     └── Set Fire To The Rain.mp4
#       ├── 2026/
#       │     └── ...
#       └── michael/
#             └── ...
# ─────────────────────────────────────────────────────────────────────────────

PASTA_MUSICAS = r"C:\Users\vladi\Music" # ← ALTERE AQUI


def main():
    pasta = os.path.expanduser(PASTA_MUSICAS)

    if not os.path.isdir(pasta):
        print(f"\n[ERRO] Pasta não encontrada: {pasta}")
        print("Edite a variável PASTA_MUSICAS no arquivo main.py e tente novamente.")
        return

    sistema = Interface(pasta_raiz=pasta)
    sistema.executar()


if __name__ == "__main__":
    main()
