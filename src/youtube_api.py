from ytmusicapi import YTMusic
import yt_dlp
import pygame
import tempfile
import os
import threading

ytmusic = YTMusic()

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
    return musicas


def tocar_musica(video_id):
    global _reproduzindo, _thread_musica

    # Para música anterior se estiver tocando
    parar_musica()

    _reproduzindo = True
    _thread_musica = threading.Thread(target=_reproduzir, args=(video_id,), daemon=True)
    _thread_musica.start()


def _reproduzir(video_id):
    global _reproduzindo

    url = f"https://www.youtube.com/watch?v={video_id}"

    # Cria arquivo temporário para o áudio
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        caminho_audio = tmp.name

    opcoes_ydl = {
        'format': 'bestaudio/best',
        'outtmpl': caminho_audio,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    print("Carregando audio...")

    try:
        with yt_dlp.YoutubeDL(opcoes_ydl) as ydl:
            ydl.download([url])

        # O yt-dlp adiciona .mp3 ao nome
        if not os.path.exists(caminho_audio):
            caminho_audio = caminho_audio + ".mp3"

        pygame.mixer.init()
        pygame.mixer.music.load(caminho_audio)
        pygame.mixer.music.play()

        print("Tocando! (pressione Enter para voltar ao menu)")

        # Aguarda até terminar ou ser parado
        while pygame.mixer.music.get_busy() and _reproduzindo:
            pygame.time.wait(500)

    except Exception as e:
        print(f"Erro ao reproduzir: {e}")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        # Remove arquivo temporário
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