#!/usr/bin/env python3
import os, re, sys, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTACT_PATH = REPO_ROOT / "CONTACT.md"

MARKER_START = "<!-- CONTACT-START -->"
MARKER_END = "<!-- CONTACT-END -->"

EXCLUDE_DIRS = {
    ".git", ".github", ".venv", "venv", "node_modules", "dist", "build",
    ".next", ".cache", ".vscode", ".idea", "__pycache__", "target"
}

def load_contact_md() -> str:
    if not CONTACT_PATH.exists():
        sys.exit("CONTACT.md não encontrado.")
    raw = CONTACT_PATH.read_text(encoding="utf-8").strip()
    # Sem o comentário inicial e título duplicado no rodapé
    # Mantemos o H2 e o conteúdo integral do CONTACT.md
    return raw

def iter_markdown_files():
    for root, dirs, files in os.walk(REPO_ROOT):
        # filtra pastas
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            p = pathlib.Path(root) / f
            # Não editar a própria fonte
            if p.resolve() == CONTACT_PATH.resolve():
                continue
            yield p

def ensure_trailing_newline(s: str) -> str:
    return s if s.endswith("\n") else s + "\n"

def main():
    contact_block = load_contact_md()
    block = f"{MARKER_START}\n<!-- atualize apenas CONTACT.md; este bloco é gerado automaticamente -->\n\n{contact_block}\n\n{MARKER_END}\n"

    changed = 0
    pattern = re.compile(rf"{re.escape(MARKER_START)}[\s\S]*?{re.escape(MARKER_END)}", flags=re.MULTILINE)

    for md in iter_markdown_files():
        text = md.read_text(encoding="utf-8")
        if pattern.search(text):
            new_text = pattern.sub(block, text)
        else:
            # anexa no final
            new_text = ensure_trailing_newline(text) + "\n" + block

        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"Atualizado: {md.relative_to(REPO_ROOT)}")

    print(f"\nConcluído. Arquivos alterados: {changed}")

if __name__ == "__main__":
    main()
