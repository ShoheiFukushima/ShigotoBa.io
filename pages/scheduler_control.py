#!/usr/bin/env python3
"""
スケジューラー制御ダッシュボード
自動化タスクの設定・監視・管理
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
from enum import Enum

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from automation.scheduler import (
    scheduler as marketing_scheduler, TaskStatus, TaskType,
    get_all_scheduled_tasks, create_scheduled_task, toggle_scheduled_task, run_task_now
)

# 追加のEnum定義
class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TriggerType(Enum):
    CRON = "cron"
    INTERVAL = "interval"
    ONE_TIME = "one_time"
    EVENT = "event"

# スタブ関数
def schedule_daily_social_posts():
    return create_scheduled_task(
        name="毎日のSNS投稿",
        task_type="social_post",
        schedule="0 9 * * *",
        config={"platforms": ["twitter", "linkedin"]}
    )

def schedule_weekly_competitor_analysis():
    return create_scheduled_task(
        name="週次競合分析",
        task_type="data_analysis",
        schedule="0 10 * * MON",
        config={"analysis_type": "competitor"}
    )

def schedule_monthly_performance_report():
    return create_scheduled_task(
        name="月次パフォーマンスレポート",
        task_type="report_generation",
        schedule="0 9 1 * *",
        config={"report_type": "monthly_performance"}
    )

# ページ設定
st.set_page_config(
    page_title="スケジューラー制御",
    page_icon="⚙️",
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
    
    /* スケジューラー状態表示 */
    .scheduler-status {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        border: 2px solid;
    }
    
    .scheduler-running {
        border-color: #10b981;
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
    }
    
    .scheduler-stopped {
        border-color: #ef4444;
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
    }
    
    .status-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #e2e8f0;
        margin-bottom: 10px;
    }
    
    .status-indicator {
        font-size: 3rem;
        margin: 10px 0;
    }
    
    /* タスクカード */
    .task-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        transition: all 0.3s;
    }
    
    .task-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .task-card.pending {
        border-left: 4px solid #f59e0b;
    }
    
    .task-card.running {
        border-left: 4px solid #3b82f6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .task-card.completed {
        border-left: 4px solid #10b981;
    }
    
    .task-card.failed {
        border-left: 4px solid #ef4444;
    }
    
    .task-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .task-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e2e8f0;
    }
    
    .task-status {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-pending {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
    }
    
    .status-running {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
    }
    
    .status-completed {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .status-failed {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .task-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }
    
    .detail-item {
        text-align: center;
    }
    
    .detail-label {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 5px;
    }
    
    .detail-value {
        font-weight: bold;
        color: #e2e8f0;
    }
    
    /* 統計カード */
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
        border: 1px solid rgba(59, 130, 246, 0.2);
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
    
    /* タスク作成フォーム */
    .task-form {
        background: rgba(30, 41, 59, 0.5);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        margin: 20px 0;
    }
    
    .form-section {
        margin: 20px 0;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #3b82f6;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'scheduler_auto_started' not in st.session_state:
    st.session_state.scheduler_auto_started = False

def render_scheduler_status():
    """スケジューラー状態表示"""
    stats = marketing_scheduler.get_statistics()
    is_running = stats.get('is_running', False)
    
    status_class = "scheduler-running" if is_running else "scheduler-stopped"
    status_text = "稼働中" if is_running else "停止中"
    status_emoji = "🟢" if is_running else "🔴"
    
    st.markdown(f"""
    <div class="scheduler-status {status_class}">
        <div class="status-title">スケジューラー状態</div>
        <div class="status-indicator">{status_emoji}</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 制御ボタン
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not is_running:
            if st.button("▶️ スケジューラー開始", type="primary", use_container_width=True):
                marketing_scheduler.start()
                st.success("スケジューラーを開始しました")
                st.rerun()
    
    with col2:
        if is_running:
            if st.button("⏹️ スケジューラー停止", type="secondary", use_container_width=True):
                marketing_scheduler.stop()
                st.success("スケジューラーを停止しました")
                st.rerun()
    
    with col3:
        if st.button("🔄 状態更新", use_container_width=True):
            st.rerun()
    
    # 統計表示
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('total_tasks', 0)}</div>
            <div class="stat-label">総タスク数</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('pending_tasks', 0)}</div>
            <div class="stat-label">待機中</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('completed_tasks', 0)}</div>
            <div class="stat-label">完了</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_time = stats.get('avg_execution_time', 0)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_time:.1f}s</div>
            <div class="stat-label">平均実行時間</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_task_list():
    """タスク一覧表示"""
    st.header("📋 タスク一覧")
    
    # フィルター
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox(
            "ステータスフィルター",
            options=["全て"] + [status.value for status in TaskStatus],
            index=0
        )
    
    with col2:
        sort_option = st.selectbox(
            "並び順",
            ["作成日時（新しい順）", "作成日時（古い順）", "優先度（高い順）", "次回実行時間"]
        )
    
    # タスク取得
    if status_filter == "全て":
        tasks = marketing_scheduler.list_tasks()
    else:
        tasks = marketing_scheduler.list_tasks(TaskStatus(status_filter))
    
    # ソート
    if sort_option == "作成日時（古い順）":
        tasks.sort(key=lambda t: t.created_at)
    elif sort_option == "優先度（高い順）":
        tasks.sort(key=lambda t: t.priority.value, reverse=True)
    elif sort_option == "次回実行時間":
        tasks.sort(key=lambda t: t.next_run or datetime.max)
    
    # タスク表示
    if tasks:
        for task in tasks:
            status_class = f"task-card {task.status.value}"
            status_badge_class = f"status-{task.status.value}"
            
            # 次回実行時間の表示
            next_run_str = "N/A"
            if task.next_run:
                if task.status == TaskStatus.PENDING:
                    time_diff = task.next_run - datetime.now()
                    if time_diff.total_seconds() > 0:
                        if time_diff.days > 0:
                            next_run_str = f"{time_diff.days}日後"
                        elif time_diff.seconds > 3600:
                            next_run_str = f"{time_diff.seconds // 3600}時間後"
                        elif time_diff.seconds > 60:
                            next_run_str = f"{time_diff.seconds // 60}分後"
                        else:
                            next_run_str = "まもなく"
                    else:
                        next_run_str = "実行待ち"
                else:
                    next_run_str = task.next_run.strftime("%Y-%m-%d %H:%M")
            
            st.markdown(f"""
            <div class="{status_class}">
                <div class="task-header">
                    <div class="task-name">{task.name}</div>
                    <div class="task-status {status_badge_class}">
                        {task.status.value.upper()}
                    </div>
                </div>
                <p style="color: #94a3b8; margin-bottom: 15px;">{task.description}</p>
                <div class="task-details">
                    <div class="detail-item">
                        <div class="detail-label">優先度</div>
                        <div class="detail-value">{task.priority.value}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">実行回数</div>
                        <div class="detail-value">{task.run_count}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">次回実行</div>
                        <div class="detail-value">{next_run_str}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">関数</div>
                        <div class="detail-value">{task.function_name}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # タスク操作ボタン
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                    if st.button(f"⏸️ キャンセル", key=f"cancel_{task.id}"):
                        marketing_scheduler.cancel_task(task.id)
                        st.success(f"タスク '{task.name}' をキャンセルしました")
                        st.rerun()
            
            with col2:
                if st.button(f"🗑️ 削除", key=f"delete_{task.id}"):
                    marketing_scheduler.remove_task(task.id)
                    st.success(f"タスク '{task.name}' を削除しました")
                    st.rerun()
            
            with col3:
                if st.button(f"📊 詳細", key=f"detail_{task.id}"):
                    st.session_state[f"show_detail_{task.id}"] = True
                    st.rerun()
            
            with col4:
                # 実行結果表示
                result = marketing_scheduler.get_task_result(task.id)
                if result:
                    if st.button(f"📋 結果", key=f"result_{task.id}"):
                        st.session_state[f"show_result_{task.id}"] = True
                        st.rerun()
            
            # 詳細表示
            if st.session_state.get(f"show_detail_{task.id}", False):
                with st.expander(f"📊 {task.name} の詳細", expanded=True):
                    st.json({
                        "ID": task.id,
                        "作成日時": task.created_at.isoformat(),
                        "トリガータイプ": task.trigger_type.value,
                        "トリガー設定": task.trigger_config,
                        "引数": task.args,
                        "キーワード引数": task.kwargs,
                        "最大リトライ回数": task.max_retries,
                        "現在のリトライ回数": task.retry_count,
                        "タイムアウト": f"{task.timeout_seconds}秒"
                    })
                    
                    if st.button(f"閉じる", key=f"close_detail_{task.id}"):
                        st.session_state[f"show_detail_{task.id}"] = False
                        st.rerun()
            
            # 実行結果表示
            if st.session_state.get(f"show_result_{task.id}", False) and result:
                with st.expander(f"📋 {task.name} の実行結果", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("実行時間", f"{result.duration_seconds:.2f}秒")
                        st.metric("ステータス", result.status.value)
                    
                    with col2:
                        if result.start_time:
                            st.write(f"**開始**: {result.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        if result.end_time:
                            st.write(f"**終了**: {result.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if result.result:
                        st.subheader("実行結果")
                        st.json(result.result)
                    
                    if result.error:
                        st.subheader("エラー")
                        st.error(result.error)
                    
                    if st.button(f"閉じる", key=f"close_result_{task.id}"):
                        st.session_state[f"show_result_{task.id}"] = False
                        st.rerun()
            
            st.markdown("---")
    
    else:
        st.info("タスクがありません")

def render_task_creation():
    """タスク作成フォーム"""
    st.header("➕ 新規タスク作成")
    
    # クイック作成ボタン
    st.subheader("🚀 クイック作成")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 毎日のSNS投稿", use_container_width=True):
            if 'current_project_id' in st.session_state and st.session_state.current_project_id:
                task_id = schedule_daily_social_posts(st.session_state.current_project_id)
                st.success(f"毎日のSNS投稿タスクを作成しました (ID: {task_id[:8]}...)")
                st.rerun()
            else:
                st.error("プロジェクトを選択してください")
    
    with col2:
        if st.button("📊 週次競合分析", use_container_width=True):
            if 'current_project_id' in st.session_state and st.session_state.current_project_id:
                task_id = schedule_weekly_competitor_analysis(st.session_state.current_project_id)
                st.success(f"週次競合分析タスクを作成しました (ID: {task_id[:8]}...)")
                st.rerun()
            else:
                st.error("プロジェクトを選択してください")
    
    with col3:
        if st.button("📈 月次レポート", use_container_width=True):
            if 'current_project_id' in st.session_state and st.session_state.current_project_id:
                task_id = schedule_monthly_performance_report(st.session_state.current_project_id)
                st.success(f"月次レポートタスクを作成しました (ID: {task_id[:8]}...)")
                st.rerun()
            else:
                st.error("プロジェクトを選択してください")
    
    st.markdown("---")
    
    # 詳細作成フォーム
    st.subheader("🔧 詳細設定")
    
    st.markdown('<div class="task-form">', unsafe_allow_html=True)
    
    with st.form("create_task_form"):
        # 基本情報
        st.markdown('<div class="section-title">📋 基本情報</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("タスク名", placeholder="例: 毎日のTwitter投稿")
            task_description = st.text_area("説明", placeholder="タスクの詳細説明")
        
        with col2:
            function_options = marketing_scheduler.task_registry.list_functions()
            selected_function = st.selectbox("実行関数", function_options)
            
            priority = st.selectbox(
                "優先度",
                options=list(TaskPriority),
                format_func=lambda x: f"{x.name} ({x.value})"
            )
        
        # トリガー設定
        st.markdown('<div class="section-title">⏰ スケジュール設定</div>', unsafe_allow_html=True)
        
        trigger_type = st.selectbox(
            "トリガータイプ",
            options=list(TriggerType),
            format_func=lambda x: {
                TriggerType.ONE_TIME: "一回限り実行",
                TriggerType.INTERVAL: "定期実行",
                TriggerType.CRON: "時刻指定",
                TriggerType.EVENT: "イベント駆動"
            }[x]
        )
        
        trigger_config = {}
        
        if trigger_type == TriggerType.ONE_TIME:
            run_immediately = st.checkbox("即座に実行", value=True)
            if not run_immediately:
                run_date = st.date_input("実行日")
                run_time = st.time_input("実行時刻")
                trigger_config["run_at"] = datetime.combine(run_date, run_time)
        
        elif trigger_type == TriggerType.INTERVAL:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                days = st.number_input("日", min_value=0, value=0, step=1)
            with col2:
                hours = st.number_input("時間", min_value=0, value=0, step=1)
            with col3:
                minutes = st.number_input("分", min_value=0, value=0, step=1)
            with col4:
                seconds = st.number_input("秒", min_value=0, value=0, step=1)
            
            trigger_config = {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            }
        
        elif trigger_type == TriggerType.CRON:
            col1, col2 = st.columns(2)
            
            with col1:
                hour = st.number_input("時", min_value=0, max_value=23, value=9)
            with col2:
                minute = st.number_input("分", min_value=0, max_value=59, value=0)
            
            trigger_config = {"hour": hour, "minute": minute}
        
        # 実行設定
        st.markdown('<div class="section-title">⚙️ 実行設定</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_retries = st.number_input("最大リトライ回数", min_value=0, value=3, step=1)
        
        with col2:
            timeout_seconds = st.number_input("タイムアウト（秒）", min_value=30, value=300, step=30)
        
        # 引数設定
        st.markdown('<div class="section-title">📝 引数設定</div>', unsafe_allow_html=True)
        
        args_text = st.text_area(
            "引数（JSON配列形式）",
            value='["project_id", ["twitter", "linkedin"]]',
            help="例: [\"arg1\", \"arg2\", 123]"
        )
        
        kwargs_text = st.text_area(
            "キーワード引数（JSON辞書形式）",
            value='{}',
            help="例: {\"param1\": \"value1\", \"param2\": 123}"
        )
        
        # 送信ボタン
        submitted = st.form_submit_button("🚀 タスクを作成", type="primary")
        
        if submitted and task_name and selected_function:
            try:
                # 引数をパース
                import json
                args = json.loads(args_text) if args_text.strip() else []
                kwargs = json.loads(kwargs_text) if kwargs_text.strip() else {}
                
                # タスクを作成
                task_id = marketing_scheduler.add_task(
                    name=task_name,
                    description=task_description,
                    function_name=selected_function,
                    args=args,
                    kwargs=kwargs,
                    trigger_type=trigger_type,
                    trigger_config=trigger_config,
                    priority=priority,
                    max_retries=max_retries,
                    timeout_seconds=timeout_seconds
                )
                
                st.success(f"✅ タスクを作成しました: {task_name} (ID: {task_id[:8]}...)")
                st.rerun()
                
            except json.JSONDecodeError as e:
                st.error(f"JSON解析エラー: {e}")
            except Exception as e:
                st.error(f"タスク作成エラー: {e}")
        
        elif submitted:
            st.error("タスク名と実行関数は必須です")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    """分析・統計表示"""
    st.header("📊 実行統計・分析")
    
    stats = marketing_scheduler.get_statistics()
    tasks = marketing_scheduler.list_tasks()
    
    if not tasks:
        st.info("まだタスクがありません")
        return
    
    # ステータス別グラフ
    status_counts = {}
    for status in TaskStatus:
        status_counts[status.value] = len([t for t in tasks if t.status == status])
    
    if any(status_counts.values()):
        col1, col2 = st.columns(2)
        
        with col1:
            # 円グラフ
            fig_pie = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="タスクステータス分布",
                color_discrete_sequence=['#f59e0b', '#3b82f6', '#10b981', '#ef4444', '#8b5cf6']
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # 優先度別グラフ
            priority_counts = {}
            for priority in TaskPriority:
                priority_counts[priority.name] = len([t for t in tasks if t.priority == priority])
            
            fig_bar = px.bar(
                x=list(priority_counts.keys()),
                y=list(priority_counts.values()),
                title="優先度別タスク数",
                color=list(priority_counts.values()),
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # 実行履歴テーブル
    st.subheader("📜 最近の実行履歴")
    
    results = []
    for task in tasks:
        result = marketing_scheduler.get_task_result(task.id)
        if result:
            results.append({
                "タスク名": task.name,
                "ステータス": result.status.value,
                "実行時間": f"{result.duration_seconds:.2f}秒",
                "開始時刻": result.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "エラー": result.error or "なし"
            })
    
    if results:
        df_results = pd.DataFrame(results)
        st.dataframe(df_results, use_container_width=True)
    else:
        st.info("実行履歴がありません")

# スケジューラーの自動開始
if not st.session_state.scheduler_auto_started:
    marketing_scheduler.start()
    st.session_state.scheduler_auto_started = True

# ヘッダー
st.title("⚙️ スケジューラー制御センター")
st.caption("マーケティング自動化タスクの設定・監視・管理")

# タブ構成
tabs = st.tabs(["📊 ダッシュボード", "📋 タスク一覧", "➕ タスク作成", "📈 分析"])

with tabs[0]:
    render_scheduler_status()

with tabs[1]:
    render_task_list()

with tabs[2]:
    render_task_creation()

with tabs[3]:
    render_analytics()

# サイドバー
with st.sidebar:
    st.header("⚙️ スケジューラー制御")
    
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
    
    # リアルタイム統計
    st.subheader("📊 リアルタイム統計")
    
    stats = marketing_scheduler.get_statistics()
    
    st.metric("稼働状況", "稼働中" if stats.get('is_running') else "停止中")
    st.metric("待機中タスク", stats.get('pending_tasks', 0))
    st.metric("実行中タスク", stats.get('running_tasks', 0))
    st.metric("完了タスク", stats.get('completed_tasks', 0))
    
    # 登録済み関数
    st.subheader("🔧 登録済み関数")
    functions = marketing_scheduler.task_registry.list_functions()
    for func in functions:
        st.write(f"• {func}")
    
    st.markdown("---")
    
    # エクスポート
    st.subheader("📥 データエクスポート")
    
    if st.button("📊 タスク設定をエクスポート", use_container_width=True):
        export_data = marketing_scheduler.export_tasks()
        
        st.download_button(
            label="💾 JSON ダウンロード",
            data=json.dumps(export_data, ensure_ascii=False, indent=2),
            file_name=f"scheduler_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📊 フローダッシュボード", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("📤 自動投稿", use_container_width=True):
        st.switch_page("pages/auto_posting.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: スケジューラーは自動的に開始されます。定期的な監視をお勧めします。")