"""Filas por especialidade: emissão, chamada e estimativa de espera."""
import heapq
import math
from datetime import datetime

from especialistas import CadastroEspecialistas
from modelos import Especialidade, Prioridade, Senha, StatusSenha

TEMPO_ATENDIMENTO_MIN = 30   # RN02


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


class GerenciadorFilas:
    """Uma fila por especialidade, mais as regras que dependem do cadastro."""

    def __init__(self, cadastro: CadastroEspecialistas):
        self._filas: dict[Especialidade, FilaEspecialidade] = {}
        self._atendimentos: dict[int, Senha] = {}  # consultório -> senha em atendimento
        self._cadastro = cadastro
        self._dia_encerrado = False

    def _verificar_dia_aberto(self) -> None:
        """Impede operações de fila depois do encerramento diário."""
        if self._dia_encerrado:
            raise ValueError("O dia foi encerrado; inicie um novo dia antes de continuar.")

    def emitir_senha(self, especialidade: Especialidade,
                     prioridade: Prioridade = Prioridade.NORMAL) -> Senha:
        """RN06: ValueError se a especialidade não tem especialista."""
        self._verificar_dia_aberto()
        if not self._cadastro.tem_especialista(especialidade):
            raise ValueError(f"Não há especialista cadastrado para {especialidade.value}.")
        if especialidade not in self._filas:
            self._filas[especialidade] = FilaEspecialidade(especialidade)
        return self._filas[especialidade].emitir(prioridade)

    def chamar_proxima(self, consultorio: int) -> Senha | None:
        """RF08. Marca EM_ATENDIMENTO, preenche hora_chamada, consultório e especialista.
        ValueError se o consultório não existe ou já tem atendimento aberto."""
        self._verificar_dia_aberto()
        especialista = self._cadastro.buscar_por_consultorio(consultorio)
        if especialista is None:
            raise ValueError(f"Consultório {consultorio} inválido.")
        if consultorio in self._atendimentos:
            raise ValueError(f"Consultório {consultorio} já tem atendimento aberto.")
        fila = self._filas.get(especialista.especialidade)
        if fila is None:
            return None
        senha = fila.proxima()
        if senha is None:
            return None

        senha.status = StatusSenha.EM_ATENDIMENTO
        senha.hora_chamada = datetime.now()
        senha.consultorio = consultorio
        senha.especialista = especialista
        self._atendimentos[consultorio] = senha
        return senha

    def finalizar_atendimento(self, consultorio: int) -> Senha:
        """Marca a senha do consultório como FINALIZADA."""
        if consultorio not in self._atendimentos:
            raise ValueError(f"Consultório {consultorio} não tem atendimento em andamento.")
        senha = self._atendimentos.pop(consultorio)
        senha.status = StatusSenha.FINALIZADA
        return senha

    def encerrar_dia(self) -> list[Senha]:
        """Encerra o dia e reinicia as filas.

        Finaliza os atendimentos que ainda estavam abertos (a senha já foi chamada,
        então conta como atendida) e marca como não atendidas as senhas que ainda
        aguardavam. Devolve todas elas, as finalizadas primeiro, para que o módulo de
        relatório registre cada uma de acordo com o status.
        """
        self._verificar_dia_aberto()

        encerradas = []
        for consultorio in list(self._atendimentos):  # list(...): o dict muda dentro do for
            encerradas.append(self.finalizar_atendimento(consultorio))

        for fila in self._filas.values():
            for senha in fila.encerrar():
                senha.status = StatusSenha.NAO_ATENDIDA
                encerradas.append(senha)

        self._filas.clear()
        self._dia_encerrado = True
        return encerradas

    def iniciar_novo_dia(self) -> None:
        """Reabre a emissão após encerrar o dia anterior."""
        if not self._dia_encerrado:
            raise ValueError("Encerre o dia atual antes de iniciar outro.")
        self._dia_encerrado = False

    def tempo_espera_estimado(self, especialidade: Especialidade) -> int | None:
        """RN05. Minutos estimados, ou None se não há consultório ativo."""
        self._verificar_dia_aberto()
        if not self._cadastro.tem_especialista(especialidade):
            return None
        fila = self._filas.get(especialidade)
        tamanho_fila = fila.tamanho() if fila else 0
        num_consultorios = self._cadastro.consultorios_ativos(especialidade)
        tempo_estimado = math.ceil((tamanho_fila * TEMPO_ATENDIMENTO_MIN) / num_consultorios)
        return tempo_estimado
