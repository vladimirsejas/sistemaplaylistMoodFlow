import os


class Musica:

    contador_id = 1

    def __init__(self, titulo, artista, caminho, playlist):
        self.id = Musica.contador_id
        Musica.contador_id += 1

        self.titulo = titulo
        self.artista = artista
        self.caminho = caminho      # caminho absoluto do arquivo
        self.playlist = playlist    # nome da pasta/playlist de origem
        self.extensao = os.path.splitext(caminho)[1].lower()

    def exibir_dados(self):
        print(f"ID       : {self.id}")
        print(f"Titulo   : {self.titulo}")
        print(f"Artista  : {self.artista}")
        print(f"Playlist : {self.playlist}")
        print(f"Arquivo  : {os.path.basename(self.caminho)}")

    def __str__(self):
        if self.artista and self.artista != self.titulo:
            return f"{self.titulo} - {self.artista}"
        return self.titulo
