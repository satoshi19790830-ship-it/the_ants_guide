"""ページ内アンカー(#...)のリンク先が実在するか確認する。

見出しIDは markdown の toc 拡張が生成するため、見出し文言を変えるとアンカーが
静かに壊れる。索引を手で書いているページがあるので、ビルド後に必ず通す。
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

bad = []
checked = 0
for html in sorted(DOCS.rglob("*.html")):
    text = html.read_text(encoding="utf-8")
    ids = set(re.findall(r'\sid="([^"]+)"', text))
    for href in re.findall(r'href="#([^"]+)"', text):
        checked += 1
        if href not in ids:
            bad.append(f"{html.relative_to(DOCS)} -> #{href}")

print(f"ページ内アンカー {checked}件を確認")
print("\n".join(bad) if bad else "リンク切れなし")
