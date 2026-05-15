from src.nodo_lista import NodoLista


class Biblioteca:

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
        print(f"'{musica.titulo}' adicionada na biblioteca!")

    def listar_musicas(self):
        if self.head is None:
            print("Biblioteca vazia.")
            return
        atual = self.head
        print("\nMusicas na biblioteca:")
        while atual is not None:
            print(f"  [{atual.musica.id}] {atual.musica}")
            atual = atual.proximo

    def buscar_por_id(self, id):
        atual = self.head
        while atual is not None:
            if atual.musica.id == id:
                return atual.musica
            atual = atual.proximo
        return None

    def remover_por_id(self, id):
        if self.head is None:
            print("Biblioteca vazia.")
            return
        if self.head.musica.id == id:
            removida = self.head.musica
            self.head = self.head.proximo
            print(f"'{removida.titulo}' removida da biblioteca.")
            return
        atual = self.head
        while atual.proximo is not None:
            if atual.proximo.musica.id == id:
                removida = atual.proximo.musica
                atual.proximo = atual.proximo.proximo
                print(f"'{removida.titulo}' removida da biblioteca.")
                return
            atual = atual.proximo
        print(f"Musica com ID {id} nao encontrada.")

    def esta_vazia(self):
        return self.head is None

    def total_musicas(self):
        count = 0
        atual = self.head
        while atual is not None:
            count += 1
            atual = atual.proximo
        return count