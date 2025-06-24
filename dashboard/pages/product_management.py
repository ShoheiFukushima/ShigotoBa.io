#!/usr/bin/env python3
"""
プロダクト情報管理システム
製品情報の一元管理・編集・バージョン管理
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
from typing import Dict, List, Optional

# ページ設定
st.set_page_config(
    page_title="プロダクト情報管理",
    page_icon="📦",
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
    
    /* プロダクトカード */
    .product-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s;
        position: relative;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
        border-color: #3b82f6;
    }
    
    .product-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .product-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3b82f6;
        margin: 0;
    }
    
    .product-category {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    .product-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }
    
    .detail-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 10px;
        border-radius: 8px;
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
    
    /* バージョン履歴 */
    .version-item {
        background: rgba(30, 41, 59, 0.5);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #3b82f6;
    }
    
    .version-date {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    /* 統計カード */
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
    
    /* アクションボタン */
    .action-buttons {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態初期化
if 'products' not in st.session_state:
    st.session_state.products = {}

if 'product_versions' not in st.session_state:
    st.session_state.product_versions = {}

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = None

def generate_product_id():
    """プロダクトIDを生成"""
    return f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def save_product_version(product_id: str, product_data: Dict):
    """プロダクトのバージョンを保存"""
    if product_id not in st.session_state.product_versions:
        st.session_state.product_versions[product_id] = []
    
    version = {
        "version": len(st.session_state.product_versions[product_id]) + 1,
        "timestamp": datetime.now().isoformat(),
        "data": product_data.copy(),
        "changes": []  # 将来的に変更履歴を追跡
    }
    
    st.session_state.product_versions[product_id].append(version)

def get_product_statistics():
    """プロダクト統計を取得"""
    products = st.session_state.products
    
    stats = {
        "total": len(products),
        "categories": {},
        "price_ranges": {
            "0-1000円": 0,
            "1000-5000円": 0,
            "5000-10000円": 0,
            "10000円以上": 0
        }
    }
    
    for product in products.values():
        # カテゴリ別集計
        category = product.get('category', '未分類')
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        # 価格帯別集計
        try:
            price_str = product.get('price', '0')
            price = int(''.join(filter(str.isdigit, price_str)))
            
            if price < 1000:
                stats['price_ranges']['0-1000円'] += 1
            elif price < 5000:
                stats['price_ranges']['1000-5000円'] += 1
            elif price < 10000:
                stats['price_ranges']['5000-10000円'] += 1
            else:
                stats['price_ranges']['10000円以上'] += 1
        except:
            pass
    
    return stats

# ヘッダー
st.title("📦 プロダクト情報管理システム")
st.caption("製品情報の一元管理・編集・バージョン管理")

# タブ構成
tabs = st.tabs(["📋 プロダクト一覧", "➕ 新規登録", "📊 統計・分析", "📜 バージョン履歴"])

# プロダクト一覧タブ
with tabs[0]:
    # フィルター
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "カテゴリフィルター",
            ["すべて"] + list(set(p.get('category', '未分類') for p in st.session_state.products.values())),
            key="category_filter"
        )
    
    with col2:
        search_term = st.text_input("プロダクト名検索", placeholder="検索キーワード...")
    
    with col3:
        sort_by = st.selectbox(
            "並び替え",
            ["登録日（新しい順）", "登録日（古い順）", "名前順", "価格順"],
            key="sort_by"
        )
    
    # プロダクト表示
    if st.session_state.products:
        filtered_products = {}
        
        for pid, product in st.session_state.products.items():
            # カテゴリフィルター
            if category_filter != "すべて" and product.get('category') != category_filter:
                continue
            
            # 検索フィルター
            if search_term and search_term.lower() not in product.get('name', '').lower():
                continue
            
            filtered_products[pid] = product
        
        if filtered_products:
            # ソート
            sorted_items = sorted(
                filtered_products.items(),
                key=lambda x: x[1].get('created_at', ''),
                reverse=(sort_by == "登録日（新しい順）")
            )
            
            for pid, product in sorted_items:
                with st.container():
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-header">
                            <h3 class="product-name">{product['name']}</h3>
                            <span class="product-category">{product.get('category', '未分類')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 詳細情報
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="detail-item">
                            <div class="detail-label">価格</div>
                            <div class="detail-value">{product.get('price', 'N/A')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="detail-item">
                            <div class="detail-label">ターゲット</div>
                            <div class="detail-value">{product.get('target', 'N/A')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="detail-item">
                            <div class="detail-label">登録日</div>
                            <div class="detail-value">{product.get('created_at', 'N/A')[:10]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        versions = len(st.session_state.product_versions.get(pid, []))
                        st.markdown(f"""
                        <div class="detail-item">
                            <div class="detail-label">バージョン</div>
                            <div class="detail-value">v{versions}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 説明
                    if product.get('description'):
                        st.markdown(f"**説明**: {product['description'][:100]}...")
                    
                    # アクションボタン
                    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                    
                    with action_col1:
                        if st.button(f"✏️ 編集", key=f"edit_{pid}"):
                            st.session_state.edit_mode = pid
                            st.rerun()
                    
                    with action_col2:
                        if st.button(f"📋 複製", key=f"clone_{pid}"):
                            new_product = product.copy()
                            new_product['name'] = f"{product['name']} (コピー)"
                            new_product['created_at'] = datetime.now().isoformat()
                            new_pid = generate_product_id()
                            st.session_state.products[new_pid] = new_product
                            st.success(f"プロダクト '{new_product['name']}' を複製しました")
                            st.rerun()
                    
                    with action_col3:
                        if st.button(f"📊 分析", key=f"analyze_{pid}"):
                            st.session_state.current_project_id = pid
                            st.switch_page("pages/product_analysis.py")
                    
                    with action_col4:
                        if st.button(f"🗑️ 削除", key=f"delete_{pid}"):
                            if st.session_state.get(f"confirm_delete_{pid}", False):
                                del st.session_state.products[pid]
                                if pid in st.session_state.product_versions:
                                    del st.session_state.product_versions[pid]
                                st.success(f"プロダクト '{product['name']}' を削除しました")
                                st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{pid}"] = True
                                st.warning("もう一度クリックして削除を確認してください")
                    
                    st.markdown("---")
        else:
            st.info("フィルター条件に一致するプロダクトがありません")
    else:
        st.info("まだプロダクトが登録されていません")

