#!/usr/bin/env python3
"""
コンテンツ自動生成システム
プロダクト説明文、SNS投稿、プレスリリース、LPコピーを自動生成
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re

@dataclass
class GeneratedContent:
    """生成されたコンテンツを格納"""
    content_type: str
    title: str
    body: str
    hashtags: List[str]
    cta: str
    metadata: Dict[str, Any]

class ContentGenerator:
    """マーケティングコンテンツを自動生成"""
    
    def __init__(self):
        self.templates_dir = '/Users/fukushimashouhei/dev/marketing-automation-tools/data/templates'
        self.outputs_dir = '/Users/fukushimashouhei/dev/marketing-automation-tools/outputs'
        
    def generate_all_content(self, product_info: Dict[str, Any], market_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, GeneratedContent]:
        """全種類のコンテンツを一括生成"""
        
        print(f"📝 {product_info['name']}のコンテンツ生成を開始...")
        
        contents = {}
        
        # 1. プロダクト説明文
        contents['product_description'] = self._generate_product_description(product_info)
        print("✅ プロダクト説明文生成完了")
        
        # 2. SNS投稿文
        contents['social_posts'] = self._generate_social_posts(product_info)
        print("✅ SNS投稿文生成完了")
        
        # 3. プレスリリース
        contents['press_release'] = self._generate_press_release(product_info)
        print("✅ プレスリリース生成完了")
        
        # 4. ランディングページコピー
        contents['landing_page'] = self._generate_landing_page_copy(product_info)
        print("✅ LPコピー生成完了")
        
        # 5. メールマーケティング
        contents['email_campaign'] = self._generate_email_campaign(product_info)
        print("✅ メールキャンペーン生成完了")
        
        # 結果を保存
        self._save_all_content(product_info['name'], contents)
        
        return contents
    
    def _generate_product_description(self, product_info: Dict[str, Any]) -> GeneratedContent:
        """プロダクト説明文を生成"""
        
        # ショート版
        short_desc = f"{product_info['name']}は、{product_info['category']}を革新する{product_info.get('type', 'ツール')}です。"
        
        # ロング版
        long_desc = f"""
{product_info['name']}は、{product_info['category']}における課題を解決する革新的な{product_info.get('type', 'ソリューション')}です。

【主な特徴】
• {product_info.get('feature1', 'AI搭載で作業を自動化')}
• {product_info.get('feature2', '直感的なインターフェース')}
• {product_info.get('feature3', 'セキュアなクラウド同期')}

【こんな方におすすめ】
• {product_info.get('target_user1', '効率化を求める個人')}
• {product_info.get('target_user2', '成長中の中小企業')}
• {product_info.get('target_user3', 'リモートワークチーム')}

【価格】
{product_info.get('price', '月額980円から')}

今すぐ無料トライアルを始めて、{product_info['category']}の新しい体験を。
"""
        
        return GeneratedContent(
            content_type="product_description",
            title=f"{product_info['name']} - {product_info['category']}を革新",
            body=long_desc,
            hashtags=self._generate_hashtags(product_info),
            cta="無料で試す",
            metadata={"short_version": short_desc, "word_count": len(long_desc)}
        )
    
    def _generate_social_posts(self, product_info: Dict[str, Any]) -> Dict[str, GeneratedContent]:
        """SNS投稿文を生成"""
        
        posts = {}
        
        # Twitter/X用
        twitter_post = f"""
🚀 {product_info['name']}リリース！

{product_info['category']}の常識を変える新サービス

✨ {product_info.get('unique_value', 'AI自動化')}
📱 {product_info.get('platform', 'どこでもアクセス可能')}
💰 {product_info.get('price', '今なら特別価格')}

詳細はこちら→ [URL]

#{product_info['name'].replace(' ', '')} #{product_info['category']}
"""
        
        posts['twitter'] = GeneratedContent(
            content_type="social_post_twitter",
            title="新サービスリリース告知",
            body=twitter_post.strip(),
            hashtags=self._generate_hashtags(product_info),
            cta="詳細を見る",
            metadata={"char_count": len(twitter_post), "platform": "Twitter/X"}
        )
        
        # LinkedIn用
        linkedin_post = f"""
【新サービスのご案内】{product_info['name']}

{product_info['category']}における業務効率化をお考えの皆様へ

弊社は、{product_info['category']}の課題を解決する新しいソリューション「{product_info['name']}」をリリースいたしました。

◆ 主な特徴
- {product_info.get('feature1', 'AI技術による自動化')}
- {product_info.get('feature2', 'コスト削減効果')}
- {product_info.get('feature3', 'セキュアな環境')}

◆ 導入効果
- 作業時間を最大70%削減
- ヒューマンエラーの防止
- チーム全体の生産性向上

詳細資料のダウンロードはこちら: [URL]

