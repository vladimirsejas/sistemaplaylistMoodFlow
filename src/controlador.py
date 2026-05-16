import random
import threading
from src.biblioteca import Biblioteca
from src.fila import Fila
from src.youtube_api import buscar_musica, tocar_musica, parar_musica
from src.musica import Musica

TERMOS_HUMOR = {
    "relaxar": [
        "lofi chill beats",
        "jazz relax instrumental",
        "acoustic calm songs",
        "ambient music relaxing",
        "bossa nova suave",
        "piano relaxante",
        "soft indie folk",
        "musica para dormir calma",
    ],
    "focar": [
        "lofi study beats",
        "deep focus music",
        "instrumental concentration",
        "classical music focus",
        "ambient work music",
        "musica para estudar",
        "post rock instrumental",
        "electronic focus playlist",
    ],
    "animar": [
        "funk hits brasil",
        "pop hits 2024",
        "samba animado",
        "pagode festa",
        "rock energetico",
        "eletronico dancante",
        "hip hop hype",
        "forro animado",
    ],
}


class Controlador:

    def __init__(self):
        self.biblioteca = Biblioteca()
        self.fila_relaxar = Fila("Relaxar")
        self.fila_focar = Fila("Focar")
        self.fila_animar = Fila("Animar")
        self.historico = Fila("Historico")
        self._humor_ativo = None
        self._reproducao_continua = False
        self._thread_continua = None

    def buscar_especifica(self):
        query = input("\nNome da musica (ou artista + musica): ").strip()
        if not query:
            return
        print("Buscando...")
        resultados = buscar_musica(query, limite=8)
        if not resultados:
            print("Nenhuma musica encontrada.")
            return
        print("\nResultados:")
        for i, item in enumerate(resultados):
            print(f"  [{i}] {item['titulo']} - {item['artista']}  ({item['duracao']})")
        try:
            escolha = int(input("\nEscolha o numero: "))
            if escolha < 0 or escolha >= len(resultados):
                print("Opcao invalida.")
                return
        except ValueError:
            print("Entrada invalida.")
            return
        item = resultados[escolha]
        musica = self._criar_musica(item, humor="focar")
        self.biblioteca.adicionar_musica(musica)
        self._parar_continua()
        print(f"\nTocando: {musica.titulo} - {musica.artista}")
        tocar_musica(musica.video_id)
        self.historico.enqueue(musica)

    def buscar_artista(self):
        artista = input("\nNome do artista: ").strip()
        if not artista:
            return
        print(f"Buscando musicas de {artista}...")
        resultados = buscar_musica(artista, limite=10)
        if not resultados:
            print("Nenhuma musica encontrada.")
            return
        print(f"\nMusicas encontradas:")
        for i, item in enumerate(resultados):
            print(f"  [{i}] {item['titulo']}  ({item['duracao']})")
        print("\n  [1] Tocar uma musica especifica")
        print("  [2] Tocar todas em sequencia")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            try:
                escolha = int(input("Numero da musica: "))
                item = resultados[escolha]
                musica = self._criar_musica(item, humor="focar")
                self.biblioteca.adicionar_musica(musica)
                self._parar_continua()
                print(f"\nTocando: {musica.titulo}")
                tocar_musica(musica.video_id)
                self.historico.enqueue(musica)
            except (ValueError, IndexError):
                print("Opcao invalida.")
        elif opcao == "2":
            fila_temp = Fila("Artista")
            for item in resultados:
                musica = self._criar_musica(item, humor="focar")
                self.biblioteca.adicionar_musica(musica)
                fila_temp.enqueue(musica)
            print(f"\n{fila_temp.tamanho} musicas adicionadas. Iniciando reproducao...")
            self._iniciar_continua_fila(fila_temp)

    def gerar_playlist_humor(self, humor):
        print(f"\nGerando playlist '{humor}' automaticamente...")
        termos = TERMOS_HUMOR[humor]
        query = random.choice(termos)
        print(f"Buscando por: '{query}'")
        resultados = buscar_musica(query, limite=10)
        if not resultados:
            print("Nao foi possivel gerar a playlist agora. Tente novamente.")
            return
        random.shuffle(resultados)
        fila = Fila(humor.capitalize())
        for item in resultados:
            musica = self._criar_musica(item, humor=humor)
            self.biblioteca.adicionar_musica(musica)
            fila.enqueue(musica)
        if humor == "relaxar":
            self.fila_relaxar = fila
        elif humor == "focar":
            self.fila_focar = fila
        elif humor == "animar":
            self.fila_animar = fila
        print(f"\n{fila.tamanho} musicas prontas! Iniciando reproducao continua...")
        self._humor_ativo = humor
        self._iniciar_continua_fila(fila, humor=humor)

    def playlist_aleatoria(self):
        humor = random.choice(["relaxar", "focar", "animar"])
        print(f"\nHumor aleatorio sorteado: {humor.upper()}")
        self.gerar_playlist_humor(humor)

    def _iniciar_continua_fila(self, fila, humor=None):
        self._parar_continua()
        self._reproducao_continua = True
        self._thread_continua = threading.Thread(
            target=self._loop_reproducao,
            args=(fila, humor),
            daemon=True
        )
        self._thread_continua.start()

    def _loop_reproducao(self, fila, humor=None):
        import time
        while self._reproducao_continua:
            musica = fila.dequeue()
            if musica is None:
                if humor:
                    print(f"\nPlaylist '{humor}' acabou. Buscando mais musicas automaticamente...")
                    termos = TERMOS_HUMOR[humor]
                    query = random.choice(termos)
                    resultados = buscar_musica(query, limite=10)
                    if resultados:
                        random.shuffle(resultados)
                        for item in resultados:
                            m = self._criar_musica(item, humor=humor)
                            fila.enqueue(m)
                        continue
                break
            print(f"\n Tocando: {musica.titulo} - {musica.artista}")
            tocar_musica(musica.video_id)
            self.historico.enqueue(musica)
            time.sleep(3)
            try:
                import pygame
                while pygame.mixer.get_init() and pygame.mixer.music.get_busy() and self._reproducao_continua:
                    time.sleep(1)
            except Exception:
                time.sleep(180)
        print("\nReproducao encerrada.")

    def _parar_continua(self):
        self._reproducao_continua = False
        parar_musica()

    def ver_historico(self):
        self.historico.listar()

    def ver_biblioteca(self):
        self.biblioteca.listar_musicas()

    def parar(self):
        self._parar_continua()

    def _criar_musica(self, item, humor):
        return Musica(
            titulo=item['titulo'],
            artista=item['artista'],
            album="YouTube Music",
            humor=humor,
            duracao=item['duracao'],
            video_id=item['video_id']
        )