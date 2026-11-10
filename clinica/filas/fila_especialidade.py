"""Fila de uma única especialidade: heap de prioridade, fila FIFO e numeração das senhas."""
import heapq
from collections import deque   # fila FIFO: entra no fim, sai do começo
from clinica.modelos import Especialidade, Prioridade, Senha


class FilaEspecialidade:
    """Fila de uma especialidade: um heap (prioritárias), um deque (normais) e o contador (RN08)."""

    def __init__(self, especialidade: Especialidade):
        self.especialidade = especialidade

        # Prioritárias: heap de tuplas (código da prioridade, número, senha).
        # O heapq devolve sempre a MENOR tupla, comparando campo a campo:
        self._heap: list[tuple[int, int, Senha]] = []

        self._contador = 0

        # Normais: FIFO puro. Não precisa de prioridade nem de desempate,
        self._normais = deque()

    def emitir(self, prioridade: Prioridade) -> Senha:
        """Cria a senha com o próximo número e a coloca na estrutura certa (RF04 e RF05)."""
        self._contador += 1
        senha = Senha(
            numero=self._contador,
            especialidade=self.especialidade,
            prioridade=prioridade,
        )
        if prioridade == Prioridade.NORMAL:
            self._normais.append(senha)      # entra no FIM da fila FIFO
        else:
            # Guardamos a tupla, não só a senha, para o heap saber ordenar.
            heapq.heappush(self._heap, (prioridade.value, senha.numero, senha))
        return senha                         

    def proxima(self) -> Senha | None:
        """Tira a próxima senha: prioritárias primeiro, depois as normais; None se vazia."""
        if self._heap:                       # 1º caso: há prioritárias
            _, _, senha = heapq.heappop(self._heap)   # "_" ignora os 2 primeiros campos da tupla
            return senha
        if self._normais:                    # 2º caso: só há normais
            return self._normais.popleft()   # tira do COMEÇO (a mais antiga)
        return None                          # 3º caso: nenhuma estrutura tem ninguém

    def tamanho(self) -> int:
        """Quantas senhas aguardam, somando as duas estruturas."""
        return len(self._heap) + len(self._normais)

    def encerrar(self) -> list[Senha]:
        """Retira e devolve todas as senhas aguardando, em ordem de chamada."""
        senhas = []
        while self._heap:                    # primeiro esvazia as prioritárias, da mais urgente...
            _, _, senha = heapq.heappop(self._heap)
            senhas.append(senha)
        while self._normais:                 # ...depois as normais, na ordem de chegada
            senhas.append(self._normais.popleft())
        return senhas
    
    def ordem_prevista(self) -> list[Senha]:
        """Senhas aguardando na ordem em que serão chamadas (sem remover nenhuma)."""
        prioritarias = [item[2] for item in sorted(self._heap)]
        return prioritarias + list(self._normais)
    
    def posicao(self, numero: int) -> int | None:
        """Quantas senhas estão à frente da senha com esse número; None se ela não está aguardando."""
        for indice, senha in enumerate(self.ordem_prevista()):
            if senha.numero == numero:
                return indice
        return None
