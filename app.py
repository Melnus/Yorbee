import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# --- 0. ゲーム設定 (Config) ---
st.set_page_config(page_title="Yorbee | 冒険の書", page_icon="⚔️", layout="centered")

# SBCM理論に基づく地域単価 (柏市の標準ブロックから算出された1人あたり時間単価)
LOCAL_STD_PRICE = 2500  # ¥2,500/時間

# セッション管理
if 'phase' not in st.session_state: st.session_state['phase'] = 'register'
if 'my_stats' not in st.session_state: st.session_state['my_stats'] = {}
if 'quest' not in st.session_state: st.session_state['quest'] = {}
if 'party' not in st.session_state: st.session_state['party'] = []

# --- モックデータ: ギルドの仲間たち (匿名) ---
GUILD_MEMBERS = [
    {"id": 1, "class": "魔法使い(経理)", "skills": {"INT": 8, "STR": 1}, "fee": 2000},
    {"id": 2, "class": "戦士(肉体派)", "skills": {"INT": 2, "STR": 9}, "fee": 1800},
    {"id": 3, "class": "遊び人(クリエイティブ)", "skills": {"INT": 6, "LUCK": 8}, "fee": 3000},
]

# ==========================================
# Phase 1: キャラクター登録 (Registration)
# ==========================================
if st.session_state['phase'] == 'register':
    st.title("🛡️ 冒険の書を作る")
    st.caption("まずは君の分身（アバター）を作ろう！")

    # 名前
    name = st.text_input("君の名前は？", "勇者ヨシヒコ")

    # PR文を捨てる演出
    st.write("---")
    st.write("📝 **自己PR文 (長文)**")
    pr_text = st.text_area("ここにダラダラとした職務経歴書を書こうとしてない？", height=100, placeholder="私は大学時代にサークルの副代表として...")
    
    col_bin1, col_bin2 = st.columns([1, 4])
    with col_bin1:
        if st.button("🗑️ 捨てる"):
            st.toast("ポイッ！ 長いPRなんて誰も読まないよ！", icon="🗑️")
    with col_bin2:
        st.caption("← PR文はゴミ箱へ。大事なのは「今、何ができるか」だけ！")

    # スキルセット入力 (楽しく！)
    st.write("---")
    st.subheader("⚡ 君のステータス")
    c1, c2, c3 = st.columns(3)
    str_score = c1.slider("💪 STR (体力・根性)", 1, 10, 5)
    int_score = c2.slider("🧠 INT (事務・論理)", 1, 10, 5)
    cha_score = c3.slider("💖 CHA (接客・愛嬌)", 1, 10, 5)

    # 志向性
    st.write("---")
    st.subheader("💎 キミは何したい？")
    quest_type = st.multiselect("興味のあるクエスト", ["魔王討伐 (大プロジェクト)", "薬草採取 (単発バイト)", "街の警備 (定常業務)", "武器生成 (クリエイティブ)"])

    if st.button("🚀 冒険を始める (登録完了)", type="primary"):
        st.session_state['my_stats'] = {"name": name, "STR": str_score, "INT": int_score, "CHA": cha_score}
        st.session_state['phase'] = 'order'  # 本来はホーム画面だが、デモ用に発注画面へ
        st.balloons()
        st.rerun()

# ==========================================
# Phase 2: クエスト発注 (Ordering)
# ==========================================
elif st.session_state['phase'] == 'order':
    st.title("📜 クエストボード (発注)")
    st.caption("君がギルドマスターだ。解決したい問題を教えてくれ。")

    # 1. 欲しいスキル
    st.subheader("1. どんな魔法(スキル)が必要？")
    req_int = st.slider("必要な 🧠 INT (事務レベル)", 0, 10, 5)
    req_str = st.slider("必要な 💪 STR (体力レベル)", 0, 10, 3)

    # 2. 匿名マッチングプレビュー
    st.info("👀 **チラ見せ:** 今、ギルドにはこんな冒険者が待機中だよ！")
    matched_count = 0
    for m in GUILD_MEMBERS:
        if m['skills']['INT'] >= req_int and m['skills']['STR'] >= req_str:
            st.markdown(f"- 👤 **{m['class']}** (Lv.{sum(m['skills'].values())}) が興味を持っています")
            matched_count += 1
    if matched_count == 0:
        st.warning("条件が厳しいかも…もう少しレベルを下げられる？")

    # 3. 予算入力 (SBCMチェック)
    st.subheader("2. 報酬 (SBCMチェック)")
    
    hours = st.number_input("想定時間 (Hours)", 1, 100, 10)
    
    # 推定予算の算出
    est_budget = hours * LOCAL_STD_PRICE
    st.caption(f"💡 SBCM理論による、この街の適正報酬目安: **¥{est_budget:,}**")

    budget = st.number_input("君の提示額 (¥)", step=1000, value=int(est_budget))

    if budget < est_budget * 0.8:
        st.error(f"⚠️ 安すぎるよ！この街の平均(¥{est_budget:,})より低いと、誰も来てくれないかも…")
    elif budget > est_budget * 1.5:
        st.success("✨ お大臣様！これなら凄腕の勇者が来るよ！")
    else:
        st.info("✅ ちょうどいい相場感だね。")

    if st.button("⚔️ パーティを集める (次へ)", type="primary"):
        st.session_state['quest'] = {"budget": budget, "req_int": req_int, "req_str": req_str}
        st.session_state['phase'] = 'teambuilding'
        st.rerun()

