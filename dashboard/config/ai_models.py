#!/usr/bin/env python3
"""
AI Models Configuration - モデル設定と管理
"""

from enum import Enum
from typing import Dict, List, Optional, Any
import os
from dataclasses import dataclass

class TaskType(Enum):
    """タスクタイプの定義"""
    CHAT = "chat"
    CONTENT_GENERATION = "content_generation"
    MARKET_ANALYSIS = "market_analysis"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    CREATIVE_WRITING = "creative_writing"
    CODE_GENERATION = "code_generation"
    IMAGE_ANALYSIS = "image_analysis"

class AIProvider(Enum):
    """AIプロバイダーの定義"""
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

@dataclass
class AIModel:
    """AIモデルの定義"""
    id: str
    name: str
    provider: AIProvider
    capabilities: List[TaskType]
    max_tokens: int
    cost_per_1k_tokens: float
    description: str
    is_available: bool = True

# 利用可能なAIモデル
AI_MODELS = {
    "gemini-1.5-flash": AIModel(
        id="gemini-1.5-flash",
        name="Gemini 1.5 Flash",
        provider=AIProvider.GEMINI,
        capabilities=[TaskType.CHAT, TaskType.CONTENT_GENERATION, TaskType.MARKET_ANALYSIS, 
                     TaskType.TRANSLATION, TaskType.SUMMARIZATION, TaskType.CREATIVE_WRITING],
        max_tokens=8192,
        cost_per_1k_tokens=0.000075,
        description="超高速・超低コスト。短いタスクに最適",
        is_available=True
    ),
    "gemini-1.5-pro": AIModel(
        id="gemini-1.5-pro",
        name="Gemini 1.5 Pro",
        provider=AIProvider.GEMINI,
        capabilities=[TaskType.CHAT, TaskType.CONTENT_GENERATION, TaskType.MARKET_ANALYSIS,
                     TaskType.TRANSLATION, TaskType.SUMMARIZATION, TaskType.CREATIVE_WRITING,
                     TaskType.CODE_GENERATION, TaskType.IMAGE_ANALYSIS],
        max_tokens=32768,
        cost_per_1k_tokens=0.0035,
        description="バランス型。複雑なタスクに対応",
        is_available=True
    ),
    "gpt-3.5-turbo": AIModel(
        id="gpt-3.5-turbo",
        name="GPT-3.5 Turbo",
        provider=AIProvider.OPENAI,
        capabilities=[TaskType.CHAT, TaskType.CONTENT_GENERATION, TaskType.TRANSLATION,
                     TaskType.SUMMARIZATION, TaskType.CREATIVE_WRITING],
        max_tokens=4096,
        cost_per_1k_tokens=0.0015,
        description="高速・低コスト。一般的なタスクに適切",
        is_available=False  # APIキーが設定されるまでは無効
    ),
    "gpt-4": AIModel(
        id="gpt-4",
        name="GPT-4",
        provider=AIProvider.OPENAI,
        capabilities=[TaskType.CHAT, TaskType.CONTENT_GENERATION, TaskType.MARKET_ANALYSIS,
                     TaskType.TRANSLATION, TaskType.SUMMARIZATION, TaskType.CREATIVE_WRITING,
                     TaskType.CODE_GENERATION],
        max_tokens=8192,
        cost_per_1k_tokens=0.03,
        description="最高品質。複雑な推論が必要なタスクに最適",
        is_available=False
    ),
    "claude-3-haiku": AIModel(
        id="claude-3-haiku-20240307",
        name="Claude 3 Haiku",
        provider=AIProvider.ANTHROPIC,
        capabilities=[TaskType.CHAT, TaskType.CONTENT_GENERATION, TaskType.TRANSLATION,
                     TaskType.SUMMARIZATION],
        max_tokens=4096,
        cost_per_1k_tokens=0.00025,
        description="超高速・超低コスト。シンプルなタスクに最適",
        is_available=False
    ),
    "claude-3-opus": AIModel(
        id="claude-3-opus-20240229",
        name="Claude 3 Opus",
        provider=AIProvider.ANTHROPIC,
        capabilities=[TaskType.CHAT, TaskType.CONTENT_GENERATION, TaskType.MARKET_ANALYSIS,
                     TaskType.TRANSLATION, TaskType.SUMMARIZATION, TaskType.CREATIVE_WRITING,
                     TaskType.CODE_GENERATION],
        max_tokens=4096,
        cost_per_1k_tokens=0.015,
        description="最高品質。創造的で複雑なタスクに最適",
        is_available=False
    )
}

