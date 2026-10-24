"""Filas: uma fila de prioridade por especialidade e o gerenciador do atendimento."""

from .fila_especialidade import FilaEspecialidade
from .gerenciador import GerenciadorFilas

__all__ = ["FilaEspecialidade", "GerenciadorFilas"]
