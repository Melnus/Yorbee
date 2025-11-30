# Yorbee: The Gamified Skill Guild ⚔️
### "Job Title" is Dead. Long live "Skill Set".

[![SBCM Economics](https://img.shields.io/badge/Theory-SBCM_HR-blue)](https://doi.org/10.5281/zenodo.17766604)
[![Python](https://img.shields.io/badge/Built_with-Streamlit-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Yorbee（ヨルビー）は、仕事を「クエスト」に、労働者を「冒険者」に再定義する、ゲーミフィケーション求人プラットフォームです。**
「店長」や「営業部長」といった巨大な役職（Job Title）を解体し、個人の得意な「スキル（Skill）」をパズルのように組み合わせてチームを結成します。

---

## 📖 コンセプト (Concept)

**「スーパーマンを探すのは、もうやめよう。」**

従来の人材市場は、全ての業務を一人でこなせる「正社員（勇者）」を探し求め、結果として「人手不足」に陥っていました。
Yorbeeは、SBCM理論に基づき**「ジョブのアンバンドリング（解体）」**を行います。

*   **Before:** 「カフェ店長募集 (月給30万)」 → 誰も来ない 💀
*   **After (Yorbee):**
    *   クエストA: 「接客のプロ (Lv.5)」
    *   クエストB: 「シフト管理の鬼 (Lv.4)」
    *   クエストC: 「力持ちの搬入係 (Lv.3)」
    *   **→ 3人の冒険者でパーティを組んで解決！ 🎉**

## 🚀 機能 (Features)

### 1. 冒険の書 (Registration without PR)
長くて退屈な「職務経歴書」や「自己PR」はゴミ箱へ。
STR（体力）、INT（知力）、CHA（魅力）などのステータスをスライダーで直感的に登録します。

### 2. クエストボード (SBCM Price Check)
発注者が予算を入力すると、SBCM理論に基づく**「地域の適正単価」**と比較判定されます。
*   安すぎる報酬には「誰も来ないよ」と警告 ⚠️
*   適正な報酬には「これなら勇者が来る！」と推奨 ✨

### 3. 酒場マッチング (Skill Tetris)
足りないスキルを補う仲間を、AIが自動でリコメンド。
「自分ひとりでは倒せないボス（業務）」も、得意分野が違う仲間とパーティを組めば攻略可能です。

### 4. ダンジョン & ウォレット (Auto-Pilot Work)
業務（ダンジョン攻略）の進捗は、AIオートパイロットで管理されます。
クエストクリアと同時に、スマートコントラクトにより報酬がメンバーのウォレットに即時分配されます。

## 🛠️ インストールと実行 (Installation)

Python環境があれば、すぐにローカルでギルドを設立できます。

```bash
# 1. リポジトリをクローン
git clone https://github.com/your-name/Yorbee.git
cd Yorbee

# 2. 依存ライブラリをインストール
pip install -r requirements.txt

# 3. アプリを起動
streamlit run yorbee_game.py
```

## 📚 Theoretical Background

Yorbeeは、建設DXシステム **[G-Cart](https://github.com/Melnus/Virtual-General-Contractor)** の「人材版」です。

> **SBCM Human Resources Theory:**
> 1人の人間が持つキャパシティ ($C_{single}$) が業務負荷 ($I_{job}$) を下回る場合でも、異なるスキルセットを持つ $n$ 人を集めれば、総キャパシティは負荷を上回る ($\Sigma C \ge I$)。これにより、潜在的な労働力（主婦、高齢者、副業）を市場に還流させる。

## 🛡️ セキュリティとプライバシー

Yorbeeは個人の「弱点（スキル不足）」もデータとして扱います。
そのため、`robots.txt` により、冒険者のプライバシー情報は検索エンジンから厳格に保護されています。

- ✅ **Public:** クエスト内容（仕事）
- ⛔ **Private:** 冒険者のステータス、パーティ会話、ウォレット

## 📷 スクリーンショット

| 冒険の書 (Status) | 酒場 (Party Making) |
| :---: | :---: |
| <img src="docs/screen_status.png" width="300"> | <img src="docs/screen_party.png" width="300"> |

## 📝 ライセンス

[MIT License](LICENSE)

---
**Author:** Hokuto Koyama(Melnus)
```
