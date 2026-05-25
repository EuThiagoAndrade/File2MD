<p align="center">
  <img alt="File2MD Logo" src=".assets/Logo_verde_borda.svg" width="400">
</p>

<p align="center">
  🇧🇷 <a href="README.md">Leia em Português</a> | 🇺🇸 <a href="README_en.md">Read in English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg?style=flat-square" alt="Python 3.7+">
  <a href="https://github.com/EuThiagoAndrade/File2MD/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License: MIT">
  </a>
  <a href="https://github.com/EuThiagoAndrade/File2MD/commits/main">
    <img src="https://img.shields.io/github/last-commit/EuThiagoAndrade/File2MD?style=flat-square" alt="Last Commit">
  </a>
  <a href="https://github.com/EuThiagoAndrade/File2MD/issues">
    <img src="https://img.shields.io/github/issues/EuThiagoAndrade/File2MD?style=flat-square" alt="Open Issues">
  </a>
  <a href="https://github.com/EuThiagoAndrade/File2MD/stargazers">
    <img src="https://img.shields.io/github/stars/EuThiagoAndrade/File2MD?style=flat-square" alt="Stars">
  </a>
</p>

# File2MD - Manual de Utilização

Este script é um "wrapper" em Python para a ferramenta **MarkItDown**, projetado para facilitar a conversão de diversos formatos de arquivos para Markdown de maneira rápida e organizada.

---

## Pré-requisitos

Para utilizar este script, você precisa de:
1.  **Python** instalado na sua máquina (versão 3.7+).
2.  **MarkItDown** e outras dependências.

### Instalação

Clone o repositório e instale as dependências:

```powershell
git clone https://github.com/EuThiagoAndrade/File2MD.git
cd File2MD
pip install -r requirements.txt
```

> [!TIP]
> **Descoberta Automática:** O script é inteligente! Ele tentará encontrar o MarkItDown sozinho no seu sistema ou em pastas `.venv` e `venv` próximas. Se não encontrar, ele solicitará o caminho na primeira execução e salvará a configuração para que você não precise digitar novamente.

---

## Como Executar

O script oferece dois modos principais de operação: **Menu Interativo** e **Linha de Comando (CLI)**.

### 1. Modo Menu Interativo (Recomendado)
Execute o script sem argumentos para abrir a interface visual:

```powershell
python Scripts/File2MD.py
```

**Funcionalidades do Menu:**
*   **Interface Visual**: Design inspirado em terminais modernos com navegação por setas (**↑** e **↓**).
*   **1. Converter Arquivo Único**: Suporte a URLs, PDFs, Office, Imagens, Áudio e mais.
*   **2. Converter Pasta em Lote**: Agora com **processamento paralelo (multi-threading)** para alta performance.
*   **3. Monitorar Pasta (Watcher Mode)**: O script vigia uma pasta e converte novos arquivos automaticamente.
*   **4. Converter do Clipboard**: Detecta caminhos ou URLs copiados na sua área de transferência.
*   **5. Preview Integrado**: Visualize o Markdown gerado diretamente no terminal com formatação rica.
*   **6. Configuração de IA**: Integre com OpenAI ou modelos locais para descrição de imagens e áudio.
*   **7. Limpeza de Metadados YAML**: Controle visual se os metadados serão removidos ou mantidos.
*   **8. Definir Pasta de Saída**: Configuração de pasta padrão para salvar os arquivos gerados.
*   **Idioma / Language**: Alternância dinâmica de idioma (Português e Inglês) no menu interativo com persistência automática.

---

### 2. Modo Linha de Comando (CLI)
Para uso rápido ou em automações.

| Comando | Descrição |
| :--- | :--- |
| `python Scripts/File2MD.py "arquivo.pdf"` | Converte o arquivo com limpeza de cabeçalho padrão. |
| `python Scripts/File2MD.py "C:\Pasta" -d` | Processamento paralelo em lote de uma pasta inteira. |
| `python Scripts/File2MD.py "C:\Entrada" --watch` | Inicia o monitoramento em tempo real (Watcher Mode). |
| `python Scripts/File2MD.py "doc.docx" --keep-header` | Converte mantendo os metadados originais. |

---

## Inteligência e Configuração

O script agora gerencia as configurações de forma dinâmica:

*   **Arquitetura Nativa**: Agora utiliza a API Python do MarkItDown diretamente para maior estabilidade.
*   **Configuração Avançada**: Salva chaves de IA e preferências no `file2md_config.json`.
*   **Correção de Caracteres (Encoding)**: Suporte robusto para Windows, corrigindo problemas com acentuação.
*   **Limpeza Inteligente 2.0**: Remove Front Matter, normaliza quebras de linha e remove espaços residuais.
*   **Multimodal**: Suporte para descrever imagens e transcrever áudio via integração com LLMs.
*   **Flexibilidade Total**: Se o script for movido para outra máquina ou diretório, ele saberá se reajustar.

---

## Referência de Parâmetros

Se você preferir não usar o menu e invocar o script diretamente via terminal, aqui estão todos os parâmetros disponíveis:

| Parâmetro | Descrição | Exemplo de Uso |
| :--- | :--- | :--- |
| `input` | (Posicional) O arquivo, pasta ou URL que você deseja converter. | `python Scripts/File2MD.py "doc.pdf"` |
| `-o`, `--output` | Especifica o nome ou caminho do arquivo de saída. | `python Scripts/File2MD.py "doc.pdf" -o "final.md"` |
| `-d`, `--directory` | Indica que o input é uma pasta e deve converter tudo nela. | `python Scripts/File2MD.py "C:\Docs" -d` |
| `--watch` | Inicia o monitoramento de uma pasta em tempo real. | `python Scripts/File2MD.py "C:\Docs" --watch` |
| `--keep-header` | Pula a limpeza automática e mantém o cabeçalho YAML original. | `python Scripts/File2MD.py "doc.pdf" --keep-header` |
| `-h`, `--help` | Mostra a ajuda oficial do script com todos os comandos. | `python Scripts/File2MD.py --help` |

---

## Contato / Contact

Tem alguma dúvida, sugestão ou precisa de ajuda?
- **Discussões gerais e ideias:** Acesse o [GitHub Discussions](https://github.com/EuThiagoAndrade/File2MD/discussions) do projeto.
- **Contato direto (E-mail):** [contato@euthiagoandrade.com.br](mailto:contato@euthiagoandrade.com.br)

<p align="center">
  <img src="https://img.shields.io/badge/Support-GitHub-black?style=flat-square" alt="Support">
  <img src="https://img.shields.io/badge/Contact-Email-blue?style=flat-square" alt="Email">
</p>
