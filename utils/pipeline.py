"""
AIツール間のデータパイプライン管理システム
各ツールを連携させ、エンドツーエンドの自動化を実現
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from collections import defaultdict
import streamlit as st
import logging

# ロギング設定
logger = logging.getLogger(__name__)

class PipelineStatus(Enum):
    """パイプライン実行状態"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StepStatus(Enum):
    """ステップ実行状態"""
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class PipelineError(Exception):
    """パイプライン実行エラー"""
    def __init__(self, step_id: str, tool_id: str, original_error: Exception):
        self.step_id = step_id
        self.tool_id = tool_id
        self.original_error = original_error
        super().__init__(f"Pipeline error at step {step_id} (tool: {tool_id}): {str(original_error)}")

class PipelineEventBus:
    """イベント駆動アーキテクチャ用のイベントバス"""
    def __init__(self):
        self.listeners = defaultdict(list)
    
    def emit(self, event_type: str, data: Dict):
        """イベントを発火"""
        for listener in self.listeners[event_type]:
            asyncio.create_task(listener(data))
    
    def on(self, event_type: str, handler: Callable):
        """イベントリスナーを登録"""
        self.listeners[event_type].append(handler)

class DataTransformer:
    """ツール間のデータ変換を管理"""
    
    @staticmethod
    def apply_mapping(data: Dict, mapping: Dict) -> Dict:
        """JSONPathライクなマッピングを適用"""
        result = {}
        for target_key, source_path in mapping.items():
            value = DataTransformer._extract_value(data, source_path)
            result[target_key] = value
        return result
    
    @staticmethod
    def _extract_value(data: Dict, path: str) -> Any:
        """パスから値を抽出（簡易版JSONPath）"""
        if path.startswith("$."):
            path = path[2:]
        
        parts = path.split(".")
        current = data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current

class WorkflowStep:
    """ワークフローの1ステップを表現"""
    def __init__(self, step_id: str, tool_id: str, config: Dict):
        self.id = step_id
        self.tool_id = tool_id
        self.config = config
        self.input_mapping = config.get('input_mapping', {})
        self.condition = config.get('condition', None)
        self.retry_count = config.get('retry_count', 3)
        self.timeout = config.get('timeout', 300)  # 秒
        self.status = StepStatus.WAITING
        self.result = None
        self.error = None

class WorkflowDefinition:
    """ワークフローの定義を管理"""
    def __init__(self, workflow_id: str, name: str, description: str = ""):
        self.id = workflow_id
        self.name = name
        self.description = description
        self.steps = []
        self.global_config = {}
        self.error_handlers = {}
    
    def add_step(self, step: WorkflowStep):
        """ステップを追加"""
        self.steps.append(step)
    
    def add_error_handler(self, error_type: str, handler: Callable):
        """エラーハンドラーを追加"""
        self.error_handlers[error_type] = handler
    
    def validate(self) -> bool:
        """ワークフロー定義の妥当性を検証"""
        if not self.steps:
            raise ValueError("Workflow must have at least one step")
        
        # ステップIDの重複チェック
        step_ids = [step.id for step in self.steps]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("Duplicate step IDs found")
        
        return True

class PipelineExecution:
    """パイプライン実行インスタンス"""
    def __init__(self, execution_id: str, workflow: WorkflowDefinition, initial_data: Dict):
        self.id = execution_id
        self.workflow = workflow
        self.status = PipelineStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.data = {
            "input": initial_data,
            "steps": {},
            "output": None
        }
        self.current_step_index = 0
        self.error = None

