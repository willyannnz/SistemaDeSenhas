"""Cadastro de especialistas e autenticação do admin."""

import hashlib
import hmac
import os

from modelos import Especialista, Especialidade

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


ITERACOES_HASH = 100_000


def _gerar_hash(senha: str, salt: bytes) -> bytes:
    """Gera o hash da senha com o salt informado (pbkdf2_hmac, sha256)."""
    # .encode() transforma o texto em bytes, que é o que o hashlib aceita.
    # O pbkdf2_hmac mistura a senha com o salt e repete o processo ITERACOES_HASH vezes.
    return hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES_HASH)


class Administrador:
    """Conta do administrador. Guarda apenas o salt e o hash da senha (RNF06)."""

    def __init__(self, usuario: str, senha: str):
        """Levanta ValueError se usuário ou senha estiverem vazios."""
        usuario = usuario.strip()
        # Não usamos strip() na senha: espaço pode fazer parte dela e mudaria o hash.
        if not usuario or not senha:
            raise ValueError("Usuário e senha não podem ser vazios.")
        self.usuario = usuario
        # Salt: 16 bytes aleatórios, únicos para esta conta. Pode ficar guardado junto do hash.
        self._salt = os.urandom(16)
        # Guardamos só o hash. A senha em si nunca é salva em nenhum atributo (RNF06).
        self._hash = _gerar_hash(senha, self._salt)

    def autenticar(self, usuario: str, senha: str) -> bool:
        """RF09. Devolve True só se usuário e senha conferem."""
        usuario_ok = usuario.strip() == self.usuario
        # Refaz o hash da senha digitada com o MESMO salt guardado no cadastro.
        hash_digitado = _gerar_hash(senha, self._salt)
        # compare_digest compara sem vazar informação pelo tempo de resposta (o == vazaria).
        senha_ok = hmac.compare_digest(self._hash, hash_digitado)
        return usuario_ok and senha_ok