#!/usr/bin/env python3
"""
メトリクス表示コンポーネント
ダッシュボード等で使用される統一されたメトリクス表示
"""

import streamlit as st
from typing import List, Dict, Optional, Union

def render_metrics_row(
    metrics_data: List[Dict[str, Union[str, int, float]]],
    columns: int = 4,
    use_container: bool = False
) -> None:
    """
    メトリクスを横並びで表示
    
    Args:
        metrics_data: メトリクスデータのリスト
            各要素は以下のキーを持つ辞書:
            - label: ラベル
            - value: 値
            - delta (optional): 変化量
            - delta_color (optional): "normal", "inverse", "off"
            - help (optional): ヘルプテキスト
        columns: カラム数
        use_container: コンテナスタイルを使用するか
    """
    if use_container:
        st.markdown("""
        <style>
            [data-testid="metric-container"] {
                background-color: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
    
    cols = st.columns(columns)
    
    for idx, metric in enumerate(metrics_data):
        with cols[idx % columns]:
            delta_color = metric.get('delta_color', 'normal')
            help_text = metric.get('help', None)
            
            st.metric(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta'),
                delta_color=delta_color,
                help=help_text
            )

def render_metric_card(
    title: str,
    value: Union[str, int, float],
    subtitle: Optional[str] = None,
    trend: Optional[Dict[str, Union[str, float]]] = None,
    icon: Optional[str] = None,
    color: str = "#3b82f6"
) -> None:
    """
    カード形式でメトリクスを表示
    
    Args:
        title: タイトル
        value: メイン値
        subtitle: サブタイトル
        trend: トレンド情報 {'value': '+10%', 'direction': 'up'}
        icon: アイコン
        color: アクセントカラー
    """
    trend_icon = ""
    trend_color = color
    
    if trend:
        if trend.get('direction') == 'up':
            trend_icon = "↗"
            trend_color = "#10b981"
        elif trend.get('direction') == 'down':
            trend_icon = "↘"
            trend_color = "#ef4444"
        else:
            trend_icon = "→"
            trend_color = "#f59e0b"
    
    card_html = f"""
    <div class="metric-card" style="border-left: 4px solid {color};">
        <div class="metric-header">
            {f'<span class="metric-icon">{icon}</span>' if icon else ''}
            <span class="metric-title" style="color: {color};">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        {f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''}
        {f'<div class="metric-trend" style="color: {trend_color};">{trend_icon} {trend["value"]}</div>' if trend else ''}
    </div>
    """
    
    st.markdown("""
    <style>
        .metric-card {
            background: rgba(30, 41, 59, 0.8);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        
        .metric-card:hover {
            background: rgba(30, 41, 59, 0.9);
            transform: translateX(5px);
        }
        
        .metric-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .metric-icon {
            font-size: 1.5rem;
            margin-right: 10px;
        }
        
        .metric-title {
            font-size: 1rem;
            font-weight: 600;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #e2e8f0;
            margin: 10px 0;
        }
        
        .metric-subtitle {
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        .metric-trend {
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 5px;
        }
    </style>
    """ + card_html, unsafe_allow_html=True)

def render_progress_metric(
    title: str,
    current: Union[int, float],
    total: Union[int, float],
    unit: str = "",
    color: str = "#3b82f6",
    show_percentage: bool = True
) -> None:
    """
    プログレスバー付きメトリクスを表示
    
    Args:
        title: タイトル
        current: 現在値
        total: 合計値
        unit: 単位
        color: プログレスバーの色
        show_percentage: パーセンテージを表示するか
    """
    percentage = (current / total * 100) if total > 0 else 0
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**{title}**")
        st.progress(percentage / 100)
    
    with col2:
        if show_percentage:
            st.markdown(f"<div style='text-align: right; color: {color}; font-size: 1.2rem; font-weight: bold;'>{percentage:.0f}%</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: right; color: #e2e8f0;'>{current}{unit} / {total}{unit}</div>", unsafe_allow_html=True)

def render_comparison_metrics(
    title: str,
    metrics: List[Dict[str, Union[str, float]]],
    highlight_max: bool = True
) -> None:
    """
    比較メトリクスを表示
    
    Args:
        title: セクションタイトル
        metrics: 比較するメトリクスのリスト
            各要素: {'label': 'A', 'value': 100, 'color': '#3b82f6'}
        highlight_max: 最大値をハイライトするか
    """
    st.markdown(f"### {title}")
    
    if highlight_max:
        max_value = max(m['value'] for m in metrics if isinstance(m['value'], (int, float)))
    
    cols = st.columns(len(metrics))
    
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            is_max = highlight_max and metric['value'] == max_value
            color = metric.get('color', '#3b82f6')
            
            if is_max:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background: rgba(59, 130, 246, 0.2); border-radius: 10px; border: 2px solid {color};">
                    <div style="color: {color}; font-weight: bold;">{metric['label']}</div>
                    <div style="font-size: 2rem; font-weight: bold; color: #e2e8f0; margin: 10px 0;">{metric['value']}</div>
                    <div style="color: #10b981; font-size: 0.8rem;">👑 最高値</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px;">
                    <div style="color: #94a3b8;">{metric['label']}</div>
                    <div style="font-size: 1.5rem; color: #e2e8f0; margin: 10px 0;">{metric['value']}</div>
                </div>
                """, unsafe_allow_html=True)

# プリセットメトリクス
def render_project_metrics(project_count: int, active_count: int, completed_count: int) -> None:
    """プロジェクト関連のメトリクスを表示"""
    metrics_data = [
        {'label': '総プロジェクト数', 'value': project_count},
        {'label': 'アクティブ', 'value': active_count, 'delta': f"+{active_count}"},
        {'label': '完了', 'value': completed_count, 'delta': f"{completed_count/project_count*100:.0f}%"},
        {'label': '進行率', 'value': f"{active_count/project_count*100:.0f}%"}
    ]
    render_metrics_row(metrics_data)

def render_performance_metrics(
    conversion_rate: float,
    revenue: Union[int, float],
    visitors: int,
    growth_rate: float
) -> None:
    """パフォーマンス関連のメトリクスを表示"""
    metrics_data = [
        {
            'label': 'コンバージョン率',
            'value': f"{conversion_rate:.1f}%",
            'delta': f"+{growth_rate:.1f}%"
        },
        {
            'label': '収益',
            'value': f"¥{revenue:,.0f}",
            'delta': f"+{growth_rate:.0f}%"
        },
        {
            'label': '訪問者数',
            'value': f"{visitors:,}",
            'delta': f"+{int(visitors * growth_rate / 100)}"
        },
        {
            'label': '成長率',
            'value': f"{growth_rate:.1f}%",
            'delta': "改善中",
            'delta_color': 'off'
        }
    ]
    render_metrics_row(metrics_data)