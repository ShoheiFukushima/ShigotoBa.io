#!/usr/bin/env python3
"""
自動投稿管理ダッシュボード
SNS自動投稿の設定・スケジュール・監視
"""

import streamlit as st
import sys
import os
import asyncio
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.social_media_integrations import social_manager, PlatformType, PostStatus, validate_api_keys, quick_post
from config.ai_models import TaskType
from config.ai_client import ai_client

# ページ設定
st.set_page_config(
    page_title="自動投稿管理",
    page_icon="📱",
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
    
    /* プラットフォームカード */
    .platform-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        transition: all 0.3s;
    }
    
    .platform-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .platform-card.connected {
        border-color: #10b981;
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
    }
    
    .platform-card.disconnected {
        border-color: #ef4444;
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
    }
    
    .platform-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .platform-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e2e8f0;
    }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-connected {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .status-disconnected {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    /* 投稿エディター */
    .post-editor {
        background: rgba(30, 41, 59, 0.8);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 20px 0;
    }
    
    .editor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .editor-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #3b82f6;
    }
    
    .character-count {
        font-size: 0.9rem;
        color: #94a3b8;
    }
    
    .over-limit {
        color: #ef4444;
        font-weight: bold;
    }
    
    /* 投稿履歴 */
    .post-history-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid;
    }
    
    .post-published {
        border-left-color: #10b981;
    }
    
    .post-failed {
        border-left-color: #ef4444;
    }
    
    .post-scheduled {
        border-left-color: #f59e0b;
    }
    
    .post-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .platform-icon {
        font-size: 1.2rem;
        margin-right: 8px;
    }
    
    .post-time {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    /* スケジューラー */
    .schedule-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .schedule-slot {
        background: rgba(30, 41, 59, 0.8);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        text-align: center;
    }
    
    .schedule-time {
        font-size: 1.1rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 10px;
    }
    
    .schedule-content {
        color: #e2e8f0;
        font-size: 0.9rem;
    }
    
    /* 統計カード */
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    .stat-change {
        font-size: 0.8rem;
        margin-top: 5px;
    }
    
    .stat-up {
        color: #10b981;
    }
    
    .stat-down {
        color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'draft_posts' not in st.session_state:
    st.session_state.draft_posts = {}
if 'posting_in_progress' not in st.session_state:
    st.session_state.posting_in_progress = False
if 'projects' not in st.session_state:
    st.session_state.projects = {}
if 'current_project_id' not in st.session_state:
    st.session_state.current_project_id = None

# プラットフォーム情報
PLATFORM_INFO = {
    PlatformType.TWITTER: {
        "name": "Twitter/X",
        "icon": "🐦",
        "char_limit": 280,
        "color": "#1DA1F2"
    },
    PlatformType.LINKEDIN: {
        "name": "LinkedIn", 
        "icon": "💼",
        "char_limit": 3000,
        "color": "#0077B5"
    },
    PlatformType.FACEBOOK: {
        "name": "Facebook",
        "icon": "📘", 
        "char_limit": 63206,
        "color": "#1877F2"
    }
}

async def generate_social_content(product_info: dict, platform: str) -> str:
    """プラットフォーム別コンテンツ生成"""
    
    platform_prompts = {
        "twitter": f"""
        Twitterに投稿する魅力的で拡散されやすい投稿を作成してください。
        
        プロダクト情報：
        - 名前: {product_info.get('name', 'N/A')}
        - カテゴリ: {product_info.get('category', 'N/A')}
        - 独自価値: {product_info.get('unique_value', 'N/A')}
        
        要件：
        - 280文字以内
        - ハッシュタグ2-3個含む
        - エモジ使用
        - 行動喚起含む
        """,
        
        "linkedin": f"""
        LinkedInのプロフェッショナル向け投稿を作成してください。
        
        プロダクト情報：
        - 名前: {product_info.get('name', 'N/A')}
        - カテゴリ: {product_info.get('category', 'N/A')}
        - ターゲット: {product_info.get('target', 'N/A')}
        
        要件：
        - ビジネス価値を強調
        - プロフェッショナルなトーン
        - 具体的なメリット
        - 関連ハッシュタグ
        """,
        
        "facebook": f"""
        Facebookページ用の投稿を作成してください。
        
        プロダクト情報：
        - 名前: {product_info.get('name', 'N/A')}
        - 価格: {product_info.get('price', 'N/A')}
        - 独自価値: {product_info.get('unique_value', 'N/A')}
        
        要件：
        - 親しみやすいトーン
        - ストーリーテリング
        - 具体的な使用例
        - エンゲージメント促進
        """
    }
    
    prompt = platform_prompts.get(platform, platform_prompts["twitter"])
    
    response = await ai_client.generate_content(
        prompt=prompt,
        task_type=TaskType.CONTENT_CREATION,
        temperature=0.8,
        max_tokens=300
    )
    
    return response.content

def render_platform_status():
    """プラットフォーム接続状況表示"""
    st.header("📱 プラットフォーム接続状況")
    
    api_status = validate_api_keys()
    
    cols = st.columns(3)
    
    for i, (platform, info) in enumerate(PLATFORM_INFO.items()):
        platform_key = platform.value
        is_connected = api_status.get(platform_key, False)
        
        with cols[i % 3]:
            status_class = "connected" if is_connected else "disconnected"
            status_text = "接続済み" if is_connected else "未接続"
            status_badge_class = "status-connected" if is_connected else "status-disconnected"
            
            st.markdown(f"""
            <div class="platform-card {status_class}">
                <div class="platform-header">
                    <div class="platform-name">
                        <span class="platform-icon">{info['icon']}</span>
                        {info['name']}
                    </div>
                    <div class="status-badge {status_badge_class}">
                        {status_text}
                    </div>
                </div>
                <p>文字制限: {info['char_limit']:,}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_connected:
                st.warning(f"{info['name']} APIキーが未設定です")

def render_post_editor():
    """投稿エディター"""
    st.header("✍️ 投稿エディター")
    
    # プロジェクト情報確認
    if 'current_project_id' not in st.session_state or not st.session_state.current_project_id:
        st.warning("プロジェクトが選択されていません")
        return
    
    current_project = st.session_state.projects.get(st.session_state.current_project_id, {})
    product_info = current_project.get('flow_data', {}).get('product', {})
    
    if not product_info:
        st.warning("プロダクト情報が見つかりません")
        return
    
    st.markdown('<div class="post-editor">', unsafe_allow_html=True)
    
    # AI生成セクション
    st.subheader("🤖 AI投稿生成")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_platform = st.selectbox(
            "プラットフォーム選択",
            options=list(PLATFORM_INFO.keys()),
            format_func=lambda x: f"{PLATFORM_INFO[x]['icon']} {PLATFORM_INFO[x]['name']}"
        )
    
    with col2:
        if st.button("🚀 AI生成", type="primary"):
            with st.spinner("AI投稿を生成中..."):
                try:
                    # 非同期AI生成
                    import concurrent.futures
                    
                    async def generate():
                        return await generate_social_content(product_info, selected_platform.value)
                    
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, generate())
                        generated_content = future.result(timeout=30)
                    
                    st.session_state.draft_posts[selected_platform.value] = generated_content
                    st.success("✅ AI投稿を生成しました")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"AI生成エラー: {e}")
    
    st.markdown("---")
    
    # 投稿編集セクション
    st.subheader("📝 投稿内容編集")
    
    # タブで各プラットフォーム表示
    platform_tabs = st.tabs([
        f"{info['icon']} {info['name']}" 
        for info in PLATFORM_INFO.values()
    ])
    
    edited_posts = {}
    
    for i, (platform, info) in enumerate(PLATFORM_INFO.items()):
        with platform_tabs[i]:
            platform_key = platform.value
            
            # 既存のドラフトまたは空文字
            initial_content = st.session_state.draft_posts.get(platform_key, "")
            
            # コンテンツ編集
            content = st.text_area(
                f"{info['name']}投稿内容",
                value=initial_content,
                height=120,
                key=f"content_{platform_key}",
                placeholder=f"{info['name']}用の投稿を作成してください..."
            )
            
            # 文字数カウント
            char_count = len(content)
            char_limit = info['char_limit']
            is_over_limit = char_count > char_limit
            
            count_class = "over-limit" if is_over_limit else ""
            st.markdown(f"""
            <div class="character-count {count_class}">
                文字数: {char_count:,} / {char_limit:,}
            </div>
            """, unsafe_allow_html=True)
            
            if is_over_limit:
                st.error(f"文字数制限を{char_count - char_limit}文字超過しています")
            
            # ハッシュタグ
            hashtags = st.text_input(
                "ハッシュタグ（カンマ区切り）",
                key=f"hashtags_{platform_key}",
                placeholder="マーケティング, 自動化, AI"
            )
            
            hashtag_list = [tag.strip() for tag in hashtags.split(",") if tag.strip()]
            
            # プレビュー
            if content:
                preview_content = content
                if hashtag_list:
                    preview_content += f"\n\n{' '.join(f'#{tag}' for tag in hashtag_list)}"
                
                st.subheader("👀 プレビュー")
                st.info(preview_content)
            
            edited_posts[platform_key] = {
                "content": content,
                "hashtags": hashtag_list,
                "char_count": char_count,
                "is_valid": not is_over_limit and bool(content.strip())
            }
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 投稿実行セクション
    st.markdown("---")
    st.subheader("🚀 投稿実行")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # プラットフォーム選択
        selected_platforms = st.multiselect(
            "投稿先プラットフォーム",
            options=list(PLATFORM_INFO.keys()),
            default=list(PLATFORM_INFO.keys()),
            format_func=lambda x: f"{PLATFORM_INFO[x]['icon']} {PLATFORM_INFO[x]['name']}"
        )
    
    with col2:
        # スケジュール設定
        is_scheduled = st.checkbox("スケジュール投稿")
        scheduled_time = None
        
        if is_scheduled:
            scheduled_date = st.date_input("投稿日", value=datetime.now().date())
            scheduled_time_input = st.time_input("投稿時刻", value=datetime.now().time())
            scheduled_time = datetime.combine(scheduled_date, scheduled_time_input)
    
    with col3:
        # 投稿実行ボタン
        can_post = any(
            edited_posts.get(p.value, {}).get('is_valid', False) 
            for p in selected_platforms
        )
        
        if st.button("📤 投稿実行", type="primary", disabled=not can_post or st.session_state.posting_in_progress):
            if can_post:
                st.session_state.posting_in_progress = True
                st.rerun()
    
    # 投稿実行処理
    if st.session_state.posting_in_progress:
        with st.spinner("投稿を実行中..."):
            try:
                results = []
                
                for platform in selected_platforms:
                    platform_key = platform.value
                    post_data = edited_posts.get(platform_key, {})
                    
                    if post_data.get('is_valid'):
                        # 投稿実行
                        import concurrent.futures
                        
                        async def post():
                            return await quick_post(
                                content=post_data['content'],
                                platforms=[platform_key],
                                hashtags=post_data['hashtags']
                            )
                        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(asyncio.run, post())
                            result = future.result(timeout=30)
                        
                        results.append({
                            "platform": platform_key,
                            "result": result
                        })
                
                # 結果表示
                success_count = sum(1 for r in results if r["result"].get("success"))
                
                if success_count > 0:
                    st.success(f"✅ {success_count}/{len(results)} プラットフォームに投稿成功")
                else:
                    st.error("❌ 投稿に失敗しました")
                
                # 詳細結果
                for result in results:
                    platform_name = PLATFORM_INFO[PlatformType(result["platform"])]["name"]
                    if result["result"].get("success"):
                        st.info(f"✅ {platform_name}: 投稿成功")
                    else:
                        st.error(f"❌ {platform_name}: 投稿失敗")
                
                st.session_state.posting_in_progress = False
                
                # ドラフトをクリア
                for platform_key in selected_platforms:
                    if platform_key.value in st.session_state.draft_posts:
                        del st.session_state.draft_posts[platform_key.value]
                
                st.rerun()
                
            except Exception as e:
                st.error(f"投稿実行エラー: {e}")
                st.session_state.posting_in_progress = False
                st.rerun()

def render_post_history():
    """投稿履歴表示"""
    st.header("📜 投稿履歴")
    
    analytics = social_manager.get_post_analytics()
    
    # 統計表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{analytics.get('total', 0)}</div>
            <div class="stat-label">総投稿数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        success_rate = analytics.get('success_rate', 0)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{success_rate:.1f}%</div>
            <div class="stat-label">成功率</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        published_count = analytics.get('by_status', {}).get('published', 0)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{published_count}</div>
            <div class="stat-label">投稿成功</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        failed_count = analytics.get('by_status', {}).get('failed', 0)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{failed_count}</div>
            <div class="stat-label">投稿失敗</div>
        </div>
        """, unsafe_allow_html=True)
    
    # プラットフォーム別グラフ
    if analytics.get('total', 0) > 0:
        st.subheader("📊 プラットフォーム別統計")
        
        platform_data = analytics.get('by_platform', {})
        
        if platform_data:
            # データフレーム作成
            df_platform = pd.DataFrame([
                {
                    "プラットフォーム": platform,
                    "投稿数": data.get('total', 0),
                    "成功": data.get('published', 0),
                    "失敗": data.get('failed', 0)
                }
                for platform, data in platform_data.items()
                if data.get('total', 0) > 0
            ])
            
            if not df_platform.empty:
                # 棒グラフ
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='成功',
                    x=df_platform['プラットフォーム'],
                    y=df_platform['成功'],
                    marker_color='#10b981'
                ))
                
                fig.add_trace(go.Bar(
                    name='失敗',
                    x=df_platform['プラットフォーム'],
                    y=df_platform['失敗'],
                    marker_color='#ef4444'
                ))
                
                fig.update_layout(
                    title="プラットフォーム別投稿結果",
                    xaxis_title="プラットフォーム",
                    yaxis_title="投稿数",
                    barmode='stack',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # 投稿履歴詳細
    st.subheader("📋 最近の投稿")
    
    if social_manager.post_history:
        # 最新10件表示
        recent_posts = social_manager.post_history[-10:][::-1]
        
        for post in recent_posts:
            platform_info = PLATFORM_INFO.get(post.platform, {"icon": "📱", "name": post.platform.value})
            
            status_class = f"post-{post.status.value}"
            status_emoji = "✅" if post.status == PostStatus.PUBLISHED else "❌" if post.status == PostStatus.FAILED else "⏰"
            
            published_time = post.metadata.get('published_at', 'N/A')
            if published_time != 'N/A':
                try:
                    dt = datetime.fromisoformat(published_time.replace('Z', '+00:00'))
                    published_time = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            st.markdown(f"""
            <div class="post-history-item {status_class}">
                <div class="post-meta">
                    <div>
                        <span class="platform-icon">{platform_info['icon']}</span>
                        <strong>{platform_info['name']}</strong>
                        {status_emoji} {post.status.value}
                    </div>
                    <div class="post-time">{published_time}</div>
                </div>
                <div>{post.content[:100]}{'...' if len(post.content) > 100 else ''}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("投稿履歴がありません")

# ヘッダー
st.title("📱 自動投稿管理ダッシュボード")
st.caption("SNS自動投稿の設定・実行・監視")

# タブ構成
tabs = st.tabs(["📱 プラットフォーム", "✍️ 投稿エディター", "📜 投稿履歴", "⚙️ 設定"])

with tabs[0]:
    render_platform_status()

with tabs[1]:
    render_post_editor()

with tabs[2]:
    render_post_history()

with tabs[3]:
    st.header("⚙️ 設定")
    
    st.subheader("🔑 API設定")
    st.info("現在の実装ではAPIキーは環境変数で設定します。")
    
    api_keys_needed = [
        "TWITTER_BEARER_TOKEN",
        "LINKEDIN_ACCESS_TOKEN", 
        "FACEBOOK_ACCESS_TOKEN",
        "FACEBOOK_PAGE_ID"
    ]
    
    for key in api_keys_needed:
        is_set = bool(os.getenv(key))
        status = "✅ 設定済み" if is_set else "❌ 未設定"
        st.write(f"**{key}**: {status}")
    
    st.subheader("📊 エクスポート")
    
    if st.button("📥 投稿履歴をエクスポート"):
        export_data = social_manager.export_post_history()
        
        st.download_button(
            label="💾 JSON ダウンロード",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"post_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# サイドバー
with st.sidebar:
    st.header("📱 自動投稿制御")
    
    # 現在のプロジェクト
    if 'current_project_id' in st.session_state and st.session_state.current_project_id:
        current_project = st.session_state.projects.get(st.session_state.current_project_id, {})
        if current_project:
            st.success(f"**{current_project['name']}**")
        else:
            st.warning("プロジェクト情報を読み込み中...")
    else:
        st.warning("プロジェクトが選択されていません")
    
    st.markdown("---")
    
    # クイック統計
    st.subheader("📊 クイック統計")
    
    analytics = social_manager.get_post_analytics()
    
    st.metric("今日の投稿", analytics.get('total', 0))
    st.metric("成功率", f"{analytics.get('success_rate', 0):.1f}%")
    
    # API接続状況
    st.subheader("🔗 API状況")
    api_status = validate_api_keys()
    
    for platform, is_connected in api_status.items():
        status_emoji = "🟢" if is_connected else "🔴"
        st.write(f"{status_emoji} {platform.title()}")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("💬 AIチャット", use_container_width=True):
        st.switch_page("pages/realtime_chat.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: API設定完了後、各プラットフォームへの自動投稿が可能になります。")