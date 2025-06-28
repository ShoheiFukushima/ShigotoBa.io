#!/usr/bin/env python3
"""
Google Sheets設定ページ
"""

import streamlit as st
import os
import sys
from datetime import datetime

# パスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ページ設定
st.set_page_config(
    page_title="Google Sheets設定",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* ダークモード設定 */
    .stApp {
        background-color: #0e1117;
    }
    
    /* 設定カード */
    .settings-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    .status-connected {
        color: #10b981;
        font-weight: bold;
    }
    
    .status-disconnected {
        color: #ef4444;
        font-weight: bold;
    }
    
    .sheet-link {
        color: #3b82f6;
        text-decoration: none;
        font-weight: bold;
    }
    
    .sheet-link:hover {
        text-decoration: underline;
    }
    
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    .sync-button {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .sync-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Google Sheets データベース設定")

# 設定状態を確認
try:
    from utils.google_sheets_db import get_db
    db = get_db()
    connection_status = db.spreadsheet is not None
    spreadsheet_url = db.get_spreadsheet_url() if connection_status else None
    spreadsheet_id = db.spreadsheet_id if connection_status else None
except Exception as e:
    connection_status = False
    spreadsheet_url = None
    spreadsheet_id = None
    error_message = str(e)

# 接続状態表示
st.markdown("### 🔌 接続状態")

col1, col2 = st.columns([2, 1])

with col1:
    if connection_status:
        st.markdown('<p class="status-connected">✅ 接続済み</p>', unsafe_allow_html=True)
        if spreadsheet_url:
            st.markdown(f'<p>スプレッドシート: <a href="{spreadsheet_url}" target="_blank" class="sheet-link">Google Sheetsで開く</a></p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-disconnected">❌ 未接続</p>', unsafe_allow_html=True)
        if 'error_message' in locals():
            st.error(f"エラー: {error_message}")

with col2:
    if st.button("🔄 接続を再試行", key="retry_connection"):
        with st.spinner("接続中..."):
            try:
                from utils.google_sheets_db import GoogleSheetsDB
                # 新しいインスタンスを作成
                import utils.google_sheets_db as sheets_module
                sheets_module._db_instance = None
                db = sheets_module.get_db()
                st.success("接続に成功しました！")
                st.rerun()
            except Exception as e:
                st.error(f"接続に失敗しました: {str(e)}")

# 設定情報
st.markdown("### ⚙️ 設定情報")

settings_col1, settings_col2 = st.columns(2)

with settings_col1:
    st.markdown("""
    <div class="settings-card">
        <h4>📄 認証情報</h4>
        <p>現在の設定:</p>
        <ul>
            <li>credentials.json: {"✅ 存在" if os.path.exists('credentials.json') else "❌ 未設定"}</li>
            <li>環境変数 GOOGLE_SHEETS_CREDENTIALS: {"✅ 設定済み" if os.getenv('GOOGLE_SHEETS_CREDENTIALS') else "❌ 未設定"}</li>
            <li>環境変数 GOOGLE_SHEETS_ID: {"✅ 設定済み" if os.getenv('GOOGLE_SHEETS_ID') else "❌ 未設定"}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with settings_col2:
    st.markdown(f"""
    <div class="settings-card">
        <h4>📊 スプレッドシート情報</h4>
        <p>現在の状態:</p>
        <ul>
            <li>スプレッドシートID: {spreadsheet_id or "未設定"}</li>
            <li>データシート数: {"4" if connection_status else "N/A"}</li>
            <li>最終同期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S') if connection_status else "N/A"}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# データ同期
st.markdown("### 🔄 データ同期")

sync_col1, sync_col2, sync_col3 = st.columns(3)

with sync_col1:
    if st.button("📥 データを読み込む", key="load_data", use_container_width=True):
        if connection_status:
            with st.spinner("データを読み込み中..."):
                try:
                    from utils.google_sheets_db import sync_sheets_to_session
                    sync_sheets_to_session()
                    st.success("データの読み込みが完了しました！")
                except Exception as e:
                    st.error(f"読み込みエラー: {str(e)}")
        else:
            st.error("Google Sheetsに接続されていません")

with sync_col2:
    if st.button("📤 データを保存する", key="save_data", use_container_width=True):
        if connection_status:
            with st.spinner("データを保存中..."):
                try:
                    from utils.google_sheets_db import sync_session_to_sheets
                    sync_session_to_sheets()
                    st.success("データの保存が完了しました！")
                except Exception as e:
                    st.error(f"保存エラー: {str(e)}")
        else:
            st.error("Google Sheetsに接続されていません")

with sync_col3:
    if st.button("♻️ 自動同期を有効化", key="auto_sync", use_container_width=True):
        st.session_state.auto_sync_enabled = not st.session_state.get('auto_sync_enabled', False)
        if st.session_state.auto_sync_enabled:
            st.success("自動同期を有効にしました")
        else:
            st.info("自動同期を無効にしました")

# 現在のデータ状況
if connection_status:
    st.markdown("### 📊 データ状況")
    
    data_col1, data_col2, data_col3 = st.columns(3)
    
    with data_col1:
        projects_count = len(st.session_state.get('projects', {}))
        st.metric("プロジェクト数", projects_count)
    
    with data_col2:
        todos_count = len(st.session_state.get('todos', []))
        st.metric("TODOアイテム数", todos_count)
    
    with data_col3:
        auto_sync_status = "有効" if st.session_state.get('auto_sync_enabled', False) else "無効"
        st.metric("自動同期", auto_sync_status)

# セットアップガイド
with st.expander("📚 セットアップガイド", expanded=not connection_status):
    st.markdown("""
    ### Google Sheets接続のセットアップ手順
    
    1. **Google Cloud Consoleでプロジェクトを作成**
       - [Google Cloud Console](https://console.cloud.google.com/)にアクセス
       - 新しいプロジェクトを作成または既存のプロジェクトを選択
    
    2. **必要なAPIを有効化**
       - Google Sheets API
       - Google Drive API
    
    3. **サービスアカウントを作成**
       - 「APIとサービス」→「認証情報」→「認証情報を作成」→「サービスアカウント」
       - JSONキーをダウンロード
    
    4. **認証情報を設定**
       - ダウンロードしたJSONファイルを`credentials.json`として保存
       - または環境変数`GOOGLE_SHEETS_CREDENTIALS`に設定
    
    5. **スプレッドシートを作成**
       - 新しいGoogle Sheetsを作成
       - サービスアカウントのメールアドレスに編集権限を付与
    
    詳細な手順は[設定ドキュメント](./docs/GOOGLE_SHEETS_SETUP.md)を参照してください。
    """)

# トラブルシューティング
with st.expander("🔧 トラブルシューティング"):
    st.markdown("""
    ### よくある問題と解決方法
    
    **Q: 「認証情報が見つかりません」エラーが出る**
    - A: `credentials.json`ファイルが正しい場所にあるか確認してください
    
    **Q: 「APIが有効化されていません」エラーが出る**
    - A: Google Cloud ConsoleでSheets APIとDrive APIが有効になっているか確認してください
    
    **Q: 「権限がありません」エラーが出る**
    - A: スプレッドシートにサービスアカウントのメールアドレスが編集者として追加されているか確認してください
    
    **Q: データが同期されない**
    - A: 「データを保存する」ボタンをクリックして手動で同期してみてください
    """)

# 戻るボタン
st.markdown("---")
if st.button("⬅️ ホームに戻る", type="secondary"):
    st.switch_page("app.py")