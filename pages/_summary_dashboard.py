#!/usr/bin/env python3
"""
統合サマリーダッシュボード
全ての複雑な機能を統合した一元管理ページ
Google Spreadsheetsへの直接出力機能付き
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import asyncio
from typing import Dict, Any, List

# 必要なモジュールのインポート
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_chain_pipeline import get_ai_chain_pipeline
from utils.google_sheets_db import get_db, GoogleSheetsDB
from utils.sheets_exporter import get_sheets_exporter

# ページ設定
st.set_page_config(
    page_title="統合サマリーダッシュボード",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    /* メインヘッダー */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        border: 2px solid #3b82f6;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* セクションカード */
    .section-card {
        background: rgba(30, 41, 59, 0.5);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* メトリクスカード */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* データテーブル */
    .data-table {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    /* アクションボタン */
    .action-button {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%;
        margin: 10px 0;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* Sheets出力エリア */
    .sheets-output {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #10b981;
        margin: 20px 0;
    }
    
    .sheets-title {
        color: #10b981;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    /* タブスタイル */
    .tab-container {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* ステータスインジケーター */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background-color: #10b981; }
    .status-pending { background-color: #f59e0b; }
    .status-completed { background-color: #3b82f6; }
    .status-failed { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'summary_data' not in st.session_state:
    st.session_state.summary_data = {}
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'export_status' not in st.session_state:
    st.session_state.export_status = {}

# ヘッダー
st.markdown("""
<div class="main-header">
    <h1 class="main-title">📋 統合サマリーダッシュボード</h1>
    <p style="color: #94a3b8;">全ての分析結果を一元管理・可視化・Sheets出力</p>
