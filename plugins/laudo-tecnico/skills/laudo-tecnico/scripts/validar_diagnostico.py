#!/usr/bin/env python3
"""
Valida se um diagnóstico consolidado da skill laudo-tecnico contém todas as
seções esperadas, dado quais fases foram executadas — e, para as seções
com tabela de rótulos fixos (Demanda, As-Is/To-Be/Gap, Arquitetura,
Production Readiness, RAID, Business Case, TCO, EAP), se cada item/linha
esperado também está presente, não só o cabeçalho da seção.

A Fase 1 (Entendimento) e a Fase 4 (Planejamento/EAP) são sempre
obrigatórias e não precisam de flag — a EAP é o "por onde começar" que a
skill sempre entrega, mesmo quando o objetivo original era só diagnóstico.
A EAP também precisa rastrear a um item do Gap (Fase 1.2); isso é checado
como parte dos marcadores obrigatórios da seção.

Checagem determinística de texto — não depende do modelo "lembrar" de
incluir cada seção ou cada item dentro dela. Uso:

    python scripts/validar_diagnostico.py <caminho_do_diagnostico.md> \
        [--fase2] [--fase3]

Passe --fase2 e/ou --fase3 apenas para as fases que de fato foram
executadas nesta invocação da skill.

Saída: lista de seções e marcadores internos encontrados/faltando. Código
de saída 0 se tudo obrigatório está presente; 1 caso contrário.
"""

import argparse
import re
import sys

# Cada entrada: (regex do cabeçalho, rótulo legível, fase que a exige)
# fase_exigida em {1, 4}: sempre obrigatória, independente de flags.
SECTIONS = [
    (r"^#\s+Diagn[oó]stico:", "Título do diagnóstico", 1),
    (r"^##\s+Demanda \(To-Be\)", "Demanda (To-Be) — Fase 1.1", 1),
    (r"^##\s+As-Is", "As-Is — Estado atual do repositório — Fase 1.2", 1),
    (r"^##\s+Arquitetura", "Arquitetura (C4) — Fase 1.3", 1),
    (r"^##\s+Production Readiness", "Production Readiness — Fase 2.1", 2),
    (r"^##\s+RAID", "RAID — Riscos e Dependências — Fase 2.2", 2),
    (r"^##\s+Business Case", "Business Case — Fase 3.1", 3),
    (r"^##\s+TCO", "TCO — Custo — Fase 3.2", 3),
    (r"^##\s+EAP", "EAP — Estrutura Analítica de Projeto — Fase 4.1", 4),
]

SEMPRE_OBRIGATORIAS = {1, 4}

# Seções com estrutura interna fixa e obrigatória: (regex do cabeçalho da
# seção, lista de marcadores que devem aparecer no CONTEÚDO da seção,
# rótulo, fase que a exige). O conteúdo é tudo entre este cabeçalho e o
# próximo cabeçalho de mesmo nível (## ) ou superior (# ).
SUBSECTION_MARKERS = [
    (
        r"^##\s+Demanda \(To-Be\)",
        ["Entregável", "Escopo", "Prazos", "Critérios de aceite",
         "Responsáveis", "Existente vs pendente"],
        "6 itens da tabela Demanda — Fase 1.1",
        1,
    ),
    (
        r"^##\s+As-Is",
        ["As-Is", "To-Be", "Gap"],
        "colunas As-Is / To-Be / Gap — Fase 1.2",
        1,
    ),
    (
        r"^##\s+Arquitetura",
        ["Context", "Container", "Fluxo de dados", "Configuração",
         "Lógica similar"],
        "5 itens da tabela Arquitetura — Fase 1.3",
        1,
    ),
    (
        r"^##\s+Production Readiness",
        ["Estágio atual", "Promoção", "Dependências de infraestrutura",
         "Gates", "Observabilidade"],
        "5 itens da tabela Production Readiness — Fase 2.1",
        2,
    ),
    (
        r"^##\s+RAID",
        ["Risks", "Assumptions", "Issues", "Dependencies"],
        "4 categorias RAID — Fase 2.2",
        2,
    ),
    (
        r"^##\s+Business Case",
        ["Problema/oportunidade", "Custo de não agir", "Métricas de sucesso"],
        "3 itens da tabela Business Case — Fase 3.1",
        3,
    ),
    (
        r"^##\s+TCO",
        ["Serviços e cobrança", "Volume de dados", "Custo de implementação",
         "Custo operacional"],
        "4 itens da tabela TCO — Fase 3.2",
        3,
    ),
    (
        r"^##\s+EAP",
        ["Pacote de trabalho", "Origem", "Pré-requisitos",
         "Critério de conclusão", "Bloqueado por"],
        "6 colunas da tabela EAP — Fase 4.1",
        4,
    ),
]

# Marcador extra de rastreabilidade exigido dentro do corpo da seção EAP
# (todo pacote de trabalho deve rastrear a um item do Gap/PRR/RAID).
EAP_HEADER_REGEX = r"^##\s+EAP"
EAP_RASTREABILIDADE_MARCADOR = "gap"


