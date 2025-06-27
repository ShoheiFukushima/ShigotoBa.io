"""
ツール検索機能コンポーネント
全ツールから目的のツールを素早く検索
"""

import streamlit as st
from typing import List, Dict, Optional, Tuple
import re

# 全ツールのデータベース
TOOLS_DATABASE = [
    # 新規開発カテゴリ
    {"id": "dev_room", "name": "開発室", "icon": "🏗️", "category": "開発", 
     "tags": ["タスク管理", "進捗", "開発", "プロジェクト"], "path": "pages/_development_room.py"},
    {"id": "project_mgmt", "name": "プロジェクト管理室", "icon": "📊", "category": "開発",
     "tags": ["プロジェクト", "管理", "監視", "全体"], "path": "pages/_project_management.py"},
    {"id": "product_mgmt", "name": "プロダクト管理", "icon": "📦", "category": "開発",
     "tags": ["製品", "ライフサイクル", "プロダクト", "管理"], "path": "pages/_product_management.py"},
    {"id": "ab_test", "name": "A/Bテスト", "icon": "🧪", "category": "開発",
     "tags": ["テスト", "実験", "効果測定", "AB"], "path": "pages/_ab_testing.py"},
    {"id": "new_product", "name": "新製品", "icon": "📋", "category": "開発",
     "tags": ["新規", "製品", "開発", "企画"], "path": "pages/_new_product.py"},
    
    # 運営・分析カテゴリ
    {"id": "performance", "name": "パフォーマンスダッシュボード", "icon": "📈", "category": "分析",
     "tags": ["パフォーマンス", "KPI", "監視", "ダッシュボード"], "path": "pages/_performance_dashboard.py"},
    {"id": "attribution", "name": "アトリビューション分析", "icon": "🎯", "category": "分析",
     "tags": ["効果測定", "要因分析", "ROI", "アトリビューション"], "path": "pages/_attribution_analysis.py"},
    {"id": "journey", "name": "カスタマージャーニー", "icon": "🛤️", "category": "分析",
     "tags": ["顧客", "体験", "ジャーニー", "最適化"], "path": "pages/_customer_journey_engine.py"},
    {"id": "product_analysis", "name": "プロダクト分析", "icon": "📊", "category": "分析",
     "tags": ["製品分析", "データ", "インサイト", "改善"], "path": "pages/_product_analysis.py"},
    {"id": "ai_chat", "name": "AIチャット", "icon": "💬", "category": "分析",
     "tags": ["AI", "チャット", "支援", "Gemini"], "path": "pages/_realtime_chat.py"},
    
    # 広告・マーケティングカテゴリ
    {"id": "creative", "name": "AI Creative Studio", "icon": "🎨", "category": "マーケティング",
     "tags": ["クリエイティブ", "AI", "デザイン", "自動生成"], "path": "pages/_ai_creative_studio.py"},
    {"id": "ad_optimizer", "name": "リアルタイム広告最適化", "icon": "⚡", "category": "マーケティング",
     "tags": ["広告", "最適化", "リアルタイム", "運用"], "path": "pages/_realtime_ad_optimizer.py"},
    {"id": "pricing", "name": "価格戦略コンサルティング", "icon": "💰", "category": "マーケティング",
     "tags": ["価格", "戦略", "最適化", "コンサルティング"], "path": "pages/_pricing_strategy.py"},
    {"id": "multi_platform", "name": "マルチプラットフォーム管理", "icon": "🌐", "category": "マーケティング",
     "tags": ["マルチ", "プラットフォーム", "統合", "管理"], "path": "pages/_multi_platform_manager.py"},
    {"id": "auto_post", "name": "自動投稿", "icon": "🚀", "category": "マーケティング",
     "tags": ["自動", "投稿", "スケジュール", "SNS"], "path": "pages/_auto_posting.py"},
]

def search_tools(query: str) -> List[Dict]:
    """ツールを検索"""
    if not query:
        return TOOLS_DATABASE
    
    query_lower = query.lower()
    results = []
    
    for tool in TOOLS_DATABASE:
        # スコア計算
        score = 0
        
        # 名前に含まれる場合は高スコア
        if query_lower in tool["name"].lower():
            score += 10
        
        # カテゴリに含まれる場合
        if query_lower in tool["category"].lower():
            score += 5
        
        # タグに含まれる場合
        for tag in tool["tags"]:
            if query_lower in tag.lower():
                score += 3
        
        # アイコンで検索（絵文字検索対応）
        if query in tool["icon"]:
            score += 8
        
        if score > 0:
            results.append((tool, score))
    
    # スコアでソート
    results.sort(key=lambda x: x[1], reverse=True)
    
    return [tool for tool, _ in results]

