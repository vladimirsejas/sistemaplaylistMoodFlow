from src.biblioteca import Biblioteca
from src.fila import Fila
from src.youtube_api import buscar_musica, tocar_musica
from src.musica import Musica


class Controlador:

    def __init__(self):
        self.biblioteca = Biblioteca()
        self.fila_relaxar = Fila("Relaxar")
        self.fila_focar = Fila("Focar")
        self.fila_animar = Fila("Animar")
        self.historico = Fila("Historico")

    def buscar_e_adicionar(self, query):
        resultados = buscar_musica(query, limite=5)

        if not resultados:
            print("Nenhuma musica encontrada.")
            return

        print("\nResultados encontrados:")
        for i, item in enumerate(resultados):
            print(f"  [{i}] {item['titulo']} - {item['artista']}")

        escolha = int(input("\nEscolha o numero da musica: "))
        item = resultados[escolha]

        bpm = int(input("Informe o BPM da musica (ou 0 se nao souber): "))

        musica = Musica(
            titulo=item['titulo'],
            artista=item['artista'],
            album="YouTube Music",
            bpm=bpm,
            duracao=item['duracao'],
            spotify_uri="",
            spotify_url="",
            video_id=item['video_id']
        )

        self.biblioteca.adicionar_musica(musica)

    def montar_playlists(self):
        if self.biblioteca.esta_vazia():
            print("Biblioteca vazia. Adicione musicas primeiro.")
            return

        self.fila_relaxar = Fila("Relaxar")
        self.fila_focar = Fila("Focar")
        self.fila_animar = Fila("Animar")

        atual = self.biblioteca.head
        while atual is not None:
            musica = atual.musica
            if musica.bpm <= 90:
                self.fila_relaxar.enqueue(musica)
            elif musica.bpm <= 130:
                self.fila_focar.enqueue(musica)
            else:
                self.fila_animar.enqueue(musica)
            atual = atual.proximo

        print("\nPlaylists montadas com sucesso!")
        print(f"  Relaxar : {self.fila_relaxar.tamanho} musica(s)")
        print(f"  Focar   : {self.fila_focar.tamanho} musica(s)")
        print(f"  Animar  : {self.fila_animar.tamanho} musica(s)")

    def reproduzir_proximo(self, humor):
        if humor == "relaxar":
            fila = self.fila_relaxar
        elif humor == "focar":
            fila = self.fila_focar
        elif humor == "animar":
            fila = self.fila_animar
        else:
            print("Humor invalido. Use: relaxar, focar ou animar.")
            return

        musica = fila.dequeue()
        if musica is None:
            return

        print(f"\nTocando: {musica}")
        tocar_musica(musica.video_id)
        self.historico.enqueue(musica)

    def ver_historico(self):
        self.historico.listar()

    def ver_biblioteca(self):
        self.biblioteca.listar_musicas()

    def ver_playlists(self):
        self.fila_relaxar.listar()
        self.fila_focar.listar()
        self.fila_animar.listar()