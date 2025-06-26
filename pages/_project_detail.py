#!/usr/bin/env python3
"""
プロジェクト詳細画面
各プロジェクトの全情報を一覧表示
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 既存ツールをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.market_analyzer import MarketAnalyzer
from tools.content_generator import ContentGenerator

# ページ設定
st.set_page_config(
    page_title="Project Detail - Marketing Flow",
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
    
    /* プロジェクトヘッダー */
    .project-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    
    .project-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    /* ステータスカード */
    .status-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .status-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    /* タイムライン */
    .timeline-item {
        background: rgba(30, 41, 59, 0.8);
        padding: 20px;
        border-left: 3px solid #3b82f6;
        margin-bottom: 15px;
        border-radius: 8px;
        position: relative;
    }
    
    .timeline-item::before {
        content: "●";
        position: absolute;
        left: -9px;
        top: 20px;
        color: #3b82f6;
        font-size: 20px;
    }
    
    .timeline-item.completed {
        border-left-color: #10b981;
    }
    
    .timeline-item.completed::before {
        color: #10b981;
    }
    
    /* メトリクスグリッド */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(59, 130, 246, 0.2);
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
    
    /* コンテンツプレビュー */
    .content-preview {
        background: rgba(30, 41, 59, 0.5);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin-bottom: 15px;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .content-preview::-webkit-scrollbar {
        width: 8px;
    }
    
    .content-preview::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
    }
    
    .content-preview::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'projects' not in st.session_state:
    st.session_state.projects = {}
if 'selected_project_id' not in st.session_state:
    st.session_state.selected_project_id = None

# パンくずナビゲーション
st.markdown("""
<div style="background: rgba(30, 41, 59, 0.5); padding: 10px 20px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem;">
    <a href="javascript:void(0)" onclick="window.parent.postMessage({type: 'streamlit:rerun', data: {page: 'home.py'}}, '*')" style="color: #3b82f6; text-decoration: none;">🏠 ダッシュボード</a>
    <span style="color: #94a3b8;"> > </span>
    <a href="javascript:void(0)" onclick="window.parent.postMessage({type: 'streamlit:rerun', data: {page: 'project_management.py'}}, '*')" style="color: #3b82f6; text-decoration: none;">📊 プロジェクト管理室</a>
    <span style="color: #94a3b8;"> > </span>
    <span style="color: #e2e8f0;">📈 プロジェクト室</span>
