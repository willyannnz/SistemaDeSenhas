"""Enums do sistema: especialidades, prioridades e status das senhas."""

from enum import Enum


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
