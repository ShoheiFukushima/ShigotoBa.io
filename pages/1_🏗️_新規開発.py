import streamlit as st

st.set_page_config(page_title="新規開発", page_icon="🏗️", layout="wide")

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

st.title("🏗️ 新規開発")

# ツールメニュー
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏗️ 開発室", use_container_width=True):
        st.switch_page("pages/_development_room.py")
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/_project_management.py")
        
with col2:
    if st.button("📦 プロダクト管理", use_container_width=True):
        st.switch_page("pages/_product_management.py")
    if st.button("🧪 A/Bテスト", use_container_width=True):
        st.switch_page("pages/_ab_testing.py")
        
with col3:
    if st.button("📋 新製品", use_container_width=True):
        st.switch_page("pages/_new_product.py")
    if st.button("📋 ツール一覧", use_container_width=True):
        st.switch_page("pages/_dev_tools_list.py")