</div>
""", unsafe_allow_html=True)

# Sheets接続確認
def check_sheets_connection():
    """Google Sheets接続状態を確認"""
    try:
        db = get_db()
        return db.spreadsheet is not None
    except:
        return False

# データ統合関数
def integrate_all_data():
    """全ての分析データを統合"""
    integrated_data = {
        'ai_pipeline_results': {},
        'project_data': {},
        'market_analysis': {},
        'competitor_analysis': {},
        'financial_projections': {},
        'marketing_strategy': {}
    }
    
    # AIパイプライン結果の統合
    if hasattr(st.session_state, 'pipeline_results') and st.session_state.pipeline_results:
        integrated_data['ai_pipeline_results'] = st.session_state.pipeline_results
    
    # プロジェクトデータの統合
    if hasattr(st.session_state, 'projects') and st.session_state.projects:
        integrated_data['project_data'] = st.session_state.projects
    
    # AIで生成されたプロジェクトデータの統合
    if hasattr(st.session_state, 'current_ai_project'):
        ai_project = st.session_state.current_ai_project
        if 'ai_analysis' in ai_project:
            integrated_data['market_analysis'] = ai_project['ai_analysis'].get('market_analysis', '')
            integrated_data['competitor_analysis'] = ai_project['ai_analysis'].get('competitor_analysis', '')
            integrated_data['marketing_strategy'] = ai_project['ai_analysis'].get('go_to_market_strategy', '')
    
    return integrated_data

# メイン分析ダッシュボード
def render_main_dashboard(data):
    """メイン分析ダッシュボードを表示"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">総プロジェクト数</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(len(data.get('project_data', {}))), unsafe_allow_html=True)
    
    with col2:
        pipeline_count = len(data.get('ai_pipeline_results', {}))
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AI分析完了</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(pipeline_count), unsafe_allow_html=True)
    
    with col3:
        market_analysis_count = 1 if data.get('market_analysis') else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">市場分析</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(market_analysis_count), unsafe_allow_html=True)
    
    with col4:
        strategy_count = 1 if data.get('marketing_strategy') else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">戦略策定</div>
            <div class="metric-value">{}</div>
        </div>
        """.format(strategy_count), unsafe_allow_html=True)

# プロジェクト選択
def render_project_selector(data):
    """プロジェクト選択UI"""
    st.markdown("""
    <div class="section-card">
        <div class="section-title">📁 プロジェクト選択</div>
    </div>
    """, unsafe_allow_html=True)
    
    projects = data.get('project_data', {})
    if not projects:
        st.info("📝 プロジェクトがありません。AIパイプラインスタジオで新しいプロジェクトを作成してください。")
        if st.button("🏭 AIパイプラインスタジオへ", type="primary"):
            st.switch_page("pages/_ai_pipeline_studio.py")
        return None
    
    project_options = {}
    for project_id, project in projects.items():
        name = project.get('name', f'プロジェクト {project_id}')
        status = project.get('status', '不明')
        created_at = project.get('created_at', '日時不明')
        project_options[f"{name} ({status}) - {created_at}"] = project_id
    
    selected_display = st.selectbox(
        "分析するプロジェクトを選択",
        list(project_options.keys())
    )
    
    if selected_display:
        selected_id = project_options[selected_display]
        st.session_state.selected_project = selected_id
        return projects[selected_id]
    
    return None

# 分析結果表示
def render_analysis_results(project_data):
    """分析結果を表示"""
    if not project_data:
        return
    
    # タブ作成
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 概要分析", "🏪 市場分析", "🎯 競合分析", 
        "👥 ペルソナ", "💰 ビジネス戦略"
    ])
    
    with tab1:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">📊 プロジェクト概要</div>
        </div>
        """, unsafe_allow_html=True)
        
        basic_info = {
            "プロジェクト名": project_data.get('name', 'N/A'),
            "カテゴリ": project_data.get('type', 'N/A'),
            "ステータス": project_data.get('status', 'N/A'),
            "作成日": project_data.get('created_at', 'N/A')
        }
        
        for key, value in basic_info.items():
            st.info(f"**{key}**: {value}")
        
        # プロジェクトの技術スタック
        if 'tech_stack' in project_data:
            st.markdown("#### 💻 技術スタック")
            tech_stack = project_data['tech_stack']
            for tech_type, tech_value in tech_stack.items():
                if tech_value:
                    st.text(f"• {tech_type}: {tech_value}")
    
    with tab2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">🏪 市場分析結果</div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'ai_analysis' in project_data and 'market_analysis' in project_data['ai_analysis']:
            market_analysis = project_data['ai_analysis']['market_analysis']
            st.markdown(market_analysis)
        else:
            st.info("市場分析データがありません。AIパイプラインで分析を実行してください。")
    
    with tab3:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">🎯 競合分析結果</div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'ai_analysis' in project_data and 'competitor_analysis' in project_data['ai_analysis']:
            competitor_analysis = project_data['ai_analysis']['competitor_analysis']
            st.markdown(competitor_analysis)
        else:
            st.info("競合分析データがありません。AIパイプラインで分析を実行してください。")
    
    with tab4:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">👥 ターゲットペルソナ</div>
        </div>
        """, unsafe_allow_html=True)
        
        if 'ai_analysis' in project_data and 'target_personas' in project_data['ai_analysis']:
            personas = project_data['ai_analysis']['target_personas']
            st.markdown(personas)
        else:
            st.info("ペルソナデータがありません。AIパイプラインで分析を実行してください。")
    
    with tab5:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">💰 ビジネス戦略</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 価格戦略
        if 'ai_analysis' in project_data and 'pricing_strategy' in project_data['ai_analysis']:
            st.markdown("#### 💵 価格戦略")
            pricing_strategy = project_data['ai_analysis']['pricing_strategy']
            st.markdown(pricing_strategy)
        
        # GTM戦略
        if 'ai_analysis' in project_data and 'go_to_market_strategy' in project_data['ai_analysis']:
            st.markdown("#### 🚀 Go-to-Market戦略")
            gtm_strategy = project_data['ai_analysis']['go_to_market_strategy']
            st.markdown(gtm_strategy)

# Google Sheets出力機能
def render_sheets_export(project_data):
    """Google Sheets出力機能"""
    st.markdown("""
    <div class="sheets-output">
        <div class="sheets-title">📊 Google Sheets出力</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not check_sheets_connection():
        st.error("📊 Google Sheetsに接続されていません。設定ページで接続してください。")
        if st.button("⚙️ 設定ページへ"):
            st.switch_page("pages/_sheets_settings.py")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 出力オプション")
        
        export_options = st.multiselect(
            "出力する分析結果を選択",
            [
                "プロジェクト基本情報",
                "市場分析",
                "競合分析", 
                "ターゲットペルソナ",
                "機能設計",
                "価格戦略",
                "Go-to-Market戦略"
            ],
            default=["プロジェクト基本情報", "市場分析", "競合分析"]
        )
        
        sheet_name = st.text_input(
            "シート名",
            value=f"分析結果_{datetime.now().strftime('%Y%m%d_%H%M')}"
        )
        
        include_timestamp = st.checkbox("タイムスタンプを含める", value=True)
        format_as_table = st.checkbox("テーブル形式で出力", value=True)
    
    with col2:
        st.markdown("#### 📊 プレビュー")
        
        if project_data and export_options:
            preview_data = prepare_export_data(project_data, export_options, include_timestamp)
            st.json(preview_data, expanded=False)
        else:
            st.info("プロジェクトと出力オプションを選択してください")
    
    # 出力実行ボタン
    if st.button("📤 Google Sheetsに出力", type="primary", use_container_width=True):
        if project_data and export_options:
            try:
                success = export_to_sheets(project_data, export_options, sheet_name, include_timestamp, format_as_table)
                if success:
                    st.success("✅ Google Sheetsに正常に出力されました！")
                    st.balloons()
                else:
                    st.error("❌ 出力に失敗しました")
            except Exception as e:
                st.error(f"❌ エラー: {str(e)}")
        else:
            st.error("プロジェクトと出力オプションを選択してください")

