"""利益率の試算：data/margin_items.csv の品目ごとに、eBay で直接売る場合と業者向け代行の場合を計算する。

使い方：
    py tools/margin_calc.py            # 関税15%で計算
    py tools/margin_calc.py --duty 27.5

前提の数字（手数料・送料・関税など）は下の ASSUMPTIONS にまとめてある。要検証の値は変わったらここを直す。
"""
import argparse
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASSUMPTIONS = {
    # eBay（日本から米国の買い手へ）
    "ebay_fvf": 0.136,          # 落札手数料（自動車部品）。売上＋送料＋売上税にかかる
    "us_sales_tax": 0.07,       # 買い手が払う売上税の平均（手数料の計算にだけ使う。要検証）
    "ebay_intl_fee": 0.0165,    # 海外取引手数料
    "ebay_order_fee": 60,       # 1注文 0.40ドル
    "payout_fx": 0.02,          # 円で受け取る時の為替コスト（要検証）
    # 発送（日本郵便、米国宛て）
    "packing_kg": 0.2,          # 梱包材の重さ
    "packing_jpy": 150,         # 梱包材の費用
    "zonos_fee": 500,           # 関税前払いの手数料（金額は未確認・要検証）
    # 業者向け代行（DECISIONS D-002 の案）
    "b2b_fee_rate": 0.20,
    "b2b_fee_min": 3000,
    "b2b_payment_fee": 0.03,    # PayPal・Wise の受取手数料（要検証）
    "b2b_ship_per_kg": 1800,    # 週1回のまとめ発送（クーリエ）の1kgあたり（要検証）
    "importer_ebay_fee": 0.146, # 業者が米国内の eBay で売るときの手数料（売上税込みの基準）
}

# EMS 米国宛て（第4地帯）公式料金。間は直線で補う（概算）
EMS_TABLE = [(0.5, 3900), (1.0, 5300), (1.5, 6600), (2.0, 7900), (3.0, 10300), (5.0, 15100), (10.0, 27100)]


def ems_rate(kg):
    if kg <= EMS_TABLE[0][0]:
        return EMS_TABLE[0][1]
    for (w0, r0), (w1, r1) in zip(EMS_TABLE, EMS_TABLE[1:]):
        if kg <= w1:
            return round(r0 + (r1 - r0) * (kg - w0) / (w1 - w0))
    raise ValueError(f"{kg}kg は表の範囲外")


def airpacket_rate(kg):
    # 国際エアパケット 米国宛て：100gまで1,200円、以降100gごとに210円（2kgまで、長さ60cmまで）
    steps = math.ceil(kg / 0.1)
    return 1200 + 210 * (steps - 1)


def shipping(kg, long_item):
    total = kg + ASSUMPTIONS["packing_kg"]
    if long_item or total > 2.0:
        return ems_rate(total), "EMS"
    return airpacket_rate(total), "エアパケット"


def ebay_direct(row, duty_rate):
    a = ASSUMPTIONS
    price = int(row["sell_price_jpy"])
    revenue = price + int(row["buyer_ship_jpy"])
    fees = revenue * (a["ebay_fvf"] * (1 + a["us_sales_tax"]) + a["ebay_intl_fee"] + a["payout_fx"]) + a["ebay_order_fee"]
    ship, method = shipping(float(row["weight_kg"]), row["long_item"] == "1")
    duty = price * duty_rate
    cost = int(row["cost_jpy"])
    profit = revenue - fees - ship - duty - a["zonos_fee"] - a["packing_jpy"] - cost
    return revenue, fees, ship, method, duty, profit


def b2b(row, duty_rate):
    a = ASSUMPTIONS
    cost = int(row["cost_jpy"])
    fee = max(cost * a["b2b_fee_rate"], a["b2b_fee_min"])
    invoice = cost + fee
    our_profit = fee - invoice * a["b2b_payment_fee"] - a["packing_jpy"]
    kg = float(row["weight_kg"]) + a["packing_kg"]
    landed = invoice + kg * a["b2b_ship_per_kg"] + invoice * duty_rate
    resale = int(row["sell_price_jpy"]) + int(row["buyer_ship_jpy"])
    importer_profit = resale * (1 - a["importer_ebay_fee"]) - landed
    return invoice, our_profit, landed, importer_profit, resale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duty", type=float, default=15.0, help="米国の関税率（%%）")
    ap.add_argument("--csv", default=str(ROOT / "data" / "margin_items.csv"))
    ap.add_argument("--oem-cost-rate", type=float, default=1.0,
                    help="純正部品の仕入れ値に掛ける率（部品商の業者価格を想定するなら 0.8 など）")
    args = ap.parse_args()
    duty = args.duty / 100

    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if "純正" in r["group"]:
            r["cost_jpy"] = str(round(int(r["cost_jpy"]) * args.oem_cost_rate))

    print(f"## eBay で直接売る場合（関税 {args.duty:g}%）\n")
    print("| 区分 | 品目 | 売上（送料込） | 仕入れ | 手数料 | 送料 | 関税 | 利益 | 利益率 |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in rows:
        rev, fees, ship, method, d, profit = ebay_direct(r, duty)
        print(f"| {r['group']} | {r['item']} | {rev:,} | {int(r['cost_jpy']):,} | {fees:,.0f} | {ship:,}（{method}） | {d:,.0f} | {profit:,.0f} | {profit / rev:.0%} |")

    print(f"\n## 業者向け代行の場合（手数料20%・最低3,000円、関税 {args.duty:g}%は業者が負担）\n")
    print("| 区分 | 品目 | 請求額 | 当方の利益 | 業者の到着原価 | 業者の再販価格 | 業者の粗利 | 業者の粗利率 |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in rows:
        invoice, ours, landed, imp, resale = b2b(r, duty)
        print(f"| {r['group']} | {r['item']} | {invoice:,.0f} | {ours:,.0f} | {landed:,.0f} | {resale:,} | {imp:,.0f} | {imp / resale:.0%} |")


if __name__ == "__main__":
    main()
