from src.nodo_lista import NodoLista


class Biblioteca:
    """
    Lista encadeada que armazena todas as músicas carregadas.
    Cada nó aponta para o próximo — sem arrays, sem índices nativos.
    """

    def __init__(self):
        self.head = None

    def adicionar_musica(self, musica):
        novo_nodo = NodoLista(musica)
        if self.head is None:
            self.head = novo_nodo
        else:
            atual = self.head
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_nodo

    def listar_musicas(self):
        if self.head is None:
            print("  Biblioteca vazia.")
            return
        atual = self.head
        while atual is not None:
            print(f"  [{atual.musica.id:>3}] {atual.musica}")
            atual = atual.proximo

    def buscar_por_id(self, id_buscado):
        atual = self.head
        while atual is not None:
            if atual.musica.id == id_buscado:
                return atual.musica
            atual = atual.proximo
        return None

    def listar_por_playlist(self, nome_playlist):
        """Retorna lista (Python list) de Musica de uma playlist específica."""
        resultado = []
        atual = self.head
        while atual is not None:
            if atual.musica.playlist.lower() == nome_playlist.lower():
                resultado.append(atual.musica)
            atual = atual.proximo
        return resultado

    def playlists_disponiveis(self):
        """Retorna conjunto de nomes de playlists sem duplicatas."""
        playlists = []
        vistas = set()
        atual = self.head
        while atual is not None:
            nome = atual.musica.playlist
            if nome not in vistas:
                playlists.append(nome)
                vistas.add(nome)
            atual = atual.proximo
        return playlists

    def esta_vazia(self):
        return self.head is None

    def total_musicas(self):
        count = 0
        atual = self.head
        while atual is not None:
            count += 1
            atual = atual.proximo
        return count
