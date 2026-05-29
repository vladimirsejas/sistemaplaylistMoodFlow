"""
Módulo de reprodução de áudio local.
Usa python-vlc (suporta mp4, mp3, e praticamente tudo).
Fallback: abre com o player padrão do sistema.
"""

import os
import subprocess
import sys

_backend = None  # "vlc" ou "sistema"


def _detectar_backend():
    global _backend
    if _backend:
        return _backend

    # Tenta vlc
    try:
        import vlc  # noqa
        _backend = "vlc"
        return _backend
    except Exception:
        pass

    # Fallback: player do sistema
    _backend = "sistema"
    return _backend


# ─── Estado interno ────────────────────────────────────────────────────────────

_vlc_instance = None
_vlc_player = None


# ─── API pública ───────────────────────────────────────────────────────────────

def tocar(caminho):
    """Toca o arquivo de áudio/vídeo no caminho informado."""
    backend = _detectar_backend()

    if backend == "vlc":
        _tocar_vlc(caminho)
    else:
        _tocar_sistema(caminho)


def parar():
    """Para a reprodução atual."""
    backend = _detectar_backend()
    try:
        if backend == "vlc" and _vlc_player:
            _vlc_player.stop()
    except Exception:
        pass


def esta_tocando():
    """Retorna True se há áudio sendo reproduzido agora."""
    backend = _detectar_backend()
    try:
        if backend == "vlc" and _vlc_player:
            import vlc
            return _vlc_player.get_state() == vlc.State.Playing
    except Exception:
        pass
    return False


def aguardar_fim():
    """Bloqueia até a música atual terminar."""
    import time
    while esta_tocando():
        time.sleep(0.5)


# ─── Backends internos ─────────────────────────────────────────────────────────

def _tocar_vlc(caminho):
    global _vlc_instance, _vlc_player
    import vlc
    if _vlc_instance is None:
        _vlc_instance = vlc.Instance("--no-video")
    if _vlc_player:
        _vlc_player.stop()
    media = _vlc_instance.media_new(caminho)
    _vlc_player = _vlc_instance.media_player_new()
    _vlc_player.set_media(media)
    _vlc_player.play()


def _tocar_sistema(caminho):
    """Abre com o player padrão do sistema operacional."""
    try:
        if sys.platform == "win32":
            os.startfile(caminho)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", caminho])
        else:
            subprocess.Popen(["xdg-open", caminho])
    except Exception as e:
        print(f"  [sistema] Não foi possível abrir o arquivo: {e}")