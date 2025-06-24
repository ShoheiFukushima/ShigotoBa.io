#!/usr/bin/env python3
"""
コンテンツ生成ツール - Gemini APIを使用したマーケティングコンテンツ生成
"""

import os
import sys
import asyncio
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ai_client import ai_client
from config.ai_models import TaskType

class ContentGenerator:
    """コンテンツ生成クラス"""
    
    def __init__(self):
        self.ai_client = ai_client
    
    async def generate_social_media_posts(
        self,
        product_info: Dict[str, str],
        platforms: List[str] = ["twitter", "linkedin", "facebook"],
        tone: str = "professional"
    ) -> Dict[str, str]:
        """
        ソーシャルメディア投稿を生成
        
        Args:
            product_info: 製品情報
            platforms: 生成するプラットフォーム
            tone: トーン（professional/casual/friendly）
        
        Returns:
            プラットフォームごとの投稿内容
        """
        platform_specs = {
            "twitter": "280文字以内、ハッシュタグ付き",
            "linkedin": "プロフェッショナルなトーン、500文字程度",
            "facebook": "カジュアルで親しみやすい、300-500文字",
            "instagram": "視覚的な説明、ハッシュタグ多め、200文字程度"
        }
        
        posts = {}
        
        for platform in platforms:
            if platform not in platform_specs:
                continue
            
            prompt = f"""
            以下の製品について{platform}用の投稿を作成してください：
            
            製品名: {product_info.get('name', 'N/A')}
            カテゴリ: {product_info.get('category', 'N/A')}
            ターゲット: {product_info.get('target', 'N/A')}
            特徴: {product_info.get('uniqueness', 'N/A')}
            
            要件:
            - プラットフォーム: {platform}
            - 仕様: {platform_specs[platform]}
            - トーン: {tone}
            - CTAを含める
            - 適切なハッシュタグを追加
            
            投稿内容のみを返してください。
            """
            
            response = await self.ai_client.generate_content(
                prompt=prompt,
                task_type=TaskType.CONTENT_GENERATION.value,
                temperature=0.7,
                max_tokens=500
            )
            
            posts[platform] = response.get('content', '').strip()
        
        return posts
    
    async def generate_blog_post(
        self,
        topic: str,
        keywords: List[str],
        word_count: int = 800,
        style: str = "informative"
    ) -> Dict[str, str]:
        """
        ブログ記事を生成
        
        Args:
            topic: トピック
            keywords: キーワードリスト
            word_count: 目標文字数
            style: スタイル（informative/persuasive/educational）
        
        Returns:
            タイトルと本文
        """
        prompt = f"""
        以下の要件でブログ記事を作成してください：
        
        トピック: {topic}
        キーワード: {', '.join(keywords)}
        文字数: 約{word_count}文字
        スタイル: {style}
        
        以下の形式で回答してください：
        
        【タイトル】
        （魅力的なタイトル）
        
        【本文】
        （構造化された本文）
        
        構成:
        1. 導入（問題提起）
        2. 本論（3-4つのポイント）
        3. まとめ（CTA含む）
        """
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.CONTENT_GENERATION.value,
            temperature=0.6,
            max_tokens=2000
        )
        
        content = response.get('content', '')
        
        # タイトルと本文を分離
        title = ""
        body = ""
        
        if "【タイトル】" in content:
            parts = content.split("【本文】")
            if len(parts) >= 2:
                title_part = parts[0].replace("【タイトル】", "").strip()
                title = title_part.split('\n')[0].strip()
                body = parts[1].strip()
        else:
            lines = content.split('\n')
            if lines:
                title = lines[0].strip()
                body = '\n'.join(lines[1:]).strip()
        
        return {
            "title": title,
            "body": body
        }
    
    async def generate_email_campaign(
        self,
        campaign_type: str,
        product_info: Dict[str, str],
        target_audience: str
    ) -> Dict[str, str]:
        """
        メールキャンペーンを生成
        
        Args:
            campaign_type: キャンペーンタイプ（launch/promotion/newsletter）
            product_info: 製品情報
            target_audience: ターゲットオーディエンス
        
        Returns:
            件名と本文
        """
        campaign_descriptions = {
            "launch": "新製品ローンチ",
            "promotion": "期間限定プロモーション",
            "newsletter": "定期ニュースレター"
        }
        
        prompt = f"""
        以下の要件でメールキャンペーンを作成してください：
        
        キャンペーンタイプ: {campaign_descriptions.get(campaign_type, campaign_type)}
        製品: {product_info.get('name', 'N/A')}
        特徴: {product_info.get('uniqueness', 'N/A')}
        ターゲット: {target_audience}
        
        以下の形式で回答してください：
        
        【件名】
        （開封率を高める魅力的な件名）
        
        【プレヘッダー】
        （件名を補完する短文）
        
        【本文】
        （パーソナライズされた本文）
        - 導入
        - メインメッセージ
        - ベネフィット（箇条書き）
        - CTA
        - 追伸
        """
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.CONTENT_GENERATION.value,
            temperature=0.6,
            max_tokens=1500
        )
        
        content = response.get('content', '')
        
        # 各要素を抽出
        subject = ""
        preheader = ""
        body = ""
        
        if "【件名】" in content:
            parts = content.split("【")
            for part in parts:
                if part.startswith("件名】"):
                    subject = part.replace("件名】", "").split('\n')[0].strip()
                elif part.startswith("プレヘッダー】"):
                    preheader = part.replace("プレヘッダー】", "").split('\n')[0].strip()
                elif part.startswith("本文】"):
                    body = part.replace("本文】", "").strip()
        
        return {
            "subject": subject,
            "preheader": preheader,
            "body": body
        }
    
    async def generate_press_release(
        self,
        announcement_type: str,
        company_info: Dict[str, str],
        details: str
    ) -> str:
        """
        プレスリリースを生成
        
        Args:
            announcement_type: 発表タイプ（product_launch/partnership/achievement）
            company_info: 企業情報
            details: 詳細情報
        
        Returns:
            プレスリリース全文
        """
        prompt = f"""
        以下の情報でプレスリリースを作成してください：
        
        発表タイプ: {announcement_type}
        企業名: {company_info.get('name', '株式会社〇〇')}
        詳細: {details}
        
        プレスリリースの形式：
        1. タイトル（報道発表用）
        2. リード文（要約）
        3. 本文
           - 背景
           - 詳細内容
           - 今後の展望
        4. 企業概要
        5. 問い合わせ先
        
        プロフェッショナルで信頼性の高い文体で作成してください。
        """
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.CONTENT_GENERATION.value,
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.get('content', '').strip()
    
    async def generate_ad_copy(
        self,
        ad_platform: str,
        product_info: Dict[str, str],
        campaign_goal: str
    ) -> Dict[str, Any]:
        """
        広告コピーを生成
        
        Args:
            ad_platform: 広告プラットフォーム（google/facebook/instagram）
            product_info: 製品情報
            campaign_goal: キャンペーン目標（awareness/conversion/engagement）
        
        Returns:
            広告要素の辞書
        """
        platform_specs = {
            "google": {
                "headline_limit": 30,
                "description_limit": 90,
                "headlines_count": 3
            },
            "facebook": {
                "headline_limit": 40,
                "text_limit": 125,
                "description_limit": 30
            },
            "instagram": {
                "caption_limit": 2200,
                "hashtag_count": 30
            }
        }
        
        spec = platform_specs.get(ad_platform, platform_specs["google"])
        
        prompt = f"""
        {ad_platform}広告用のコピーを作成してください：
        
        製品: {product_info.get('name', 'N/A')}
        特徴: {product_info.get('uniqueness', 'N/A')}
        価格: {product_info.get('price', 'N/A')}
        目標: {campaign_goal}
        
        制限:
        {json.dumps(spec, ensure_ascii=False, indent=2)}
        
        JSON形式で以下を含めて回答してください：
        {{
            "headlines": ["見出し1", "見出し2", "見出し3"],
            "descriptions": ["説明文1", "説明文2"],
            "cta": "CTAボタンテキスト",
            "hashtags": ["#タグ1", "#タグ2"] // Instagram用
        }}
        """
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.CONTENT_GENERATION.value,
            temperature=0.8,
            max_tokens=1000
        )
        
        try:
            content = response.get('content', '')
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content
            
            return json.loads(json_str)
        except:
            # フォールバック
            return {
                "headlines": ["革新的な" + product_info.get('name', '製品'), "今すぐ体験", "期間限定オファー"],
                "descriptions": ["最高の体験をお届けします", "今なら特別価格でご提供"],
                "cta": "詳細を見る",
                "hashtags": ["#イノベーション", "#新製品"]
            }

# シングルトンインスタンス
content_generator = ContentGenerator()