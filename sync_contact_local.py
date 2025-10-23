#!/usr/bin/env python3
import os, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONTACT = ROOT / "CONTACT.md"
START = "<!-- CONTACT-START -->"
END = "<!-- CONTACT-END -->"

# pastas a ignorar (ajuste se quiser)
EXCLUDE = {".git", ".github", "node_modules", "dist", "build", "target", ".venv", "venv", "__pycache__"}

if not CONTACT.exists():
    raise SystemExit("ERRO: CONTACT.md não encontrado na raiz do repositório.")

contact_md = CONTACT.read_text(encoding="utf-8").strip()
block = f"{START}\n\n{contact_md}\n\n{END}\n"
pattern = re.compile(re.escape(START) + r"[\s\S]*?" + re.escape(END), flags=re.MULTILINE)

def skip_path(p: pathlib.Path) -> bool:
    return any(part in EXCLUDE for part in p.parts)

updated = 0
for p in ROOT.rglob("*.md"):
    if p.name == "CONTACT.md":  # não mexe na fonte
        continue
    if skip_path(p):
        continue
    text = p.read_text(encoding="utf-8")
    new = pattern.sub(block, text)
    if new == text:  # não tinha bloco -> anexa no final
        new = text.rstrip() + "\n\n" + block
    if new != text:
        p.write_text(new, encoding="utf-8")
        updated += 1
        print("Atualizado:", p.relative_to(ROOT))

print(f"Concluído. Arquivos alterados: {updated}")
