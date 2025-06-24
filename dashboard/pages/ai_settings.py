#!/usr/bin/env python3
"""
AI模型設定画面
リアルタイムでAIモデルを切り替え・コスト監視
"""

import streamlit as st
import sys
import os
import asyncio
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ai_models import model_manager, TaskType, AI_MODELS, AIProvider
from config.ai_client import ai_client

# ページ設定
st.set_page_config(
    page_title="AI模型設定",
    page_icon="🤖",
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
    
    /* 模型カード */
    .model-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px solid #374151;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .model-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    .model-card.selected {
        border-color: #10b981;
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
    }
    
    .model-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 8px;
    }
    
    .model-card.selected .model-name {
        color: #10b981;
    }
    
    .model-specs {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 10px;
        margin: 15px 0;
    }
    
    .spec-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 8px 12px;
        border-radius: 6px;
        text-align: center;
    }
    
    .spec-label {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    
    .spec-value {
        font-weight: bold;
        color: #e2e8f0;
    }
    
    /* コスト表示 */
    .cost-display {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    
    .cost-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ef4444;
    }
    
    /* 最適化ボタン */
    .optimization-button {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .optimization-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* 統計グリッド */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
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
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'ai_test_results' not in st.session_state:
    st.session_state.ai_test_results = []

# ヘッダー
st.title("🤖 AI模型設定・監視センター")
st.caption("マーケティングツールのAI使用量とコストをリアルタイム管理")

# タブ構成
tabs = st.tabs(["⚙️ 模型設定", "📊 使用統計", "💰 コスト分析", "🧪 テスト・ベンチマーク"])

# タブ1: 模型設定
with tabs[0]:
    st.header("🎯 用途別AI模型設定")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("現在の設定")
        
        # 各タスクタイプの設定
        for task_type in TaskType:
            current_model = model_manager.get_current_config()[task_type]
            if current_model is None:
                st.warning(f"{task_type.value}: 利用可能なAIモデルがありません。APIキーを設定してください。")
                continue
            current_config = AI_MODELS[current_model]
            
            with st.expander(f"{task_type.value.replace('_', ' ').title()}", expanded=True):
                col_model, col_change = st.columns([3, 1])
                
                with col_model:
                    # 現在の模型情報表示
                    st.markdown(f"""
                    <div class="model-card selected">
                        <div class="model-name">{current_model}</div>
                        <div class="model-specs">
                            <div class="spec-item">
                                <div class="spec-label">プロバイダー</div>
                                <div class="spec-value">{current_config.provider.value}</div>
                            </div>
                            <div class="spec-item">
                                <div class="spec-label">コスト/1K tokens</div>
                                <div class="spec-value">¥{current_config.cost_per_1k_tokens:.4f}</div>
                            </div>
                            <div class="spec-item">
                                <div class="spec-label">最大トークン</div>
                                <div class="spec-value">{current_config.max_tokens:,}</div>
                            </div>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.9rem;">{current_config.description}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_change:
                    # 模型変更
                    new_model = st.selectbox(
                        "模型を変更",
                        options=list(AI_MODELS.keys()),
                        index=list(AI_MODELS.keys()).index(current_model),
                        key=f"model_select_{task_type.value}"
                    )
                    
                    if new_model != current_model:
                        if st.button(f"変更", key=f"change_{task_type.value}"):
                            model_manager.set_model_for_task(task_type, new_model)
                            st.success(f"✅ {task_type.value}の模型を{new_model}に変更しました")
                            st.rerun()
    
    with col2:
        st.subheader("クイック最適化")
        
        # 最適化オプション
        if st.button("💰 コスト最適化", help="全タスクを最安模型に設定"):
            model_manager.optimize_for_cost()
            st.success("コスト最適化設定を適用しました")
            st.rerun()
        
        if st.button("✨ 品質最適化", help="全タスクを最高品質模型に設定"):
            model_manager.optimize_for_quality()
            st.success("品質最適化設定を適用しました")
            st.rerun()
        
        if st.button("⚖️ バランス設定", help="推奨バランス設定に戻す"):
            from config.ai_models import TASK_MODEL_MAPPING
            for task_type, model_name in TASK_MODEL_MAPPING.items():
                model_manager.set_model_for_task(task_type, model_name)
            st.success("推奨バランス設定を適用しました")
            st.rerun()
        
        # 現在の設定でのコスト見積もり
        st.subheader("📈 コスト見積もり")
        
        st.write("**1回の実行あたり（1000 input + 500 output tokens）:**")
        
        total_cost = 0
        for task_type in TaskType:
            cost = model_manager.get_cost_estimate(task_type, 1000, 500)
            total_cost += cost
            st.metric(
                task_type.value.replace('_', ' ').title(),
                f"¥{cost:.4f}"
            )
        
        st.markdown(f"""
        <div class="cost-display">
            <div style="color: #94a3b8;">総コスト</div>
            <div class="cost-value">¥{total_cost:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

# タブ2: 使用統計
with tabs[1]:
    st.header("📊 AI使用統計")
    
    # 統計データ取得
    usage_stats = ai_client.get_usage_stats()
    
    # 統計表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{usage_stats['requests']}</div>
            <div class="stat-label">総リクエスト数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">¥{usage_stats['total_cost']:.2f}</div>
            <div class="stat-label">総コスト</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{usage_stats['total_tokens']:,}</div>
            <div class="stat-label">総トークン数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_cost = usage_stats['total_cost'] / max(usage_stats['requests'], 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">¥{avg_cost:.4f}</div>
            <div class="stat-label">平均コスト/リクエスト</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 模型別使用量グラフ
    if usage_stats['model_usage']:
        st.subheader("模型別使用量")
        
        model_data = []
        for model, stats in usage_stats['model_usage'].items():
            model_data.append({
                "模型": model,
                "リクエスト数": stats['requests'],
                "コスト": stats['cost'],
                "トークン数": stats['tokens']
            })
        
        df = pd.DataFrame(model_data)
        
        # 円グラフ
        col1, col2 = st.columns(2)
        
        with col1:
            fig_requests = px.pie(
                df, 
                values='リクエスト数', 
                names='模型',
                title="リクエスト数分布",
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
            )
            fig_requests.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_requests, use_container_width=True)
        
        with col2:
            fig_cost = px.pie(
                df, 
                values='コスト', 
                names='模型',
                title="コスト分布",
                color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981', '#3b82f6']
            )
            fig_cost.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # データテーブル
        st.subheader("詳細データ")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("まだ使用データがありません")

# タブ3: コスト分析
with tabs[2]:
    st.header("💰 コスト分析・予測")
    
    # 月間使用量予測
    st.subheader("📈 月間コスト予測")
    
    # 予測パラメータ
    col1, col2 = st.columns(2)
    
    with col1:
        daily_requests = st.number_input("1日のリクエスト数", min_value=1, value=100, step=10)
        avg_input_tokens = st.number_input("平均入力トークン数", min_value=100, value=1000, step=100)
        avg_output_tokens = st.number_input("平均出力トークン数", min_value=50, value=500, step=50)
    
    with col2:
        # 各タスクタイプの使用頻度
        st.write("**タスク別使用比率 (%)**")
        task_ratios = {}
        total_ratio = 0
        
        for task_type in TaskType:
            ratio = st.slider(
                task_type.value.replace('_', ' ').title(),
                0, 100, 
                value=100 // len(TaskType),
                key=f"ratio_{task_type.value}"
            )
            task_ratios[task_type] = ratio
            total_ratio += ratio
        
        if total_ratio > 100:
            st.warning(f"合計が100%を超えています ({total_ratio}%)")
    
    # コスト計算
    if st.button("💰 コスト予測を実行"):
        monthly_costs = {}
        total_monthly_cost = 0
        
        for task_type, ratio in task_ratios.items():
            if ratio > 0:
                daily_task_requests = daily_requests * (ratio / 100)
                daily_cost = model_manager.get_cost_estimate(
                    task_type, avg_input_tokens, avg_output_tokens
                ) * daily_task_requests
                monthly_cost = daily_cost * 30
                monthly_costs[task_type.value] = monthly_cost
                total_monthly_cost += monthly_cost
        
        # 結果表示
        st.subheader("📊 予測結果")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="cost-display">
                <div style="color: #94a3b8;">月間総コスト</div>
                <div class="cost-value">¥{total_monthly_cost:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px;">
                <div style="color: #94a3b8;">年間予測コスト</div>
                <div style="font-size: 1.3rem; font-weight: bold; color: #10b981;">¥{total_monthly_cost * 12:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if monthly_costs:
                # タスク別コストグラフ
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(monthly_costs.keys()),
                        y=list(monthly_costs.values()),
                        marker_color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4']
                    )
                ])
                
                fig.update_layout(
                    title="タスク別月間コスト",
                    xaxis_title="タスクタイプ",
                    yaxis_title="コスト (¥)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig, use_container_width=True)

# タブ4: テスト・ベンチマーク
with tabs[3]:
    st.header("🧪 AI模型テスト・ベンチマーク")
    
    # テスト実行
    st.subheader("⚡ クイックテスト")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        test_prompt = st.text_area(
            "テストプロンプト",
            value="AIマーケティングツールの利点を3つ挙げてください。",
            height=100
        )
        
        test_task_type = st.selectbox(
            "テストタスクタイプ",
            options=list(TaskType),
            format_func=lambda x: x.value.replace('_', ' ').title()
        )
    
    with col2:
        if st.button("🚀 テスト実行", type="primary"):
            with st.spinner("AI模型をテスト中..."):
                try:
                    # 非同期処理のためのイベントループ処理
                    import asyncio
                    
                    async def run_test():
                        return await ai_client.generate_content(test_prompt, test_task_type)
                    
                    # 既存のイベントループがある場合の処理
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # Streamlitの環境では新しいスレッドで実行
                            import concurrent.futures
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(asyncio.run, run_test())
                                response = future.result(timeout=30)
                        else:
                            response = loop.run_until_complete(run_test())
                    except RuntimeError:
                        response = asyncio.run(run_test())
                    
                    # 結果を保存
                    test_result = {
                        "timestamp": datetime.now(),
                        "prompt": test_prompt,
                        "task_type": test_task_type.value,
                        "response": response.to_dict()
                    }
                    st.session_state.ai_test_results.append(test_result)
                    
                    # 結果表示
                    st.success("✅ テスト完了！")
                    
                    with st.expander("📋 テスト結果", expanded=True):
                        st.write(f"**使用模型:** {response.model}")
                        st.write(f"**プロバイダー:** {response.provider}")
                        st.write(f"**レスポンス時間:** {response.response_time:.2f}秒")
                        st.write(f"**使用トークン:** {response.tokens_used}")
                        st.write(f"**コスト:** ¥{response.cost:.4f}")
                        
                        st.markdown("**生成内容:**")
                        st.info(response.content)
                
                except Exception as e:
                    st.error(f"テスト実行エラー: {e}")
    
    # テスト履歴
    if st.session_state.ai_test_results:
        st.subheader("📜 テスト履歴")
        
        # 最新5件のテスト結果を表示
        recent_tests = st.session_state.ai_test_results[-5:]
        
        for i, test_result in enumerate(reversed(recent_tests)):
            with st.expander(f"テスト {len(recent_tests)-i}: {test_result['timestamp'].strftime('%H:%M:%S')} - {test_result['task_type']}", expanded=False):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write(f"**プロンプト:** {test_result['prompt'][:100]}...")
                    st.write(f"**模型:** {test_result['response']['model']}")
                    st.write(f"**コスト:** ¥{test_result['response']['cost']:.4f}")
                
                with col2:
                    st.write(f"**レスポンス時間:** {test_result['response']['response_time']:.2f}秒")
                    st.write(f"**トークン数:** {test_result['response']['tokens_used']}")
                
                st.markdown("**応答内容:**")
                st.code(test_result['response']['content'][:200] + "..." if len(test_result['response']['content']) > 200 else test_result['response']['content'])
        
        # 履歴クリア
        if st.button("🗑️ テスト履歴をクリア"):
            st.session_state.ai_test_results = []
            st.success("履歴をクリアしました")
            st.rerun()

# サイドバー
with st.sidebar:
    st.header("🎛️ システム制御")
    
    # 統計リセット
    if st.button("🔄 使用統計リセット", type="secondary"):
        ai_client.reset_stats()
        st.success("統計をリセットしました")
        st.rerun()
    
    # 設定エクスポート
    if st.button("📥 設定エクスポート"):
        config_data = {
            "model_config": model_manager.get_current_config(),
            "usage_stats": ai_client.get_usage_stats(),
            "export_time": datetime.now().isoformat()
        }
        
        st.download_button(
            label="💾 JSON ダウンロード",
            data=json.dumps({k: str(v) if not isinstance(v, (dict, list)) else v for k, v in config_data.items()}, 
                          ensure_ascii=False, indent=2),
            file_name=f"ai_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    st.header("📊 リアルタイム監視")
    
    # 現在の設定サマリー
    current_config = model_manager.get_current_config()
    
    for task_type, model_name in current_config.items():
        if model_name is None:
            st.metric(
                task_type.value.replace('_', ' ').title(),
                "Not Available",
                "No API Key"
            )
        else:
            config = AI_MODELS[model_name]
            st.metric(
                task_type.value.replace('_', ' ').title(),
                model_name,
                f"¥{config.cost_per_1k_tokens:.4f}/1K"
            )
    
    st.markdown("---")
    
    # クイックアクセス
    st.header("🚀 クイックアクセス")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("pages/../home.py")
    
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/project_management.py")