# Validação no Google Colab

**Pendente: não executado no serviço nesta revisão.** Execução local não comprova o frontend/runtime do Colab.

1. Abra o master em uma sessão nova CPU com Python compatível com as dependências.
2. Use o SHA da revisão publicada na URL do notebook e em `REPO_REF`.
3. Execute o bootstrap e registre SHA resolvido, origem do Meridian e versões. Se necessário, reinicie a sessão depois da instalação e execute desde o início.
4. Use **Executar tudo**. Confirme os capítulos 00–07 sem erros e o ZIP gerado.
5. Execute `!python scripts/validate_artifacts.py` no diretório do projeto.
6. Guarde notebook executado, ZIP, data UTC, runtime, versões e log/gate. Validação dos modulares no serviço deve ser registrada individualmente, se realizada.

Critério de encerramento: Run all do master no serviço, versão identificada e todos os capítulos/gates concluídos. Nove notebooks no repositório significam oito modulares e um master, não nove capítulos.
