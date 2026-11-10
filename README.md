# Sistema de Senhas para Clínica Médica

Sistema acadêmico em Python para organizar a fila de atendimento de uma clínica médica por especialidade e prioridade. O projeto está sendo desenvolvido passo a passo pelos integrantes do grupo, com foco em modularização e no uso de estruturas de dados.

> **Estado atual:** os modelos, o cadastro de especialistas (com autenticação do administrador) e as filas por especialidade estão implementados. As filas separam senhas prioritárias e normais, permitem consultar a ordem de chamada e oferecem estimativas de espera. O painel, a persistência, o relatório, a interface gráfica e a integração do fluxo pelo `main.py` ainda estão em desenvolvimento.

## Objetivos

- Emitir senhas normais e prioritárias para cada especialidade.
- Organizar as senhas prioritárias por prioridade e ordem de chegada, mantendo as normais em ordem FIFO.
- Permitir que especialistas chamem pacientes para seus consultórios.
- Exibir informações da chamada e uma estimativa de espera.
- Registrar os atendimentos do dia em SQLite e gerar um relatório diário.

## Especialidades e prioridades

As especialidades disponíveis no modelo atual são Clínica Geral, Pediatria, Ginecologia, Cardiologia e Psiquiatria.

| Código | Prioridade |
| --- | --- |
| 1 | Idosos com 80 anos ou mais |
| 2 | Idosos de 60 a 79 anos |
| 3 | Pessoas com deficiência (PCD) |
| 4 | Gestantes |
| 5 | Pessoas obesas |
| 6 | Crianças no colo |
| 7 | Senha normal |

Os códigos 1 a 6 representam as prioridades previstas no projeto. O código 2 e a regra de prioridade estrita ainda precisam ser confirmados com a professora. O código 7 é uma escolha interna de implementação para posicionar senhas normais depois das prioritárias no heap.

## Tecnologias previstas

- Python 3.10 ou superior.
- `dataclasses` e `Enum` para os modelos.
- `heapq` para as filas de prioridade.
- `collections.deque` para manter as senhas normais em ordem FIFO.
- `sqlite3` para persistir os dados do dia.
- Tkinter para a interface gráfica, em etapa posterior.

As bibliotecas citadas fazem parte da biblioteca padrão do Python; não há dependências externas definidas até o momento.

## Organização dos módulos

O código fica no pacote `clinica/`, com uma pasta por módulo do enunciado. Cada pasta tem um `__init__.py` que indica o que os outros módulos podem usar, então quem importa não precisa saber em qual arquivo cada classe está. O `main.py` fica na raiz.

```
Clinica-SistemaSenhaPrioridade/
├── main.py
├── clinica/
│   ├── modelos/          enums.py, entidades.py
│   ├── especialistas/    cadastro.py, administrador.py
│   ├── filas/            fila_especialidade.py, gerenciador.py
│   ├── painel/           painel.py
│   ├── relatorio/        relatorio.py
│   └── interface/        interface gráfica (etapa posterior)
└── testes/
```

| Pasta | Responsabilidade | Estado |
| --- | --- | --- |
| `clinica/modelos/` | Especialidades, prioridades, estados, senhas e especialistas | Implementado |
| `clinica/especialistas/` | Cadastro de especialistas e autenticação do administrador | Implementado |
| `clinica/filas/` | Emissão e chamada de senhas, fila FIFO para senhas normais, heap para prioritárias, encerramento diário e estimativas de espera | Implementado; a prioridade estrita depende da professora |
| `clinica/painel/` | Preparação das informações para exibição | Planejado |
| `clinica/relatorio/` | Persistência em SQLite e geração do relatório diário | Planejado |
| `clinica/interface/` | Interface gráfica em Tkinter | Planejado, etapa posterior |
| `main.py` | Integração do fluxo da aplicação | Planejado |

Os módulos são importados a partir da raiz do projeto, por exemplo `from clinica.filas import GerenciadorFilas`. Os comandos devem ser executados na pasta raiz.

## Regras do projeto

- Cada especialidade pode ter até três especialistas; os consultórios vão de 1 a 12.
- Uma especialidade sem especialista cadastrado não deve emitir senhas.
- O tempo médio de atendimento usado na estimativa é de 30 minutos.
- A senha é diária: senhas não atendidas até o encerramento não passam para o dia seguinte.
- A clínica não realiza atendimentos de emergência.
- A prioridade estrita foi escolhida pelo grupo, mas ainda depende de confirmação da professora.
- A estimativa geral de espera considera o total de senhas aguardando, o tempo médio de atendimento de 30 minutos e a quantidade de consultórios ativos da especialidade.
- A estimativa por senha considera a quantidade de pessoas à frente multiplicada por 30 minutos. Ela ainda não considera a quantidade de consultórios ativos e deve ser tratada como uma estimativa inicial a validar.
- Alguns detalhes do encerramento diário também continuam como propostas a validar.

## Como executar

O fluxo completo da aplicação ainda não está pronto. As instruções de execução serão adicionadas quando a integração pelo `main.py` estiver concluída.

## Grupo

- Willyan
- Luana Felix Ribeiro
- Iago de Castro Sarmento
- Bruna Stéfany

