#!/usr/bin/env python3
"""
統一AI客户端包装器
各種AIプロバイダーを統一インターフェースで使用
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
from .ai_models import TaskType, model_manager, get_ai_client

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIResponse:
    """AI応答の統一フォーマット"""
    
    def __init__(self, 
                 content: str, 
                 model: str, 
                 provider: str,
                 tokens_used: Optional[int] = None,
                 cost: Optional[float] = None,
                 response_time: Optional[float] = None):
        self.content = content
        self.model = model
        self.provider = provider
        self.tokens_used = tokens_used
        self.cost = cost
        self.response_time = response_time
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "response_time": self.response_time,
            "timestamp": self.timestamp.isoformat()
        }

class UnifiedAIClient:
    """統一AI客户端"""
    
    def __init__(self):
        self.usage_stats = {
            "requests": 0,
            "total_cost": 0.0,
            "total_tokens": 0,
            "model_usage": {}
        }
    
    async def generate_content(self, 
                              prompt: str, 
                              task_type: TaskType,
                              system_prompt: Optional[str] = None,
                              temperature: Optional[float] = None,
                              max_tokens: Optional[int] = None) -> AIResponse:
        """
        統一されたコンテンツ生成メソッド
        """
        start_time = datetime.now()
        
        try:
            model_config = model_manager.get_model_for_task(task_type)
            client, config = get_ai_client(task_type)
            
            # 温度設定の適用
            if temperature is None:
                temperature = config.temperature
            
            # プロバイダー別の処理
            if config.provider.value == "openai":
                response = await self._call_openai(client, prompt, system_prompt, config, temperature, max_tokens)
            elif config.provider.value == "anthropic":
                response = await self._call_anthropic(client, prompt, system_prompt, config, temperature, max_tokens)
            elif config.provider.value == "google":
                response = await self._call_google(client, prompt, system_prompt, config, temperature, max_tokens)
            else:
                raise ValueError(f"Unsupported provider: {config.provider}")
            
            # 統計更新
            self._update_stats(response)
            
            return response
            
        except Exception as e:
            logger.error(f"AI API call failed: {e}")
            # フォールバック処理
            return await self._fallback_response(prompt, task_type, str(e))
    
    async def _call_openai(self, client, prompt: str, system_prompt: Optional[str], 
                          config, temperature: float, max_tokens: Optional[int]) -> AIResponse:
        """OpenAI API呼び出し"""
        import openai
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            start_time = datetime.now()
            
            response = await openai.ChatCompletion.acreate(
                model=config.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or config.max_tokens
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = (tokens_used / 1000) * config.cost_per_1k_tokens
            
            return AIResponse(
                content=content,
                model=config.model_name,
                provider="openai",
                tokens_used=tokens_used,
                cost=cost,
                response_time=response_time
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _call_anthropic(self, client, prompt: str, system_prompt: Optional[str],
                             config, temperature: float, max_tokens: Optional[int]) -> AIResponse:
        """Anthropic API呼び出し"""
        try:
            start_time = datetime.now()
            
            # Anthropicの新しいAPI形式に合わせる
            messages = [{"role": "user", "content": prompt}]
            
            response = await asyncio.to_thread(
                client.messages.create,
                model=config.model_name,
                messages=messages,
                system=system_prompt or "",
                temperature=temperature,
                max_tokens=max_tokens or min(config.max_tokens, 4000)
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            cost = (tokens_used / 1000) * config.cost_per_1k_tokens
            
            return AIResponse(
                content=content,
                model=config.model_name,
                provider="anthropic",
                tokens_used=tokens_used,
                cost=cost,
                response_time=response_time
            )
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def _call_google(self, client, prompt: str, system_prompt: Optional[str],
                          config, temperature: float, max_tokens: Optional[int]) -> AIResponse:
        """Google Gemini API呼び出し"""
        try:
            start_time = datetime.now()
            
            # システムプロンプトがある場合は結合
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = await asyncio.to_thread(
                client.generate_content,
                full_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens or min(config.max_tokens, 8192)
                }
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            content = response.text
            # Geminiはtoken使用量の詳細APIがないため推定
            tokens_used = len(full_prompt.split()) + len(content.split()) * 1.3
            cost = (tokens_used / 1000) * config.cost_per_1k_tokens
            
            return AIResponse(
                content=content,
                model=config.model_name,
                provider="google",
                tokens_used=int(tokens_used),
                cost=cost,
                response_time=response_time
            )
            
        except Exception as e:
            logger.error(f"Google API error: {e}")
            raise
    
    async def _fallback_response(self, prompt: str, task_type: TaskType, error: str) -> AIResponse:
        """フォールバック応答"""
        fallback_content = f"""
        【AI処理エラー】
        申し訳ございませんが、AI処理中にエラーが発生しました。
        
        エラー詳細: {error}
        タスクタイプ: {task_type.value}
        
        手動で処理を続行してください。
        """
        
        return AIResponse(
            content=fallback_content,
            model="fallback",
            provider="system",
            tokens_used=0,
            cost=0.0,
            response_time=0.0
        )
    
    def _update_stats(self, response: AIResponse):
        """使用統計を更新"""
        self.usage_stats["requests"] += 1
        self.usage_stats["total_cost"] += response.cost or 0
        self.usage_stats["total_tokens"] += response.tokens_used or 0
        
        model_key = f"{response.provider}:{response.model}"
        if model_key not in self.usage_stats["model_usage"]:
            self.usage_stats["model_usage"][model_key] = {
                "requests": 0,
                "cost": 0.0,
                "tokens": 0
            }
        
        self.usage_stats["model_usage"][model_key]["requests"] += 1
        self.usage_stats["model_usage"][model_key]["cost"] += response.cost or 0
        self.usage_stats["model_usage"][model_key]["tokens"] += response.tokens_used or 0
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """使用統計を取得"""
        return self.usage_stats.copy()
    
    def reset_stats(self):
        """統計をリセット"""
        self.usage_stats = {
            "requests": 0,
            "total_cost": 0.0,
            "total_tokens": 0,
            "model_usage": {}
        }
    
    # 特化メソッド（使いやすさ向上）
    async def summarize(self, content: str, max_length: int = 200) -> AIResponse:
        """要約専用メソッド"""
        prompt = f"""
        以下のコンテンツを{max_length}文字以内で要約してください：
        
        {content}
        """
        return await self.generate_content(prompt, TaskType.SUMMARIZATION)
    
    async def create_social_post(self, product_info: str, platform: str = "twitter") -> AIResponse:
        """SNS投稿作成専用メソッド"""
        system_prompt = f"""
        あなたは{platform}マーケティングの専門家です。
        魅力的で拡散されやすい投稿を作成してください。
        """
        
        prompt = f"""
        以下の製品情報を基に、{platform}向けの投稿を作成してください：
        
        {product_info}
        """
        
        return await self.generate_content(prompt, TaskType.CONTENT_CREATION, system_prompt)
    
    async def analyze_market(self, product_description: str) -> AIResponse:
        """市場分析専用メソッド"""
        system_prompt = """
        あなたは市場分析の専門家です。
        競合情報、市場規模、トレンドを含む包括的な分析を行ってください。
        """
        
        prompt = f"""
        以下の製品について市場分析を行ってください：
        
        {product_description}
        
        分析項目：
        1. 市場規模と成長率
        2. 主要競合企業
        3. 市場トレンド
        4. 機会と課題
        5. 推奨戦略
        """
        
        return await self.generate_content(prompt, TaskType.MARKET_ANALYSIS, system_prompt)

# グローバルクライアントインスタンス
ai_client = UnifiedAIClient()

# 使用例
async def test_ai_client():
    """テスト関数"""
    print("=== AI統一クライアントテスト ===")
    
    # 要約テスト
    test_content = "人工知能技術の進歩により、マーケティング業界は大きな変革を迎えています。..."
    summary_response = await ai_client.summarize(test_content)
    print(f"要約結果: {summary_response.content[:100]}...")
    print(f"使用モデル: {summary_response.model} | コスト: ¥{summary_response.cost:.4f}")
    
    # 使用統計
    stats = ai_client.get_usage_stats()
    print(f"\n使用統計: {json.dumps(stats, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    asyncio.run(test_ai_client())