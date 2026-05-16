class Musica:

    contador_id = 1

    def __init__(
        self,
        titulo,
        artista,
        album,
        humor,
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

        self.humor = humor  # "relaxar", "focar" ou "animar"
        self.duracao = duracao

        self.video_id = video_id
        self.spotify_uri = spotify_uri
        self.spotify_url = spotify_url

    def exibir_dados(self):

        print(f"ID: {self.id}")
        print(f"Titulo: {self.titulo}")
        print(f"Artista: {self.artista}")
        print(f"Album: {self.album}")
        print(f"Humor: {self.humor}")
        print(f"Duracao: {self.duracao}")
        print(f"Video ID: {self.video_id}")

    def __str__(self):

        return (
            f"{self.titulo} - "
            f"{self.artista} "
            f"[{self.humor}]"
        )