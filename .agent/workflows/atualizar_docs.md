---
description: Atualizar arquivos de documentação técnica do File2MD de forma direta, sem precisar passar pelo fluxo de issue ou PR
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/atualizar_docs]`, o agente DEVE iniciar sua resposta com: *"Protocolo Atualizador de Docs ativado."*. Em seguida, DEVE criar ou atualizar o arquivo `.agent/task.md` listando estas etapas como pendentes `[ ]`.

# Atualizador de Documentação

> **Nota:** Este workflow executa as mesmas regras da skill `@doc-updater`, adaptadas para uso direto sem fluxo de issue/PR. Para atualizações dentro de um fluxo de implementação, use `@[/implementar_issue]` (que aciona `@doc-updater` em modo orquestrado).

Siga este workflow quando precisar atualizar a documentação técnica no repositório diretamente, sem estar no fluxo de uma issue ou PR.

## Regras Gerais
- **NUNCA** reescreva o `README.md` integralmente se não for solicitado explicitamente.
- **SEMPRE** leia o conteúdo atual do arquivo antes de editá-lo.
- Em modo standalone (invocado diretamente pelo usuário), **aguarde aprovação expressa** antes de salvar as alterações.

---

## 0. Identificação do Escopo

Antes de qualquer edição, mapeue claramente o que mudou no código e onde deve ser documentado:

Use a tabela de referência:

| O que mudou | Onde documentar no README.md |
|---|---|
| Novo parâmetro CLI ou flag | Tabela de "Referência de Parâmetros" e seção de exemplos de linha de comando |
| Nova funcionalidade de menu (TUI) | Bullet correspondente na seção "Modo Menu Interativo" |
| Novo formato de arquivo suportado | Tabela de "Formatos Suportados" |
| Nova dependência ou biblioteca | Seção de "Instalação" e `requirements.txt` |
| Procedimento de execução/configuração de IA | Seção de "Inteligência e Configuração" ou "Como Executar" |

---

## 1. Leitura Obrigatória

**Para cada arquivo de documentação identificado no passo 0 (geralmente README.md):**
1. Leia o conteúdo atual completo do arquivo.
2. Localize a seção-alvo dentro do arquivo.
3. Confirme que a informação ainda não está documentada (evitar duplicação).

**Proibido:** editar sem ler antes.

---

## 2. Rascunho das Alterações

Produza o rascunho de cada alteração de forma cirúrgica:
- Indique: arquivo → seção → tipo de mudança (adicionar, substituir, remover).
- Mostre o conteúdo antes e depois quando relevante.

---

## 3. Barreira de Aprovação (Hard Stop)

PAUSE a execução. Apresente o rascunho completo das alterações propostas e **aguarde** a autorização explícita do usuário (ex: "Aprovado", "Pode aplicar", "Prosseguir").

- **PROIBIDO:** Executar o passo 4 sem ter recebido a mensagem do usuário autorizando.

---

## 4. Aplicação das Alterações

Após a aprovação, aplique as alterações de forma cirúrgica em cada arquivo usando edição por bloco (não reescrita total).

---

## 5. Verificação Pós-Atualização

Confira para cada arquivo editado:
- [ ] Nomes de arquivos, funções e parâmetros mencionados existem no projeto?
- [ ] Comandos documentados estão corretos e executáveis no terminal?
- [ ] Não houve duplicação de seções?
- [ ] Edição foi cirúrgica (sem alterar partes não relacionadas)?
- [ ] A codificação foi preservada em **UTF-8 sem BOM** (sem caracteres corrompidos em acentos)?

---

## 6. Relatório Final

Apresente ao usuário:
- Lista de seções modificadas no `README.md`.
- Resultado da verificação pós-atualização.
- Lacunas documentais identificadas mas fora do escopo desta atualização (se houver).
