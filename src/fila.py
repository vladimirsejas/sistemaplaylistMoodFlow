from src.nodo_fila import NodoFila


class Fila:
    """
    Fila FIFO para controle de reprodução.
    Primeiro a entrar, primeiro a tocar.
    """

    def __init__(self, nome):
        self.nome = nome
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

    def dequeue(self):
        if self.esta_vazia():
            return None
        removida = self.inicio.musica
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        self.tamanho -= 1
        return removida

    def peek(self):
        """Retorna a próxima música sem removê-la."""
        if self.esta_vazia():
            return None
        return self.inicio.musica

    def listar(self):
        if self.esta_vazia():
            print(f"  Fila '{self.nome}' vazia.")
            return
        atual = self.inicio
        i = 1
        print(f"\n  Fila '{self.nome}' ({self.tamanho} músicas):")
        while atual is not None:
            print(f"    {i}. {atual.musica}")
            atual = atual.proximo
            i += 1

    def esta_vazia(self):
        return self.inicio is None
