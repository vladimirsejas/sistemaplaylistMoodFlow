from src.nodo_fila import NodoFila


class Fila:

    def __init__(self, humor):
        self.humor = humor
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def enqueue(self, musica):
        novo_nodo = NodoFila(musica)
        if self.fim is None:
            self.inicio = novo_nodo
            self.fim = novo_nodo
        else:
            self.fim.proximo = novo_nodo
            self.fim = novo_nodo
        self.tamanho += 1
        print(f"'{musica.titulo}' adicionada na fila {self.humor}.")

    def dequeue(self):
        if self.esta_vazia():
            print(f"Fila {self.humor} vazia.")
            return None
        removida = self.inicio.musica
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        self.tamanho -= 1
        return removida

    def listar(self):
        if self.esta_vazia():
            print(f"Fila {self.humor} vazia.")
            return
        atual = self.inicio
        print(f"\nFila {self.humor}:")
        while atual is not None:
            print(f"  {atual.musica}")
            atual = atual.proximo

    def esta_vazia(self):
        return self.inicio is None