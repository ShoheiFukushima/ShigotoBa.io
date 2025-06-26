import streamlit as st

st.set_page_config(page_title="広告・マーケ", page_icon="🎨", layout="wide")

# ヘッダーとサイドバー
try:
    from components.header import render_header
    render_header()
except:
    pass

try:
    from components.sidebar_simple import render_sidebar
    render_sidebar()
except:
    pass

st.title("🎨 広告・マーケ")

# ツールメニュー
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎨 AI Creative Studio", use_container_width=True):
        st.switch_page("pages_backup/ai_creative_studio.py")
    if st.button("⚡ リアルタイム広告最適化", use_container_width=True):
        st.switch_page("pages_backup/realtime_ad_optimizer.py")
        
with col2:
    if st.button("💰 価格戦略コンサルティング", use_container_width=True):
        st.switch_page("pages_backup/pricing_strategy.py")
    if st.button("🌐 マルチプラットフォーム管理", use_container_width=True):
        st.switch_page("pages_backup/multi_platform_manager.py")
        
with col3:
    if st.button("🚀 自動投稿", use_container_width=True):
        st.switch_page("pages_backup/auto_posting.py")
    if st.button("📋 ツール一覧", use_container_width=True):
        st.switch_page("pages_backup/marketing_tools_list.py")