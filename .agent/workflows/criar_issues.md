---
description: Criar e gerenciar issues no GitHub usando planejamento e MCP
---

> [!IMPORTANT]
> **MODO ESTRITO**: Ao ser invocado por `@[/criar_issues]`, o agente DEVE iniciar sua resposta com: *"Protocolo Criador de Issues ativado."*. Em seguida, DEVE criar ou atualizar o arquivo `.agent/task.md` listando estas etapas como pendentes `[ ]`.

# Gerenciador de Issues do GitHub

Siga este workflow para criar novas issues no repositório, garantindo planejamento adequado e padronização.

## Regras de Integridade
- **NUNCA** avance para o passo 5 (criação) antes do passo 4 (aprovação).
- O protocolo só é válido se estiver documentado no `task.md`.

## 0. Classificação e Busca de Contexto (SoT)

**Classificação da demanda:**
- `feature`: nova funcionalidade ou melhoria visível ao usuário.
- `fix`: correção de bug ou regressão.
- `chore`: manutenção técnica, refatoração, dependências ou testes.

**Busca de Contexto (SoT):**
- O agente **DEVE** listar a pasta `.agent/plans/` para verificar se existe um documento de planejamento relacionado à demanda.
- Caso um plano exista, ele deve ser lido integralmente e usado como a base primária para a criação das issues.

**Validação de Status do Plano:**
- O agente **DEVE** verificar o campo `Status` no cabeçalho do plano.
- Se `Status: Aprovado`: prossiga normalmente.
- Se `Status: Rascunho` ou `Em Revisão`: **PARE**. Informe ao usuário que o plano ainda não passou pela revisão crítica e sugira executar `@[/revisar_plano]` antes de gerar as issues.

---

## 1. Ler templates de issue (Leitura Obrigatória do Conteúdo)

O agente **DEVE abrir e ler o conteúdo** de cada arquivo `.yml` em `.github/ISSUE_TEMPLATE/` que seja relevante para os tipos de issue identificados no Passo 0.

**Procedimento obrigatório:**
1. Abrir o(s) arquivo(s) `.yml` correspondentes ao tipo (`feature_request.yml`, `chore.yml`, `bug_report.yml`).
2. Extrair a lista completa de campos (`id`, `label`, `required`) de cada template.
3. Montar um **mapa de campos por tipo** que será usado obrigatoriamente no Passo 3.

**Caso não existam templates no repositório ainda:**
- Utilize as definições estruturais padrões do GitHub em Markdown (Descrição, Contexto, Critérios de Aceite).

---

## 2. Planejamento e Decomposição
- **Com Plano Local:** Se um plano foi encontrado no Passo 0, o agente deve sugerir a **decomposição** do plano em múltiplas issues atômicas se o escopo for grande. Cada issue deve seguir o template adequado.
- **Sem Plano Local:**
    - Para `feature`, acione e utilize a skill `@feature-workflow` para planejar a solução detalhadamente.
    - Para `fix` e `chore`, sintetize um plano curto de conversão/lógica.

---

## 3. Formatação do rascunho e padronização de títulos

### 3.1. Título
Formule o título respeitando estas convenções:
- Para novas funcionalidades: prefixo `[FEATURE]`
- Para correção de bugs: prefixo `[FIX]`
- Para tarefas técnicas ou manutenção: prefixo `[CHORE]`

Diretrizes obrigatórias para o título:
- Seja conciso, claro e direto.
- Inicie a frase com verbo no infinitivo.
- Não utilize ponto final.

### 3.2. Corpo da Issue (Aderência Obrigatória ao Template)
O corpo da issue **DEVE** usar como esqueleto os campos extraídos no Passo 1. Cada campo do template `.yml` deve ser mapeado para uma seção markdown no corpo:

```markdown
### {label do campo}
{conteúdo preenchido a partir do plano/contexto}
```

### 3.3. Rastreabilidade Obrigatória
- Se um plano local foi utilizado, o corpo de **cada issue** DEVE incluir uma seção de referência **ao final**:
    ```markdown
    ### 📋 Plano de Referência
    Arquivo local: `.agent/plans/<nome_do_arquivo>.md`
    ```

---

## 4. Barreira de Aprovação (Hard Stop Obrigatório)

PAUSE a execução aqui. Apresente o rascunho completo da issue e **aguarde** a autorização explícita do usuário (ex: "Aprovado", "Pode criar", "Prosseguir").
- **PROIBIDO**: Executar o passo 5 sem ter recebido a autorização expressa do usuário.

---

## 5. Criação e Rastreabilidade

Após obter a aprovação final:
- A(s) issue(s) DEVE(M) ser criada(s) pelas ferramentas nativas do servidor GitHub via MCP.
- **PROIBIDO:** usar terminal, scripts de linha de comando ou a CLI do GitHub (`gh`) para criar a issue quando o MCP estiver disponível.
- **Rastreabilidade Automática:** Após a criação, o agente **DEVE**:
    1. Obter o(s) número(s) da(s) issue(s) gerada(s).
    2. **Renomear** o arquivo original em `.agent/plans/` para incluir os números (ex: `MeuPlano.md` → `MeuPlano_#40_#41.md`).
       - **Procedimento de rename:** Use a ferramenta **local** de criação de arquivo para salvar com o novo nome e depois delete o arquivo antigo.
    3. Atualizar o corpo das issues no GitHub com o novo nome do arquivo de referência (na seção `📋 Plano de Referência`) via MCP (`issue_write/update`).
    4. Confirmar que **cada issue criada** contém a seção de referência correta.