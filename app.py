import streamlit as st
import pandas as pd
import random
import time
import traceback

# --- 0. ゲーム設定 & SBCM定数 ---
st.set_page_config(page_title="Yorbee | SBCM Lite", page_icon="⚔️", layout="wide")

# メソ経済学: 標準ブロック単価 (Standard Unit Price)
# これが全ての価値基準になります
LOCAL_STD_PRICE = 2500

# ==========================================
# 🛡️ 汎用エラー画面
# ==========================================
def show_error_screen(e):
    st.error("💀 通信魔法が途切れました (System Error)")
    with st.expander("詳細ログ"):
        st.code(traceback.format_exc())
    if st.button("🔄 リセット"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 🧠 データ・セッション管理
# ==========================================
def init_session():
    if 'my_stats' not in st.session_state:
        st.session_state['my_stats'] = {"name": "名無しの冒険者", "STR": 5, "INT": 5, "CHA": 5}
    if 'active_quest' not in st.session_state:
        st.session_state['active_quest'] = None
    if 'party' not in st.session_state:
        st.session_state['party'] = []
    if 'wallet' not in st.session_state:
        st.session_state['wallet'] = 0

# モックデータ: ギルドメンバー
GUILD_MEMBERS = [
    {"id": 1, "class": "魔法使い(経理)", "skills": {"INT": 8, "STR": 1}, "fee": 2000},
    {"id": 2, "class": "戦士(肉体派)", "skills": {"INT": 2, "STR": 9}, "fee": 1800},
    {"id": 3, "class": "遊び人(クリエイティブ)", "skills": {"INT": 6, "LUCK": 8}, "fee": 3000},
    {"id": 4, "class": "僧侶(メンター)", "skills": {"CHA": 9, "INT": 4}, "fee": 2500},
]

# ==========================================
# 📺 各ページ画面の定義
# ==========================================

def page_profile():
    st.title("🛡️ 冒険の書 (ステータス)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://api.dicebear.com/7.x/adventurer/svg?seed=" + st.session_state['my_stats']['name'], width=200)
    
    with col2:
        name = st.text_input("名前", st.session_state['my_stats']['name'])
        
        st.caption("現在の能力値")
        c1, c2, c3 = st.columns(3)
        str_s = c1.slider("💪 STR", 1, 10, st.session_state['my_stats']['STR'])
        int_s = c2.slider("🧠 INT", 1, 10, st.session_state['my_stats']['INT'])
        cha_s = c3.slider("💖 CHA", 1, 10, st.session_state['my_stats']['CHA'])
        
        # 保存処理
        st.session_state['my_stats'] = {"name": name, "STR": str_s, "INT": int_s, "CHA": cha_s}
        
        st.info(f"所持金: ¥{st.session_state['wallet']:,}")

    st.divider()
    st.caption("※ ここで設定した能力値に基づいて、クエストの適性が判定されます。")

def page_quest_board():
    st.title("📜 クエストボード (SBCM監査機能付)")
    
    tab1, tab2 = st.tabs(["📝 クエストを作る (発注)", "🔍 クエストを探す (受注)"])
    
    with tab1:
        st.subheader("新しいクエストを張り出す")
        
        with st.container(border=True):
            q_title = st.text_input("クエスト名", "魔王城の決算報告書作成")
            
            c1, c2 = st.columns(2)
            req_int = c1.slider("必要な 🧠 INT", 0, 10, 5, key="q_int")
            req_str = c2.slider("必要な 💪 STR", 0, 10, 2, key="q_str")
            
            # --- ここからSBCMロジック適用 ---
            hours = st.number_input("想定時間 (Hours)", 1, 100, 10)
            
            # 標準予算の計算
            std_budget = hours * LOCAL_STD_PRICE
            st.caption(f"📉 標準ブロック適正価格: ¥{std_budget:,}")
            
            # 実際の予算入力
            budget = st.number_input("報酬額 (¥)", value=std_budget, step=1000)
            
            # 予算歪曲指数 (D_index) の判定
            d_index = budget / std_budget if std_budget > 0 else 0
            is_valid_quest = False
            
            if d_index < 0.5:
                st.error(f"🛑 予算不足: 報酬が標準の{d_index:.0%}しかありません。ブラック案件として却下されます。")
                is_valid_quest = False
            elif d_index > 3.0:
                st.warning(f"⚠️ 予算過剰: 報酬が標準の{d_index:.1f}倍です。不自然な高コスト（ハコモノ案件）の疑いがあります。")
                st.caption("※ SBCM監査により、予算の見直しが推奨されます。")
                is_valid_quest = False 
            else:
                st.success(f"✅ 監査承認: 適正な予算規模です ($D_{{index}}$ = {d_index:.2f})")
                is_valid_quest = True
            
            # 発注ボタン (監査に通らないと押せない)
            if st.button("✨ クエスト発行", type="primary", disabled=not is_valid_quest):
                st.session_state['active_quest'] = {
                    "title": q_title,
                    "budget": budget,
                    "req_int": req_int,
                    "req_str": req_str,
                    "status": "recruiting"
                }
                st.toast("クエストボードに張り出されました！")
                time.sleep(1)
                st.rerun()

    with tab2:
        st.info("現在は受注できるクエストがありません。(デモ版のため発注機能を使ってください)")

def page_party():
    st.title("🍻 酒場 (チーム編成)")
    
    q = st.session_state['active_quest']
    
    if not q:
        st.warning("現在進行中のクエストがありません。「クエストボード」で発注してください。")
        return

    if q['status'] != 'recruiting':
        st.info("このクエストは既に冒険に出発しています。「ダンジョン」を確認してください。")
        return

    st.subheader(f"クエスト: {q['title']}")
    st.metric("予算", f"¥{q['budget']:,}")
    
    col_L, col_R = st.columns([1, 1])
    
    with col_L:
        st.markdown("### 🕵️ 候補者リスト")
        total_fee = sum([m['fee'] for m in st.session_state['party']])
        remaining = q['budget'] - total_fee
        
        st.caption(f"残り予算: ¥{remaining:,}")
        
        for m in GUILD_MEMBERS:
            if m in st.session_state['party']: continue
            
            m_int = m['skills'].get('INT', 0)
            m_str = m['skills'].get('STR', 0)
            is_match = m_int >= q['req_int'] or m_str >= q['req_str']
            
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                c1.markdown(f"**{m['class']}** (Fee: ¥{m['fee']})")
                if is_match: c1.caption("✨ スキル適合")
                
                if m['fee'] <= remaining:
                    if c2.button("勧誘", key=f"inv_{m['id']}"):
                        st.session_state['party'].append(m)
                        st.rerun()
                else:
                    c2.button("予算外", disabled=True)

    with col_R:
        st.markdown("### ⛺ 現在のパーティ")
        
        if not st.session_state['party']:
            st.caption("誰もいません...")
        else:
            current_power = 0
            for p_mem in st.session_state['party']:
                st.success(f"👤 {p_mem['class']}")
                current_power += sum(p_mem['skills'].values()) * 10
            
            boss_hp = (q['req_int'] + q['req_str']) * 20
            win_rate = min(1.0, current_power / boss_hp)
            
            st.write(f"攻略成功率: {int(win_rate*100)}%")
            st.progress(win_rate)
            
            if win_rate >= 1.0:
                if st.button("🚀 このメンバーで出発する！", type="primary", use_container_width=True):
                    st.session_state['active_quest']['status'] = 'active'
                    st.balloons()
                    st.toast("ダンジョンへ移動しました！サイドバーから移動してください。")

def page_dungeon():
    st.title("🔥 ダンジョン (進捗管理)")
    
    q = st.session_state['active_quest']
    
    if not q or q['status'] == 'recruiting':
        st.warning("現在攻略中のクエストはありません。酒場でパーティを組んで出発してください。")
        return
    
    st.subheader(f"攻略中: {q['title']}")
    st.info("🤖 AIオートパイロット: ON")
    
    if q['status'] == 'active':
        my_bar = st.progress(0)
        status = st.empty()
        
        for i in range(101):
            time.sleep(0.02)
            my_bar.progress(i)
            if i < 100:
                status.caption(f"進捗... {i}%")
            else:
                status.success("🎉 クエストクリア！")
                st.session_state['active_quest']['status'] = 'cleared'
                st.rerun()
                
    elif q['status'] == 'cleared':
        st.progress(100)
        st.success("🎉 クエストクリア！")
        
        st.markdown("---")
        st.subheader("💰 報酬の分配")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("パーティメンバーへの送金準備完了")
            for m in st.session_state['party']:
                st.text(f"💸 {m['class']} へ ¥{m['fee']} 送金")
        
        with col2:
            remain = q['budget'] - sum([m['fee'] for m in st.session_state['party']])
            st.metric("あなたの取り分 (管理費)", f"¥{remain:,}")
            
            if st.button("💎 報酬を受け取って解散", type="primary"):
                st.session_state['wallet'] += remain
                st.session_state['active_quest'] = None
                st.session_state['party'] = []
                st.balloons()
                st.success("お疲れ様でした！次のクエストを探しましょう。")
                time.sleep(2)
                st.rerun()

# ==========================================
# 🚀 メインルーチン
# ==========================================
def main():
    init_session()

    with st.sidebar:
        st.header("Yorbee Menu")
        st.caption(f"冒険者: {st.session_state['my_stats']['name']}")
        st.caption(f"所持金: ¥{st.session_state['wallet']:,}")
        st.divider()
        
        selection = st.radio(
            "移動先",
            ["冒険の書 (Profile)", "クエストボード (Job)", "酒場 (Team)", "ダンジョン (Work)"],
            index=1 # デモのためJobからスタート
        )
        st.divider()
        st.info("💡 サイドバーでいつでも画面を切り替えられます")

    if selection == "冒険の書 (Profile)":
        page_profile()
    elif selection == "クエストボード (Job)":
        page_quest_board()
    elif selection == "酒場 (Team)":
        page_party()
    elif selection == "ダンジョン (Work)":
        page_dungeon()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_error_screen(e)
