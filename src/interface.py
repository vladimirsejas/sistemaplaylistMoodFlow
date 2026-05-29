from src.controlador import Controlador


class Interface:

    def __init__(self, pasta_raiz):
        self.controlador = Controlador(pasta_raiz)

    # ─── Menus ─────────────────────────────────────────────────────────────────

    def _menu_principal(self):
        print("\n" + "=" * 34)
        print("          🎵  MOOD FLOW")
        print("=" * 34)
        print("  1 - Playlists")
        print("  2 - Biblioteca completa")
        print("  3 - Fila atual")
        print("  4 - Histórico")
        print("  5 - O que está tocando?")
        print("  6 - Próxima música")
        print("  7 - Parar música")
        print("  8 - Atualizar biblioteca")
        print("  0 - Sair")
        print("=" * 34)

    def _menu_playlist(self, nome_playlist, musicas):
        print(f"\n  [{nome_playlist.upper()}]")
        print("  1 - Tocar playlist completa")
        print("  2 - Escolher uma música")
        print("  3 - Adicionar música à fila")
        print("  0 - Voltar")

    # ─── Fluxo principal ───────────────────────────────────────────────────────

    def executar(self):
        print("\n  Bem-vindo ao MoodFlow!")
        print("  O player da sua coleção musical.")

        while True:
            self._menu_principal()
            opcao = input("  > ").strip()

            if opcao == "1":
                self._tela_playlists()

            elif opcao == "2":
                self.controlador.ver_biblioteca_completa()

            elif opcao == "3":
                self.controlador.ver_fila()

            elif opcao == "4":
                self.controlador.ver_historico()

            elif opcao == "5":
                self.controlador.musica_atual()

            elif opcao == "6":
                self.controlador.proxima_musica()

            elif opcao == "7":
                self.controlador.parar()

            elif opcao == "8":
                print("\n  Verificando músicas novas nas pastas...")
                self.controlador.atualizar_biblioteca()

            elif opcao == "0":
                self.controlador.parar()
                print("\n  Até logo! 🎵\n")
                break

            else:
                print("\n  Opção inválida.")

    # ─── Tela de playlists ─────────────────────────────────────────────────────

    def _tela_playlists(self):
        playlists = self.controlador.listar_playlists()
        if not playlists:
            return

        entrada = input("\n  Número da playlist (ou Enter para voltar): ").strip()
        if not entrada:
            return
        try:
            idx = int(entrada) - 1
            if idx < 0 or idx >= len(playlists):
                print("  Número inválido.")
                return
            nome = playlists[idx]
        except ValueError:
            print("  Entrada inválida.")
            return

        self._tela_dentro_playlist(nome)

    def _tela_dentro_playlist(self, nome_playlist):
        musicas = self.controlador.listar_musicas_da_playlist(nome_playlist)
        if not musicas:
            return

        self._menu_playlist(nome_playlist, musicas)
        opcao = input("  > ").strip()

        if opcao == "1":
            self.controlador.tocar_playlist(nome_playlist)

        elif opcao == "2":
            self._escolher_musica(musicas, tocar_imediato=True)

        elif opcao == "3":
            self._escolher_musica(musicas, tocar_imediato=False)

        elif opcao == "0":
            return
        else:
            print("  Opção inválida.")

    def _escolher_musica(self, musicas, tocar_imediato):
        entrada = input("\n  Número da música: ").strip()
        try:
            idx = int(entrada) - 1
            if idx < 0 or idx >= len(musicas):
                print("  Número inválido.")
                return
            musica = musicas[idx]
        except ValueError:
            print("  Entrada inválida.")
            return

        if tocar_imediato:
            self.controlador.tocar_musica_especifica(musica)
        else:
            self.controlador.adicionar_a_fila(musica)
