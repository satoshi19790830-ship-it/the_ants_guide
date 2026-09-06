"""公式フォーラムのRSSから最新情報を取得し、更新情報ページの元データを更新する。

情報源は The Ants 公式フォーラム（All Star Union 運営、Discourse製）。
ログイン不要でRSSが公開されているため、Facebook公式ページ（ログイン必須）より
機械的に扱いやすい。

ただし**アップデート告知については、公式サイトに日本語版の本文がある**ことが
2026-09-06に判明した（英語フォーラムから訳す必要はない）。

    一覧: https://theants.allstarunion.com/ja/news
    本文: https://theants.allstarunion.com/ja/news/<記事id>

記事idは一覧ページのSSRペイロード(__NUXT_DATA__)に入っている。ただし本文は
クライアント側で取得されるため、素のHTTP GETでは本文まで取れない
（本文APIは platform-sdkgateway.apps.allstarunion.com の
/sdk-gateway/web/website/notice/detail だが、パラメータ名が未特定）。
現状は本文だけブラウザで開いて読む運用にしている。
なお初回アクセスはCookie(valid=1)を立てて再読み込みさせる作りなので、
HTTPで叩くときはこのCookieを付ける。

    python scripts/fetch_news.py            # RSS取得 → data/news.json を更新
    python scripts/fetch_news.py --render   # data/news.json → content/ja/news.md を生成
    python scripts/fetch_news.py --all      # 取得と生成を続けて行う

日本語・英語の要約は自動生成しない。取得直後は summary_ja / summary_en が空のまま
「未要約」として残るので、そこをAI（または人）が埋めてから --render する。
公式の文面をそのまま転載しないための設計でもある。
"""
import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEWS_JSON = ROOT / "data" / "news.json"
CONTENT_DIR = ROOT / "content"

FORUM = "https://theantsforum.allstarunion.com"
FEEDS = [
    f"{FORUM}/latest.rss",
    f"{FORUM}/c/news-events/game-updates/60.rss",
    f"{FORUM}/c/news-events/5.rss",
]

# 攻略サイトに載せる価値があるカテゴリ。雑談・アライアンス募集・各言語別の
# 質問板は除外する。
KEEP_CATEGORIES = {
    "Information",
    "News and Events",
    "Events",
    "Game Updates",
    "Announcements",
}

# カテゴリが付き損ねている公式告知を拾うための保険（実際に "Forum Feedback" に
# 分類されたコラボ告知があった）。
KEEP_TITLE_PATTERNS = [
    re.compile(r"maintenance notice", re.I),
    re.compile(r"\bupdate\b", re.I),
    re.compile(r"\bseason\b", re.I),
    re.compile(r"the ants\s*[×x]\s*", re.I),
    re.compile(r"announcement", re.I),
]

# 公式アカウントが投げる「みんなはどう思う？」系の交流投稿。攻略情報ではないので落とす。
# 疑問符で終わる投稿はほぼこれに該当するが、告知系（KEEP_TITLE_PATTERNS）が
# 疑問形になっている場合は残す。
ENGAGEMENT = re.compile(r"[?？]\s*$")
# 交流投稿は末尾に日付や絵文字が付くことが多いので、判定前に剥がす
ENGAGEMENT_TAIL = re.compile(r"(\s*\([^)]*\d{4}\)|\s*\d{4}-\d{2}-\d{2}|[^\w?？)]+)\s*$")

# フォーラム上のプレゼント企画（「コメントにゲームIDを書いたら抽選で報酬」形式）。
# カテゴリは Events だが中身はゲーム内の更新ではないので、本文で判別して落とす。
# 「Unknown Event #N」「Cave Exploration is coming」等がこれに該当した。
GIVEAWAY_BODY = [
    re.compile(r"within\s+\d+\s+working\s+days", re.I),
    re.compile(r"\b(in-?game|game)\s*id\b", re.I),
    re.compile(r"mysterious reward", re.I),
]

# タイトル先頭に付く装飾絵文字を落とす
EMOJI_PREFIX = re.compile(r"^[^\w\[\(（]+")