def extrair_blocos(linhas: list[str]) -> list[tuple[str, str]]:
    """Divide o documento em blocos (cabeçalho, conteúdo-até-o-próximo-cabeçalho)."""
    blocos = []
    cabecalho_atual = None
    corpo_atual: list[str] = []

    for linha in linhas:
        if re.match(r"^#{1,2}\s+", linha):
            if cabecalho_atual is not None:
                blocos.append((cabecalho_atual, "\n".join(corpo_atual)))
            cabecalho_atual = linha
            corpo_atual = []
        else:
            corpo_atual.append(linha)

    if cabecalho_atual is not None:
        blocos.append((cabecalho_atual, "\n".join(corpo_atual)))

    return blocos


def validar(caminho: str, fases_executadas: set[int]) -> bool:
    try:
        with open(caminho, encoding="utf-8") as f:
            conteudo = f.read()
    except FileNotFoundError:
        print(f"ERRO: arquivo não encontrado: {caminho}")
        return False

    linhas = conteudo.splitlines()
    blocos = extrair_blocos(linhas)
    ok = True

    print(f"Validando: {caminho}")
    print(f"Fases sempre obrigatórias: {sorted(SEMPRE_OBRIGATORIAS)}")
    print(f"Fases opcionais executadas: {sorted(fases_executadas - SEMPRE_OBRIGATORIAS) or 'nenhuma'}")
    print("-" * 60)
    print("Seções (nível: cabeçalho presente?)")

    for padrao, rotulo, fase_exigida in SECTIONS:
        obrigatoria = fase_exigida in SEMPRE_OBRIGATORIAS or fase_exigida in fases_executadas
        encontrada = any(re.match(padrao, linha) for linha in linhas)

        if obrigatoria and encontrada:
            print(f"[OK]     {rotulo}")
        elif obrigatoria and not encontrada:
            print(f"[FALTA]  {rotulo}  <- obrigatória, fase executada, seção ausente")
            ok = False
        elif not obrigatoria and encontrada:
            print(f"[EXTRA]  {rotulo}  (presente mesmo sem a fase ter sido marcada como executada)")
        else:
            print(f"[--]     {rotulo}  (fase não executada, seção não exigida)")

    print("-" * 60)
    print("Conteúdo interno (nível: marcadores obrigatórios dentro da seção)")

    for padrao, marcadores, rotulo, fase_exigida in SUBSECTION_MARKERS:
        obrigatoria = fase_exigida in SEMPRE_OBRIGATORIAS or fase_exigida in fases_executadas
        if not obrigatoria:
            print(f"[--]     {rotulo}  (fase não executada, checagem não exigida)")
            continue

        bloco_encontrado = next(
            (corpo for cabecalho, corpo in blocos if re.match(padrao, cabecalho)),
            None,
        )
        if bloco_encontrado is None:
            # Já reportado como seção FALTA acima — não duplicar erro aqui
            print(f"[--]     {rotulo}  (seção ausente — ver erro acima)")
            continue

        faltando = [m for m in marcadores if m.lower() not in bloco_encontrado.lower()]
        if not faltando:
            print(f"[OK]     {rotulo}")
        else:
            print(f"[FALTA]  {rotulo}  <- ausentes: {', '.join(faltando)}")
            ok = False

    # Rastreabilidade da EAP: todo diagnóstico precisa apontar pelo menos
    # um pacote de trabalho de volta a um item do Gap (Fase 1.2).
    bloco_eap = next(
        (corpo for cabecalho, corpo in blocos if re.match(EAP_HEADER_REGEX, cabecalho)),
        None,
    )
    if bloco_eap is not None:
        if EAP_RASTREABILIDADE_MARCADOR in bloco_eap.lower():
            print("[OK]     EAP rastreia a um item do Gap (Fase 1.2)")
        else:
            print("[FALTA]  EAP rastreia a um item do Gap (Fase 1.2)  <- coluna 'Origem' não menciona 'Gap'")
            ok = False

    print("-" * 60)
    print("RESULTADO: " + ("APROVADO — todas as seções e marcadores obrigatórios presentes" if ok
                            else "REPROVADO — completar os itens marcados [FALTA] antes de entregar"))
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida a estrutura de um diagnóstico laudo-tecnico.")
    parser.add_argument("caminho", help="Caminho do arquivo markdown do diagnóstico consolidado")
    parser.add_argument("--fase2", action="store_true", help="Fase 2 (Preparação para Produção/PRR/RAID) foi executada")
    parser.add_argument("--fase3", action="store_true", help="Fase 3 (Justificativa/Business Case/TCO) foi executada")
    args = parser.parse_args()

    fases = set(SEMPRE_OBRIGATORIAS)
    if args.fase2:
        fases.add(2)
    if args.fase3:
        fases.add(3)

    aprovado = validar(args.caminho, fases)
    return 0 if aprovado else 1


if __name__ == "__main__":
    sys.exit(main())