#{product_info['category']} #DX推進 #業務効率化
"""
        
        posts['linkedin'] = GeneratedContent(
            content_type="social_post_linkedin",
            title="B2B向けリリース告知",
            body=linkedin_post.strip(),
            hashtags=["DX推進", "業務効率化", product_info['category']],
            cta="資料ダウンロード",
            metadata={"char_count": len(linkedin_post), "platform": "LinkedIn"}
        )
        
        return posts
    
    def _generate_press_release(self, product_info: Dict[str, Any]) -> GeneratedContent:
        """プレスリリースを生成"""
        
        today = datetime.now().strftime('%Y年%m月%d日')
        
        press_release = f"""
報道関係者各位
プレスリリース

{today}
{product_info.get('company', '株式会社〇〇')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{product_info['category']}を革新する「{product_info['name']}」をリリース
〜{product_info.get('unique_value', 'AI技術で業務を自動化')}〜
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{product_info.get('company', '株式会社〇〇')}（本社：東京都、代表取締役：〇〇）は、{product_info['category']}向けの新サービス「{product_info['name']}」を{today}より提供開始することを発表いたします。

■ サービス開発の背景
{product_info['category']}業界では、{product_info.get('problem', '効率化と品質向上')}が大きな課題となっています。当社はこの課題を解決するため、{product_info.get('solution', 'AI技術を活用した革新的なソリューション')}を開発しました。

■ サービスの特徴
1. {product_info.get('feature1', 'AIによる自動化機能')}
   {product_info.get('feature1_detail', '従来の手作業を大幅に削減')}

2. {product_info.get('feature2', '直感的な操作性')}
   {product_info.get('feature2_detail', '専門知識不要で誰でも使える')}

3. {product_info.get('feature3', '高度なセキュリティ')}
   {product_info.get('feature3_detail', '企業の重要データを安全に管理')}

■ 価格・提供開始日
- 提供開始日：{today}
- 価格：{product_info.get('price', '月額980円〜（税別）')}
- 無料トライアル：14日間

■ 今後の展開
当社は、{product_info['name']}を通じて{product_info['category']}業界のDX推進に貢献してまいります。

■ 本件に関するお問い合わせ先
{product_info.get('company', '株式会社〇〇')} 広報部
Email: pr@example.com
TEL: 03-XXXX-XXXX
"""
        
        return GeneratedContent(
            content_type="press_release",
            title=f"{product_info['category']}を革新する「{product_info['name']}」をリリース",
            body=press_release.strip(),
            hashtags=[],
            cta="",
            metadata={"date": today, "format": "formal"}
        )
    
    def _generate_landing_page_copy(self, product_info: Dict[str, Any]) -> GeneratedContent:
        """ランディングページのコピーを生成"""
        
        lp_copy = {
            "hero": {
                "headline": f"{product_info['category']}の常識を変える",
                "subheadline": f"{product_info['name']}で、作業時間を70%削減",
                "cta_button": "無料で始める"
            },
            "problem": {
                "title": "こんなお悩みありませんか？",
                "points": [
                    f"{product_info['category']}に時間がかかりすぎる",
                    "ミスが多くて品質が安定しない",
                    "チーム間の連携がうまくいかない"
                ]
            },
            "solution": {
                "title": f"{product_info['name']}が全て解決します",
                "features": [
                    {
                        "title": "AI自動化",
                        "description": "面倒な作業はAIにお任せ",
                        "icon": "🤖"
                    },
                    {
                        "title": "リアルタイム同期",
                        "description": "チーム全員が常に最新情報を共有",
                        "icon": "🔄"
                    },
                    {
                        "title": "簡単操作",
                        "description": "直感的UIで誰でもすぐに使える",
                        "icon": "✨"
                    }
                ]
            },
            "testimonials": {
                "title": "ユーザーの声",
                "items": [
                    {
                        "text": "導入してから作業効率が3倍になりました！",
                        "author": "A社 マーケティング部"
                    },
                    {
                        "text": "もう手放せません。チーム全体の生産性が向上しました。",
                        "author": "B社 プロジェクトマネージャー"
                    }
                ]
            },
            "pricing": {
                "title": "シンプルな料金プラン",
                "plans": [
                    {
                        "name": "スターター",
                        "price": "¥980/月",
                        "features": ["基本機能", "5ユーザーまで", "メールサポート"]
                    },
                    {
                        "name": "プロ",
                        "price": "¥2,980/月",
                        "features": ["全機能", "無制限ユーザー", "優先サポート", "API連携"]
                    }
                ]
            },
            "cta_final": {
                "headline": "今すぐ始めて、違いを実感してください",
                "button": "14日間無料トライアル",
                "subtext": "クレジットカード不要・いつでもキャンセル可能"
            }
        }
        
        return GeneratedContent(
            content_type="landing_page",
            title=f"{product_info['name']} - ランディングページ",
            body=json.dumps(lp_copy, ensure_ascii=False, indent=2),
            hashtags=[],
            cta="無料トライアル開始",
            metadata={"sections": len(lp_copy), "format": "structured_json"}
        )
    
    def _generate_email_campaign(self, product_info: Dict[str, Any]) -> Dict[str, GeneratedContent]:
        """メールキャンペーンを生成"""
        
        campaigns = {}
        
        # ウェルカムメール
        welcome_email = f"""
件名: {product_info['name']}へようこそ！

こんにちは、

{product_info['name']}にご登録いただき、ありがとうございます。

これから14日間の無料トライアル期間中に、{product_info['category']}の新しい体験をお楽しみください。

【まず始めに】
1. ダッシュボードにログイン
2. 初期設定を完了（約3分）
3. チュートリアルを確認

【おすすめ機能】
• {product_info.get('feature1', 'AI自動化機能')}を試す
• {product_info.get('feature2', 'チーム招待')}でコラボレーション
• {product_info.get('feature3', 'レポート機能')}で成果を可視化

ご不明な点がございましたら、お気軽にサポートまでお問い合わせください。

今すぐログイン → [URL]

{product_info['name']}チーム
"""
        
        campaigns['welcome'] = GeneratedContent(
            content_type="email_welcome",
            title="ウェルカムメール",
            body=welcome_email.strip(),
            hashtags=[],
            cta="ログイン",
            metadata={"sequence": 1, "trigger": "signup"}
        )
        
        return campaigns
    
    def _generate_hashtags(self, product_info: Dict[str, Any]) -> List[str]:
        """関連ハッシュタグを生成"""
        
        hashtags = [
            product_info['name'].replace(' ', ''),
            product_info['category'],
            f"{product_info['category']}ツール",
            "DX",
            "業務効率化",
            "AI活用"
        ]
        
        # 日本語ハッシュタグをクリーニング
        cleaned_hashtags = []
        for tag in hashtags:
            # 特殊文字を除去
            clean_tag = re.sub(r'[^\w\s]', '', tag)
            if clean_tag:
                cleaned_hashtags.append(clean_tag)
        
        return cleaned_hashtags[:5]  # 最大5個まで
    
    def _save_all_content(self, product_name: str, contents: Dict[str, Any]):
        """全コンテンツを保存"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 個別ファイルとして保存
        for content_type, content in contents.items():
            if isinstance(content, dict):
                # SNS投稿など複数プラットフォーム
                for platform, platform_content in content.items():
                    filename = f"{product_name}_{content_type}_{platform}_{timestamp}.json"
                    filepath = os.path.join(self.outputs_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        if hasattr(platform_content, '__dict__'):
                            json.dump(platform_content.__dict__, f, ensure_ascii=False, indent=2)
                        else:
                            json.dump(platform_content, f, ensure_ascii=False, indent=2)
            else:
                # 単一コンテンツ
                filename = f"{product_name}_{content_type}_{timestamp}.json"
                filepath = os.path.join(self.outputs_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    if hasattr(content, '__dict__'):
                        json.dump(content.__dict__, f, ensure_ascii=False, indent=2)
                    else:
                        json.dump(content, f, ensure_ascii=False, indent=2)
        
        # 統合ファイルも作成
        all_content_file = os.path.join(self.outputs_dir, f"{product_name}_all_content_{timestamp}.json")
        
        # シリアライズ可能な形式に変換
        serializable_contents = {}
        for key, value in contents.items():
            if isinstance(value, dict):
                serializable_contents[key] = {}
                for sub_key, sub_value in value.items():
                    if hasattr(sub_value, '__dict__'):
                        serializable_contents[key][sub_key] = sub_value.__dict__
                    else:
                        serializable_contents[key][sub_key] = sub_value
            elif hasattr(value, '__dict__'):
                serializable_contents[key] = value.__dict__
            else:
                serializable_contents[key] = value
        
        with open(all_content_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_contents, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 コンテンツを保存しました: {self.outputs_dir}")


def main():
    """使用例"""
    generator = ContentGenerator()
    
    # サンプルプロダクト情報
    product_info = {
        "name": "TaskMaster Pro",
        "category": "タスク管理",
        "type": "SaaSツール",
        "target": "個人・中小企業",
        "price": "月額980円から",
        "unique_value": "AI自動スケジューリング",
        "feature1": "AIが最適なタスク順序を提案",
        "feature2": "Slack/Teams連携",
        "feature3": "ガントチャート自動生成",
        "company": "タスクマスター株式会社"
    }
    
    # コンテンツ生成
    contents = generator.generate_all_content(product_info)
    
    print("\n✨ コンテンツ生成が完了しました！")


if __name__ == "__main__":
    main()