def fetch(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (the-ants-guide news fetcher)"})
    try:
        return urllib.request.urlopen(req, timeout=30).read()
    except Exception as exc:  # フィードが1本落ちても他は処理する
        print(f"[warn] 取得失敗 {url}: {exc}")
        return None


def topic_id(link: str) -> str | None:
    m = re.search(r"/(\d+)(?:/\d+)?/?$", link)
    return m.group(1) if m else None


def wanted(title: str, categories: list[str], body: str = "") -> bool:
    if any(p.search(title) for p in KEEP_TITLE_PATTERNS):
        return True
    if ENGAGEMENT.search(ENGAGEMENT_TAIL.sub("", title.strip())):
        return False
    if any(p.search(body) for p in GIVEAWAY_BODY):
        return False
    return any(c in KEEP_CATEGORIES for c in categories)


def parse_feed(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    out = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        cats = [(c.text or "").strip() for c in item.findall("category")]
        body = item.findtext("description") or ""
        tid = topic_id(link)
        if not tid or not wanted(title, cats, body):
            continue
        pub = item.findtext("pubDate")
        date = parsedate_to_datetime(pub).astimezone(timezone.utc).date().isoformat() if pub else ""
        out.append(
            {
                "id": tid,
                "date": date,
                "title_en": EMOJI_PREFIX.sub("", title).strip(),
                "url": link,
                "category": cats[0] if cats else "",
            }
        )
    return out


def load_news() -> dict:
    if NEWS_JSON.exists():
        return json.loads(NEWS_JSON.read_text(encoding="utf-8"))
    return {"source": FORUM, "fetched_at": None, "items": []}


def cmd_fetch() -> int:
    data = load_news()
    known = {item["id"]: item for item in data["items"]}

    found: dict[str, dict] = {}
    for url in FEEDS:
        raw = fetch(url)
        if raw:
            for entry in parse_feed(raw):
                found.setdefault(entry["id"], entry)
    print(f"[fetch] 対象記事: {len(found)}件")

    added = 0
    for tid, entry in found.items():
        if tid in known:
            # 既存の要約は温存し、日付・URLだけ最新に合わせる
            known[tid].update({k: entry[k] for k in ("date", "url", "category")})
        else:
            known[tid] = {
                **entry,
                "title_ja": "",
                "summary_ja": "",
                "summary_en": "",
            }
            added += 1

    # news.json 側で "hidden": true を立てた項目は、再取得しても復活させない
    items = sorted(
        (i for i in known.values() if not i.get("hidden")),
        key=lambda i: (i["date"], i["id"]),
        reverse=True,
    )
    data["items"] = items
    data["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    NEWS_JSON.parent.mkdir(parents=True, exist_ok=True)
    NEWS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pending = [i for i in items if not i["summary_ja"]]
    print(f"[fetch] 新規: {added}件 / 全体: {len(items)}件 / 未要約: {len(pending)}件")
    for item in pending[:20]:
        print(f"  - [{item['date']}] {item['title_en']}")
    if pending:
        print("\n未要約の項目に title_ja / summary_ja / summary_en を書いてから --render すること。")
    return len(pending)


FRONTMATTER = {
    "ja": {
        "title": "最新情報",
        "description": "The Ants の公式アップデート・シーズン調整・コラボイベントの最新情報を、日付順にまとめています。",
        "category": "最新情報",
    },
    "en": {
        "title": "Latest News",
        "description": "Official The Ants updates, season adjustments and collaboration events, listed by date.",
        "category": "Latest News",
    },
}
INTRO = {
    "ja": (
        "公式フォーラムで発表された内容を、日付の新しい順にまとめています。"
        "各項目の見出しから公式の原文（英語）に飛べます。\n\n"
        "アップデート告知は公式サイトの日本語版（theants.allstarunion.com/ja/news）の"
        "表記に合わせています。フォーラムでしか発表されていない項目は、英語からの訳が混ざります。"
    ),
    "en": (
        "Announcements from the official forum, newest first. "
        "Each heading links to the original post."
    ),
}
SOURCE_NOTE = {
    "ja": f'<p class="source-note">出典: <a href="{FORUM}" rel="nofollow">The Ants 公式フォーラム</a>（All Star Union 運営）。本ページは公式発表の要約であり、原文の転載ではありません。</p>',
    "en": f'<p class="source-note">Source: <a href="{FORUM}" rel="nofollow">The Ants official forum</a> (run by All Star Union). This page summarises official announcements; it does not reproduce them.</p>',
}


def render_lang(lang: str, items: list[dict]) -> str:
    meta = FRONTMATTER[lang]
    latest = items[0]["date"] if items else datetime.now(timezone.utc).date().isoformat()
    lines = [
        "---",
        f"title: {meta['title']}",
        f"description: {meta['description']}",
        f"category: {meta['category']}",
        "order: 5",
        f"updated: {latest}",
        "---",
        "",
        INTRO[lang],
        "",
    ]
    current_month = None
    for item in items:
        month = item["date"][:7]
        if month != current_month:
            current_month = month
            y, m = month.split("-")
            lines.append(f"## {y}年{int(m)}月" if lang == "ja" else f"## {y}-{m}")
            lines.append("")
        title = item["title_ja"] if lang == "ja" and item["title_ja"] else item["title_en"]
        summary = item["summary_ja"] if lang == "ja" else item["summary_en"]
        lines.append(f"### [{title}]({item['url']})")
        lines.append("")
        lines.append(f"{item['date']}")
        lines.append("")
        if summary:
            lines.append(summary)
            lines.append("")
    lines.append(SOURCE_NOTE[lang])
    lines.append("")
    return "\n".join(lines)


def cmd_render() -> None:
    data = load_news()
    items = [i for i in data["items"] if i.get("summary_ja") and i.get("summary_en")]
    skipped = len(data["items"]) - len(items)
    if not items:
        print("[render] 要約済みの項目が無いため生成しない。先に data/news.json を埋めること。")
        return
    for lang in ("ja",):
        path = CONTENT_DIR / lang / "news.md"
        path.write_text(render_lang(lang, items), encoding="utf-8")
        print(f"[render] {path} ({len(items)}件)")
    if skipped:
        print(f"[render] 未要約のため除外: {skipped}件")
    print("[render] このあと build/build_site.py を実行すること。")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true", help="news.json から news.md を生成する")
    parser.add_argument("--all", action="store_true", help="取得と生成を続けて行う")
    args = parser.parse_args()

    if args.render:
        cmd_render()
        return
    pending = cmd_fetch()
    if args.all:
        if pending:
            print("[all] 未要約があるため生成は行わない。")
            sys.exit(1)
        cmd_render()


if __name__ == "__main__":
    main()
