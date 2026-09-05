# ダメージ実測データ収集フォーム 設計仕様

Google Forms API のプログラム作成には別途OAuth認証の設定が必要なため、まずは仕様書として設計する。
以下の項目でGoogleフォームを作成し（所要時間目安5分）、回答先はGoogleスプレッドシートに接続する。
フォームのタイトル・質問文は日本語/英語併記にして、世界中のプレイヤーが回答できるようにする。

## フォーム名（例）

`The Ants ダメージ計算検証プロジェクト / The Ants Damage Formula Research`

冒頭の説明文（日英併記）:

> あなたの戦闘ログを教えてください。攻撃力・防御力とダメージの関係を集めて計算式を検証します。
> 画像を直接アップロードいただいても構いませんが、公開サイトには転載せず、数値の確認用にのみ使用します。
>
> Please share your combat log data. We are collecting attack/defense/damage examples to verify the damage formula.
> Screenshots are only used to double-check the numbers you enter and will NOT be reposted publicly.

## 質問項目（フォームの質問順）

| # | 列名(CSV/シート) | 質問文(日/英) | 型 | 必須 |
|---|---|---|---|---|
| 1 | timestamp | (自動記録 / auto-recorded) | 日時 | - |
| 2 | battle_type | 戦闘の種類は？ / Battle type? | 選択式: `PvE-資源採集地`, `PvE-遠征/ボス`, `PvP-侵略`, `PvP-真菌大戦`, `PvP-掠奪`, `その他/Other` | ○ |
| 3 | attacker_ant_type | 自分の蟻の種類 / Your ant type | 記述式 | ○ |
| 4 | attacker_level | 自分の蟻のレベル / Your ant level | 数値 | ○ |
| 5 | attacker_atk | 自分の攻撃力(ステータス画面の数値) / Your ATK stat | 数値 | ○ |
| 6 | attacker_def | 自分の防御力 / Your DEF stat | 数値 | 任意 |
| 7 | attacker_hp | 自分のHP / Your HP stat | 数値 | 任意 |
| 8 | skill_active | 発動していたスキル名（あれば） / Active skill name (if any) | 記述式 | 任意 |
| 9 | skill_level | そのスキルのLv、または特化アリのLv / Skill level, or the special ant's level | 数値 | 任意 |
| 10 | attacker_dmg_amp | 自分のステータス画面の「ダメージ増幅」% / Your "Damage Amplification" % (from stat screen) | 数値 | 任意 |
| 11 | defender_type | 相手の種類（敵NPC名 or 相手プレイヤーの蟻種） / Enemy type or opponent's ant type | 記述式 | ○ |
| 12 | defender_def | 相手の防御力（わかれば） / Enemy DEF (if known) | 数値 | 任意 |
| 13 | defender_hp | 相手のHP（わかれば） / Enemy HP (if known) | 数値 | 任意 |
| 14 | defender_dmg_reduction_amp | 相手の「ダメージ軽減増幅」%（わかれば） / Opponent's "Damage Reduction Amplification" % (if known) | 数値 | 任意 |
| 15 | damage_dealt | 実際に与えたダメージ量（戦闘ログの数値） / Actual damage dealt (from combat log) | 数値 | ○ |
| 16 | screenshot_url | スクリーンショットのURL（Googleドライブ等の共有リンク、任意） / Screenshot URL (optional) | URL | 任意 |
| 17 | server_region | サーバー/地域（わかれば） / Server or region (if known) | 記述式 | 任意 |
| 18 | notes | 備考 / Notes | 記述式(長文) | 任意 |

## 運用メモ

- 必須項目は「戦闘の種類」「自分の蟻の種類」「自分の攻撃力」「相手の種類」「実際のダメージ」の5つに絞り、回答のハードルを下げる。他は任意にして埋めやすくする。
- `skill_active`／`skill_level`／`attacker_dmg_amp`／`defender_dmg_reduction_amp` の4項目は、2026-07-19の自アカウント調査で「スキルダメージ＝基礎%（+特化アリLv×係数%）」「最終ダメージには攻撃側ダメージ増幅%・防御側ダメージ軽減増幅%が別レイヤーで乗る」ことが判明したために追加した項目。これらを記録しておくことで、既知の変数を差し引いた上でATK対DEFの純粋な関係を分離抽出できる（詳細は `content/ja/damage-calculation.md` 参照）。
- フォームの回答は自動的にGoogleスプレッドシートに集約される。集計時は `scripts/analyze_damage.py` にCSVエクスポートしたものを渡す。
- 列名はこの表の1列目（英数字）に合わせてスプレッドシートのヘッダーを設定しておくと、分析スクリプトがそのまま読める。
- SNS(X/Reddit/Discord)で個別に投稿されている数値例も、投稿者の許可を得た上でこの形式に変換してこのフォーム経由で追加していく運用とする（画像の無断転載はしない）。