</div>
""", unsafe_allow_html=True)

# サイドバー：プロジェクト選択
with st.sidebar:
    st.header("📂 プロジェクト選択")
    
    if st.session_state.projects:
        project_names = {pid: data['name'] for pid, data in st.session_state.projects.items()}
        selected_name = st.selectbox(
            "プロジェクトを選択",
            options=list(project_names.values()),
            index=0 if st.session_state.selected_project_id is None else 
                  list(project_names.keys()).index(st.session_state.selected_project_id)
        )
        
        # 選択されたプロジェクトIDを取得
        st.session_state.selected_project_id = [pid for pid, name in project_names.items() if name == selected_name][0]
        
        st.markdown("---")
        
        # 戻るボタン
        if st.button("⬅️ プロジェクト管理室に戻る", type="secondary", use_container_width=True):
            st.switch_page("pages/project_management.py")
    else:
        st.info("プロジェクトがありません")
        if st.button("⬅️ プロジェクト管理室に戻る", type="secondary", use_container_width=True):
            st.switch_page("pages/project_management.py")

# メインコンテンツ
if st.session_state.selected_project_id and st.session_state.selected_project_id in st.session_state.projects:
    project = st.session_state.projects[st.session_state.selected_project_id]
    
    # プロジェクトヘッダー
    st.markdown(f"""
    <div class="project-header">
        <h1 class="project-title">{project['name']}</h1>
        <p style="color: #94a3b8;">作成日: {project['created_at']} | 最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # タブ構成
    tabs = st.tabs(["📊 概要", "📈 進捗状況", "📝 コンテンツ", "🎯 マーケティング施策", "💰 予算・ROI", "⚙️ 設定"])
    
    # 概要タブ
    with tabs[0]:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="status-card">
                <h3>🎯 現在のステージ</h3>
                <p style="font-size: 2rem; color: #3b82f6;">Stage {}/8</p>
                <p>{}</p>
            </div>
            """.format(
                project['flow_stage'] + 1,
                ["プロダクト入力", "調査フェーズ", "ベンチマーク策定", "ベネフィット決定", 
                 "マーケティング施策", "コンテンツ作成", "デプロイメント", "測定・分析"][project['flow_stage']]
            ), unsafe_allow_html=True)
        
        with col2:
            progress = (project['flow_stage'] / 7) * 100
            st.markdown(f"""
            <div class="status-card">
                <h3>📊 進捗率</h3>
                <p style="font-size: 2rem; color: #10b981;">{progress:.1f}%</p>
                <p>完了まであと{8 - project['flow_stage'] - 1}ステップ</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="status-card">
                <h3>📅 経過日数</h3>
                <p style="font-size: 2rem; color: #f59e0b;">3日</p>
                <p>平均: 2.3日/ステージ</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="status-card">
                <h3>🚀 予想完了日</h3>
                <p style="font-size: 1.5rem; color: #8b5cf6;">2025/01/15</p>
                <p>残り12日</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 📋 プロダクト情報")
        if 'product_info' in project['flow_data']:
            info = project['flow_data']['product_info']
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**製品名**: {info.get('name', 'N/A')}")
                st.info(f"**カテゴリ**: {info.get('category', 'N/A')}")
                st.info(f"**価格**: {info.get('price', 'N/A')}")
            with col2:
                st.info(f"**ターゲット**: {info.get('target', 'N/A')}")
                st.info(f"**独自性**: {info.get('uniqueness', 'N/A')}")
        
        # 競合分析結果
        if project.get('competitive_analysis'):
            st.markdown("### 🔍 競合分析サマリー")
            analysis = project['competitive_analysis']
            
            metrics_html = '<div class="metrics-grid">'
            
            if 'market_size' in analysis:
                metrics_html += f"""
                <div class="metric-box">
                    <div class="metric-label">市場規模</div>
                    <div class="metric-value">{analysis['market_size']}</div>
                </div>
                """
            
            if 'competitors' in analysis:
                metrics_html += f"""
                <div class="metric-box">
                    <div class="metric-label">主要競合数</div>
                    <div class="metric-value">{len(analysis['competitors'])}</div>
                </div>
                """
            
            if 'market_growth' in analysis:
                metrics_html += f"""
                <div class="metric-box">
                    <div class="metric-label">市場成長率</div>
                    <div class="metric-value">{analysis['market_growth']}</div>
                </div>
                """
            
            metrics_html += '</div>'
            st.markdown(metrics_html, unsafe_allow_html=True)
    
    # 進捗状況タブ
    with tabs[1]:
        st.markdown("### 📅 プロジェクトタイムライン")
        
        stages = [
            {"name": "プロダクト入力", "status": "completed" if project['flow_stage'] > 0 else "active" if project['flow_stage'] == 0 else "pending"},
            {"name": "調査フェーズ", "status": "completed" if project['flow_stage'] > 1 else "active" if project['flow_stage'] == 1 else "pending"},
            {"name": "ベンチマーク策定", "status": "completed" if project['flow_stage'] > 2 else "active" if project['flow_stage'] == 2 else "pending"},
            {"name": "ベネフィット決定", "status": "completed" if project['flow_stage'] > 3 else "active" if project['flow_stage'] == 3 else "pending"},
            {"name": "マーケティング施策", "status": "completed" if project['flow_stage'] > 4 else "active" if project['flow_stage'] == 4 else "pending"},
            {"name": "コンテンツ作成", "status": "completed" if project['flow_stage'] > 5 else "active" if project['flow_stage'] == 5 else "pending"},
            {"name": "デプロイメント", "status": "completed" if project['flow_stage'] > 6 else "active" if project['flow_stage'] == 6 else "pending"},
            {"name": "測定・分析", "status": "completed" if project['flow_stage'] > 7 else "active" if project['flow_stage'] == 7 else "pending"}
        ]
        
        for i, stage in enumerate(stages):
            status_class = "completed" if stage['status'] == "completed" else ""
            icon = "✅" if stage['status'] == "completed" else "🔵" if stage['status'] == "active" else "⚪"
            
            st.markdown(f"""
            <div class="timeline-item {status_class}">
                <h4>{icon} Stage {i+1}: {stage['name']}</h4>
                <p>ステータス: {stage['status']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 進捗チャート
        st.markdown("### 📊 進捗チャート")
        
        # ガントチャート風の表示
        fig = go.Figure()
        
        # 各ステージのデータ
        stage_data = []
        for i, stage in enumerate(stages):
            if stage['status'] == 'completed':
                stage_data.append({
                    'Task': stage['name'],
                    'Start': i,
                    'Finish': i + 1,
                    'Status': 'completed'
                })
            elif stage['status'] == 'active':
                stage_data.append({
                    'Task': stage['name'],
                    'Start': i,
                    'Finish': i + 0.5,
                    'Status': 'active'
                })
        
        # プロットの追加
        for item in stage_data:
            color = '#10b981' if item['Status'] == 'completed' else '#3b82f6'
            fig.add_trace(go.Bar(
                x=[item['Finish'] - item['Start']],
                y=[item['Task']],
                orientation='h',
                name=item['Task'],
                marker=dict(color=color),
                base=item['Start'],
                showlegend=False
            ))
        
        fig.update_layout(
            title="ステージ進捗状況",
            xaxis_title="進捗",
            yaxis_title="ステージ",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(range=[0, 8])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # コンテンツタブ
    with tabs[2]:
        st.markdown("### 📝 生成されたコンテンツ")
        
        # コンテンツが存在する場合
        if 'generated_content' in project['flow_data']:
            content_types = ["SNS投稿", "プレスリリース", "ブログ記事", "メールテンプレート"]
            content_tabs = st.tabs(content_types)
            
            with content_tabs[0]:
                st.markdown("#### Twitter/X 投稿案")
                st.markdown("""
                <div class="content-preview">
                🚀 新製品リリース！<br><br>
                AI搭載の次世代タスク管理ツールで、<br>
                あなたの生産性を3倍にアップ⚡<br><br>
                ✅ 自動優先順位付け<br>
                ✅ スマート通知<br>
                ✅ チーム連携強化<br><br>
                今なら30日間無料トライアル！<br>
                #AI #生産性向上 #タスク管理
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### LinkedIn 投稿案")
                st.markdown("""
                <div class="content-preview">
                プロフェッショナルの皆様へ<br><br>
                働き方改革の次のステップは「AI活用」です。<br><br>
                新しいタスク管理ツールは：<br>
                • 業務の自動化で時間を30%削減<br>
                • データドリブンな意思決定をサポート<br>
                • チームの生産性を大幅向上<br><br>
                詳細はコメント欄のリンクから<br>
                #働き方改革 #DX #生産性向上
                </div>
                """, unsafe_allow_html=True)
            
            with content_tabs[1]:
                st.markdown("#### プレスリリース")
                st.markdown("""
                <div class="content-preview">
                <strong>【プレスリリース】AI搭載タスク管理ツール「TaskFlow AI」をリリース</strong><br><br>
                2025年1月10日<br>
                株式会社〇〇<br><br>
                株式会社〇〇（本社：東京都港区、代表取締役：山田太郎）は、
                AI技術を活用した革新的なタスク管理ツール「TaskFlow AI」を
                2025年1月15日より提供開始することを発表しました。<br><br>
                【製品の特徴】<br>
                1. AIによる自動タスク優先順位付け<br>
                2. 予測分析に基づくスケジュール最適化<br>
                3. チーム全体の生産性可視化<br><br>
                【価格】<br>
                月額980円〜（30日間無料トライアルあり）<br><br>
                【お問い合わせ】<br>
                press@example.com
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("コンテンツはステージ6で生成されます")
    
    # マーケティング施策タブ
    with tabs[3]:
        st.markdown("### 🎯 マーケティング戦略")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📱 チャネル戦略")
            channels = {
                "SNS広告": 40,
                "インフルエンサー": 25,
                "コンテンツマーケティング": 20,
                "メールマーケティング": 15
            }
            
            fig = px.pie(
                values=list(channels.values()),
                names=list(channels.keys()),
                title="予算配分",
                color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 KPI目標")
            kpis = {
                "リーチ数": "100万インプレッション",
                "エンゲージメント率": "5%以上",
                "コンバージョン率": "2%",
                "CAC": "¥3,000以下",
                "LTV": "¥30,000以上"
            }
            
            for kpi, target in kpis.items():
                st.metric(kpi, target)
        
        st.markdown("#### 📅 キャンペーンスケジュール")
        
        # スケジュールのガントチャート
        schedule_data = [
            {"Task": "ティザーキャンペーン", "Start": "2025-01-10", "Finish": "2025-01-14"},
            {"Task": "ローンチキャンペーン", "Start": "2025-01-15", "Finish": "2025-01-22"},
            {"Task": "インフルエンサー施策", "Start": "2025-01-18", "Finish": "2025-01-25"},
            {"Task": "リターゲティング", "Start": "2025-01-20", "Finish": "2025-02-15"}
        ]
        
        df_schedule = pd.DataFrame(schedule_data)
        
        fig = px.timeline(
            df_schedule,
            x_start="Start",
            x_end="Finish",
            y="Task",
            title="マーケティングスケジュール"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 予算・ROIタブ
    with tabs[4]:
        st.markdown("### 💰 予算管理とROI予測")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-box">
                <div class="metric-label">総予算</div>
                <div class="metric-value">¥500万</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-box">
                <div class="metric-label">使用済み</div>
                <div class="metric-value">¥120万</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-box">
                <div class="metric-label">予測ROI</div>
                <div class="metric-value">320%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ROI予測グラフ
        st.markdown("#### 📊 ROI予測推移")
        
        months = ['1月', '2月', '3月', '4月', '5月', '6月']
        investment = [50, 80, 100, 120, 140, 150]
        revenue = [30, 120, 250, 400, 550, 700]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='投資額（万円）',
            x=months,
            y=investment,
            marker_color='#ef4444'
        ))
        
        fig.add_trace(go.Bar(
            name='収益（万円）',
            x=months,
            y=revenue,
            marker_color='#10b981'
        ))
        
        fig.update_layout(
            title="投資対効果の推移",
            xaxis_title="月",
            yaxis_title="金額（万円）",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 詳細な予算内訳
        st.markdown("#### 💸 予算内訳")
        
        budget_breakdown = {
            "広告費": {"予算": "¥200万", "使用済み": "¥60万", "進捗": 30},
            "コンテンツ制作": {"予算": "¥100万", "使用済み": "¥30万", "進捗": 30},
            "インフルエンサー": {"予算": "¥150万", "使用済み": "¥20万", "進捗": 13},
            "ツール・システム": {"予算": "¥50万", "使用済み": "¥10万", "進捗": 20}
        }
        
        for category, data in budget_breakdown.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{category}**")
                st.progress(data['進捗'] / 100)
            with col2:
                st.write(f"予算: {data['予算']}")
            with col3:
                st.write(f"使用: {data['使用済み']}")
    
    # 設定タブ
    with tabs[5]:
        st.markdown("### ⚙️ プロジェクト設定")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("基本設定")
            
            project_name = st.text_input("プロジェクト名", value=project['name'])
            project_desc = st.text_area("プロジェクト説明", value=project.get('description', ''))
            
            st.subheader("通知設定")
            
            notify_progress = st.checkbox("進捗更新時に通知", value=True)
            notify_complete = st.checkbox("ステージ完了時に通知", value=True)
            notify_alert = st.checkbox("アラート発生時に通知", value=True)
        
        with col2:
            st.subheader("自動化設定")
            
            auto_progress = st.checkbox("自動進行モード", value=False)
            auto_content = st.checkbox("コンテンツ自動生成", value=True)
            auto_deploy = st.checkbox("自動デプロイ", value=False)
            
            st.subheader("データ管理")
            
            if st.button("📥 データをエクスポート", type="secondary"):
                st.success("プロジェクトデータをエクスポートしました")
            
            if st.button("🗑️ プロジェクトを削除", type="secondary"):
                st.warning("本当に削除しますか？この操作は取り消せません。")
        
        if st.button("💾 設定を保存", type="primary"):
            # 設定を保存
            st.session_state.projects[st.session_state.selected_project_id]['name'] = project_name
            st.session_state.projects[st.session_state.selected_project_id]['description'] = project_desc
            st.success("設定を保存しました")

else:
    st.info("プロジェクトを選択してください")