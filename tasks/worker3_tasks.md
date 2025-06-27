# Worker3 - データパイプライン基盤 実装タスク

## 🎯 目標
各AIツール間でデータを自動的に受け渡し、エンドツーエンドの自動化を実現するパイプライン基盤を構築する。

## 📋 タスクリスト

### 1. パイプライン設計
- [ ] データフロー図の作成
- [ ] 各ツールの入出力仕様定義
- [ ] エラーハンドリング戦略

### 2. 基盤クラス実装
- [ ] `PipelineManager` クラス作成
- [ ] `WorkflowDefinition` クラス作成
- [ ] `DataTransformer` クラス作成

### 3. 実装
```python
# utils/pipeline.py
class PipelineManager:
    """
    AIツール間のデータフローを管理するメインクラス
    """
    def __init__(self):
        self.workflows = {}
        self.active_pipelines = {}
        self.data_store = {}
    
    async def execute_workflow(
        self,
        workflow_id: str,
        initial_data: dict,
        options: dict = None
    ) -> dict:
        """
        ワークフローを実行
        
        Returns:
            {
                "workflow_id": "campaign_automation_001",
                "status": "completed",
                "execution_time": 45.2,
                "steps": [
                    {
                        "tool": "ai_creative_studio",
                        "status": "success",
                        "output": {...}
                    },
                    ...
                ],
                "final_output": {...}
            }
        """

class WorkflowDefinition:
    """
    ワークフローの定義を管理
    """
    def __init__(self, workflow_id: str):
        self.id = workflow_id
        self.steps = []
        self.conditions = {}
        self.error_handlers = {}
    
    def add_step(self, tool_id: str, config: dict):
        """ワークフローにステップを追加"""
    
    def add_condition(self, condition_type: str, handler):
        """条件分岐を追加"""
```

### 4. ワークフロー定義システム
```python
# 標準ワークフローテンプレート
WORKFLOW_TEMPLATES = {
    "campaign_automation": {
        "name": "キャンペーン自動化",
        "description": "企画から配信まで自動化",
        "steps": [
            {
                "id": "creative_generation",
                "tool": "ai_creative_studio",
                "input_mapping": {
                    "campaign_type": "$.campaign.type",
                    "theme": "$.campaign.theme"
                }
            },
            {
                "id": "performance_prediction",
                "tool": "realtime_ad_optimizer",
                "input_mapping": {
                    "creatives": "$.steps.creative_generation.output.creatives"
                }
            },
            {
                "id": "auto_posting",
                "tool": "auto_posting",
                "condition": "$.steps.performance_prediction.output.score > 0.7"
            }
        ]
    }
}
```

### 5. データ変換とマッピング
- [ ] JSONPath実装
- [ ] データバリデーション
- [ ] 型変換ロジック

### 6. 実行エンジン
- [ ] 非同期実行管理
- [ ] 並列実行サポート
- [ ] リトライメカニズム

### 7. モニタリング機能
- [ ] 実行状況のリアルタイム追跡
- [ ] エラー通知
- [ ] パフォーマンスメトリクス

## 🔧 技術仕様

### セッション状態管理
```python
# パイプライン実行状態の管理
st.session_state.pipeline_executions = {
    "execution_001": {
        "workflow_id": "campaign_automation",
        "status": "running",
        "current_step": 2,
        "start_time": "2025-06-27T10:00:00Z",
        "data": {
            "input": {...},
            "intermediate": {...},
            "output": {...}
        }
    }
}
```

### エラーハンドリング
```python
class PipelineError(Exception):
    def __init__(self, step_id, tool_id, original_error):
        self.step_id = step_id
        self.tool_id = tool_id
        self.original_error = original_error

# エラーハンドラー
async def handle_pipeline_error(error: PipelineError):
    # 1. ログ記録
    # 2. リトライ判定
    # 3. 代替フロー実行
    # 4. 通知送信
```

### イベント駆動アーキテクチャ
```python
class PipelineEventBus:
    def __init__(self):
        self.listeners = defaultdict(list)
    
    def emit(self, event_type: str, data: dict):
        for listener in self.listeners[event_type]:
            asyncio.create_task(listener(data))
    
    def on(self, event_type: str, handler):
        self.listeners[event_type].append(handler)
```

## 📊 成功基準
1. 3つ以上のツールを連携したワークフロー実行
2. エラー発生時の自動リカバリー
3. 実行履歴の完全な追跡
4. 90%以上の成功率

## 🚀 開始コマンド
```bash
cd /Users/fukushimashouhei/dev/marketing-automation-tools
mkdir -p utils
code utils/pipeline.py
```

## 🎯 初期実装の優先順位
1. 基本的なワークフロー実行（直列）
2. データマッピング機能
3. エラーハンドリング
4. 並列実行サポート
5. UI統合

---
*担当: Worker3 | 更新: 2025-06-27*