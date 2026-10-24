"""Cadastro de especialistas e validação das regras de cadastro."""

from clinica.modelos import Especialidade, Especialista

LIMITE_POR_ESPECIALIDADE = 3  # Limite de especialistas por especialidade RN03
CONSULTORIOS = range(1, 13)  # Consultórios disponíveis de 1 a 12 RN07


class CadastroEspecialistas:
    """Guarda os especialistas e valida as regras de cadastro."""

    def __init__(self):
        self._especialistas: list[Especialista] = []

    def cadastrar(self, nome: str, especialidade: Especialidade, consultorio: int) -> Especialista:
        """RF01. Levanta ValueError se: nome vazio, consultório fora de 1-12,
        consultório já ocupado (RN07) ou especialidade já com 3 (RN03)."""
        nome = nome.strip()
        if not nome:
            raise ValueError("Nome do especialista não pode ser vazio.")
        if consultorio not in CONSULTORIOS:
            raise ValueError(f"Consultório {consultorio} inválido. Deve ser entre 1 e 12.")
        if any(e.consultorio == consultorio for e in self._especialistas):
            raise ValueError(f"Consultório {consultorio} já ocupado.")
        if self.consultorios_ativos(especialidade) >= LIMITE_POR_ESPECIALIDADE:
            raise ValueError(f"Limite de especialistas para {especialidade.value} atingido.")
        especialista = Especialista(nome=nome, especialidade=especialidade, consultorio=consultorio)
        self._especialistas.append(especialista)
        return especialista

    def listar(self, especialidade: Especialidade | None = None) -> list[Especialista]:
        """Devolve uma cópia da lista de especialistas, de todos ou só de uma especialidade."""
        if especialidade is None:
            return list(self._especialistas)
        return [e for e in self._especialistas if e.especialidade == especialidade]

    def buscar_por_consultorio(self, consultorio: int) -> Especialista | None:
        """RF08: é assim que o especialista 'seleciona o seu cadastro'."""
        for especialista in self._especialistas:
            if especialista.consultorio == consultorio:
                return especialista
        return None

    def tem_especialista(self, especialidade: Especialidade) -> bool:
        """RN06: só dá para retirar senha se for True."""
        return self.consultorios_ativos(especialidade) > 0

    def consultorios_ativos(self, especialidade: Especialidade) -> int:
        """RN05: usado no cálculo do tempo de espera."""
        return sum(1 for e in self._especialistas if e.especialidade == especialidade)
