"""Modelos do sistema de senhas da clínica: especialidades, prioridades, senhas e especialistas."""

from .entidades import Especialista, Senha
from .enums import Especialidade, Prioridade, StatusSenha

__all__ = ["Especialidade", "Prioridade", "StatusSenha", "Especialista", "Senha"]
