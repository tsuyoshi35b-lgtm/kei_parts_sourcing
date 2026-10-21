# kei_parts_sourcing

海外の軽トラ輸入業者・販売店向けに、日本から軽トラ部品を調達する代行事業のプロジェクトです。

## フォルダ構成

| 場所 | 中身 |
| --- | --- |
| `CLAUDE.md` | Claude Code 向けの指示（目的・状態・固有ルール） |
| `DECISIONS.md` | 決定事項の記録（D-001〜） |
| `PLAN.md` | 段階別の進め方、次に進む条件、撤退条件 |
| `docs/01_business_model.md` | 事業モデル、料金、ウェブサイトとプラットフォームの方針 |
| `docs/02_legal_compliance.md` | 古物商・名義・輸出規制・関税・海外の法律の確認事項 |
| `docs/03_operations_flow.md` | 注文1件の流れと、AIと人の役割分担 |
| `docs/04_research_summary.md` | 市場調査の要約（GPT・Geminiとの比較を含む） |
| `docs/05_future_candidates.md` | 将来の候補（FA部品・大工道具・対物レンズなど） |
| `outreach/importer_list.csv` | 営業先リスト（米国46社・欧州4社、状況を書き込む） |
| `outreach/email_templates.md` | 英文の営業メール3通（和訳つき） |
| `data/parts_db.csv` | 部品データベースのひな形（車台番号→品番→仕入れ先→価格→納期） |
| `data/inquiries.csv` | 問い合わせ・見積もりの管理表のひな形 |
| `tools/` | 見積もり計算などのスクリプト置き場（これから作る） |
| `references/sources.md` | 調査の出典 |

## 次にやること
`PLAN.md` の「段階0：土台づくり」から始める。
