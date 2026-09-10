#!/bin/bash
# PostToolUse hook do plugin laudo-tecnico.
#
# Reforça o "Gate de entrada (Definition of Ready)" da Fase 1.1
# (references/01-entendimento.md): assim que a tabela da 1.1 é salva em
# disco, conta quantos dos 6 itens vieram "não especificado". Se mais da
# metade, avisa via stderr — o write já aconteceu, então isto não bloqueia
# o arquivo, mas força uma mensagem que o Claude precisa considerar antes
# de seguir para 1.2, em vez de depender só da instrução em prosa.
#
# Só age quando o Write for exatamente para
# laudo-tecnico-output/01-entendimento.md — não interfere em outros writes.

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

TARGET="laudo-tecnico-output/01-entendimento.md"
case "$FILE_PATH" in
  *"$TARGET") ;;
  *) exit 0 ;;
esac

if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

TOTAL_ITENS=6
NAO_ESPECIFICADO=$(grep -oi "não especificado" "$FILE_PATH" | wc -l | tr -d ' ')

if [ "$NAO_ESPECIFICADO" -gt $((TOTAL_ITENS / 2)) ]; then
  {
    echo "Gate de entrada (Definition of Ready) da Fase 1.1: $NAO_ESPECIFICADO de $TOTAL_ITENS itens vieram \"não especificado\"."
    echo "Isso reprova o DoR (ver references/01-entendimento.md) — a demanda está majoritariamente sem especificação."
    echo "Antes de prosseguir para 1.2, liste ao usuário especificamente quais itens estão \"não especificado\" e peça esclarecimento — não seguir com um To-Be majoritariamente vazio."
  } >&2
  exit 2
fi

exit 0