def prepare_export_data(project_data, options, include_timestamp):
    """出力用データを準備"""
    export_data = {}
    
    if include_timestamp:
        export_data['出力日時'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if "プロジェクト基本情報" in options:
        export_data['プロジェクト基本情報'] = {
            'プロジェクト名': project_data.get('name', ''),
            'カテゴリ': project_data.get('type', ''),
            'ステータス': project_data.get('status', ''),
            '作成日': project_data.get('created_at', '')
        }
    
    if "市場分析" in options and 'ai_analysis' in project_data:
        export_data['市場分析'] = project_data['ai_analysis'].get('market_analysis', '')
    
    if "競合分析" in options and 'ai_analysis' in project_data:
        export_data['競合分析'] = project_data['ai_analysis'].get('competitor_analysis', '')
    
    if "ターゲットペルソナ" in options and 'ai_analysis' in project_data:
        export_data['ターゲットペルソナ'] = project_data['ai_analysis'].get('target_personas', '')
    
    if "機能設計" in options and 'ai_analysis' in project_data:
        export_data['機能設計'] = project_data['ai_analysis'].get('feature_design', '')
    
    if "価格戦略" in options and 'ai_analysis' in project_data:
        export_data['価格戦略'] = project_data['ai_analysis'].get('pricing_strategy', '')
    
    if "Go-to-Market戦略" in options and 'ai_analysis' in project_data:
        export_data['Go-to-Market戦略'] = project_data['ai_analysis'].get('go_to_market_strategy', '')
    
    return export_data

def export_to_sheets(project_data, options, sheet_name, include_timestamp, format_as_table):
    """Google Sheetsに実際にデータを出力（高度なエクスポーター使用）"""
    try:
        exporter = get_sheets_exporter()
        
        if format_as_table:
            # 構造化されたテーブル形式で出力
            success = exporter.export_to_structured_sheet(project_data, options, sheet_name)
        else:
            # ダッシュボード形式で出力
            success = exporter.export_to_analysis_dashboard(project_data)
        
        return success
        
    except Exception as e:
        st.error(f"出力エラー: {str(e)}")
        return False

# メイン処理
def main():
    # データ統合
    integrated_data = integrate_all_data()
    
    # メインダッシュボード
    render_main_dashboard(integrated_data)
    
    st.markdown("---")
    
    # プロジェクト選択
    selected_project = render_project_selector(integrated_data)
    
    if selected_project:
        st.markdown("---")
        
        # 分析結果表示
        render_analysis_results(selected_project)
        
        st.markdown("---")
        
        # Sheets出力
        render_sheets_export(selected_project)

# サイドバー
with st.sidebar:
    st.header("📋 サマリーダッシュボード")
    
    st.markdown("""
    ### 💡 機能一覧
    
    - **📊 統合分析表示**
      - 全プロジェクト概要
      - AI分析結果の一覧
    
    - **📁 プロジェクト管理**
      - プロジェクト選択
      - 詳細分析表示
    
    - **📊 Google Sheets出力**
      - 選択式データ出力
      - テーブル/JSON形式
      - カスタムシート名
    
    - **🎯 可視化統合**
      - 全ての複雑な分析を統合
      - リアルタイム更新
    """)
    
    st.markdown("---")
    
    # クイックアクション
    st.header("⚡ クイックアクション")
    
    if st.button("🏭 新規AI分析", use_container_width=True):
        st.switch_page("pages/_ai_pipeline_studio.py")
    
    if st.button("⚙️ Sheets設定", use_container_width=True):
        st.switch_page("pages/_sheets_settings.py")
    
    if st.button("🏠 ホーム", use_container_width=True):
        st.switch_page("app.py")
    
    st.markdown("---")
    
    # 接続ステータス
    st.header("🔗 接続ステータス")
    
    sheets_connected = check_sheets_connection()
    status_color = "🟢" if sheets_connected else "🔴"
    status_text = "接続済み" if sheets_connected else "未接続"
    
    st.markdown(f"""
    **Google Sheets**: {status_color} {status_text}
    """)
    
    if sheets_connected:
        st.success("出力準備完了")
    else:
        st.warning("設定が必要")

if __name__ == "__main__":
    main()