# ==========================================
# Phase 3: チームビルディング (Party)
# ==========================================
elif st.session_state['phase'] == 'teambuilding':
    st.title("🍻 酒場 (チーム編成)")
    st.caption("1人で岩(課題)にぶち当たらなくても大丈夫！")

    q = st.session_state['quest']
    
    # ボス（課題）の強さ表示
    st.markdown("### 🦖 クエストの難易度")
    boss_hp = (q['req_int'] + q['req_str']) * 10
    st.progress(0.0, text=f"BOSS HP: {boss_hp}")
    st.markdown("---")

    col_L, col_R = st.columns([1, 1])

    with col_L:
        st.subheader("🤝 おすすめのパーティ")
        # 自動マッチングロジック
        current_power = 0
        total_fee = 0
        
        for m in GUILD_MEMBERS:
            # 予算内で、スキルが合う人をピックアップ
            if total_fee + m['fee'] <= q['budget']:
                if st.button(f"仲間にする: {m['class']}", key=f"add_{m['id']}"):
                    st.session_state['party'].append(m)
                    st.toast(f"{m['class']} がパーティに加わった！")
        
        st.markdown("---")
        st.text_input("📩 友達を招待する (ID or Email)")
        st.caption("登録してない友達も、招待リンクから即参戦できるよ！")

    with col_R:
        st.subheader("⚔️ 現在の戦力")
        
        # パーティ表示
        if not st.session_state['party']:
            st.warning("まだ誰もいない… 孤独だ…")
        else:
            for p_mem in st.session_state['party']:
                st.success(f"👤 {p_mem['class']}")
                current_power += (p_mem['skills']['INT'] + p_mem['skills']['STR']) * 5
                total_fee += p_mem['fee']
        
        # 勝率計算
        win_rate = min(1.0, current_power / boss_hp) if boss_hp > 0 else 1.0
        st.write(f"勝率予想: {int(win_rate*100)}%")
        st.progress(win_rate)
        
        st.metric("合計報酬", f"¥{total_fee:,}", delta=f"予算残: ¥{q['budget'] - total_fee:,}")

        if win_rate >= 1.0:
            if st.button("🚀 このメンバーで出発！", type="primary"):
                st.session_state['phase'] = 'dungeon'
                st.rerun()
        else:
            st.error("戦力が足りない！もっと仲間を呼ぼう！")

# ==========================================
# Phase 4: 進捗 & 決済 (Dungeon)
# ==========================================
elif st.session_state['phase'] == 'dungeon':
    st.title("🔥 攻略中 (進捗管理)")
    
    # オートパイロットモード
    is_auto = st.toggle("🤖 AIオートパイロットモード", value=True)
    
    if is_auto:
        st.info("AIがチームのチャットログを解析し、進捗を自動更新しています...")
        prog_bar = st.progress(0)
        status_text = st.empty()
        
        # デモ用アニメーション
        for percent in range(0, 101, 20):
            time.sleep(0.5)
            prog_bar.progress(percent)
            if percent < 100:
                status_text.text(f"現在 {percent}% ... 敵の群れを突破中！")
            else:
                status_text.text("🎉 クエストクリア！")
    
    else:
        st.slider("マニュアル進捗管理", 0, 100, 50)
        st.warning("手動モードです。チームに声をかけて進捗を確認してね。")

    st.markdown("---")
    
    # トラブル対応
    with st.expander("🆘 ピンチ！敵が強すぎる（進捗が遅れてる）"):
        st.write("大丈夫、追加の助っ人を呼べるよ。")
        st.button("📞 近いスキルの人に救援要請 (Help)")

    # 決済エリア
    st.markdown("---")
    st.subheader("💰 山分け (決済)")
    
    # まだクリアしてない場合の制御
    if is_auto: # デモなのでオートなら完了扱い
        st.success("成果が出たね！おめでとう！")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write("報酬の分配準備ができました。")
            wallet_ready = st.checkbox("ウォレットは登録した？ (まだなら急いで！)")
        
        with c2:
            if wallet_ready:
                if st.button("💎 報酬を受け取る", type="primary"):
                    st.balloons()
                    st.markdown("## 💸 チャリーン！")
                    st.write("メンバー全員のウォレットに着金しました。")
                    st.write("お疲れ様！次の冒険でまた会おう！")
                    if st.button("最初に戻る"):
                        st.session_state['phase'] = 'register'
                        st.session_state['party'] = []
                        st.rerun()
            else:
                st.button("💎 報酬を受け取る", disabled=True)
