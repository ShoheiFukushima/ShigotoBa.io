#!/usr/bin/env python3
"""
AI模型配置管理系統
用途別AI模型選択とコスト最適化
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AIProvider(Enum):
    """AI提供者"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic" 
    GOOGLE = "google"
    LOCAL = "local"

class TaskType(Enum):
    """タスクタイプ別分類"""
    SUMMARIZATION = "summarization"
    CONTENT_CREATION = "content_creation"
    MARKET_ANALYSIS = "market_analysis"
    CHAT = "chat"
    DATA_ANALYSIS = "data_analysis"
    TRANSLATION = "translation"

@dataclass
class AIModelConfig:
    """AI模型配置"""
    provider: AIProvider
    model_name: str
    cost_per_1k_tokens: float
    max_tokens: int
    temperature: float = 0.7
    description: str = ""

# AI模型定義
AI_MODELS = {
    # OpenAI Models
    "gpt-4": AIModelConfig(
        provider=AIProvider.OPENAI,
        model_name="gpt-4",
        cost_per_1k_tokens=0.03,
        max_tokens=8192,
        temperature=0.7,
        description="高品質創作・複雑分析向け"
    ),
    "gpt-3.5-turbo": AIModelConfig(
        provider=AIProvider.OPENAI,
        model_name="gpt-3.5-turbo",
        cost_per_1k_tokens=0.0015,
        max_tokens=4096,
        temperature=0.7,
        description="汎用・チャット向け"
    ),
    
    # Anthropic Models
    "claude-3-opus": AIModelConfig(
        provider=AIProvider.ANTHROPIC,
        model_name="claude-3-opus-20240229",
        cost_per_1k_tokens=0.015,
        max_tokens=200000,
        temperature=0.7,
        description="最高品質・長文処理"
    ),
    "claude-3-haiku": AIModelConfig(
        provider=AIProvider.ANTHROPIC,
        model_name="claude-3-haiku-20240307",
        cost_per_1k_tokens=0.00025,
        max_tokens=200000,
        temperature=0.7,
        description="高速・低コスト"
    ),
    
    # Google Models
    "gemini-1.5-pro": AIModelConfig(
        provider=AIProvider.GOOGLE,
        model_name="gemini-1.5-pro",
        cost_per_1k_tokens=0.0035,
        max_tokens=1000000,
        temperature=0.7,
        description="コスパ良・最新情報"
    ),
    "gemini-1.5-flash": AIModelConfig(
        provider=AIProvider.GOOGLE,
        model_name="gemini-1.5-flash",
        cost_per_1k_tokens=0.000075,
        max_tokens=1000000,
        temperature=0.7,
        description="超高速・超低コスト"
    )
}

# 用途別推奨模型配置（福島さんの推奨設定）
TASK_MODEL_MAPPING = {
    TaskType.SUMMARIZATION: "gemini-1.5-flash",      # 低コスト・高速
    TaskType.CONTENT_CREATION: "gemini-1.5-pro",     # 高品質創作（Gemini使用）
    TaskType.MARKET_ANALYSIS: "gemini-1.5-pro",      # バランス型・最新情報
    TaskType.CHAT: "gemini-1.5-flash",               # リアルタイム・安定性（Gemini使用）
    TaskType.DATA_ANALYSIS: "gemini-1.5-pro",        # 長文・詳細分析（Gemini使用）
    TaskType.TRANSLATION: "gemini-1.5-flash"         # 低コスト・高精度（Gemini使用）
}

