#!/usr/bin/env python3
"""
競合インテリジェンス統合ダッシュボード V2
ヒューマンインザループ機能付きフロー
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime
import pandas as pd
import time

# 既存ツールをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.market_analyzer import MarketAnalyzer
from tools.content_generator import ContentGenerator
from tools.competitive_intelligence import CompetitiveIntelligence

# ページ設定
st.set_page_config(
    page_title="Marketing Flow Dashboard V2",
    page_icon="🔄",
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
    
    /* フローステップのスタイル */
    .flow-step {
        background-color: #1a1f2e;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #3b82f6;
        transition: all 0.3s;
    }
    
    .flow-step:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .flow-step.active {
        border-left-color: #10b981;
        background-color: #1e293b;
    }
    
    .flow-step.completed {
        border-left-color: #10b981;
        opacity: 0.8;
    }
    
    /* AI生成結果のスタイル */
    .ai-output {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .human-edit {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* レビューボタン */
    .review-button {
        background: linear-gradient(90deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .review-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.4);
    }
    
    /* オートメーションモード表示 */
    .automation-mode {
        position: fixed;
        top: 80px;
        right: 20px;
        background: rgba(30, 41, 59, 0.9);
        padding: 10px 20px;
        border-radius: 30px;
        border: 1px solid #3b82f6;
        z-index: 30;
    }
    
    .mode-auto {
        color: #10b981;
    }
    
    .mode-manual {
        color: #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'flow_stage' not in st.session_state:
    st.session_state.flow_stage = 0
if 'flow_data' not in st.session_state:
    st.session_state.flow_data = {}
if 'ai_outputs' not in st.session_state:
    st.session_state.ai_outputs = {}
if 'human_edits' not in st.session_state:
    st.session_state.human_edits = {}
if 'automation_mode' not in st.session_state:
    st.session_state.automation_mode = "manual"  # "auto" or "manual"
if 'review_required' not in st.session_state:
    st.session_state.review_required = {}

# フローステージの定義（8段階）
FLOW_STAGES = [
    {"id": 0, "name": "プロダクト入力", "icon": "📝", "status": "pending"},
    {"id": 1, "name": "調査フェーズ", "icon": "🔍", "status": "pending"},
    {"id": 2, "name": "ベンチマーク策定", "icon": "📊", "status": "pending"},
    {"id": 3, "name": "ベネフィット決定", "icon": "💡", "status": "pending"},
    {"id": 4, "name": "マーケティング施策", "icon": "🎯", "status": "pending"},
    {"id": 5, "name": "コンテンツ作成", "icon": "✍️", "status": "pending"},
    {"id": 6, "name": "デプロイメント", "icon": "🚀", "status": "pending"},
    {"id": 7, "name": "測定・分析", "icon": "📈", "status": "pending"}
]

# AI処理をシミュレートする関数
def simulate_ai_processing(stage_name, input_data):
    """AI処理のシミュレーション（実際にはAPIを呼ぶ）"""
    # プログレスバー表示
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    steps = [
        "データを分析中...",
        "AIモデルを起動中...",
        "最適化を実行中...",
        "結果を生成中..."
    ]
    
    for i, step in enumerate(steps):
        progress_placeholder.progress((i + 1) / len(steps))
        status_placeholder.info(f"🤖 {step}")
        time.sleep(0.5)
    
    # ダミーの結果を返す（実際にはAPIレスポンス）
    results = {
        "調査フェーズ": {
            "market_size": "国内500億円（年成長率15%）",
            "competitors": ["Notion", "Asana", "Monday.com"],
            "trends": ["AI統合需要", "リモートワーク", "自動化"],
            "opportunities": "日本市場でのローカライズ不足"
        },
        "ベンチマーク策定": {
            "quality_metrics": {
                "使いやすさ": "95%以上",
                "応答速度": "200ms以下",
                "AI精度": "90%以上"
            },
            "differentiators": ["日本語特化", "AI自動化", "低価格"]
        },
        "ベネフィット決定": {
            "primary": "作業時間を50%削減",
            "secondary": ["ミス削減", "チーム連携強化", "意思決定支援"],
            "emotional": "ストレスフリーな業務環境"
        },
        "マーケティング施策": {
            "channels": ["SNS広告", "インフルエンサー", "コンテンツマーケ"],
            "budget_allocation": {"SNS": 40, "インフルエンサー": 30, "コンテンツ": 30},
            "timeline": "3ヶ月キャンペーン"
        },
        "コンテンツ作成": {
            "sns_posts": ["Twitter投稿5本", "LinkedIn記事3本"],
            "blog_articles": ["導入事例", "使い方ガイド"],
            "email_templates": ["ウェルカムメール", "フォローアップ"]
        }
    }
    
    progress_placeholder.empty()
    status_placeholder.empty()
    
    return results.get(stage_name, {"error": "No data available"})

# レビュー機能
def show_review_interface(stage_name, ai_output):
    """AI出力のレビューインターフェース"""
    st.markdown(f"### 🔍 {stage_name}の結果レビュー")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🤖 AI生成結果")
        st.markdown('<div class="ai-output">', unsafe_allow_html=True)
        st.json(ai_output)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ✏️ 人間による調整")
        st.markdown('<div class="human-edit">', unsafe_allow_html=True)
        
        # 編集可能なフィールドを表示
        edited_data = {}
        for key, value in ai_output.items():
            if isinstance(value, str):
                edited_data[key] = st.text_area(f"{key}:", value, key=f"edit_{key}")
            elif isinstance(value, list):
                edited_data[key] = st.text_area(f"{key}:", "\n".join(value), key=f"edit_{key}").split("\n")
            elif isinstance(value, dict):
                st.write(f"**{key}:**")
                edited_data[key] = {}
                for sub_key, sub_value in value.items():
                    edited_data[key][sub_key] = st.text_input(f"  {sub_key}:", sub_value, key=f"edit_{key}_{sub_key}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # アクションボタン
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("✅ 承認して次へ", key=f"approve_{stage_name}", type="primary"):
            st.session_state.human_edits[stage_name] = ai_output
            st.session_state.review_required[stage_name] = False
            return "approved"
    
    with action_col2:
        if st.button("📝 編集を保存", key=f"save_{stage_name}"):
            st.session_state.human_edits[stage_name] = edited_data
            st.session_state.review_required[stage_name] = False
            return "edited"
    
    with action_col3:
        if st.button("🔄 再生成", key=f"regenerate_{stage_name}"):
            return "regenerate"
    
    return None

# ヘッダー
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.title("🔄 Marketing Flow Dashboard V2")
    st.caption("ヒューマンインザループ対応 - AIと人間の協調作業")

with col2:
    # オートメーションモード切り替え
    mode = st.selectbox(
        "実行モード",
        ["manual", "auto"],
        format_func=lambda x: "🤖 自動" if x == "auto" else "👤 手動",
        key="mode_selector"
    )
    st.session_state.automation_mode = mode

with col3:
    # 現在のモード表示
    mode_text = "🤖 自動モード" if st.session_state.automation_mode == "auto" else "👤 手動モード"
    mode_class = "mode-auto" if st.session_state.automation_mode == "auto" else "mode-manual"
    st.markdown(f'<div class="automation-mode"><span class="{mode_class}">{mode_text}</span></div>', unsafe_allow_html=True)

# プログレスバー
progress = st.session_state.flow_stage / 7
st.progress(progress)
st.caption(f"進捗: {int(progress * 100)}% - 現在のステージ: {FLOW_STAGES[st.session_state.flow_stage]['name']}")

# メインコンテンツエリア
st.markdown("---")

# 現在のステージ処理
current_stage = FLOW_STAGES[st.session_state.flow_stage]
st.header(f"{current_stage['icon']} {current_stage['name']}")

if st.session_state.flow_stage == 0:
    # ステージ0: プロダクト入力
    with st.form("product_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("プロダクト名", placeholder="例: AI Task Manager")
            category = st.selectbox("カテゴリ", ["SaaS", "モバイルアプリ", "Webサービス", "その他"])
            target_audience = st.text_area("ターゲットオーディエンス", placeholder="例: 中小企業のマネージャー")
        
        with col2:
            price_model = st.text_input("価格モデル", placeholder="例: 月額2,980円")
            unique_features = st.text_area("独自機能・強み", placeholder="例: AI自動タスク振り分け")
        
        submitted = st.form_submit_button("次へ: 調査開始 →", type="primary")
        
        if submitted and product_name:
            st.session_state.flow_data['product_info'] = {
                'name': product_name,
                'category': category,
                'target': target_audience,
                'price': price_model,
                'features': unique_features
            }
            st.session_state.flow_stage = 1
            st.rerun()

elif st.session_state.flow_stage in [1, 2, 3, 4, 5]:
    # AI処理ステージ
    stage_name = current_stage['name']
    
    # レビューが必要かチェック
    if stage_name not in st.session_state.review_required:
        st.session_state.review_required[stage_name] = True
    
    if st.session_state.review_required[stage_name]:
        # AI処理実行
        if st.button(f"🤖 {stage_name}を開始", type="primary"):
            with st.spinner(f'{stage_name}を実行中...'):
                # AI処理（実際にはAPIコール）
                ai_output = simulate_ai_processing(stage_name, st.session_state.flow_data)
                st.session_state.ai_outputs[stage_name] = ai_output
            
            st.success(f"✅ {stage_name}が完了しました！")
            
            if st.session_state.automation_mode == "manual":
                st.info("👤 レビューが必要です。結果を確認してください。")
            else:
                # 自動モードの場合は自動承認
                st.session_state.human_edits[stage_name] = ai_output
                st.session_state.review_required[stage_name] = False
                st.session_state.flow_stage += 1
                time.sleep(2)
                st.rerun()
    
    # レビューインターフェース表示（手動モード）
    if stage_name in st.session_state.ai_outputs and st.session_state.review_required[stage_name]:
        action = show_review_interface(stage_name, st.session_state.ai_outputs[stage_name])
        
        if action == "approved":
            st.success("✅ 承認されました")
            st.session_state.flow_stage += 1
            st.rerun()
        elif action == "edited":
            st.success("📝 編集が保存されました")
            st.session_state.flow_stage += 1
            st.rerun()
        elif action == "regenerate":
            st.session_state.review_required[stage_name] = True
            st.rerun()

elif st.session_state.flow_stage == 6:
    # ステージ6: デプロイメント
    st.info("デプロイメント準備")
    
    # これまでの結果サマリー
    with st.expander("📊 これまでの結果サマリー", expanded=True):
        for stage_name, data in st.session_state.human_edits.items():
            st.markdown(f"**{stage_name}:**")
            st.json(data)
    
    if st.button("🚀 デプロイ実行", type="primary"):
        with st.spinner('デプロイ中...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
        
        st.success("✅ デプロイ完了！")
        st.session_state.flow_stage = 7
        st.rerun()

elif st.session_state.flow_stage == 7:
    # ステージ7: 測定・分析
    st.success("🎉 全フロー完了！")
    
    # パフォーマンスメトリクス
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("完了時間", "45分", "-15分")
    with col2:
        st.metric("AI提案採用率", "85%", "+10%")
    with col3:
        st.metric("人間の介入回数", "3回", "-2回")

# サイドバー
with st.sidebar:
    st.header("📋 フロー管理")
    
    # 全ステージの状態表示
    for i, stage in enumerate(FLOW_STAGES):
        if i < st.session_state.flow_stage:
            status = "✅ 完了"
            color = "green"
        elif i == st.session_state.flow_stage:
            status = "🔄 進行中"
            color = "blue"
        else:
            status = "⏳ 待機中"
            color = "gray"
        
        st.markdown(f"{stage['icon']} **{stage['name']}** - :{color}[{status}]")
    
    st.markdown("---")
    
    st.header("🔧 設定")
    
    # レビュー設定
    st.subheader("レビュー設定")
    
    review_all = st.checkbox("全ステージでレビュー必須", value=True)
    
    if not review_all:
        st.caption("レビューをスキップするステージ:")
        for stage in FLOW_STAGES[1:6]:
            skip = st.checkbox(stage['name'], key=f"skip_{stage['name']}")
            if skip:
                st.session_state.review_required[stage['name']] = False
    
    # AI設定
    st.subheader("AI設定")
    
    ai_creativity = st.slider("AI創造性", 0.0, 1.0, 0.7)
    ai_speed = st.radio("処理速度", ["高速", "標準", "高精度"])
    
    st.markdown("---")
    
    # エクスポート
    if st.button("📥 結果をエクスポート", use_container_width=True):
        export_data = {
            "product_info": st.session_state.flow_data,
            "ai_outputs": st.session_state.ai_outputs,
            "human_edits": st.session_state.human_edits,
            "timestamp": datetime.now().isoformat()
        }
        st.download_button(
            label="JSONダウンロード",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"marketing_flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )