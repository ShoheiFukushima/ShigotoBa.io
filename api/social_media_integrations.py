#!/usr/bin/env python3
"""
ソーシャルメディア統合API
Twitter/X, LinkedIn, Facebook等への自動投稿機能
"""

import os
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import requests
import base64

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlatformType(Enum):
    """ソーシャルメディアプラットフォーム"""
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"

class PostStatus(Enum):
    """投稿ステータス"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

@dataclass
class SocialPost:
    """ソーシャルメディア投稿データ"""
    id: str
    platform: PlatformType
    content: str
    media_urls: List[str] = None
    scheduled_time: Optional[datetime] = None
    hashtags: List[str] = None
    status: PostStatus = PostStatus.DRAFT
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.media_urls is None:
            self.media_urls = []
        if self.hashtags is None:
            self.hashtags = []
        if self.metadata is None:
            self.metadata = {}

class TwitterAPI:
    """Twitter/X API統合"""
    
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # API v2エンドポイント
        self.base_url = "https://api.twitter.com/2"
        
    def _get_headers(self) -> Dict[str, str]:
        """認証ヘッダー生成"""
        if not self.bearer_token:
            raise ValueError("Twitter Bearer Token が設定されていません")
        
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
    
    async def post_tweet(self, content: str, media_ids: List[str] = None) -> Dict[str, Any]:
        """ツイート投稿"""
        if not self.bearer_token:
            logger.warning("Twitter API未設定 - ダミーレスポンスを返します")
            return self._mock_tweet_response(content)
        
        url = f"{self.base_url}/tweets"
        headers = self._get_headers()
        
        payload = {"text": content}
        
        if media_ids:
            payload["media"] = {"media_ids": media_ids}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Twitter投稿成功: {result.get('data', {}).get('id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Twitter投稿エラー: {e}")
            return {"error": str(e)}
    
    def _mock_tweet_response(self, content: str) -> Dict[str, Any]:
        """モック用レスポンス（API未設定時）"""
        return {
            "data": {
                "id": f"mock_{int(datetime.now().timestamp())}",
                "text": content,
                "created_at": datetime.now().isoformat()
            },
            "meta": {"result_count": 1},
            "mock": True
        }
    
    async def upload_media(self, media_path: str) -> Optional[str]:
        """メディアアップロード"""
        if not os.path.exists(media_path):
            logger.error(f"メディアファイルが見つかりません: {media_path}")
            return None
        
        # Twitter Media Upload API (v1.1)
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        
        try:
            with open(media_path, 'rb') as f:
                files = {'media': f}
                headers = self._get_upload_headers()
                
                response = requests.post(upload_url, headers=headers, files=files)
                response.raise_for_status()
                
                result = response.json()
                return result.get('media_id_string')
                
        except Exception as e:
            logger.error(f"メディアアップロードエラー: {e}")
            return None
    
    def _get_upload_headers(self) -> Dict[str, str]:
        """アップロード用認証ヘッダー"""
        # OAuth 1.0a認証が必要（実装簡略化）
        return {"Authorization": f"Bearer {self.bearer_token}"}

class LinkedInAPI:
    """LinkedIn API統合"""
    
    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = "https://api.linkedin.com/v2"
    
    def _get_headers(self) -> Dict[str, str]:
        """認証ヘッダー生成"""
        if not self.access_token:
            raise ValueError("LinkedIn Access Token が設定されていません")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
    
    async def post_update(self, content: str, visibility: str = "PUBLIC") -> Dict[str, Any]:
        """LinkedIn投稿"""
        if not self.access_token:
            logger.warning("LinkedIn API未設定 - ダミーレスポンスを返します")
            return self._mock_linkedin_response(content)
        
        # まずユーザープロファイルIDを取得
        profile_id = await self._get_profile_id()
        if not profile_id:
            return {"error": "プロファイルID取得失敗"}
        
        url = f"{self.base_url}/ugcPosts"
        headers = self._get_headers()
        
        payload = {
            "author": f"urn:li:person:{profile_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"LinkedIn投稿成功: {result.get('id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"LinkedIn投稿エラー: {e}")
            return {"error": str(e)}
    
    async def _get_profile_id(self) -> Optional[str]:
        """ユーザープロファイルID取得"""
        url = f"{self.base_url}/me"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            return result.get('id')
            
        except Exception as e:
            logger.error(f"プロファイルID取得エラー: {e}")
            return None
    
    def _mock_linkedin_response(self, content: str) -> Dict[str, Any]:
        """モック用レスポンス（API未設定時）"""
        return {
            "id": f"urn:li:ugcPost:mock_{int(datetime.now().timestamp())}",
            "author": "urn:li:person:mock_user",
            "created": datetime.now().isoformat(),
            "text": content,
            "mock": True
        }

class FacebookAPI:
    """Facebook API統合"""
    
    def __init__(self):
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def _get_params(self) -> Dict[str, str]:
        """認証パラメータ生成"""
        if not self.access_token:
            raise ValueError("Facebook Access Token が設定されていません")
        
        return {"access_token": self.access_token}
    
    async def post_to_page(self, content: str) -> Dict[str, Any]:
        """Facebookページ投稿"""
        if not self.access_token or not self.page_id:
            logger.warning("Facebook API未設定 - ダミーレスポンスを返します")
            return self._mock_facebook_response(content)
        
        url = f"{self.base_url}/{self.page_id}/feed"
        params = self._get_params()
        params.update({"message": content})
        
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Facebook投稿成功: {result.get('id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Facebook投稿エラー: {e}")
            return {"error": str(e)}
    
    def _mock_facebook_response(self, content: str) -> Dict[str, Any]:
        """モック用レスポンス（API未設定時）"""
        return {
            "id": f"mock_page_id_mock_{int(datetime.now().timestamp())}",
            "created_time": datetime.now().isoformat(),
            "message": content,
            "mock": True
        }

class SocialMediaManager:
    """ソーシャルメディア統合管理"""
    
    def __init__(self):
        self.twitter = TwitterAPI()
        self.linkedin = LinkedInAPI()
        self.facebook = FacebookAPI()
        
        self.post_queue = []
        self.post_history = []
    
    async def create_post(self, 
                         content: str, 
                         platforms: List[PlatformType],
                         scheduled_time: Optional[datetime] = None,
                         hashtags: List[str] = None,
                         media_paths: List[str] = None) -> List[SocialPost]:
        """複数プラットフォーム用投稿作成"""
        
        posts = []
        
        for platform in platforms:
            post_id = f"{platform.value}_{int(datetime.now().timestamp())}"
            
            # プラットフォーム別のコンテンツ調整
            adjusted_content = self._adjust_content_for_platform(content, platform, hashtags)
            
            post = SocialPost(
                id=post_id,
                platform=platform,
                content=adjusted_content,
                scheduled_time=scheduled_time,
                hashtags=hashtags or [],
                media_urls=media_paths or []
            )
            
            posts.append(post)
            
            # 即座投稿 or スケジュール
            if scheduled_time is None:
                await self._publish_post(post)
            else:
                post.status = PostStatus.SCHEDULED
                self.post_queue.append(post)
        
        return posts
    
    def _adjust_content_for_platform(self, 
                                   content: str, 
                                   platform: PlatformType, 
                                   hashtags: List[str] = None) -> str:
        """プラットフォーム別コンテンツ調整"""
        
        if platform == PlatformType.TWITTER:
            # Twitter: 文字数制限とハッシュタグ
            max_length = 260  # ハッシュタグ分を考慮
            if hashtags:
                hashtag_text = " " + " ".join(f"#{tag}" for tag in hashtags)
                content = content[:max_length - len(hashtag_text)] + hashtag_text
            else:
                content = content[:280]  # Twitter文字数制限
                
        elif platform == PlatformType.LINKEDIN:
            # LinkedIn: プロフェッショナルなトーン
            if hashtags:
                hashtag_text = "\n\n" + " ".join(f"#{tag}" for tag in hashtags)
                content += hashtag_text
                
        elif platform == PlatformType.FACEBOOK:
            # Facebook: より詳細な説明可能
            if hashtags:
                hashtag_text = "\n\n" + " ".join(f"#{tag}" for tag in hashtags)
                content += hashtag_text
        
        return content
    
    async def _publish_post(self, post: SocialPost) -> bool:
        """投稿実行"""
        try:
            result = None
            
            if post.platform == PlatformType.TWITTER:
                # メディアアップロード
                media_ids = []
                for media_url in post.media_urls:
                    if os.path.exists(media_url):
                        media_id = await self.twitter.upload_media(media_url)
                        if media_id:
                            media_ids.append(media_id)
                
                result = await self.twitter.post_tweet(post.content, media_ids)
                
            elif post.platform == PlatformType.LINKEDIN:
                result = await self.linkedin.post_update(post.content)
                
            elif post.platform == PlatformType.FACEBOOK:
                result = await self.facebook.post_to_page(post.content)
            
            # 結果処理
            if result and not result.get("error"):
                post.status = PostStatus.PUBLISHED
                post.metadata["api_response"] = result
                post.metadata["published_at"] = datetime.now().isoformat()
                
                logger.info(f"{post.platform.value}投稿成功: {post.id}")
                return True
            else:
                post.status = PostStatus.FAILED
                post.metadata["error"] = result.get("error", "Unknown error")
                
                logger.error(f"{post.platform.value}投稿失敗: {post.id}")
                return False
                
        except Exception as e:
            post.status = PostStatus.FAILED
            post.metadata["error"] = str(e)
            
            logger.error(f"投稿実行エラー: {e}")
            return False
        
        finally:
            self.post_history.append(post)
    
    async def process_scheduled_posts(self):
        """スケジュール投稿処理"""
        current_time = datetime.now()
        
        ready_posts = [
            post for post in self.post_queue 
            if post.scheduled_time and post.scheduled_time <= current_time
        ]
        
        for post in ready_posts:
            await self._publish_post(post)
            self.post_queue.remove(post)
        
        logger.info(f"スケジュール投稿処理完了: {len(ready_posts)}件実行")
    
    def get_post_analytics(self) -> Dict[str, Any]:
        """投稿分析データ取得"""
        total_posts = len(self.post_history)
        
        if total_posts == 0:
            return {"total": 0, "by_platform": {}, "by_status": {}}
        
        # プラットフォーム別統計
        platform_stats = {}
        for platform in PlatformType:
            platform_posts = [p for p in self.post_history if p.platform == platform]
            platform_stats[platform.value] = {
                "total": len(platform_posts),
                "published": len([p for p in platform_posts if p.status == PostStatus.PUBLISHED]),
                "failed": len([p for p in platform_posts if p.status == PostStatus.FAILED])
            }
        
        # ステータス別統計
        status_stats = {}
        for status in PostStatus:
            status_posts = [p for p in self.post_history if p.status == status]
            status_stats[status.value] = len(status_posts)
        
        return {
            "total": total_posts,
            "by_platform": platform_stats,
            "by_status": status_stats,
            "success_rate": len([p for p in self.post_history if p.status == PostStatus.PUBLISHED]) / total_posts * 100
        }
    
    def export_post_history(self) -> Dict[str, Any]:
        """投稿履歴エクスポート"""
        return {
            "export_time": datetime.now().isoformat(),
            "total_posts": len(self.post_history),
            "posts": [
                {
                    "id": post.id,
                    "platform": post.platform.value,
                    "content": post.content,
                    "status": post.status.value,
                    "scheduled_time": post.scheduled_time.isoformat() if post.scheduled_time else None,
                    "hashtags": post.hashtags,
                    "metadata": post.metadata
                }
                for post in self.post_history
            ],
            "analytics": self.get_post_analytics()
        }

# グローバルマネージャーインスタンス
social_manager = SocialMediaManager()

# ユーティリティ関数
def validate_api_keys() -> Dict[str, bool]:
    """API設定確認"""
    return {
        "twitter": bool(os.getenv("TWITTER_BEARER_TOKEN")),
        "linkedin": bool(os.getenv("LINKEDIN_ACCESS_TOKEN")),
        "facebook": bool(os.getenv("FACEBOOK_ACCESS_TOKEN") and os.getenv("FACEBOOK_PAGE_ID"))
    }

async def quick_post(content: str, 
                    platforms: List[str], 
                    hashtags: List[str] = None) -> Dict[str, Any]:
    """クイック投稿関数"""
    
    # プラットフォーム変換
    platform_objs = []
    for platform_str in platforms:
        try:
            platform_objs.append(PlatformType(platform_str.lower()))
        except ValueError:
            logger.warning(f"Unknown platform: {platform_str}")
    
    if not platform_objs:
        return {"error": "有効なプラットフォームが指定されていません"}
    
    # 投稿実行
    posts = await social_manager.create_post(
        content=content,
        platforms=platform_objs,
        hashtags=hashtags
    )
    
    # 結果サマリー
    success_count = len([p for p in posts if p.status == PostStatus.PUBLISHED])
    
    return {
        "success": success_count > 0,
        "posts_created": len(posts),
        "posts_published": success_count,
        "posts": [
            {
                "platform": post.platform.value,
                "status": post.status.value,
                "id": post.id
            }
            for post in posts
        ]
    }

# テスト用関数
async def test_social_integrations():
    """ソーシャルメディア統合テスト"""
    print("=== ソーシャルメディア統合テスト ===")
    
    # API設定確認
    api_status = validate_api_keys()
    print(f"API設定状況: {api_status}")
    
    # テスト投稿
    test_content = "🚀 マーケティング自動化ツールのテスト投稿です！ #マーケティング #自動化"
    test_platforms = ["twitter", "linkedin"]
    
    result = await quick_post(test_content, test_platforms, ["マーケティング", "自動化"])
    print(f"テスト投稿結果: {result}")
    
    # 統計情報
    analytics = social_manager.get_post_analytics()
    print(f"投稿統計: {analytics}")

if __name__ == "__main__":
    asyncio.run(test_social_integrations())