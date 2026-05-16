from ytmusicapi import YTMusic
import yt_dlp
import pygame
import tempfile
import os
import threading

ytmusic = YTMusic()

# Caminho do ffmpeg.exe na raiz do projeto
FFMPEG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ffmpeg.exe")

# Controle de reprodução
_reproduzindo = False
_thread_musica = None


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
    return musicas[:limite]  # garante que nunca passa do limite


def tocar_musica(video_id):
    global _reproduzindo, _thread_musica

    parar_musica()

    _reproduzindo = True
    _thread_musica = threading.Thread(target=_reproduzir, args=(video_id,), daemon=True)
    _thread_musica.start()


def _reproduzir(video_id):
    global _reproduzindo

    url = f"https://www.youtube.com/watch?v={video_id}"

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        caminho_audio = tmp.name

    opcoes_ydl = {
        'format': 'bestaudio/best',
        'outtmpl': caminho_audio,
        'quiet': True,
        'no_warnings': True,
        'ffmpeg_location': FFMPEG_PATH,   # <-- aponta pro ffmpeg.exe do projeto
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    print(f"Carregando audio... (ffmpeg: {FFMPEG_PATH})")

    try:
        with yt_dlp.YoutubeDL(opcoes_ydl) as ydl:
            ydl.download([url])

        if not os.path.exists(caminho_audio):
            caminho_audio = caminho_audio + ".mp3"

        pygame.mixer.init()
        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.play()

        print("Tocando! (pressione Enter para voltar ao menu)")

        while pygame.mixer.music.get_busy() and _reproduzindo:
            pygame.time.wait(500)

    except Exception as e:
        print(f"Erro ao reproduzir: {e}")
    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        for ext in ["", ".mp3"]:
            try:
                os.remove(caminho_audio.replace(".mp3", "") + ext)
            except Exception:
                pass
        _reproduzindo = False


def parar_musica():
    global _reproduzindo
    _reproduzindo = False
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass