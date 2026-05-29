import threading
import time

from src.biblioteca import Biblioteca
from src.fila import Fila
from src.leitor import carregar_biblioteca_do_disco, recarregar_playlist
from src import player


class Controlador:

    def __init__(self, pasta_raiz):
        self.pasta_raiz = pasta_raiz
        self.biblioteca = Biblioteca()
        self.fila_atual = Fila("Em reprodução")
        self.historico = Fila("Histórico")

        self._reproducao_ativa = False
        self._thread_reproducao = None
        self._musica_atual = None

        print("\nCarregando sua biblioteca musical...")
        total = carregar_biblioteca_do_disco(pasta_raiz, self.biblioteca)
        if total == 0:
            print("  Nenhuma música encontrada. Verifique o caminho da pasta.")
        else:
            print(f"  {total} músicas carregadas de {len(self.biblioteca.playlists_disponiveis())} playlists.\n")

    # ─── Consultas ─────────────────────────────────────────────────────────────

    def listar_playlists(self):
        playlists = self.biblioteca.playlists_disponiveis()
        if not playlists:
            print("  Nenhuma playlist encontrada.")
            return []
        print("\n  PLAYLISTS DISPONÍVEIS")
        print("  " + "─" * 30)
        for i, nome in enumerate(playlists, 1):
            musicas = self.biblioteca.listar_por_playlist(nome)
            print(f"  {i:>2}. {nome:<20} ({len(musicas)} músicas)")
        return playlists

    def listar_musicas_da_playlist(self, nome_playlist):
        musicas = self.biblioteca.listar_por_playlist(nome_playlist)
        if not musicas:
            print(f"  Playlist '{nome_playlist}' está vazia.")
            return []
        print(f"\n  {nome_playlist.upper()}")
        print("  " + "─" * 30)
        for i, m in enumerate(musicas, 1):
            print(f"  {i:>3}. {m}")
        return musicas

    def ver_biblioteca_completa(self):
        total = self.biblioteca.total_musicas()
        print(f"\n  Biblioteca completa — {total} músicas:")
        print("  " + "─" * 30)
        self.biblioteca.listar_musicas()

    def ver_historico(self):
        print(f"\n  Histórico de reprodução ({self.historico.tamanho} músicas):")
        self.historico.listar()

    def ver_fila(self):
        print(f"\n  Fila atual ({self.fila_atual.tamanho} músicas):")
        self.fila_atual.listar()

    def musica_atual(self):
        if self._musica_atual:
            print(f"\n  ♪ Tocando agora: {self._musica_atual}")
        else:
            print("\n  Nenhuma música tocando no momento.")

    # ─── Reprodução ────────────────────────────────────────────────────────────

    def tocar_playlist(self, nome_playlist):
        musicas = self.biblioteca.listar_por_playlist(nome_playlist)
        if not musicas:
            print(f"  Playlist '{nome_playlist}' não encontrada ou vazia.")
            return
        self._parar_reproducao()
        self.fila_atual = Fila(nome_playlist)
        for m in musicas:
            self.fila_atual.enqueue(m)
        print(f"\n  {len(musicas)} músicas na fila. Iniciando '{nome_playlist}'...")
        self._iniciar_thread_reproducao()

    def tocar_musica_especifica(self, musica):
        self._parar_reproducao()
        self.fila_atual = Fila("Manual")
        self.fila_atual.enqueue(musica)
        self._iniciar_thread_reproducao()

    def adicionar_a_fila(self, musica):
        self.fila_atual.enqueue(musica)
        print(f"  '{musica}' adicionada à fila (posição {self.fila_atual.tamanho}).")
        if not self._reproducao_ativa:
            self._iniciar_thread_reproducao()

    def proxima_musica(self):
        if self._musica_atual is None:
            print("  Nenhuma música tocando.")
            return

        print(f"  Pulando: {self._musica_atual}")

        self.historico.enqueue(self._musica_atual)

        player.parar()

        time.sleep(1)

        proxima = self.fila_atual.dequeue()

        if proxima is None:
            print("  Não há próxima música na fila.")
            self._musica_atual = None
            return

        self._musica_atual = proxima

        print(f"\n  ♪ Tocando: {proxima}")

        player.tocar(proxima.caminho)

    def atualizar_biblioteca(self):
        import os
        total_novas = 0
        pasta_playlists = os.path.join(self.pasta_raiz, "playlist")
        if os.path.isdir(pasta_playlists):
            for nome_pasta in sorted(os.listdir(pasta_playlists)):
                caminho = os.path.join(pasta_playlists, nome_pasta)
                if os.path.isdir(caminho):
                    novas = recarregar_playlist(self.pasta_raiz, nome_pasta, self.biblioteca)
                    if novas > 0:
                        print(f"    + {novas} música(s) nova(s) em '{nome_pasta}'")
                        total_novas += novas
        if total_novas == 0:
            print("  Nenhuma música nova encontrada.")
        else:
            print(f"  Total: {total_novas} música(s) nova(s) adicionada(s) à biblioteca.")

    # ─── Internos ──────────────────────────────────────────────────────────────

    def _iniciar_thread_reproducao(self):
        self._reproducao_ativa = True
        self._thread_reproducao = threading.Thread(
            target=self._loop_reproducao,
            daemon=True
        )
        self._thread_reproducao.start()

    def _loop_reproducao(self):
        while self._reproducao_ativa:
            musica = self.fila_atual.dequeue()

            if musica is None:
                print("\n  Fila terminada.")
                self._reproducao_ativa = False
                self._musica_atual = None
                break

            self._musica_atual = musica

            print(f"\n  ♪ Tocando: {musica}")

            player.tocar(musica.caminho)

            # Dá tempo para o VLC abrir o arquivo
            time.sleep(8)

            # Se o VLC ainda não entrou em PLAYING,
            # aguarda mais alguns segundos.
            tentativas = 0

            while (
                self._reproducao_ativa
                and not player.esta_tocando()
                and tentativas < 15
            ):
                time.sleep(1)
                tentativas += 1

            # Agora espera terminar de verdade
            while (
                self._reproducao_ativa
                and player.esta_tocando()
            ):
                time.sleep(1)

            self.historico.enqueue(musica)

            if self._reproducao_ativa:
                time.sleep(1)

        self._musica_atual = None

    def _parar_reproducao(self):
        self._reproducao_ativa = False
        player.parar()
        time.sleep(0.5)