# 新規登録タブ
with tabs[1]:
    st.header("新規プロダクト登録")
    
    # 編集モードの場合
    if st.session_state.edit_mode:
        st.info(f"編集モード: {st.session_state.products[st.session_state.edit_mode]['name']}")
        if st.button("❌ 編集をキャンセル"):
            st.session_state.edit_mode = None
            st.rerun()
    
    # フォーム
    with st.form("product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.edit_mode:
                current_product = st.session_state.products[st.session_state.edit_mode]
                name = st.text_input("プロダクト名*", value=current_product['name'])
                category = st.selectbox(
                    "カテゴリ*",
                    ["SaaS", "アプリ", "コンテンツ", "サービス", "物販", "その他"],
                    index=["SaaS", "アプリ", "コンテンツ", "サービス", "物販", "その他"].index(current_product.get('category', 'その他'))
                )
                price = st.text_input("価格", value=current_product.get('price', ''))
            else:
                name = st.text_input("プロダクト名*", placeholder="例: AIマーケティングツール")
                category = st.selectbox(
                    "カテゴリ*",
                    ["SaaS", "アプリ", "コンテンツ", "サービス", "物販", "その他"]
                )
                price = st.text_input("価格", placeholder="例: 月額980円")
        
        with col2:
            if st.session_state.edit_mode:
                target = st.text_input("ターゲット顧客", value=current_product.get('target', ''))
                uniqueness = st.text_input("独自の価値提案", value=current_product.get('uniqueness', ''))
                website = st.text_input("ウェブサイト", value=current_product.get('website', ''))
            else:
                target = st.text_input("ターゲット顧客", placeholder="例: 中小企業のマーケティング担当者")
                uniqueness = st.text_input("独自の価値提案", placeholder="例: AIによる自動化で工数を80%削減")
                website = st.text_input("ウェブサイト", placeholder="https://example.com")
        
        if st.session_state.edit_mode:
            description = st.text_area(
                "詳細説明",
                value=current_product.get('description', ''),
                height=150
            )
            features = st.text_area(
                "主な機能（改行で区切る）",
                value='\n'.join(current_product.get('features', [])),
                height=100
            )
        else:
            description = st.text_area(
                "詳細説明",
                placeholder="プロダクトの詳細な説明を入力してください...",
                height=150
            )
            features = st.text_area(
                "主な機能（改行で区切る）",
                placeholder="AI分析機能\n自動レポート生成\nリアルタイムダッシュボード",
                height=100
            )
        
        # タグ
        if st.session_state.edit_mode:
            tags = st.text_input(
                "タグ（カンマ区切り）",
                value=', '.join(current_product.get('tags', []))
            )
        else:
            tags = st.text_input(
                "タグ（カンマ区切り）",
                placeholder="AI, マーケティング, 自動化"
            )
        
        submitted = st.form_submit_button(
            "更新" if st.session_state.edit_mode else "登録",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            if name and category:
                product_data = {
                    "name": name,
                    "category": category,
                    "price": price,
                    "target": target,
                    "uniqueness": uniqueness,
                    "website": website,
                    "description": description,
                    "features": [f.strip() for f in features.split('\n') if f.strip()],
                    "tags": [t.strip() for t in tags.split(',') if t.strip()],
                    "updated_at": datetime.now().isoformat()
                }
                
                if st.session_state.edit_mode:
                    # 既存プロダクトの更新
                    pid = st.session_state.edit_mode
                    # バージョン履歴を保存
                    save_product_version(pid, st.session_state.products[pid])
                    # プロダクト情報を更新
                    st.session_state.products[pid].update(product_data)
                    st.success(f"プロダクト '{name}' を更新しました")
                    st.session_state.edit_mode = None
                else:
                    # 新規プロダクトの作成
                    product_data["created_at"] = datetime.now().isoformat()
                    pid = generate_product_id()
                    st.session_state.products[pid] = product_data
                    # 初期バージョンを保存
                    save_product_version(pid, product_data)
                    st.success(f"プロダクト '{name}' を登録しました")
                
                st.rerun()
            else:
                st.error("必須項目を入力してください")

# 統計・分析タブ
with tabs[2]:
    st.header("📊 プロダクト統計・分析")
    
    if st.session_state.products:
        stats = get_product_statistics()
        
        # 統計カード
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{stats['total']}</div>
                <div class="stat-label">総プロダクト数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{len(stats['categories'])}</div>
                <div class="stat-label">カテゴリ数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_versions = sum(len(v) for v in st.session_state.product_versions.values())
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{total_versions}</div>
                <div class="stat-label">総バージョン数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_versions = total_versions / stats['total'] if stats['total'] > 0 else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{avg_versions:.1f}</div>
                <div class="stat-label">平均バージョン数</div>
            </div>
            """, unsafe_allow_html=True)
        
        # グラフ表示
        st.markdown("### カテゴリ別分布")
        
        if stats['categories']:
            # カテゴリ別円グラフ
            fig_category = px.pie(
                values=list(stats['categories'].values()),
                names=list(stats['categories'].keys()),
                title="カテゴリ別プロダクト分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_category.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        # 価格帯分布
        st.markdown("### 価格帯別分布")
        
        price_data = pd.DataFrame([
            {"価格帯": k, "プロダクト数": v}
            for k, v in stats['price_ranges'].items()
            if v > 0
        ])
        
        if not price_data.empty:
            fig_price = px.bar(
                price_data,
                x="価格帯",
                y="プロダクト数",
                title="価格帯別プロダクト分布",
                color="プロダクト数",
                color_continuous_scale="Blues"
            )
            fig_price.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.info("プロダクトを登録すると統計が表示されます")

# バージョン履歴タブ
with tabs[3]:
    st.header("📜 バージョン履歴")
    
    if st.session_state.products:
        # プロダクト選択
        product_names = {pid: p['name'] for pid, p in st.session_state.products.items()}
        selected_product = st.selectbox(
            "プロダクトを選択",
            options=list(product_names.keys()),
            format_func=lambda x: product_names[x]
        )
        
        if selected_product and selected_product in st.session_state.product_versions:
            versions = st.session_state.product_versions[selected_product]
            
            if versions:
                st.info(f"バージョン数: {len(versions)}")
                
                # バージョン履歴を新しい順に表示
                for version in reversed(versions):
                    with st.expander(f"バージョン {version['version']} - {version['timestamp'][:19]}"):
                        # バージョンのデータを表示
                        data = version['data']
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**名前**: {data.get('name', 'N/A')}")
                            st.write(f"**カテゴリ**: {data.get('category', 'N/A')}")
                            st.write(f"**価格**: {data.get('price', 'N/A')}")
                        
                        with col2:
                            st.write(f"**ターゲット**: {data.get('target', 'N/A')}")
                            st.write(f"**独自性**: {data.get('uniqueness', 'N/A')}")
                        
                        if data.get('description'):
                            st.write(f"**説明**: {data['description']}")
                        
                        # ロールバックボタン
                        if st.button(f"このバージョンに戻す", key=f"rollback_{selected_product}_{version['version']}"):
                            # 現在のバージョンを保存
                            save_product_version(selected_product, st.session_state.products[selected_product])
                            # ロールバック
                            st.session_state.products[selected_product] = data.copy()
                            st.session_state.products[selected_product]['updated_at'] = datetime.now().isoformat()
                            st.success(f"バージョン {version['version']} にロールバックしました")
                            st.rerun()
            else:
                st.info("このプロダクトのバージョン履歴はまだありません")
        else:
            st.info("バージョン履歴を表示するプロダクトを選択してください")
    else:
        st.info("プロダクトを登録するとバージョン履歴が記録されます")

# サイドバー
with st.sidebar:
    st.header("📦 プロダクト管理")
    
    # クイック統計
    if st.session_state.products:
        st.subheader("📊 クイック統計")
        
        stats = get_product_statistics()
        st.metric("総プロダクト数", stats['total'])
        
        # 最新登録プロダクト
        latest_products = sorted(
            st.session_state.products.items(),
            key=lambda x: x[1].get('created_at', ''),
            reverse=True
        )[:3]
        
        if latest_products:
            st.subheader("🆕 最新プロダクト")
            for pid, product in latest_products:
                st.write(f"• {product['name']}")
    
    st.markdown("---")
    
    # エクスポート機能
    st.subheader("📥 データエクスポート")
    
    if st.button("📥 全プロダクトをエクスポート", use_container_width=True):
        if st.session_state.products:
            export_data = {
                "export_date": datetime.now().isoformat(),
                "products": st.session_state.products,
                "versions": st.session_state.product_versions
            }
            
            st.download_button(
                label="💾 JSON ダウンロード",
                data=json.dumps(export_data, ensure_ascii=False, indent=2),
                file_name=f"products_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("エクスポートするプロダクトがありません")
    
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("🧭 ナビゲーション")
    
    if st.button("🏠 ホームに戻る", use_container_width=True):
        st.switch_page("pages/../home.py")
    
    if st.button("📊 プロジェクト管理室", use_container_width=True):
        st.switch_page("pages/project_management.py")
    
    if st.button("🏗️ 開発室", use_container_width=True):
        st.switch_page("pages/development_room.py")

# フッター
st.markdown("---")
st.caption("💡 ヒント: プロダクト情報を詳細に記録することで、より精度の高いマーケティング分析が可能になります。バージョン履歴で過去の状態に戻すこともできます。")