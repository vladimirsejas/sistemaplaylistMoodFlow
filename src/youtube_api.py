from ytmusicapi import YTMusic
import webbrowser

ytmusic = YTMusic()

def buscar_musica(query, limite=5):
    resultados = ytmusic.search(query, filter="songs", limit=limite)
    musicas = []
    for item in resultados:
        musica = {
            'titulo': item['title'],
            'artista': item['artists'][0]['name'],
            'video_id': item['videoId'],
            'duracao': item.get('duration', 'N/A')
        }
        musicas.append(musica)
    return musicas

def tocar_musica(video_id):
    url = f"https://music.youtube.com/watch?v={video_id}"
    webbrowser.open(url)