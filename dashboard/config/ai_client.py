#!/usr/bin/env python3
"""
AI Client - Gemini APIを使用したAIクライアント
"""

import os
import asyncio
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

class AIClient:
    """統一AIクライアント - 現在はGemini API使用（将来的に他のAPIに切り替え可能）"""
    
    def __init__(self):
        # 現在はGeminiを使用（将来的に他のプロバイダーに切り替え可能）
        self.provider = os.getenv('AI_PROVIDER', 'gemini')  # デフォルトはgemini
        
        if self.provider == 'gemini':
            self.api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
            if not self.api_key:
                raise ValueError("GOOGLE_API_KEY または GEMINI_API_KEY が設定されていません")
            
            # Gemini APIの設定
            genai.configure(api_key=self.api_key)
            
            # デフォルトモデル（環境変数で変更可能）
            self.default_model = os.getenv('DEFAULT_AI_MODEL', 'gemini-1.5-flash')
        
    async def generate_content(
        self,
        prompt: str,
        task_type: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        コンテンツ生成（将来的に複数プロバイダー対応可能な設計）
        
        Args:
            prompt: プロンプト
            task_type: タスクタイプ（将来的にプロバイダー別の最適化に使用）
            temperature: 生成の多様性（0.0-1.0）
            max_tokens: 最大トークン数
            model: 使用するモデル（None の場合はデフォルト）
        
        Returns:
            生成結果を含む辞書
        """
        try:
            if self.provider == 'gemini':
                # モデルの選択
                model_name = model or self.default_model
                
                # Geminiモデルの初期化
                generation_config = genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
                
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=generation_config
                )
                
                # 同期的に実行（Streamlitとの互換性のため）
                response = model.generate_content(prompt)
                
                return {
                    "content": response.text,
                    "model": model_name,
                    "provider": self.provider,
                    "usage": {
                        "prompt_tokens": len(prompt.split()),  # 概算
                        "completion_tokens": len(response.text.split()),  # 概算
                        "total_tokens": len(prompt.split()) + len(response.text.split())
                    }
                }
            
            # 将来的に他のプロバイダーをここに追加
            # elif self.provider == 'openai':
            #     return self._generate_with_openai(prompt, temperature, max_tokens, model)
            # elif self.provider == 'anthropic':
            #     return self._generate_with_anthropic(prompt, temperature, max_tokens, model)
            
        except Exception as e:
            return {
                "content": f"エラーが発生しました: {str(e)}",
                "error": str(e),
                "model": model or self.default_model,
                "provider": self.provider
            }
    
    def generate_content_sync(
        self,
        prompt: str,
        task_type: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        同期的なコンテンツ生成（Streamlit用）
        """
        # 新しいイベントループで非同期関数を実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.generate_content(prompt, task_type, temperature, max_tokens, model)
            )
        finally:
            loop.close()

# グローバルインスタンス
ai_client = AIClient()