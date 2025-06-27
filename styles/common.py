#!/usr/bin/env python3
"""
共通CSSスタイル定義
全アプリケーションで使用される統一されたスタイルを提供
"""

def get_common_styles():
    """共通CSSスタイルを返す"""
    return """
    <style>
        /* ========== ベーステーマ ========== */
        .stApp {
            background-color: #0e1117;
        }
        
        /* サイドバーのz-index調整 */
        section[data-testid="stSidebar"] {
            background-color: #1e2329;
            border-right: 1px solid #2a3441;
            z-index: 10;
        }
        
        section[data-testid="stSidebar"] button {
            width: 100%;
            text-align: left;
            margin-bottom: 0.25rem;
            background-color: transparent;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }
        
        section[data-testid="stSidebar"] button:hover {
            background-color: rgba(34, 197, 94, 0.1);
            border-color: rgba(34, 197, 94, 0.3);
        }
        
        /* メインコンテンツのz-index調整 */
        .main .block-container {
            z-index: 1;
            position: relative;
        }
        
        /* ========== カード共通スタイル ========== */
        .widget-card, .project-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            border: 1px solid rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
        }
        
        .widget-card:hover, .project-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.4);
        }
        
        /* ウィジェットカード専用 */
        .widget-card {
            padding: 25px;
            border-radius: 15px;
        }
        
        /* ========== ヘッダースタイル ========== */
        .widget-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .widget-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: #3b82f6;
        }
        
        /* ========== メトリクススタイル ========== */
        .metric-container {
            background: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }
        
        /* ========== ボタンスタイル ========== */
        .nav-button {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .nav-button:hover {
            background: rgba(59, 130, 246, 0.2);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
        }
        
        /* ========== バッジスタイル ========== */
        .status-badge {
            background: rgba(59, 130, 246, 0.2);
            color: #3b82f6;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .project-type-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* ========== プログレスバー ========== */
        .project-progress {
            margin-top: 0.75rem;
            height: 2px;
        }
        
        /* ========== アイテムスタイル ========== */
        .todo-item {
            background: rgba(30, 41, 59, 0.5);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            transition: all 0.2s;
        }
        
        .todo-item:hover {
            background: rgba(30, 41, 59, 0.8);
        }
        
        .todo-priority-high {
            border-left: 3px solid #ef4444;
        }
        
        .todo-priority-medium {
            border-left: 3px solid #f59e0b;
        }
        
        .todo-priority-low {
            border-left: 3px solid #10b981;
        }
        
        /* ========== グリーティングスタイル ========== */
        .greeting {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        /* ========== ツリー表示スタイル ========== */
        .tree-container {
            background: linear-gradient(145deg, #1e293b 0%, #334155 100%);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            border: 2px solid rgba(59, 130, 246, 0.2);
        }
        
        .tree-category {
            margin-bottom: 20px;
        }
        
        .tree-category-header {
            font-size: 1.2rem;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        
        .tree-category-icon {
            margin-right: 10px;
            font-size: 1.3rem;
        }
        
        .tree-item {
            margin-left: 30px;
            padding: 8px 15px;
            border-left: 2px solid rgba(59, 130, 246, 0.3);
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }
        
        .tree-item:hover {
            background: rgba(59, 130, 246, 0.1);
            border-left-color: #3b82f6;
        }
        
        .tree-item::before {
            content: '└─';
            position: absolute;
            left: -15px;
            color: rgba(59, 130, 246, 0.5);
        }
        
        .tree-item-name {
            display: flex;
            align-items: center;
            color: #e2e8f0;
        }
        
        .tree-item-icon {
            margin-right: 8px;
        }
        
        .tree-item-size {
            color: #94a3b8;
            font-size: 0.85rem;
        }
        
        /* ========== フロースタイル (Shigotoba用) ========== */
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
        
        /* ========== モード表示 ========== */
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
        
        /* ========== コスト表示 ========== */
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
    </style>
    """

def get_project_type_style(project_type):
    """プロジェクトタイプに応じたアイコンと色を返す"""
    styles = {
        'dev': {'icon': '🏗️', 'color': '#3b82f6'},
        'marketing': {'icon': '🎨', 'color': '#8b5cf6'},
        'analysis': {'icon': '📊', 'color': '#10b981'},
        'default': {'icon': '📋', 'color': '#64748b'}
    }
    return styles.get(project_type, styles['default'])