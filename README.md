# Sistema de Senhas para Clínica Médica

Sistema acadêmico em Python para organizar a fila de atendimento de uma clínica médica por especialidade e prioridade. O projeto está sendo desenvolvido passo a passo pelos integrantes do grupo, com foco em modularização e no uso de estruturas de dados.

> **Estado atual:** os modelos, o cadastro de especialistas (com a autenticação do administrador) e as filas por especialidade estão implementados. O painel, a persistência, o relatório, a interface gráfica e a integração pelo `main.py` ainda serão desenvolvidos.

## Objetivos

- Emitir senhas normais e prioritárias para cada especialidade.
- Organizar as senhas por prioridade e ordem de chegada.
- Permitir que especialistas chamem pacientes para seus consultórios.
- Exibir informações da chamada e uma estimativa de espera.
- Registrar os atendimentos do dia em SQLite e gerar um relatório diário.

## Especialidades e prioridades

As especialidades previstas são Clínica Geral, Pediatria, Ginecologia e Cardiologia.

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
| `clinica/filas/` | Emissão, ordenação e chamada de senhas, encerramento diário e estimativa de espera | Implementado; a prioridade estrita depende da professora |
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
- A fórmula de espera e alguns detalhes de encerramento diário continuam como propostas a validar.

## Como executar

O fluxo completo da aplicação ainda não está pronto. As instruções de execução serão adicionadas quando a integração pelo `main.py` estiver concluída.

## Grupo

- Willyan
- Luana Felix Ribeiro
- Iago de Castro Sarmento
- Bruna Stéfany

## Documentação do projeto

O Notion contém a versão de referência dos requisitos. O histórico de decisões e etapas fica na nota `Projetos/Sistema-Senhas-Clinica.md` do Obsidian.
