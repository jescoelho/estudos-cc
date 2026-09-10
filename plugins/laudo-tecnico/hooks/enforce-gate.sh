#!/bin/bash
# Stop hook do plugin laudo-tecnico.
#
# Reforça tecnicamente o "Gate de conclusão" do SKILL.md (passo 7): em vez
# de depender só da instrução em prosa "rode o script antes de apresentar",
# este hook roda automaticamente quando a sessão principal do Claude Code
# está prestes a encerrar, e BLOQUEIA o encerramento (exit 2) se o
# diagnóstico consolidado não passar na validação.
#
# Não interfere em sessões que não usaram esta skill — sai silenciosamente
# (exit 0) se o arquivo consolidado não existir.

set -euo pipefail

OUTPUT_DIR="laudo-tecnico-output"
DIAGNOSTICO="$OUTPUT_DIR/diagnostico-consolidado.md"

if [ ! -f "$DIAGNOSTICO" ]; then
  exit 0
fi

# Infere quais fases opcionais rodaram a partir dos arquivos intermediários
# persistidos (seção "Persistência" do SKILL.md) — não depende do modelo
# lembrar de informar isso corretamente.
FASE_FLAGS=()
[ -f "$OUTPUT_DIR/02-preparacao-producao.md" ] && FASE_FLAGS+=("--fase2")
[ -f "$OUTPUT_DIR/03-justificativa.md" ] && FASE_FLAGS+=("--fase3")

SCRIPT="${CLAUDE_PLUGIN_ROOT}/skills/laudo-tecnico/scripts/validar_diagnostico.py"

if ! RESULTADO=$(python3 "$SCRIPT" "$DIAGNOSTICO" "${FASE_FLAGS[@]}" 2>&1); then
  {
    echo "$RESULTADO"
    echo ""
    echo "O diagnóstico laudo-tecnico não passou no gate de conclusão."
    echo "Complete os itens marcados [FALTA] em $DIAGNOSTICO antes de finalizar."
  } >&2
  exit 2
fi

exit 0
