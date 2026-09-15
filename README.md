# The Ants 攻略サイト・プロジェクト

The Ants: Underground Kingdom（ザ・アンツ）の非公式攻略サイト。日本語のみ。
公式ヘルプ・公式フォーラムの一次情報の日本語まとめと、プレイヤーからの実データ収集による
ダメージ計算式の検証、の2本柱。

- 公開先: <https://satoshi19790830-ship-it.github.io/the_ants_guide/>（GitHub Pages / `docs/` を公開元に設定）
- 英語版は2026-09-06に廃止（経緯は `content/en/_RETIRED.md`）

## ディレクトリ構成

```
the_ants_guide/
  content/ja/*.md        記事の原稿（YAML frontmatter + Markdown）。編集するのはここ
  content/en/            廃止済み。ビルド対象外。更新しない
  build/
    build_site.py         ビルドスクリプト（content/ja -> docs/ にHTML生成）
    templates/base.html   共通レイアウトテンプレート
  docs/                  ビルド生成物。GitHub Pages の公開元。手で編集しない
    images/               assets/images/ からビルド時にコピーされる
  assets/images/         サイトに載せる画像（加工済み。元素材は .gitignore で除外）
  data/
    boards.json           掲示板（giscus / Tally）の設置設定
    boards_setup.md       その設置手順
    news.json             公式フォーラムRSSから取得した最新情報の元データ
    damage_log_form_spec.md  ダメージ収集フォームの項目設計仕様
    demo_damage_logs.csv     analyze_damage.py --demo が使う動作確認用データ
    faq_progress.md          公式FAQ（日本語ヘルプセンター）の読み込み進捗
    *_extraction_*.md        スクリーンショット/NotebookLM からの抽出メモ
  scripts/
    fetch_news.py         公式フォーラムRSS -> news.json -> content/ja/news.md
    check_links.py        docs/ の内部リンク切れ検査
    check_anchors.py      docs/ のページ内アンカー(#...)切れ検査
    analyze_damage.py     収集データからダメージ計算式を統計的に検証する
```

## 準備

```
pip install -r requirements.txt
```

## サイトのビルド方法

```
python build/build_site.py
```

`docs/` 直下に `index.html` `beginner-guide.html` … が生成される（言語ディレクトリは無い平坦構成）。
あわせて `assets/images/` のコピー、`sitemap.xml`、`robots.txt`、`.nojekyll` も出力される。

ビルド後は検査を通す。見出し文言を変えるとアンカーが静かに壊れるため、特に2つ目は必須。

```
python scripts/check_links.py
python scripts/check_anchors.py
```

公開URLは `build_site.py` の `SITE_URL` が既定値。環境変数 `ANTS_SITE_URL` で上書きできる。

## ページを追加する場合

`content/ja/新ページ.md` を作り、冒頭に以下のfrontmatterを付ける。

```yaml
---
title: ページタイトル
description: メタ説明文（検索結果・OGPに出る）
category: ナビゲーションのグループ名（はじめに / 最新情報 / 特集 / 攻略 / 図鑑 / 掲示板 / 検証プロジェクト）
order: 表示順（数値、小さいほど上）
updated: 2026-09-15
---
```

その後 `python build/build_site.py` を再実行すればナビゲーションに自動的に反映される。

- 目次は見出し(h2/h3)が2つ以上あると自動で付く。不要なページは frontmatter に `toc: false` を書く
- 本文に `[[GISCUS]]` `[[FORM]]` と単独行で書くと、その位置に掲示板／情報提供フォームが埋め込まれる
- サイドバーの「人気記事」は `build_site.py` の `POPULAR_SLUGS` で固定指定している

## 最新情報ページの更新

```
python scripts/fetch_news.py          # RSS取得 -> data/news.json を更新
python scripts/fetch_news.py --render # data/news.json -> content/ja/news.md を生成
python scripts/fetch_news.py --all    # 取得と生成を続けて行う
```

要約は自動生成しない。取得直後は要約が空なので、手で埋めてから `--render` する。
アップデート告知は公式サイトの日本語版（theants.allstarunion.com/ja/news）の表記に合わせる。
新着が無いときは `news.json` を書き換えない。

## 掲示板

`data/boards.json` に設定を書くと、該当ページに埋め込みが出る（空なら「設置作業中」の案内に置き換わる）。
設置手順は `data/boards_setup.md`。現状はどちらも設置済み:

- 質問掲示板: giscus（GitHub Discussions のカテゴリ「Q&A」）。投稿にはGitHubアカウントが必要
- 情報提供掲示板: Tally フォーム。Googleフォームはファイル添付を入れるとGoogleログインが必須になり
  匿名で送れないため、2026-09-06にTallyへ移行した

## ダメージ計算検証の運用

1. `data/damage_log_form_spec.md` の仕様どおりのフォームで回答を集め、CSVエクスポートする
2. `python scripts/analyze_damage.py path/to/export.csv` で複数の計算式候補をフィットさせ、R²を比較する
3. 精度が高い式が見つかったら `content/ja/damage-calculation.md` に反映する

動作確認用に合成データでのテストが可能: `python scripts/analyze_damage.py --demo`

## 編集方針

- 公式FAQ・公式フォーラムの本文は転載せず、要約＋出典リンクの形で反映する
- SNSの画像は転載しない（著作権配慮）。元のスクリーンショット素材（1GB超）は `.gitignore` でgit管理外
- `docs/` は毎回上書きされる生成物。直すのは必ず `content/ja/` 側
