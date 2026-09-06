# 掲示板の設置手順

`data/boards.json` の空欄を埋めれば、質問掲示板と情報提供掲示板が動く。
埋めるまでは、両ページに「まだ設置作業中」の案内が出る（サイト自体は未公開なので実害はない）。

## 1. 質問掲示板（giscus ＝ GitHub Discussions）

giscus は GitHub Discussions をページに埋め込むウィジェット。サーバー不要・無料。
**投稿する側にも GitHub アカウントが必要**なので、そこは割り切る。

1. GitHub Pages 用のリポジトリを **public** で作る（公開作業と同じもので良い）
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

## 2. 情報提供掲示板（Google フォーム）

匿名で送れるようにする。**「ログインが必要」「メールアドレスを収集する」は必ずオフ**にする。

作る質問は次の通り。

| # | 質問 | 形式 | 備考 |
|---|---|---|---|
| 1 | カテゴリ | プルダウン | 下の選択肢。**必須** |
| 2 | 内容 | 段落 | **必須** |
| 3 | 確かさ | ラジオ | 「自分の画面で確認した」／「うろ覚え」／「他所で見た（URLを下に）」 |
| 4 | 出典URL | 記述式 | 任意 |
| 5 | 名前の掲載 | ラジオ | 「読者提供とだけ書いてよい」／「名前を出さないでほしい」 |

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

作ったら「送信」→ 埋め込み（`< >`）タブの iframe の `src` を丸ごと
`google_form_embed_url` に貼る（`https://docs.google.com/forms/d/e/.../viewform?embedded=true` の形）。

## 3. 反映

```
python build/build_site.py
```

`docs/qa-board.html` と `docs/report-board.html` を開いて、埋め込みが出ていれば完了。
