"""公開ディレクトリ(docs/)の内部リンクが全て実在するか確認する。"""
import re
from pathlib import Path

DOCS = Path(r"C:\Users\user\Desktop\個人用\自動化試作\the_ants_project\docs")

bad = set()
checked = 0
for html in DOCS.rglob("*.html"):
    text = html.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"#]+)"', text) + re.findall(r'src="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        checked += 1
        if not (html.parent / href).resolve().exists():
            bad.add(f"{html.relative_to(DOCS)} -> {href}")

print(f"内部リンク {checked}件を確認")
print("\n".join(sorted(bad)) if bad else "リンク切れなし")
