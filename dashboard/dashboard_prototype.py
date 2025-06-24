#!/usr/bin/env python3
"""
パブリッシングダッシュボード プロトタイプ
プロダクト分析から実行まで統合管理
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import streamlit as st
import pandas as pd
from pathlib import Path

# 既存ツールをインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.market_analyzer import MarketAnalyzer
from tools.content_generator import ContentGenerator
from tools.seasonal_analyzer import SeasonalAnalyzer
from tools.growth_phase_strategist import GrowthPhaseStrategist

class PublishingDashboard:
    """統合パブリッシングダッシュボード"""
    
    def __init__(self):
        self.conversation_log_path = "conversation_log.md"
        self.product_info = {}
        self.current_plan = {}
        self.initialize_session()
    
    def initialize_session(self):
        """セッション初期化"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'product_analyzed' not in st.session_state:
            st.session_state.product_analyzed = False
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = {}
    
    def analyze_product_directory(self, directory_path: str) -> Dict[str, Any]:
        """プロダクトディレクトリを分析"""
        analysis = {
            "readme_content": "",
            "main_features": [],
            "tech_stack": [],
            "target_audience": "",
            "unique_value": ""
        }
        
        # README.mdを探して読み込み
        readme_path = os.path.join(directory_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                analysis["readme_content"] = f.read()
            
            # 簡易的な特徴抽出
            lines = analysis["readme_content"].split('\n')
            for line in lines:
                if '機能' in line or 'Features' in line:
                    analysis["main_features"].append(line.strip())
                if 'ターゲット' in line or 'Target' in line:
                    analysis["target_audience"] = line.strip()
        
        # package.jsonから技術スタック取得
        package_json_path = os.path.join(directory_path, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                analysis["tech_stack"] = list(package_data.get("dependencies", {}).keys())[:5]
        
        return analysis
    
    def update_conversation_log(self, speaker: str, message: str):
        """会話ログを更新"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n### [{timestamp}] {speaker}\n{message}\n"
        
        with open(self.conversation_log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        st.session_state.messages.append({
            "speaker": speaker,
            "message": message,
            "timestamp": timestamp
        })
    
    def generate_marketing_plan(self, product_info: Dict[str, Any], 
                              requirements: str) -> Dict[str, Any]:
        """マーケティングプランを生成"""
        
        # 既存の分析ツールを活用
        analyzer = MarketAnalyzer()
        seasonal = SeasonalAnalyzer()
        
        # 市場分析
        market_analysis = analyzer.analyze_product(product_info)
        seasonal_insights = seasonal.analyze_seasonal_opportunity(product_info)
        
        # プラン構築
        plan = {
            "generated_at": datetime.now().isoformat(),
            "items": []
        }
        
        # SNS投稿
        plan["items"].append({
            "type": "twitter_post",
            "title": "Twitter告知投稿",
            "content": f"🚀 {product_info['name']}で{product_info['category']}を効率化！\n\n{product_info.get('unique_value', '')}",
            "scheduled_time": "今すぐ",
            "selected": True
        })
        
        # ブログ記事
        plan["items"].append({
            "type": "blog_post",
            "title": f"{product_info['name']}の使い方ガイド",
            "content": "詳細なチュートリアル記事",
            "scheduled_time": "明日10:00",
            "selected": True
        })
        
        # 画像生成
        plan["items"].append({
            "type": "image_generation",
            "title": "SNS用アイキャッチ画像",
            "prompt": f"{product_info['name']}のモダンなロゴデザイン",
            "size": "1200x630",
            "selected": False
        })
        
        # Google広告
        keywords = ["効率化", product_info['category'], "AI"]
        plan["items"].append({
            "type": "google_ads",
            "title": "検索広告キャンペーン",
            "keywords": keywords,
            "budget": "¥10,000/日",
            "selected": False
        })
        
        return plan
    
    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """選択されたプラン項目を実行"""
        
        results = {
            "executed": [],
            "generated_files": [],
            "errors": []
        }
        
        generator = ContentGenerator()
        
        for item in plan["items"]:
            if not item.get("selected", False):
                continue
            
            try:
                if item["type"] == "twitter_post":
                    # 実際の投稿またはコンテンツ生成
                    results["executed"].append({
                        "type": item["type"],
                        "status": "generated",
                        "content": item["content"]
                    })
                
                elif item["type"] == "blog_post":
                    # ブログ記事生成
                    results["executed"].append({
                        "type": item["type"],
                        "status": "generated",
                        "file": f"blog_post_{datetime.now().strftime('%Y%m%d')}.md"
                    })
                
                elif item["type"] == "image_generation":
                    # 画像生成（プレースホルダー）
                    results["generated_files"].append({
                        "type": "image",
                        "path": f"images/generated_{datetime.now().strftime('%Y%m%d')}.png"
                    })
                
            except Exception as e:
                results["errors"].append({
                    "item": item["title"],
                    "error": str(e)
                })
        
        return results

def main():
    """Streamlitアプリのメイン"""
    
    st.set_page_config(
        page_title="Publishing Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Publishing Dashboard")
    
    dashboard = PublishingDashboard()
    
    # サイドバー：プロダクト情報
    with st.sidebar:
        st.header("🎯 プロダクト情報")
        
        if st.button("📁 ディレクトリを分析"):
            # デモ用の分析結果
            st.session_state.product_analyzed = True
            dashboard.update_conversation_log(
                "Claude",
                "プロダクトディレクトリを分析しました。主要機能：タスク管理、AI自動化、チーム連携"
            )
        
        if st.session_state.product_analyzed:
            st.success("✅ 分析完了")
            st.text("主要機能:")
            st.text("- AI自動スケジューリング")
            st.text("- チーム連携")
            st.text("- 進捗可視化")
    
    # メインエリア
    col1, col2 = st.columns([1, 1])
    
    # 左：チャットインターフェース
    with col1:
        st.header("💬 戦略相談チャット")
        
        # チャット履歴表示
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                if msg["speaker"] == "Claude":
                    st.info(f"🤖 Claude: {msg['message']}")
                else:
                    st.success(f"👤 You: {msg['message']}")
        
        # 入力フォーム
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("メッセージを入力")
            if st.form_submit_button("送信"):
                if user_input:
                    dashboard.update_conversation_log("You", user_input)
                    
                    # Claudeの応答（デモ）
                    if "ターゲット" in user_input:
                        response = "学生向けの場合、6月は期末試験シーズンです。勉強効率化を訴求しましょう。"
                    elif "いつ" in user_input:
                        response = "今は6月なので、梅雨の室内需要と期末試験需要が重なる絶好のタイミングです。"
                    else:
                        response = "承知しました。その方向で戦略を検討します。"
                    
                    dashboard.update_conversation_log("Claude", response)
                    st.experimental_rerun()
    
    # 右：実行プラン
    with col2:
        st.header("📋 実行プラン")
        
        if st.button("🎯 プラン生成", type="primary"):
            # デモ用のプロダクト情報
            product_info = {
                "name": "TaskMaster Pro",
                "category": "タスク管理",
                "target": "学生・若手社会人",
                "unique_value": "AI自動スケジューリング"
            }
            
            plan = dashboard.generate_marketing_plan(product_info, "学生向け訴求")
            st.session_state.current_plan = plan
        
        if st.session_state.current_plan:
            st.subheader("生成されたアクション")
            
            # チェックボックス付きリスト
            selected_items = []
            for i, item in enumerate(st.session_state.current_plan.get("items", [])):
                col_check, col_content = st.columns([1, 9])
                
                with col_check:
                    selected = st.checkbox("", value=item["selected"], key=f"item_{i}")
                    if selected:
                        selected_items.append(i)
                
                with col_content:
                    st.markdown(f"**{item['title']}**")
                    st.text(f"タイプ: {item['type']}")
                    st.text(f"実行時期: {item['scheduled_time']}")
            
            # 実行ボタン
            col_exec1, col_exec2 = st.columns(2)
            with col_exec1:
                if st.button("✅ 選択項目を実行", type="primary"):
                    # 選択状態を更新
                    for i, item in enumerate(st.session_state.current_plan["items"]):
                        item["selected"] = i in selected_items
                    
                    results = dashboard.execute_plan(st.session_state.current_plan)
                    st.success(f"✅ {len(results['executed'])}件のタスクを実行しました")
            
            with col_exec2:
                if st.button("🚀 すべて実行"):
                    for item in st.session_state.current_plan["items"]:
                        item["selected"] = True
                    
                    results = dashboard.execute_plan(st.session_state.current_plan)
                    st.success(f"✅ {len(results['executed'])}件のタスクを実行しました")
    
    # フッター
    st.markdown("---")
    st.caption("💡 ヒント: チャットで戦略を相談 → プラン生成 → 選択して実行")


if __name__ == "__main__":
    # Streamlitアプリとして実行
    # streamlit run dashboard_prototype.py
    print("🚀 ダッシュボードを起動するには:")
    print("streamlit run dashboard/dashboard_prototype.py")
    print("\nまたは、コマンドラインインターフェースを使用:")
    
    dashboard = PublishingDashboard()
    
    # CLIデモ
    print("\n📊 Publishing Dashboard (CLI版)")
    print("="*50)
    
    product_info = {
        "name": "DemoProduct",
        "category": "生産性向上",
        "target": "個人"
    }
    
    plan = dashboard.generate_marketing_plan(product_info, "デモ要件")
    
    print("\n生成されたプラン:")
    for item in plan["items"]:
        status = "✅" if item["selected"] else "⬜"
        print(f"{status} {item['title']} ({item['type']})")
    
    print("\n実行するには main_auto.py を使用してください")