class AIModelManager:
    """AI模型管理クラス"""
    
    def __init__(self):
        self.current_config = TASK_MODEL_MAPPING.copy()
        self._load_environment_config()
    
    def _load_environment_config(self):
        """環境変数から設定を読み込み"""
        for task_type in TaskType:
            env_key = f"AI_MODEL_{task_type.value.upper()}"
            if env_value := os.getenv(env_key):
                if env_value in AI_MODELS:
                    self.current_config[task_type] = env_value
    
    def get_model_for_task(self, task_type: TaskType) -> AIModelConfig:
        """タスクタイプに応じた模型を取得"""
        model_name = self.current_config.get(task_type, "gpt-3.5-turbo")
        return AI_MODELS[model_name]
    
    def set_model_for_task(self, task_type: TaskType, model_name: str):
        """タスクタイプの模型を変更"""
        if model_name not in AI_MODELS:
            raise ValueError(f"Unknown model: {model_name}")
        self.current_config[task_type] = model_name
    
    def get_cost_estimate(self, task_type: TaskType, input_tokens: int, output_tokens: int = 0) -> float:
        """コスト見積もり"""
        model_config = self.get_model_for_task(task_type)
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * model_config.cost_per_1k_tokens
    
    def list_available_models(self) -> Dict[str, AIModelConfig]:
        """利用可能な模型一覧"""
        return AI_MODELS
    
    def get_current_config(self) -> Dict[TaskType, str]:
        """現在の設定を取得"""
        return self.current_config.copy()
    
    def optimize_for_cost(self):
        """コスト最適化設定"""
        cost_optimized = {
            TaskType.SUMMARIZATION: "gemini-1.5-flash",
            TaskType.CONTENT_CREATION: "gemini-1.5-flash",  # 品質下げてコスト重視
            TaskType.MARKET_ANALYSIS: "gemini-1.5-flash",
            TaskType.CHAT: "gemini-1.5-flash",
            TaskType.DATA_ANALYSIS: "gemini-1.5-flash",
            TaskType.TRANSLATION: "gemini-1.5-flash"
        }
        self.current_config.update(cost_optimized)
    
    def optimize_for_quality(self):
        """品質最適化設定"""
        quality_optimized = {
            TaskType.SUMMARIZATION: "gemini-1.5-pro",
            TaskType.CONTENT_CREATION: "gemini-1.5-pro",
            TaskType.MARKET_ANALYSIS: "gemini-1.5-pro",
            TaskType.CHAT: "gemini-1.5-pro",
            TaskType.DATA_ANALYSIS: "gemini-1.5-pro",
            TaskType.TRANSLATION: "gemini-1.5-pro"
        }
        self.current_config.update(quality_optimized)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """使用統計（実装は後で）"""
        return {
            "total_requests": 0,
            "total_cost": 0.0,
            "model_usage": {},
            "avg_response_time": 0.0
        }

# グローバル模型管理インスタンス
model_manager = AIModelManager()

def get_ai_client(task_type: TaskType):
    """タスクタイプに応じたAIクライアントを取得"""
    model_config = model_manager.get_model_for_task(task_type)
    
    if model_config.provider == AIProvider.OPENAI:
        import openai
        return openai.ChatCompletion, model_config
    
    elif model_config.provider == AIProvider.ANTHROPIC:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        return client, model_config
    
    elif model_config.provider == AIProvider.GOOGLE:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(model_config.model_name)
        return model, model_config
    
    else:
        raise ValueError(f"Unsupported provider: {model_config.provider}")

# 使用例とテスト関数
if __name__ == "__main__":
    # 使用例
    manager = AIModelManager()
    
    print("=== 現在の設定 ===")
    for task, model in manager.get_current_config().items():
        config = manager.get_model_for_task(task)
        print(f"{task.value}: {model} (¥{config.cost_per_1k_tokens}/1K tokens)")
    
    print("\n=== コスト見積もり ===")
    for task in TaskType:
        cost = manager.get_cost_estimate(task, input_tokens=1000, output_tokens=500)
        print(f"{task.value}: ¥{cost:.4f}")
    
    print("\n=== コスト最適化後 ===")
    manager.optimize_for_cost()
    total_cost = sum(manager.get_cost_estimate(task, 1000, 500) for task in TaskType)
    print(f"全タスク総コスト: ¥{total_cost:.4f}")