def render_search_box() -> Optional[str]:
    """検索ボックスを表示"""
    search_query = st.text_input(
        "🔍 ツールを検索",
        placeholder="例: タスク管理、AI、広告...",
        key="tool_search"
    )
    return search_query

def render_search_results(results: List[Dict], query: str):
    """検索結果を表示"""
    if not query:
        return
    
    if results:
        st.markdown(f"### 検索結果: '{query}' ({len(results)}件)")
        
        # 結果をグリッド表示
        cols_per_row = 3
        for i in range(0, len(results), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(results):
                    tool = results[i + j]
                    with col:
                        st.markdown(f"""
                        <div style="background: #1e293b; border: 1px solid #334155;
                                    border-radius: 8px; padding: 1rem; height: 120px;">
                            <h4 style="color: #22c55e; margin: 0;">
                                {tool['icon']} {tool['name']}
                            </h4>
                            <p style="color: #64748b; font-size: 0.8rem; margin: 0.2rem 0;">
                                {tool['category']}
                            </p>
                            <p style="color: #94a3b8; font-size: 0.75rem; margin: 0.5rem 0;">
                                {', '.join(tool['tags'][:3])}...
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("開く", key=f"open_{tool['id']}", use_container_width=True):
                            # お気に入り機能と連携
                            if 'favorites' in st.session_state:
                                from components.favorites import add_to_recent
                                add_to_recent(tool['id'], tool['name'], tool['icon'], tool['path'])
                            st.switch_page(tool['path'])
    else:
        st.warning(f"'{query}' に一致するツールが見つかりませんでした")
        
        # 候補を提案
        st.markdown("### 💡 こちらをお探しですか？")
        suggestions = get_suggestions(query)
        if suggestions:
            for suggestion in suggestions[:3]:
                if st.button(f"{suggestion['icon']} {suggestion['name']}", 
                           key=f"suggest_{suggestion['id']}"):
                    st.switch_page(suggestion['path'])

def render_search_modal():
    """検索モーダル（全画面検索）"""
    if st.session_state.get('show_search_modal', False):
        st.markdown("""
        <style>
        .search-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 9999;
            display: flex;
            flex-direction: column;
            padding: 2rem;
        }
        .search-input-large {
            font-size: 2rem;
            padding: 1rem;
            background: #1e293b;
            border: 2px solid #22c55e;
            border-radius: 12px;
            color: #f1f5f9;
            width: 100%;
            margin-bottom: 2rem;
        }
        .search-results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            overflow-y: auto;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 検索入力
        query = st.text_input(
            "",
            placeholder="ツールを検索... (ESCで閉じる)",
            key="modal_search",
            label_visibility="collapsed"
        )
        
        # 検索結果
        if query:
            results = search_tools(query)
            render_search_results(results, query)
        else:
            # カテゴリ別表示
            render_tools_by_category()
        
        # 閉じるボタン
        if st.button("✕ 閉じる", key="close_search"):
            st.session_state.show_search_modal = False
            st.rerun()

def render_tools_by_category():
    """カテゴリ別にツールを表示"""
    categories = {}
    for tool in TOOLS_DATABASE:
        cat = tool["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tool)
    
    for category, tools in categories.items():
        st.markdown(f"### {get_category_icon(category)} {category}")
        
        cols = st.columns(4)
        for i, tool in enumerate(tools):
            with cols[i % 4]:
                if st.button(f"{tool['icon']} {tool['name']}", 
                           key=f"cat_{tool['id']}", 
                           use_container_width=True):
                    st.switch_page(tool['path'])

def get_category_icon(category: str) -> str:
    """カテゴリのアイコンを取得"""
    icons = {
        "開発": "🏗️",
        "分析": "📊",
        "マーケティング": "🎨"
    }
    return icons.get(category, "📋")

def get_suggestions(query: str) -> List[Dict]:
    """検索クエリに基づいて提案を生成"""
    # 簡単な類似度チェック
    suggestions = []
    query_lower = query.lower()
    
    # 部分一致でスコアリング
    for tool in TOOLS_DATABASE:
        score = 0
        for word in query_lower.split():
            if word in tool["name"].lower():
                score += 2
            for tag in tool["tags"]:
                if word in tag.lower():
                    score += 1
        
        if score > 0:
            suggestions.append((tool, score))
    
    suggestions.sort(key=lambda x: x[1], reverse=True)
    return [tool for tool, _ in suggestions[:5]]

def render_quick_search_button():
    """クイック検索ボタン（ヘッダー用）"""
    if st.button("🔍", key="quick_search_btn", help="ツールを検索"):
        st.session_state.show_search_modal = True
        st.rerun()