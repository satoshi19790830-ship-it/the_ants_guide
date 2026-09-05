"""The Ants ダメージ計算式 検証スクリプト。

data/damage_log_form_spec.md で設計したGoogleフォームの回答をCSVエクスポートし、
このスクリプトに渡すと、複数のダメージ計算モデル候補を実データにフィットさせて
決定係数(R^2)を比較する。どのモデルが実測値に一番近いかを判断する材料にする。

使い方:
    python analyze_damage.py path/to/exported_responses.csv
    python analyze_damage.py --demo   # 動作確認用の合成データで試す

必要なCSV列（最低限）:
    attacker_atk, defender_def, damage_dealt
（欠損は自動的に除外される）
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_COLS = ["attacker_atk", "defender_def", "damage_dealt"]


def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return float("nan")
    return 1 - ss_res / ss_tot


def fit_linear_atk_def(df):
    """damage = a*ATK + b*DEF + c"""
    X = np.column_stack([df["attacker_atk"], df["defender_def"], np.ones(len(df))])
    y = df["damage_dealt"].to_numpy()
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    return {
        "name": "線形モデル: damage = a*ATK + b*DEF + c",
        "params": {"a": coef[0], "b": coef[1], "c": coef[2]},
        "r2": r_squared(y, pred),
    }


def fit_difference(df):
    """damage = k*(ATK - DEF)、負値は0でクリップ"""
    diff = (df["attacker_atk"] - df["defender_def"]).to_numpy()
    y = df["damage_dealt"].to_numpy()
    mask = diff > 0
    if mask.sum() < 2:
        return None
    k = np.sum(diff[mask] * y[mask]) / np.sum(diff[mask] ** 2)
    pred = np.clip(diff, 0, None) * k
    return {
        "name": "差分モデル: damage = k*(ATK - DEF)",
        "params": {"k": k},
        "r2": r_squared(y, pred),
    }


def fit_ratio(df):
    """damage = k * ATK * ATK/(ATK+DEF)  （攻防比モデル、多くのソシャゲで採用される形）"""
    atk = df["attacker_atk"].to_numpy()
    dfn = df["defender_def"].to_numpy()
    base = atk * atk / (atk + dfn)
    y = df["damage_dealt"].to_numpy()
    k = np.sum(base * y) / np.sum(base**2)
    pred = base * k
    return {
        "name": "攻防比モデル: damage = k * ATK^2/(ATK+DEF)",
        "params": {"k": k},
        "r2": r_squared(y, pred),
    }


def fit_power_log(df):
    """log(damage) = log(k) + p*log(ATK) - q*log(DEF)"""
    sub = df[(df["attacker_atk"] > 0) & (df["defender_def"] > 0) & (df["damage_dealt"] > 0)]
    if len(sub) < 3:
        return None
    X = np.column_stack(
        [np.log(sub["attacker_atk"]), np.log(sub["defender_def"]), np.ones(len(sub))]
    )
    y = np.log(sub["damage_dealt"].to_numpy())
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred_log = X @ coef
    return {
        "name": "べき乗モデル: damage = k * ATK^p / DEF^q",
        "params": {"p": coef[0], "q": -coef[1], "k": np.exp(coef[2])},
        "r2": r_squared(y, pred_log),  # log空間でのR^2
        "note": "R^2はlog(damage)空間での値",
    }


def make_demo_csv(path: Path, n=60, seed=0):
    """動作確認用の合成データを生成する（真の式: damage = 2.0*ATK^2/(ATK+DEF) + ノイズ）"""
    rng = np.random.default_rng(seed)
    atk = rng.uniform(50, 500, n)
    dfn = rng.uniform(20, 400, n)
    true_damage = 2.0 * atk**2 / (atk + dfn)
    noisy_damage = true_damage * rng.normal(1.0, 0.05, n)
    df = pd.DataFrame(
        {
            "attacker_atk": atk.round(1),
            "defender_def": dfn.round(1),
            "damage_dealt": noisy_damage.round(1),
        }
    )
    df.to_csv(path, index=False, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", nargs="?", help="エクスポートしたCSVファイルのパス")
    parser.add_argument("--demo", action="store_true", help="合成データで動作確認する")
    args = parser.parse_args()

    if args.demo:
        demo_path = Path(__file__).resolve().parent.parent / "data" / "demo_damage_logs.csv"
        make_demo_csv(demo_path)
        csv_path = demo_path
        print(f"[demo] 合成データを生成しました: {csv_path}\n")
    elif args.csv_path:
        csv_path = Path(args.csv_path)
    else:
        parser.print_help()
        sys.exit(1)

    df = pd.read_csv(csv_path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        print(f"エラー: 必須列が不足しています: {missing}")
        sys.exit(1)

    before = len(df)
    df = df.dropna(subset=REQUIRED_COLS)
    df = df[(df["attacker_atk"] > 0) & (df["defender_def"] >= 0) & (df["damage_dealt"] > 0)]
    print(f"読み込み件数: {before} -> 有効データ: {len(df)}\n")

    if len(df) < 5:
        print("データが少なすぎます（5件以上を推奨）。フォームでの回答を増やしてください。")
        return

    results = []
    for fn in [fit_linear_atk_def, fit_difference, fit_ratio, fit_power_log]:
        res = fn(df)
        if res:
            results.append(res)

    results.sort(key=lambda r: (r["r2"] if r["r2"] == r["r2"] else -999), reverse=True)

    print("=== モデル比較（R^2が1に近いほど当てはまりが良い） ===\n")
    for r in results:
        params_str = ", ".join(f"{k}={v:.4f}" for k, v in r["params"].items())
        note = f"  ({r['note']})" if "note" in r else ""
        print(f"- {r['name']}")
        print(f"    R^2 = {r['r2']:.4f}{note}")
        print(f"    パラメータ: {params_str}\n")

    print("補足: R^2が最も高いモデルが有力候補ですが、データ件数が少ないうちは")
    print("      過学習の可能性があるため、戦闘種別(PvE/PvP)やスキル発動有無で")
    print("      層別しても同じ傾向になるか確認することを推奨します。")


if __name__ == "__main__":
    main()
