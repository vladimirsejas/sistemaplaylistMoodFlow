from src.controlador import Controlador


class Interface:

    def __init__(self):
        self.controlador = Controlador()

    def exibir_menu(self):
        print("\n==============================")
        print("         MOOD FLOW")
        print("==============================")
        print("1 - Buscar uma musica")
        print("2 - Buscar musicas de um artista")
        print("3 - Ouvir musicas para relaxar")
        print("4 - Ouvir musicas para focar")
        print("5 - Ouvir musicas para animar")
        print("6 - Gerar playlist aleatoria")
        print("7 - Ver historico")
        print("8 - Ver biblioteca")
        print("9 - Parar musica")
        print("0 - Sair")
        print("==============================")

    def executar(self):
        print("\nBem-vindo ao MoodFlow!")
        print("O player que entende o seu humor.")

        while True:
            self.exibir_menu()
            opcao = input("O que voce quer ouvir? ")

            if opcao == "1":
                self.controlador.buscar_especifica()

            elif opcao == "2":
                self.controlador.buscar_artista()

            elif opcao == "3":
                self.controlador.gerar_playlist_humor("relaxar")

            elif opcao == "4":
                self.controlador.gerar_playlist_humor("focar")

            elif opcao == "5":
                self.controlador.gerar_playlist_humor("animar")

            elif opcao == "6":
                self.controlador.playlist_aleatoria()

            elif opcao == "7":
                self.controlador.ver_historico()

            elif opcao == "8":
                self.controlador.ver_biblioteca()

            elif opcao == "9":
                self.controlador.parar()
                print("Musica pausada.")

            elif opcao == "0":
                self.controlador.parar()
                print("\nAte logo!")
                break

            else:
                print("\nOpcao invalida.")