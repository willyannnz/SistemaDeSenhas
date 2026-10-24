"""Fila de uma única especialidade: heap de prioridade e numeração das senhas."""
import heapq

from clinica.modelos import Especialidade, Prioridade, Senha


class FilaEspecialidade:
    """Fila de uma especialidade: um heap e o contador de numeração (RN08)."""

    def __init__(self, especialidade: Especialidade):
        self.especialidade = especialidade
        self._heap: list[tuple[int, int, Senha]] = []  # heap de (prioridade, número, senha)
        self._contador = 0  # contador de numeração da fila

    def emitir(self, prioridade: Prioridade) -> Senha:
        """Cria a senha com o próximo número e coloca no heap (RF04 e RF05)."""
        self._contador += 1
        senha = Senha(
            numero=self._contador,
            especialidade=self.especialidade,
            prioridade=prioridade,
        )
        heapq.heappush(self._heap, (prioridade.value, senha.numero, senha))
        return senha

    def proxima(self) -> Senha | None:
        """Tira a senha de maior precedência; None se a fila estiver vazia."""
        if not self._heap:
            return None
        _, _, senha = heapq.heappop(self._heap)
        return senha

    def tamanho(self) -> int:
        """Quantas senhas aguardam."""
        return len(self._heap)

    def encerrar(self) -> list[Senha]:
        """Retira e devolve todas as senhas aguardando, em ordem de chamada."""
        senhas = []
        while self._heap:
            _, _, senha = heapq.heappop(self._heap)
            senhas.append(senha)
        return senhas
