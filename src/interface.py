from src.controlador import Controlador


class Interface:

    def __init__(self):

        self.controlador = Controlador()

    def exibir_menu(self):

        print("\n==============================")
        print("   Mood Flow Music Player")
        print("==============================")
        print("1 - Buscar musica no YouTube Music")
        print("2 - Ver biblioteca")
        print("3 - Montar playlists por humor")
        print("4 - Ver playlists")
        print("5 - Tocar playlist Relaxar")
        print("6 - Tocar playlist Focar")
        print("7 - Tocar playlist Animar")
        print("8 - Ver historico")
        print("0 - Sair")
        print("==============================")

    def executar(self):

        while True:

            self.exibir_menu()

            opcao = input("Escolha uma opcao: ")

            if opcao == "1":

                query = input("\nDigite o nome da musica: ")
                self.controlador.buscar_e_adicionar(query)

            elif opcao == "2":

                self.controlador.ver_biblioteca()

            elif opcao == "3":

                self.controlador.montar_playlists()

            elif opcao == "4":

                self.controlador.ver_playlists()

            elif opcao == "5":

                self.controlador.reproduzir_proximo("relaxar")

            elif opcao == "6":

                self.controlador.reproduzir_proximo("focar")

            elif opcao == "7":

                self.controlador.reproduzir_proximo("animar")

            elif opcao == "8":

                self.controlador.ver_historico()

            elif opcao == "0":

                print("\nEncerrando sistema...")
                break

            else:

                print("\nOpcao invalida.")