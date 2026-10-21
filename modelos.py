"""Modelos do sistema de senhas da clínica: especialidades, prioridades, senhas e especialistas."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Especialidade(Enum):
    """Especialidades médicas disponíveis na clínica."""
    CLINICA_GERAL = "Clínica Geral"
    PEDIATRIA = "Pediatria"
    GINECOLOGIA = "Ginecologia"
    CARDIOLOGIA = "Cardiologia"


class Prioridade(Enum):
    """Prioridades de atendimento.

    O código numérico define a ordem de chamada: quanto menor, mais urgente.
    NORMAL (7) é a senha comum e perde para todas as prioritárias.
    """
    IDOSO_80 = 1
    IDOSO_60 = 2
    PCD = 3
    GESTANTE = 4
    OBESO = 5
    CRIANCA_COLO = 6
    NORMAL = 7


class StatusSenha(Enum):
    """Status de uma senha."""
    AGUARDANDO = "Aguardando"
    EM_ATENDIMENTO = "Em Atendimento"
    FINALIZADA = "Finalizada"
    NAO_ATENDIDA = "Não Atendida"


@dataclass
class Especialista:
    """Representa um especialista médico."""
    nome: str
    especialidade: Especialidade
    consultorio: int


@dataclass
class Senha:
    """Representa uma senha gerada para atendimento."""
    numero: int
    especialidade: Especialidade
    prioridade: Prioridade
    status: StatusSenha = StatusSenha.AGUARDANDO
    hora_geracao: datetime = field(default_factory=datetime.now)
    hora_chamada: Optional[datetime] = None
    consultorio: Optional[int] = None
    especialista: Optional[Especialista] = None
