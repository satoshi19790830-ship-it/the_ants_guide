# 掲示板の設置手順

質問掲示板と情報提供掲示板は、`data/boards.json` の設定を読んで `build/build_site.py` が
埋め込みHTMLを生成する。値が空のあいだは、埋め込みの代わりに「まだ設置作業中」の案内が出る。

**両方とも設置済み**（2026-09-06）。この手順書は、作り直すときと設定を変えるときのための記録。

現在の設定:

| 掲示板 | ページ | 使っているもの | 本文中のトークン |
|---|---|---|---|
| 質問掲示板 | `content/ja/qa-board.md` | giscus（GitHub Discussions / カテゴリ Q&A） | `[[GISCUS]]` |
| 情報提供掲示板 | `content/ja/report-board.md` | Tally フォーム（`https://tally.so/r/81BQEx`） | `[[FORM]]` |

## 1. 質問掲示板（giscus ＝ GitHub Discussions）

giscus は GitHub Discussions をページに埋め込むウィジェット。サーバー不要・無料。
**投稿する側にも GitHub アカウントが必要**なので、そこは割り切る。

1. 対象リポジトリ（`satoshi19790830-ship-it/the_ants_guide`）が **public** であること
2. リポジトリの Settings → General → Features → **Discussions にチェック**
3. Discussions で **カテゴリ「Q&A」** を作る（既定であることが多い。無ければ New category、形式は Question / Answer）
4. <https://github.com/apps/giscus> を開き、そのリポジトリに **giscus アプリをインストール**
5. <https://giscus.app> を開き、リポジトリ名（`ユーザー名/リポジトリ名`）を入力。
   ページ↔Discussion の紐付けは **「パス名」**、カテゴリは **Q&A** を選ぶ
6. ページ下部に出る `<script>` の中から次の4つを `data/boards.json` に写す
   - `data-repo` → `giscus.repo`
   - `data-repo-id` → `giscus.repo_id`
   - `data-category` → `giscus.category`
   - `data-category-id` → `giscus.category_id`

テーマは `preferred_color_scheme`、言語は `ja` を build_site.py 側で固定しているので、
giscus.app で何を選んでもそこは上書きされる。

## 2. 情報提供掲示板（Tally）

最初は Google フォームを iframe で貼っていたが、**ファイルアップロード項目を入れると回答者に
Google ログインを強制される**仕様で、匿名で送れなくなる。Tally は無料プランで匿名のまま
画像を受け取れるため、2026-09-06に移行した（`google_form_embed_url` は廃止）。

フォームの項目。`content/ja/report-board.md` の説明と食い違わないように揃える。

| # | 質問 | 形式 | 備考 |
|---|---|---|---|
| 1 | カテゴリ | プルダウン | 下の選択肢。**必須** |
| 2 | 内容 | 段落 | **必須** |
| 3 | 画像 | ファイルアップロード | 任意。複数可。1ファイル10MBまで |
| 4 | 確かさ | ラジオ | 「自分の画面で確認した」／「うろ覚え」／「他所で見た（URLを下に）」 |
| 5 | 出典URL | 記述式 | 任意 |
| 6 | 名前の掲載 | ラジオ | 「読者提供とだけ書いてよい」／「名前を出さないでほしい」 |

カテゴリの選択肢（`content/ja/report-board.md` の表と揃える）:

```
細菌
遺伝子
細胞
真菌
兵種改造
働きアリ宝物
勲章
特化アリ覚醒
征服者進化
VIP
着せ替え（星UP）
中立生物（化石・宝石・仲間）
戦闘（ダメージ・行動順・編成）
その他・サイトの誤りの指摘
```

**匿名で受け取るための設定**（Tally のフォーム設定）:

- メールアドレスの収集・ログイン必須の類はすべてオフにする
- 回答者に返信しない前提。`content/ja/report-board.md` で「誰が送ったか分からない」と
  明記しているので、個人を特定できる項目を増やさない

設定できたら、公開URL `https://tally.so/r/<フォームID>` の **フォームID部分**を
`data/boards.json` の `tally.form_id` に書く（URL全体は `tally.url` に控えとして置いている）。
埋め込みURL（`hideTitle` などのパラメータ付き）は `build_site.py` 側で組み立てるので不要。

### 埋め込みの高さについて

Tally 公式の読み込み方（`data-tally-src` + embed.js）はこの構成では src が差し込まれず、
フォームが表示されないままだったため、iframe の `src` を直接指定している。
そのため**高さが自動調整されず固定値**（880px）になっている。実測は900px幅で769px、
375px幅で783px。**フォームの項目を増やしたら `build_site.py` の `build_form_html` の
`height` を見直すこと。**

## 3. 反映

```
python build/build_site.py
```

`docs/qa-board.html` と `docs/report-board.html` を開いて、埋め込みが出ていれば完了。
本番URL（<https://satoshi19790830-ship-it.github.io/the_ants_guide/qa-board.html>）でも確認する。
giscus は **パス名でDiscussionを紐付ける**ので、ページのファイル名を変えると
それまでの書き込みが表示されなくなる点に注意。