class ModelManager:
    """AIモデルの管理クラス"""
    
    def __init__(self):
        self.models = AI_MODELS
        self._check_api_availability()
    
    def _check_api_availability(self):
        """APIキーの存在をチェックしてモデルの利用可能性を更新"""
        # Gemini
        if os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY'):
            self.models["gemini-1.5-flash"].is_available = True
            self.models["gemini-1.5-pro"].is_available = True
        else:
            self.models["gemini-1.5-flash"].is_available = False
            self.models["gemini-1.5-pro"].is_available = False
        
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            self.models["gpt-3.5-turbo"].is_available = True
            self.models["gpt-4"].is_available = True
        
        # Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            self.models["claude-3-haiku"].is_available = True
            self.models["claude-3-opus"].is_available = True
    
    def get_available_models(self) -> Dict[str, AIModel]:
        """利用可能なモデルのみを返す"""
        return {k: v for k, v in self.models.items() if v.is_available}
    
    def get_models_for_task(self, task_type: TaskType) -> Dict[str, AIModel]:
        """特定のタスクに対応したモデルを返す"""
        return {
            k: v for k, v in self.models.items() 
            if v.is_available and task_type in v.capabilities
        }
    
    def get_default_model(self, task_type: Optional[TaskType] = None) -> Optional[str]:
        """デフォルトモデルを返す（環境変数で変更可能）"""
        # 環境変数から取得（将来的な切り替えのため）
        default_model = os.getenv('DEFAULT_AI_MODEL', 'gemini-1.5-flash')
        
        # 指定されたモデルが利用可能か確認
        if default_model in self.models and self.models[default_model].is_available:
            return default_model
        
        # Geminiが利用可能ならそれを優先
        if self.models["gemini-1.5-flash"].is_available:
            return "gemini-1.5-flash"
        
        # その他の利用可能なモデルから選択
        available = self.get_available_models()
        if available:
            return list(available.keys())[0]
        
        return None
    
    def get_current_config(self) -> Dict[TaskType, str]:
        """現在のタスクごとのモデル設定を返す"""
        config = {}
        for task_type in TaskType:
            # 現在はすべてGeminiを使用（将来的にタスクごとに変更可能）
            config[task_type] = self.get_default_model(task_type)
        return config
    
    def set_model_for_task(self, task_type: TaskType, model_id: str):
        """特定のタスクに使用するモデルを設定（将来の実装用）"""
        # 将来的にデータベースや設定ファイルに保存
        pass
    
    def get_model_info(self, model_id: str) -> Optional[AIModel]:
        """モデル情報を取得"""
        return self.models.get(model_id)
    
    def get_cost_estimate(self, task_type: TaskType, input_tokens: int, output_tokens: int) -> float:
        """タスクのコスト見積もりを計算"""
        model_id = self.get_default_model(task_type)
        if not model_id:
            return 0.0
        
        model = self.models.get(model_id)
        if not model:
            return 0.0
        
        # トークン数をk単位に変換してコストを計算
        total_tokens_k = (input_tokens + output_tokens) / 1000.0
        cost = total_tokens_k * model.cost_per_1k_tokens
        
        # 日本円に変換（1ドル = 150円と仮定）
        return cost * 150.0

# グローバルインスタンス
model_manager = ModelManager()