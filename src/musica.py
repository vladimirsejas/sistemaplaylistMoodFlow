class Musica:

    contador_id = 1

    def __init__(
        self,
        titulo,
        artista,
        album,
        bpm,
        duracao,
        video_id,
        spotify_uri="",
        spotify_url=""
    ):

        self.id = Musica.contador_id
        Musica.contador_id += 1

        self.titulo = titulo
        self.artista = artista
        self.album = album

        self.bpm = bpm
        self.duracao = duracao

        self.video_id = video_id
        self.spotify_uri = spotify_uri
        self.spotify_url = spotify_url

    def exibir_dados(self):

        print(f"ID: {self.id}")
        print(f"Titulo: {self.titulo}")
        print(f"Artista: {self.artista}")
        print(f"Album: {self.album}")
        print(f"BPM: {self.bpm}")
        print(f"Duracao: {self.duracao}")
        print(f"Video ID: {self.video_id}")

    def __str__(self):

        return (
            f"{self.titulo} - "
            f"{self.artista} "
            f"({self.album})"
        )