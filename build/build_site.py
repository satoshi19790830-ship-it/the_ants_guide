"""The Ants 攻略サイト ビルドスクリプト。

content/ja/*.md (YAML frontmatter + Markdown本文) を読み込み、docs/ に静的HTMLを
書き出す。日本語のみの単一言語サイト（英語版は2026-09-06に廃止）。

使い方:
    python build_site.py
"""
import os
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT_DIR = ROOT / "docs"  # GitHub Pages の公開元（/docs）
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
ASSETS_IMAGES_DIR = ROOT / "assets" / "images"

# 公開先のURL（末尾スラッシュなし）。GitHub Pages のリポジトリ名が決まったら書き換える。
# 環境変数 ANTS_SITE_URL があればそちらを優先する。
SITE_URL = os.environ.get("ANTS_SITE_URL", "https://example.github.io/the-ants-guide").rstrip("/")

LANG = "ja"
FOOTER = "© The Ants 攻略プロジェクト（非公式・プレイヤー有志運営）"
UPDATED_LABEL = "最終更新"
SEARCH_PLACEHOLDER = "記事を検索…"
TOC_LABEL = "目次"
POPULAR_LABEL = "人気記事"
BREADCRUMB_HOME = "TOP"

# サイト全体で固定表示する人気記事ランキング（スラッグ順）
POPULAR_SLUGS = ["damage-calculation", "beginner-guide", "news"]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def slugify_unicode(value: str, separator: str) -> str:
    """日本語をそのまま残す見出しID。

    markdownのtoc拡張の既定のslugifyはASCII以外を捨てるため、日本語見出しが
    s6 / s6_1 のような連番IDになり、項目を並べ替えるとアンカーが壊れる。
    """
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[%s\s]+" % re.escape(separator), separator, value)


def parse_page(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(raw)
    if not m:
        raise ValueError(f"frontmatter missing: {path}")
    meta = yaml.safe_load(m.group(1)) or {}
    body_md = m.group(2)

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc"],
        extension_configs={"toc": {"slugify": slugify_unicode}},
    )
    html_body = md.convert(body_md)
    # toc拡張が生成する目次には最上位の<div class="toc">ラッパーが付くので中身だけ使う
    toc_html = md.toc
    heading_count = len(re.findall(r"<h[23]", html_body))

    meta["slug"] = path.stem
    meta["html"] = html_body
    want_toc = meta.get("toc", True) is not False
    meta["toc"] = toc_html if (want_toc and heading_count >= 2) else None
    return meta


def load_lang_pages(lang: str):
    pages = []
    lang_dir = CONTENT_DIR / lang
    if not lang_dir.exists():
        return pages
    for path in sorted(lang_dir.glob("*.md")):
        pages.append(parse_page(path))
    pages.sort(key=lambda p: (p.get("order", 999), p["slug"]))
    return pages


def build_nav(pages):
    nav = {}
    order_of_category = []
    for p in pages:
        cat = p.get("category", "General")
        if cat not in nav:
            nav[cat] = []
            order_of_category.append(cat)
        nav[cat].append(
            {"title": p["title"], "slug": p["slug"], "href": f"{p['slug']}.html"}
        )
    return [(cat, nav[cat]) for cat in order_of_category]


def build_popular(pages):
    by_slug = {p["slug"]: p for p in pages}
    items = []
    for slug in POPULAR_SLUGS:
        p = by_slug.get(slug)
        if p:
            items.append({"title": p["title"], "slug": slug, "href": f"{slug}.html"})
    return items


def page_url(slug: str) -> str:
    """公開URL。トップはディレクトリURL（/）を正とする。"""
    return f"{SITE_URL}/" if slug == "index" else f"{SITE_URL}/{slug}.html"


def write_sitemap(pages):
    """検索エンジンに全ページを伝える sitemap.xml を出力する。"""
    urls = []
    for page in pages:
        lastmod = page.get("updated") or date.today().isoformat()
        urls.append(
            f"  <url>\n"
            f"    <loc>{page_url(page['slug'])}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (OUTPUT_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")


def main():
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("base.html")

    pages = load_lang_pages(LANG)
    if not pages:
        raise SystemExit("[build] content/ja に記事がありません")

    nav = build_nav(pages)
    popular = build_popular(pages)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for page in pages:
        is_home = page["slug"] == "index"
        html = template.render(
            lang=LANG,
            title=page["title"],
            description=page.get("description", ""),
            content=page["html"],
            toc=page["toc"],
            toc_label=TOC_LABEL,
            updated=page.get("updated"),
            updated_label=UPDATED_LABEL,
            nav=nav,
            popular=popular,
            popular_label=POPULAR_LABEL,
            category=page.get("category", ""),
            is_home=is_home,
            breadcrumb_home=BREADCRUMB_HOME,
            search_placeholder=SEARCH_PLACEHOLDER,
            slug=page["slug"],
            home_href="index.html",
            footer_text=FOOTER,
            canonical_url=page_url(page["slug"]),
        )
        (OUTPUT_DIR / f"{page['slug']}.html").write_text(html, encoding="utf-8")
    print(f"[build] {len(pages)} pages -> {OUTPUT_DIR}")

    if ASSETS_IMAGES_DIR.exists():
        out_images_dir = OUTPUT_DIR / "images"
        if out_images_dir.exists():
            shutil.rmtree(out_images_dir)
        shutil.copytree(ASSETS_IMAGES_DIR, out_images_dir)
        print(f"[build] images: {len(list(out_images_dir.glob('*')))} files -> {out_images_dir}")

    write_sitemap(pages)
    (OUTPUT_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    # GitHub Pages の Jekyll 処理を無効化する
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print("[build] sitemap.xml / robots.txt / .nojekyll を出力")

    print("[build] done.")


if __name__ == "__main__":
    main()
