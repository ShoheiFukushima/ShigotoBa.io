#!/usr/bin/env python3
"""
リアルタイムチャット機能
低コストAIモデル（Gemini Flash）でマーケティング支援
"""

import streamlit as st
import sys
import os
import asyncio
import json
from datetime import datetime
import uuid

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ai_models import TaskType
from config.ai_client import ai_client

# ページ設定
st.set_page_config(
    page_title="リアルタイムチャット",
    page_icon="💬",
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
    
    /* チャットコンテナ */
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(30, 41, 59, 0.3);
        border-radius: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin-bottom: 20px;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }
    
    /* ユーザーメッセージ */
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0 10px 60px;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
        position: relative;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -50px;
        top: 15px;
        font-size: 1.5rem;
    }
    
    /* AIメッセージ */
    .ai-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 60px 10px 0;
        box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
        position: relative;
    }
    
    .ai-message::after {
        content: "🤖";
        position: absolute;
        right: -50px;
        top: 15px;
        font-size: 1.5rem;
    }
    
    /* システムメッセージ */
    .system-message {
        background: rgba(107, 114, 128, 0.2);
        color: #9ca3af;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 20px;
        text-align: center;
        font-size: 0.9rem;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    
    /* 入力エリア */
    .chat-input-container {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* プリセットボタン */
    .preset-button {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #3b82f6;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .preset-button:hover {
        background: rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    
    /* コスト表示 */
    .cost-indicator {
        position: fixed;
        top: 80px;
        right: 20px;
        background: rgba(30, 41, 59, 0.9);
        padding: 10px 15px;
        border-radius: 10px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        font-size: 0.8rem;
        z-index: 30;
    }
    
    .cost-value {
        color: #10b981;
        font-weight: bold;
    }
    
    /* タイピングインジケーター */
    .typing-indicator {
        background: rgba(107, 114, 128, 0.2);
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 60px 10px 0;
        position: relative;
    }
    
    .typing-dots {
        display: inline-block;
    }
    
    .typing-dots span {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #9ca3af;
        margin: 0 2px;
        animation: typing 1.4s infinite both;
    }
    
    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.4;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    /* メッセージメタ情報 */
    .message-meta {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_session_id' not in st.session_state:
    st.session_state.chat_session_id = str(uuid.uuid4())
if 'total_chat_cost' not in st.session_state:
    st.session_state.total_chat_cost = 0.0
if 'is_typing' not in st.session_state:
    st.session_state.is_typing = False

# プリセット質問
PRESET_QUESTIONS = [
    "このプロダクトの競合はどこですか？",
    "SNS投稿のアイデアを5つ教えて",
    "価格設定の戦略を提案して",
    "ターゲット層の分析をお願いします",
    "マーケティング予算の配分方法は？",
    "プレスリリースの書き方を教えて",
    "キャンペーンのKPI設定について",
    "ブランディング戦略のアドバイス"
]

# マーケティング専用システムプロンプト
MARKETING_SYSTEM_PROMPT = """
あなたは経験豊富なマーケティングコンサルタントです。

専門分野：
- デジタルマーケティング戦略
- ブランディング
- SNSマーケティング
- コンテンツマーケティング
- 競合分析
- 価格戦略
- ROI分析

回答スタイル：
- 簡潔で実用的
- 具体的なアクションプラン含む
- 数字・データを重視
- 日本市場に最適化
- コスト効率を重視

制約：
- 200文字以内で要点をまとめる
- 必要に応じて箇条書き使用
- 専門用語は分かりやすく説明
"""

def add_message(role: str, content: str, metadata: dict = None):
    """チャット履歴にメッセージを追加"""
    message = {
        "id": str(uuid.uuid4()),
        "role": role,
        "content": content,
        "timestamp": datetime.now(),
        "metadata": metadata or {}
    }
    st.session_state.chat_history.append(message)

def render_message(message: dict):
    """メッセージをレンダリング"""
    timestamp = message["timestamp"].strftime("%H:%M:%S")
    
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
            <div class="message-meta">👤 {timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    
    elif message["role"] == "assistant":
        cost = message["metadata"].get("cost", 0)
        model = message["metadata"].get("model", "AI")
        tokens = message["metadata"].get("tokens", 0)
        
        st.markdown(f"""
        <div class="ai-message">
            {message["content"]}
            <div class="message-meta">
                🤖 {model} | {timestamp} | ¥{cost:.4f} | {tokens} tokens
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif message["role"] == "system":
        st.markdown(f"""
        <div class="system-message">
            {message["content"]} - {timestamp}
        </div>
        """, unsafe_allow_html=True)

async def get_ai_response(user_message: str) -> dict:
    """AI応答を取得（低コストモデル使用）"""
    try:
        # プロジェクトコンテキストを追加
        context = ""
        if 'current_project_id' in st.session_state and st.session_state.current_project_id:
            project = st.session_state.projects.get(st.session_state.current_project_id, {})
            if project:
                product_info = project.get('flow_data', {}).get('product', {})
                if product_info:
                    context = f"""
                    
                    現在のプロジェクト情報：
                    - 製品名: {product_info.get('name', 'N/A')}
                    - カテゴリ: {product_info.get('category', 'N/A')}
                    - ターゲット: {product_info.get('target', 'N/A')}
                    - 価格: {product_info.get('price', 'N/A')}
                    - 独自価値: {product_info.get('unique_value', 'N/A')}
                    """
        
        enhanced_prompt = f"{user_message}{context}"
        
        # Chat用の低コストモデル（Gemini Flash）で応答生成
        response = await ai_client.generate_content(
            prompt=enhanced_prompt,
            task_type=TaskType.CHAT,
            system_prompt=MARKETING_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=300  # 短い応答でコスト削減
        )
        
        return {
            "content": response.content,
            "cost": response.cost,
            "model": response.model,
            "tokens": response.tokens_used
        }
        
    except Exception as e:
        return {
            "content": f"申し訳ございません。エラーが発生しました: {str(e)}",
            "cost": 0,
            "model": "error",
            "tokens": 0
        }

# ヘッダー
col1, col2 = st.columns([3, 1])

with col1:
    st.title("💬 マーケティングAIチャット")
    st.caption("低コストAI（Gemini Flash）でリアルタイム相談")

with col2:
    # コスト表示
    st.markdown(f"""
    <div class="cost-indicator">
        <div>今セッション: <span class="cost-value">¥{st.session_state.total_chat_cost:.4f}</span></div>
        <div>使用モデル: <span class="cost-value">Gemini Flash</span></div>
    </div>
    """, unsafe_allow_html=True)

# チャット表示エリア
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# 初回メッセージ
if not st.session_state.chat_history:
    add_message("system", "マーケティングAIアシスタントが起動しました")

# チャット履歴表示
for message in st.session_state.chat_history:
    render_message(message)

# タイピングインジケーター（AI応答生成後は自動的にfalseになる）
if st.session_state.get('is_typing', False) and len(st.session_state.chat_history) > 0:
    # 最後のメッセージがユーザーからの場合のみ表示
    if st.session_state.chat_history[-1]["role"] == "user":
        st.markdown("""
        <div class="typing-indicator">
            AIが入力中
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 入力エリア
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

# プリセット質問ボタン
st.markdown("**💡 よくある質問:**")
preset_cols = st.columns(4)

for i, question in enumerate(PRESET_QUESTIONS):
    col_index = i % 4
    with preset_cols[col_index]:
        if st.button(question, key=f"preset_{i}", help="クリックで質問を送信"):
            # プリセット質問を送信して処理
            add_message("user", question)
            st.session_state.is_typing = True
            
            # AI応答を生成
            try:
                import concurrent.futures
                
                async def get_response():
                    return await get_ai_response(question)
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, get_response())
                    ai_response = future.result(timeout=30)
                
                # AI応答を追加
                add_message("assistant", ai_response["content"], {
                    "cost": ai_response["cost"],
                    "model": ai_response["model"],
                    "tokens": ai_response["tokens"]
                })
                
                # コスト累計更新
                st.session_state.total_chat_cost += ai_response["cost"]
                st.session_state.is_typing = False
                
            except Exception as e:
                add_message("system", f"エラー: AI応答の取得に失敗しました - {str(e)}")
                st.session_state.is_typing = False
            
            st.rerun()

st.markdown("---")

# メインチャット入力
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "メッセージを入力してください...",
        key="chat_input",
        placeholder="例：このプロダクトの競合分析をお願いします",
        autocomplete="off"
    )

with col2:
    send_button = st.button("📤 送信", type="primary", use_container_width=True)

# メッセージ送信処理
if (send_button or user_input) and user_input.strip():
    # ユーザーメッセージを追加
    add_message("user", user_input.strip())
    st.session_state.is_typing = True
    
    # AI応答を生成（非同期処理）
    try:
        # Streamlit環境での非同期処理
        import concurrent.futures
        
        async def get_response():
            return await get_ai_response(user_input.strip())
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, get_response())
            ai_response = future.result(timeout=30)
        
        # AI応答を追加
        add_message("assistant", ai_response["content"], {
            "cost": ai_response["cost"],
            "model": ai_response["model"],
            "tokens": ai_response["tokens"]
        })
        
        # コスト累計更新
        st.session_state.total_chat_cost += ai_response["cost"]
        st.session_state.is_typing = False
        
        # 入力をクリア（session_stateを直接変更しない）
        st.rerun()
        
    except Exception as e:
        add_message("system", f"エラー: AI応答の取得に失敗しました - {str(e)}")
        st.session_state.is_typing = False
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.header("💬 チャット設定")
    
    # チャット統計
    st.subheader("📊 セッション統計")
    st.metric("メッセージ数", len([m for m in st.session_state.chat_history if m["role"] != "system"]))
    st.metric("総コスト", f"¥{st.session_state.total_chat_cost:.4f}")
    
    avg_cost = st.session_state.total_chat_cost / max(len([m for m in st.session_state.chat_history if m["role"] == "assistant"]), 1)
    st.metric("平均コスト/返答", f"¥{avg_cost:.4f}")
    
    st.markdown("---")
    
    # モデル設定
    st.subheader("🤖 AI設定")
    st.info("**使用モデル**: Gemini 1.5 Flash")
    st.info("**コスト**: ¥0.000075/1K tokens")
    st.info("**特徴**: 高速・低コスト")
    
    # 現在のプロジェクト情報
    if 'current_project_id' in st.session_state and st.session_state.current_project_id:
        st.subheader("📂 現在のプロジェクト")
        project = st.session_state.projects.get(st.session_state.current_project_id, {})
        if project:
            st.success(f"**{project['name']}**")
            st.caption("プロジェクト情報を考慮した回答を提供します")
        else:
            st.info("プロジェクト情報を読み込み中...")
    else:
        st.warning("プロジェクトが選択されていません")
    
    st.markdown("---")
    
    # チャット管理
    st.subheader("🗂️ チャット管理")
    
    if st.button("🆕 新しいチャット", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.chat_session_id = str(uuid.uuid4())
        st.session_state.total_chat_cost = 0.0
        st.session_state.is_typing = False
        add_message("system", "新しいチャットセッションを開始しました")
        st.success("新しいチャットを開始しました")
        st.rerun()
    
    if st.button("📥 チャット履歴出力", use_container_width=True):
        # チャット履歴をJSON形式でダウンロード
        chat_export = {
            "session_id": st.session_state.chat_session_id,
            "total_cost": st.session_state.total_chat_cost,
            "message_count": len(st.session_state.chat_history),
            "created_at": datetime.now().isoformat(),
            "messages": [
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"].isoformat(),
                    "metadata": msg.get("metadata", {})
                }
                for msg in st.session_state.chat_history
            ]
        }
        
        st.download_button(
            label="💾 JSON ダウンロード",
            data=json.dumps(chat_export, ensure_ascii=False, indent=2),
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("🔄 フローダッシュボード", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("🤖 AI設定", use_container_width=True):
        st.switch_page("pages/ai_settings.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: 具体的な質問ほど有用な回答が得られます。プロジェクト選択により更に精度が向上します。")