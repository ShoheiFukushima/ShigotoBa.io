"""
オンボーディング機能コンポーネント
初回利用者向けのガイドツアーと初期設定ウィザード
"""

import streamlit as st
from typing import List, Dict, Optional
import json

def check_onboarding_status() -> bool:
    """オンボーディング完了状態をチェック"""
    if 'onboarding_completed' not in st.session_state:
        st.session_state.onboarding_completed = False
    return st.session_state.onboarding_completed

def render_onboarding_modal():
    """初回利用者向けのオンボーディングモーダルを表示"""
    if not check_onboarding_status():
        with st.container():
            st.markdown("""
            <style>
            .onboarding-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                z-index: 9999;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .onboarding-modal {
                background: #1e293b;
                border-radius: 12px;
                padding: 2rem;
                max-width: 600px;
                width: 90%;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                border: 1px solid #334155;
            }
            .onboarding-header {
                color: #22c55e;
                font-size: 1.5rem;
                margin-bottom: 1rem;
                text-align: center;
            }
            .step-indicator {
                display: flex;
                justify-content: center;
                gap: 0.5rem;
                margin-bottom: 1.5rem;
            }
            .step-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #475569;
                transition: all 0.3s;
            }
            .step-dot.active {
                background: #22c55e;
                transform: scale(1.2);
            }
            </style>
            """, unsafe_allow_html=True)
            
            # オンボーディングステップ管理
            if 'onboarding_step' not in st.session_state:
                st.session_state.onboarding_step = 0
            
            steps = [
                {
                    "title": "🎉 shigotoba.io へようこそ！",
                    "content": "マーケティング自動化プラットフォームで業務を効率化しましょう。",
                    "action": "ツアーを開始"
                },
                {
                    "title": "📋 プロジェクトを選択",
                    "content": "まず、作業したいプロジェクトを選択します。サイドバーでプロジェクトを選んでください。",
                    "action": "次へ"
                },
                {
                    "title": "🎯 カテゴリを選択",
                    "content": "3つのメインカテゴリから目的に応じて選びます：\n• 🏗️ 新規開発\n• 📊 運営・分析\n• 🎨 広告・マーケ",
                    "action": "次へ"
                },
                {
                    "title": "🚀 準備完了！",
                    "content": "さっそく使い始めましょう。困ったときは右下の❓ヘルプボタンをクリック！",
                    "action": "始める"
                }
            ]
            
            current_step = steps[st.session_state.onboarding_step]
            
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.markdown(f'<h2 class="onboarding-header">{current_step["title"]}</h2>', unsafe_allow_html=True)
                
                # ステップインジケーター
                step_dots = ""
                for i in range(len(steps)):
                    active_class = "active" if i == st.session_state.onboarding_step else ""
                    step_dots += f'<div class="step-dot {active_class}"></div>'
                st.markdown(f'<div class="step-indicator">{step_dots}</div>', unsafe_allow_html=True)
                
                st.info(current_step["content"])
                
                col_btn1, col_btn2 = st.columns(2)
                
                if st.session_state.onboarding_step > 0:
                    with col_btn1:
                        if st.button("戻る", use_container_width=True):
                            st.session_state.onboarding_step -= 1
                            st.rerun()
                
                with col_btn2:
                    if st.button(current_step["action"], type="primary", use_container_width=True):
                        if st.session_state.onboarding_step < len(steps) - 1:
                            st.session_state.onboarding_step += 1
                            st.rerun()
                        else:
                            st.session_state.onboarding_completed = True
                            st.session_state.onboarding_step = 0
                            st.rerun()

def render_quick_start_guide():
    """ダッシュボードに表示するクイックスタートガイド"""
    if not check_onboarding_status():
        with st.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); 
                        padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h3 style="color: white; margin: 0;">🚀 クイックスタートガイド</h3>
                <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">
                    初めての方は、以下の手順で始めましょう：
                </p>
                <ol style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">
                    <li>サイドバーでプロジェクトを選択</li>
                    <li>目的に応じたカテゴリを選択</li>
                    <li>使いたいツールをクリック</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎯 ガイドツアーを始める", type="primary"):
                st.session_state.onboarding_completed = False
                st.rerun()

def render_help_button():
    """画面右下に固定表示するヘルプボタン"""
    st.markdown("""
    <style>
    .help-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: #22c55e;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        color: white;
        cursor: pointer;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
        z-index: 1000;
    }
    .help-button:hover {
        transform: scale(1.1);
        background: #16a34a;
    }
    </style>
    <div class="help-button" onclick="window.dispatchEvent(new CustomEvent('show-help'))">
        ❓
    </div>
    """, unsafe_allow_html=True)

