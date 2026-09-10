# Setup do graphify — troubleshooting de primeira instalação

Ler este arquivo só quando o comando `graphify` não for encontrado. Não é
necessário na maioria das invocações da skill — se o `graphify` já
responde normalmente, ignore este arquivo.

## Comando não encontrado logo após instalar

Instalação via `uv tool install graphifyy` ou `pipx install graphifyy` põe
o binário num diretório (`~/.local/bin`) que muitas vezes não está no
`PATH` do terminal recém-aberto. Isso não é indisponibilidade real do
graphify — é o shell ainda não ter sido atualizado.

Tentar, nesta ordem, antes de concluir que o graphify está indisponível:

1. `uv tool update-shell` (se instalado via `uv`) ou `pipx ensurepath` (se
   via `pipx`)
2. Abrir um terminal novo — a alteração de PATH só surte efeito em uma
   sessão de shell nova
3. Confirmar com `graphify --version`

## Se ainda assim não funcionar

Só então tratar como indisponibilidade genuína: seguir a regra do
SKILL.md — parar e avisar o usuário, sem fallback silencioso para leitura
manual do repositório.
