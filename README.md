# The Ants 攻略サイト・プロジェクト

The Ants: Underground Kingdom（ザ・アンツ）の非公式攻略サイト。日英バイリンガル。
静的サイト＋プレイヤーからの実データ収集によるダメージ計算式検証、の2本柱。

現状: **ローカルでコンテンツとビルド基盤を作成中。公開（GitHub Pages等）は未着手**（ユーザーの意向により後回し）。

## ディレクトリ構成

```
the_ants_project/
  content/ja/*.md      日本語コンテンツ（YAML frontmatter + Markdown）
  content/en/*.md      英語コンテンツ（同上）
  build/
    build_site.py       ビルドスクリプト（content/ -> docs/ にHTML生成）
    templates/base.html  共通レイアウトテンプレート
  docs/               ビルド生成物（HTML）。build_site.py実行のたびに上書きされる
  data/
    damage_log_form_spec.md  ダメージ収集用Googleフォームの項目設計仕様
    demo_damage_logs.csv      analyze_damage.py --demo で生成される動作確認用データ
  scripts/
    analyze_damage.py    収集データからダメージ計算式を統計的に検証するスクリプト
```

## サイトのビルド方法

```
python build/build_site.py
```

`docs/ja/*.html` `docs/en/*.html` に生成される。`docs/index.html` を開くと日本語版トップにリダイレクトされる。

## ページを追加する場合

`content/ja/新ページ.md` と `content/en/新ページ.md` を作り、冒頭に以下のfrontmatterを付ける。

```yaml
---
title: ページタイトル
description: メタ説明文
category: ナビゲーションのグループ名
order: 表示順（数値、小さいほど上）
updated: 2026-07-19
---
```

その後 `python build/build_site.py` を再実行すればナビゲーションに自動的に反映される。

## ダメージ計算検証の運用

1. `data/damage_log_form_spec.md` の仕様どおりにGoogleフォームを作成し、回答先をGoogleスプレッドシートに接続する
2. スプレッドシートをCSVエクスポートする
3. `python scripts/analyze_damage.py path/to/export.csv` で複数の計算式候補をフィットさせ、R²を比較する
4. 精度が高い式が見つかったら `content/ja/damage-calculation.md` と `content/en/damage-calculation.md` に反映する

動作確認用に合成データでのテストが可能: `python scripts/analyze_damage.py --demo`

## 公開時にやること（未着手・後日）

- GitHubアカウントでリポジトリ作成、`docs/` の中身をGitHub Pages等にデプロイ
- gitがこのPCに未インストールのため、公開作業に着手する際はインストールが必要
- SNS画像は転載しない方針を維持する（著作権配慮）
