# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# kei_parts_sourcing（軽トラ部品の調達代行）

<!-- 共通ルールは親の Claude_Tsuyoshi/CLAUDE.md と 01_shared/principles.md にある。ここには固有ルールだけ書く -->

## 目的
- 海外（まず米国、次に欧州）の「日本の中古機械を扱う輸入業者・販売店」から、彼らの顧客が必要とする日本国内向けモデルの部品の調達を請け負う
- 最初の商材は**軽トラ（日本国内向け軽トラック）の部品**。在庫を持たず、前金を受けてから仕入れる
- 価値の源泉は価格差ではなく「車台番号からの部品特定」「日本の仕入れ網」「まとめ発送」「見つからない部品の探索」

## 状態（更新日：2026-10-29）
- **停止（D-009）**。需要と利益率を調べた結果、薄利で事業として旨味がないと判断し、試験をせずに止めた。2026-10-29 に `99_archive/` へ移し、さらに外部ドライブ `D:\C_moved_20261029\99_archive\` へ移した
- 営業メールは送っていない。開業届・古物商許可の申請もしていない
- 決めたことは `DECISIONS.md`、進め方と判断基準は `PLAN.md`
- 調査レポート（Claude Docs）：https://claude.ai/artifact/So1mfqkRrnqcnv1BmtWT8s （タブ：本文／輸入業者リスト・メール／進め方・新商材／ホビー商材／大工道具）
- GitHub（private）：https://github.com/tsuyoshi35b-lgtm/kei_parts_sourcing 。`main` は `origin/main` を追跡。携帯からの操作手順は `docs/SETUP_GITHUB_MOBILE.md`
- コード（`tools/`）はまだ無い。ビルド・テストのコマンドも無い

## 最初に読むもの
1. `DECISIONS.md`（決定事項の正。ここにない事は推測で決めずに質問する）
2. `PLAN.md`（段階ごとのやることと、次に進む条件・撤退条件）
3. `docs/03_operations_flow.md`（業務の流れと、AIと人の分担）

## 固有ルール

### 事業主体と法令
- 事業主体は妻（さやか）。開業届・古物商許可・取引先とのやり取りの名義はすべて妻にそろえる。夫（Tsuyoshi）は手伝いの立場（名義貸しは禁止）
- 古物商許可が下りるまでは**新品部品だけ**を扱う。中古部品は許可後
- 輸出規制・関税・各国の法律の最終判断は AI がしない。根拠と確認先を示して人に判断してもらう

### AI に任せないこと
- 送金・発注・支払い
- 承認されていない見積もりや約束の送信
- 営業メールの大量自動送信（1日10社程度まで、人が確認して送る）
- 取引実績の誇張や架空の顧客の声の作成

### 書き方
- 回答・資料は日本語。英文メールは和訳の要旨をつける
- 価格は「出品価格・掲載価格」と「成約価格」を区別して書く。未確認の数字は「要検証」と書く
- 開発者（Tsuyoshi）は Python 初心者・MQL5 の実務経験あり。ツールはシンプルな構成にする

### 記録ファイルの扱い
- `DECISIONS.md` は追記のみ。変更は古い記録を消さず、新しい番号（D-009〜）で「D-00X を変更」と書く。「要確定」の項目（例：手数料20%・最低3,000円）は確定扱いしない
- `PLAN.md` の「次に進む条件」「撤退条件」を満たしたか判断するときは、`data/inquiries.csv` の実数（件数・`margin_pct`・`staff_minutes`）で示す
- 3つの CSV は Excel で開く前提の **UTF-8（BOM付き）**。書き換えるときも BOM と列の並びを保つ（Python なら `encoding="utf-8-sig"`）。カンマを含む値は `"` で囲む
  - `outreach/importer_list.csv`：営業先。`status` の初期値は `未連絡`。送信・返信したら `sent_date`・`reply_date`・`monthly_requests`・`hard_parts`・`current_source`・`next_action` を埋める（営業メールの3つの質問の答えに対応）
  - `data/inquiries.csv`：問い合わせ1件1行（`inquiry_id` 単位）。見積もり→前金→発送の進み具合を `status` で追う
  - `data/parts_db.csv`：車台番号（`frame_code`）→品番→仕入れ先→価格→納期の蓄積。事業の資産なので、成約・見積もりのたびに追記・`last_checked` を更新
- 顧客の個人情報や取引の詳細（住所・連絡先・請求書など）は `customers/` か `private/` に置く（`.gitignore` で除外済み）。Git に入る CSV には会社名・部品・金額までにする

### ツール（`tools/`、これから作る）
- 予定は `tools/README.md`：見積もり計算 `quote_calc.py`（円の部品代・重量・送り先 → 手数料・送料・ドル建て見積もり）、送料表 CSV、受信メール → `inquiries.csv` 登録の補助
- 作るときは標準ライブラリ中心の単一スクリプトにし、依存を足したら `requirements.txt` を作る・更新する。為替レートや手数料率はコードに埋め込まず引数か設定ファイルで渡す
