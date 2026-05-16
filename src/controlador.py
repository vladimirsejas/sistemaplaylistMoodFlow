from src.biblioteca import Biblioteca
from src.fila import Fila
from src.youtube_api import buscar_musica, tocar_musica
from src.musica import Musica

HUMORES_VALIDOS = ["relaxar", "focar", "animar"]


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

        try:
            escolha = int(input("\nEscolha o numero da musica: "))
            if escolha < 0 or escolha >= len(resultados):
                print("Opcao invalida.")
                return
        except ValueError:
            print("Entrada invalida.")
            return

        item = resultados[escolha]

        # Usuário escolhe o humor diretamente — sem BPM
        print("\nQual o clima dessa musica?")
        print("  [1] Relaxar  (musicas calmas, suaves)")
        print("  [2] Focar    (musicas moderadas, concentracao)")
        print("  [3] Animar   (musicas agitadas, energia)")

        opcao_humor = input("Escolha: ").strip()
        mapa = {"1": "relaxar", "2": "focar", "3": "animar"}

        humor = mapa.get(opcao_humor)
        if humor is None:
            print("Humor invalido. Musica nao adicionada.")
            return

        musica = Musica(
            titulo=item['titulo'],
            artista=item['artista'],
            album="YouTube Music",
            humor=humor,
            duracao=item['duracao'],
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
            if musica.humor == "relaxar":
                self.fila_relaxar.enqueue(musica)
            elif musica.humor == "focar":
                self.fila_focar.enqueue(musica)
            elif musica.humor == "animar":
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