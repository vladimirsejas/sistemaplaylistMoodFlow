import os
import re
from src.musica import Musica

# Extensões de áudio e vídeo suportadas
EXTENSOES_SUPORTADAS = {
    ".mp3", ".mp4", ".m4a", ".wav", ".ogg",
    ".flac", ".aac", ".wma", ".mkv", ".webm"
}


def _limpar_titulo(nome_arquivo):
    """
    Tenta extrair um título limpo do nome do arquivo.
    Remove extensão, qualidades de vídeo, canais do YouTube etc.
    """
    # Remove extensão
    nome = os.path.splitext(nome_arquivo)[0]

    # Remove padrões comuns de downloads do YouTube
    padroes = [
        r'\(Official\s*Music\s*Video\)',
        r'\(Official\s*Video\)',
        r'\(Official\s*Audio\)',
        r'\(Lyrics?\)',
        r'\(Letra\)',
        r'\(Legendad[oa]\)',
        r'\(Ao\s*Vivo\)',
        r'\(Live[^)]*\)',
        r'\[\d{3,4}p[^\]]*\]',          # [480p, h264, youtube]
        r'\(\d{3,4}p[^)]*\)',            # (480p, youtube)
        r'- \w+VEVO',
        r'- \w+Channel',
        r'_h264.*$',
        r',\s*youtube\)',
        r'YTDown\.com_YouTube[-_]Culture[-_]Beat[-_]\w+',
    ]
    for padrao in padroes:
        nome = re.sub(padrao, '', nome, flags=re.IGNORECASE)

    # Substitui underscores por espaços
    nome = nome.replace('_', ' ')

    # Remove espaços duplos
    nome = re.sub(r'\s{2,}', ' ', nome).strip()

    # Remove traços soltos no final
    nome = nome.rstrip(' -').strip()

    return nome


def _extrair_artista_titulo(nome_limpo):
    """
    Tenta separar 'Artista - Título' ou 'Título - Artista'.
    Retorna (titulo, artista).
    """
    if ' - ' in nome_limpo:
        partes = nome_limpo.split(' - ', 1)
        artista = partes[0].strip()
        titulo = partes[1].strip()
        return titulo, artista
    return nome_limpo, ""


def carregar_biblioteca_do_disco(pasta_raiz, biblioteca):
    """
    Percorre pasta_raiz/playlist/<nome_playlist>/ e carrega todos os arquivos
    de música na biblioteca (lista encadeada).

    pasta_raiz: caminho para a pasta que contém 'playlist/'
    biblioteca : instância de Biblioteca

    Retorna número de músicas carregadas.
    """
    pasta_playlists = os.path.join(pasta_raiz, "playlist")

    if not os.path.isdir(pasta_playlists):
        print(f"[ERRO] Pasta não encontrada: {pasta_playlists}")
        return 0

    total = 0
    for nome_playlist in sorted(os.listdir(pasta_playlists)):
        caminho_playlist = os.path.join(pasta_playlists, nome_playlist)
        if not os.path.isdir(caminho_playlist):
            continue

        for arquivo in sorted(os.listdir(caminho_playlist)):
            ext = os.path.splitext(arquivo)[1].lower()
            if ext not in EXTENSOES_SUPORTADAS:
                continue

            caminho_completo = os.path.join(caminho_playlist, arquivo)
            nome_limpo = _limpar_titulo(arquivo)
            titulo, artista = _extrair_artista_titulo(nome_limpo)

            musica = Musica(
                titulo=titulo,
                artista=artista,
                caminho=caminho_completo,
                playlist=nome_playlist,
            )
            biblioteca.adicionar_musica(musica)
            total += 1

    return total


def recarregar_playlist(pasta_raiz, nome_playlist, biblioteca):
    """
    Verifica se há arquivos novos em uma playlist específica e os adiciona.
    Arquivos já cadastrados (mesmo caminho) são ignorados.
    Retorna número de músicas novas adicionadas.
    """
    caminho_playlist = os.path.join(pasta_raiz, "playlist", nome_playlist)
    if not os.path.isdir(caminho_playlist):
        print(f"[ERRO] Playlist '{nome_playlist}' não encontrada.")
        return 0

    # Coleta caminhos já registrados
    caminhos_existentes = set()
    atual = biblioteca.head
    while atual is not None:
        caminhos_existentes.add(atual.musica.caminho)
        atual = atual.proximo

    novas = 0
    for arquivo in sorted(os.listdir(caminho_playlist)):
        ext = os.path.splitext(arquivo)[1].lower()
        if ext not in EXTENSOES_SUPORTADAS:
            continue
        caminho_completo = os.path.join(caminho_playlist, arquivo)
        if caminho_completo in caminhos_existentes:
            continue
        nome_limpo = _limpar_titulo(arquivo)
        titulo, artista = _extrair_artista_titulo(nome_limpo)
        musica = Musica(
            titulo=titulo,
            artista=artista,
            caminho=caminho_completo,
            playlist=nome_playlist,
        )
        biblioteca.adicionar_musica(musica)
        novas += 1

    return novas