class PipelineManager:
    """AIツール間のデータフローを管理するメインクラス"""
    
    def __init__(self):
        self.workflows = {}
        self.active_executions = {}
        self.event_bus = PipelineEventBus()
        self.tool_registry = {}
        self._setup_default_workflows()
    
    def register_workflow(self, workflow: WorkflowDefinition):
        """ワークフローを登録"""
        workflow.validate()
        self.workflows[workflow.id] = workflow
    
    def register_tool(self, tool_id: str, executor: Callable):
        """ツールの実行関数を登録"""
        self.tool_registry[tool_id] = executor
    
    async def execute_workflow(
        self,
        workflow_id: str,
        initial_data: Dict,
        options: Dict = None
    ) -> Dict:
        """ワークフローを実行"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        workflow = self.workflows[workflow_id]
        execution_id = str(uuid.uuid4())
        execution = PipelineExecution(execution_id, workflow, initial_data)
        
        self.active_executions[execution_id] = execution
        
        try:
            # 実行開始イベント
            self.event_bus.emit("execution_started", {
                "execution_id": execution_id,
                "workflow_id": workflow_id
            })
            
            execution.status = PipelineStatus.RUNNING
            execution.start_time = datetime.now()
            
            # 各ステップを順次実行
            for step_index, step in enumerate(workflow.steps):
                execution.current_step_index = step_index
                
                # 条件チェック
                if step.condition and not self._evaluate_condition(step.condition, execution.data):
                    step.status = StepStatus.SKIPPED
                    continue
                
                # ステップ実行
                await self._execute_step(execution, step)
                
                if step.status == StepStatus.FAILED:
                    execution.status = PipelineStatus.FAILED
                    break
            
            if execution.status == PipelineStatus.RUNNING:
                execution.status = PipelineStatus.COMPLETED
            
            execution.end_time = datetime.now()
            
            # 実行完了イベント
            self.event_bus.emit("execution_completed", {
                "execution_id": execution_id,
                "status": execution.status.value,
                "duration": (execution.end_time - execution.start_time).total_seconds()
            })
            
            return self._prepare_result(execution)
            
        except Exception as e:
            execution.status = PipelineStatus.FAILED
            execution.error = str(e)
            logger.error(f"Pipeline execution failed: {e}")
            
            # エラーイベント
            self.event_bus.emit("execution_failed", {
                "execution_id": execution_id,
                "error": str(e)
            })
            
            raise
        finally:
            # クリーンアップ
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]
    
    async def _execute_step(self, execution: PipelineExecution, step: WorkflowStep):
        """個別ステップを実行"""
        step.status = StepStatus.RUNNING
        
        # ステップ開始イベント
        self.event_bus.emit("step_started", {
            "execution_id": execution.id,
            "step_id": step.id,
            "tool_id": step.tool_id
        })
        
        try:
            # 入力データの準備
            input_data = DataTransformer.apply_mapping(execution.data, step.input_mapping)
            
            # ツール実行
            if step.tool_id not in self.tool_registry:
                raise ValueError(f"Tool '{step.tool_id}' not registered")
            
            tool_executor = self.tool_registry[step.tool_id]
            
            # タイムアウト付きで実行
            result = await asyncio.wait_for(
                tool_executor(input_data),
                timeout=step.timeout
            )
            
            # 結果を保存
            step.result = result
            step.status = StepStatus.COMPLETED
            execution.data["steps"][step.id] = {
                "input": input_data,
                "output": result,
                "status": "completed"
            }
            
            # ステップ完了イベント
            self.event_bus.emit("step_completed", {
                "execution_id": execution.id,
                "step_id": step.id,
                "result": result
            })
            
        except asyncio.TimeoutError:
            step.status = StepStatus.FAILED
            step.error = "Timeout"
            raise PipelineError(step.id, step.tool_id, TimeoutError(f"Step timed out after {step.timeout}s"))
            
        except Exception as e:
            step.status = StepStatus.FAILED
            step.error = str(e)
            
            # リトライロジック
            if step.retry_count > 0:
                logger.warning(f"Step {step.id} failed, retrying... ({step.retry_count} attempts left)")
                step.retry_count -= 1
                await asyncio.sleep(2)  # バックオフ
                return await self._execute_step(execution, step)
            
            raise PipelineError(step.id, step.tool_id, e)
    
    def _evaluate_condition(self, condition: str, data: Dict) -> bool:
        """条件を評価（簡易版）"""
        # TODO: より高度な条件評価ロジックを実装
        try:
            # 簡単な比較演算のサポート
            if ">" in condition:
                parts = condition.split(">")
                left_value = DataTransformer._extract_value(data, parts[0].strip())
                right_value = float(parts[1].strip())
                return float(left_value) > right_value
            
            return True
        except:
            return False
    
    def _prepare_result(self, execution: PipelineExecution) -> Dict:
        """実行結果を整形"""
        return {
            "execution_id": execution.id,
            "workflow_id": execution.workflow.id,
            "status": execution.status.value,
            "execution_time": (execution.end_time - execution.start_time).total_seconds() if execution.end_time else None,
            "steps": [
                {
                    "step_id": step.id,
                    "tool_id": step.tool_id,
                    "status": step.status.value,
                    "result": step.result,
                    "error": step.error
                }
                for step in execution.workflow.steps
            ],
            "final_output": execution.data.get("output"),
            "error": execution.error
        }
    
    def _setup_default_workflows(self):
        """デフォルトのワークフローを設定"""
        # キャンペーン自動化ワークフロー
        campaign_workflow = WorkflowDefinition(
            "campaign_automation",
            "キャンペーン自動化",
            "企画から配信まで自動化"
        )
        
        # ステップ1: クリエイティブ生成
        campaign_workflow.add_step(WorkflowStep(
            "creative_generation",
            "ai_creative_studio",
            {
                "input_mapping": {
                    "campaign_type": "$.input.campaign.type",
                    "target_audience": "$.input.campaign.target_audience",
                    "brand_info": "$.input.campaign.brand_info"
                }
            }
        ))
        
        # ステップ2: パフォーマンス予測
        campaign_workflow.add_step(WorkflowStep(
            "performance_prediction",
            "realtime_ad_optimizer",
            {
                "input_mapping": {
                    "creatives": "$.steps.creative_generation.output.content",
                    "target_metrics": "$.input.campaign.target_metrics"
                },
                "condition": "$.steps.creative_generation.output.status == 'success'"
            }
        ))
        
        # ステップ3: 自動投稿
        campaign_workflow.add_step(WorkflowStep(
            "auto_posting",
            "auto_posting",
            {
                "input_mapping": {
                    "content": "$.steps.creative_generation.output.content",
                    "schedule": "$.input.campaign.schedule",
                    "platforms": "$.input.campaign.platforms"
                },
                "condition": "$.steps.performance_prediction.output.score > 0.7"
            }
        ))
        
        self.register_workflow(campaign_workflow)

# セッション状態での管理
def get_pipeline_manager() -> PipelineManager:
    """シングルトンのPipelineManagerを取得"""
    if 'pipeline_manager' not in st.session_state:
        st.session_state.pipeline_manager = PipelineManager()
    return st.session_state.pipeline_manager