import re

def clean_header(content: str) -> str:
    """Remove o cabeçalho YAML de forma robusta."""
    pattern = r'^---\s*[\r\n]+.*?[\r\n]+---\s*'
    return re.sub(pattern, '', content, count=1, flags=re.DOTALL | re.MULTILINE).lstrip()

def post_process_markdown(content: str, remove_header: bool = True) -> str:
    """Aplica limpezas adicionais ao Markdown."""
    if remove_header:
        content = clean_header(content)
    
    # Normalização de quebras de linha excessivas (máximo 2 seguidas)
    content = re.sub(r'(\r?\n){3,}', '\n\n', content)
    
    # Limpeza de espaços no final de cada linha
    content = "\n".join(line.rstrip() for line in content.splitlines())
    
    return content