def render_project_setup_wizard():
    """プロジェクト未選択時の初期設定ウィザード"""
    st.markdown("""
    <div style="background: #1e293b; border: 2px solid #22c55e; border-radius: 12px; padding: 2rem;">
        <h2 style="color: #22c55e; text-align: center;">🎯 プロジェクトを始めましょう</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### プロジェクトをどのように始めますか？")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 既存のプロジェクトを選択", use_container_width=True, type="primary"):
            st.info("👈 サイドバーのプロジェクトセレクターから選択してください")
    
    with col2:
        if st.button("✨ 新規プロジェクトを作成", use_container_width=True):
            if 'show_new_project_form' not in st.session_state:
                st.session_state.show_new_project_form = True
            else:
                st.session_state.show_new_project_form = not st.session_state.show_new_project_form
    
    if st.session_state.get('show_new_project_form', False):
        st.markdown("---")
        st.markdown("### 新規プロジェクト作成")
        
        project_name = st.text_input("プロジェクト名", placeholder="例: 新商品キャンペーン")
        project_type = st.selectbox("プロジェクトタイプ", 
                                   ["開発系", "マーケティング系", "分析系"])
        project_desc = st.text_area("プロジェクトの説明", 
                                   placeholder="プロジェクトの目的や概要を入力...")
        
        if st.button("プロジェクトを作成", type="primary"):
            if project_name:
                # プロジェクト作成処理
                new_project = {
                    "name": project_name,
                    "type": project_type,
                    "status": "企画中",
                    "progress": 0,
                    "description": project_desc
                }
                
                if 'projects' not in st.session_state:
                    st.session_state.projects = {}
                
                project_id = f"project_{len(st.session_state.projects) + 1}"
                st.session_state.projects[project_id] = new_project
                st.session_state.current_project = project_id
                
                st.success(f"✅ プロジェクト「{project_name}」を作成しました！")
                st.balloons()
                st.session_state.show_new_project_form = False
                st.rerun()
            else:
                st.error("プロジェクト名を入力してください")

def render_recommended_tools(user_type: str = "new"):
    """ユーザータイプに応じたおすすめツールを表示"""
    recommendations = {
        "new": {
            "title": "🌟 初心者におすすめ",
            "tools": [
                {"name": "📊 プロジェクト管理室", "desc": "全体を把握", "path": "pages/_project_management.py"},
                {"name": "🏗️ 開発室", "desc": "タスク管理", "path": "pages/_development_room.py"},
                {"name": "💬 AIチャット", "desc": "相談・支援", "path": "pages/_realtime_chat.py"}
            ]
        },
        "developer": {
            "title": "👨‍💻 開発者向け",
            "tools": [
                {"name": "🏗️ 開発室", "desc": "タスク管理", "path": "pages/_development_room.py"},
                {"name": "🧪 A/Bテスト", "desc": "実験管理", "path": "pages/_ab_testing.py"},
                {"name": "📦 プロダクト管理", "desc": "製品管理", "path": "pages/_product_management.py"}
            ]
        },
        "marketer": {
            "title": "📢 マーケター向け",
            "tools": [
                {"name": "🎨 AI Creative Studio", "desc": "クリエイティブ作成", "path": "pages/_ai_creative_studio.py"},
                {"name": "⚡ リアルタイム広告最適化", "desc": "広告運用", "path": "pages/_realtime_ad_optimizer.py"},
                {"name": "🚀 自動投稿", "desc": "投稿管理", "path": "pages/_auto_posting.py"}
            ]
        }
    }
    
    rec = recommendations.get(user_type, recommendations["new"])
    
    st.markdown(f"### {rec['title']}")
    cols = st.columns(len(rec['tools']))
    
    for i, tool in enumerate(rec['tools']):
        with cols[i]:
            st.markdown(f"""
            <div style="background: #1e293b; border: 1px solid #334155; 
                        border-radius: 8px; padding: 1rem; text-align: center;">
                <h4 style="color: #22c55e; margin: 0;">{tool['name']}</h4>
                <p style="color: #94a3b8; margin: 0.5rem 0; font-size: 0.9rem;">{tool['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"開く", key=f"rec_{i}", use_container_width=True):
                st.switch_page(tool['path'])