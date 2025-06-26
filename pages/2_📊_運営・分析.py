import streamlit as st

st.set_page_config(page_title="運営・分析", page_icon="📊", layout="wide")

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

st.title("📊 運営・分析")

# ツールメニュー
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📈 パフォーマンスダッシュボード", use_container_width=True):
        st.switch_page("pages_backup/performance_dashboard.py")
    if st.button("🎯 アトリビューション分析", use_container_width=True):
        st.switch_page("pages_backup/attribution_analysis.py")
        
with col2:
    if st.button("🛤️ カスタマージャーニー", use_container_width=True):
        st.switch_page("pages_backup/customer_journey_engine.py")
    if st.button("📊 プロダクト分析", use_container_width=True):
        st.switch_page("pages_backup/product_analysis.py")
        
with col3:
    if st.button("💬 AIチャット", use_container_width=True):
        st.switch_page("pages_backup/realtime_chat.py")
    if st.button("📋 ツール一覧", use_container_width=True):
        st.switch_page("pages_backup/analysis_tools_list.py")