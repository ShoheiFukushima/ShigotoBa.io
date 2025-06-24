#!/usr/bin/env python3
"""
マーケティング自動化スケジューラー
定期実行・バッチ処理・タスクキューの管理
"""

import asyncio
import schedule
import threading
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """タスク実行ステータス"""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """タスク優先度"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TriggerType(Enum):
    """トリガータイプ"""
    INTERVAL = "interval"      # 定期実行
    CRON = "cron"             # cron式
    ONE_TIME = "one_time"     # 一回限り
    EVENT = "event"           # イベントトリガー

@dataclass
class ScheduledTask:
    """スケジュール済みタスク"""
    id: str
    name: str
    description: str
    function_name: str
    args: List[Any]
    kwargs: Dict[str, Any]
    trigger_type: TriggerType
    trigger_config: Dict[str, Any]
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    run_count: int = 0
    max_retries: int = 3
    retry_count: int = 0
    timeout_seconds: int = 300
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class TaskResult:
    """タスク実行結果"""
    task_id: str
    status: TaskStatus
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: float
    result: Any = None
    error: Optional[str] = None
    logs: List[str] = None
    
    def __post_init__(self):
        if self.logs is None:
            self.logs = []

class MarketingTaskRegistry:
    """マーケティングタスク登録管理"""
    
    def __init__(self):
        self.registered_functions = {}
        self._register_builtin_tasks()
    
    def register(self, name: str, func: Callable):
        """タスク関数を登録"""
        self.registered_functions[name] = func
        logger.info(f"タスク関数を登録: {name}")
    
    def get_function(self, name: str) -> Optional[Callable]:
        """登録済み関数を取得"""
        return self.registered_functions.get(name)
    
    def list_functions(self) -> List[str]:
        """登録済み関数一覧"""
        return list(self.registered_functions.keys())
    
    def _register_builtin_tasks(self):
        """組み込みタスクを登録"""
        
        async def generate_social_content(project_id: str, platforms: List[str]):
            """ソーシャルコンテンツ生成タスク"""
            logger.info(f"ソーシャルコンテンツ生成開始: {project_id}")
            
            # プロジェクト情報取得（実装は後で）
            await asyncio.sleep(2)  # 処理シミュレーション
            
            return {
                "project_id": project_id,
                "platforms": platforms,
                "content_generated": len(platforms),
                "timestamp": datetime.now().isoformat()
            }
        
        async def analyze_competitors(project_id: str):
            """競合分析タスク"""
            logger.info(f"競合分析開始: {project_id}")
            
            await asyncio.sleep(3)  # 分析シミュレーション
            
            return {
                "project_id": project_id,
                "competitors_analyzed": 5,
                "trends_identified": 3,
                "timestamp": datetime.now().isoformat()
            }
        
        async def post_to_social_media(project_id: str, content: str, platforms: List[str]):
            """ソーシャルメディア投稿タスク"""
            logger.info(f"ソーシャル投稿開始: {project_id}")
            
            # 実際のAPI呼び出し（実装は後で）
            await asyncio.sleep(1)
            
            return {
                "project_id": project_id,
                "platforms_posted": platforms,
                "success_count": len(platforms),
                "timestamp": datetime.now().isoformat()
            }
        
        async def generate_performance_report(project_id: str):
            """パフォーマンスレポート生成"""
            logger.info(f"レポート生成開始: {project_id}")
            
            await asyncio.sleep(4)  # レポート生成シミュレーション
            
            return {
                "project_id": project_id,
                "metrics_collected": 15,
                "report_generated": True,
                "timestamp": datetime.now().isoformat()
            }
        
        async def send_marketing_email(project_id: str, email_list: List[str]):
            """マーケティングメール送信"""
            logger.info(f"メール送信開始: {project_id}")
            
            await asyncio.sleep(2)
            
            return {
                "project_id": project_id,
                "emails_sent": len(email_list),
                "delivery_rate": 95.5,
                "timestamp": datetime.now().isoformat()
            }
        
        # タスク登録
        self.register("generate_social_content", generate_social_content)
        self.register("analyze_competitors", analyze_competitors)
        self.register("post_to_social_media", post_to_social_media)
        self.register("generate_performance_report", generate_performance_report)
        self.register("send_marketing_email", send_marketing_email)

class MarketingScheduler:
    """マーケティングスケジューラー"""
    
    def __init__(self):
        self.tasks = {}
        self.task_results = {}
        self.task_registry = MarketingTaskRegistry()
        self.is_running = False
        self.scheduler_thread = None
        self.execution_loop = None
        
        # スケジューラー統計
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "avg_execution_time": 0.0,
            "last_run": None
        }
    
    def add_task(self, 
                 name: str,
                 description: str,
                 function_name: str,
                 args: List[Any] = None,
                 kwargs: Dict[str, Any] = None,
                 trigger_type: TriggerType = TriggerType.ONE_TIME,
                 trigger_config: Dict[str, Any] = None,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 max_retries: int = 3,
                 timeout_seconds: int = 300) -> str:
        """タスクをスケジュールに追加"""
        
        task_id = str(uuid.uuid4())
        
        # 次回実行時間を計算
        next_run = self._calculate_next_run(trigger_type, trigger_config or {})
        
        task = ScheduledTask(
            id=task_id,
            name=name,
            description=description,
            function_name=function_name,
            args=args or [],
            kwargs=kwargs or {},
            trigger_type=trigger_type,
            trigger_config=trigger_config or {},
            priority=priority,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            next_run=next_run,
            max_retries=max_retries,
            timeout_seconds=timeout_seconds
        )
        
        self.tasks[task_id] = task
        self.stats["total_tasks"] += 1
        
        logger.info(f"タスクを追加: {name} (ID: {task_id})")
        return task_id
    
    def _calculate_next_run(self, trigger_type: TriggerType, config: Dict[str, Any]) -> Optional[datetime]:
        """次回実行時間を計算"""
        now = datetime.now()
        
        if trigger_type == TriggerType.ONE_TIME:
            # 一回限り - 指定時間または即座実行
            return config.get('run_at', now)
        
        elif trigger_type == TriggerType.INTERVAL:
            # 定期実行
            interval_seconds = config.get('seconds', 0)
            interval_minutes = config.get('minutes', 0)
            interval_hours = config.get('hours', 0)
            interval_days = config.get('days', 0)
            
            total_seconds = (
                interval_seconds + 
                interval_minutes * 60 + 
                interval_hours * 3600 + 
                interval_days * 86400
            )
            
            return now + timedelta(seconds=total_seconds)
        
        elif trigger_type == TriggerType.CRON:
            # CRON式（簡易実装）
            # 実際の実装ではcroniterライブラリを使用推奨
            hour = config.get('hour')
            minute = config.get('minute', 0)
            
            if hour is not None:
                next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if next_run <= now:
                    next_run += timedelta(days=1)
                return next_run
        
        return now
    
    def remove_task(self, task_id: str) -> bool:
        """タスクを削除"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"タスクを削除: {task_id}")
            return True
        return False
    
    def cancel_task(self, task_id: str) -> bool:
        """タスクをキャンセル"""
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.CANCELLED
            logger.info(f"タスクをキャンセル: {task_id}")
            return True
        return False
    
    async def execute_task(self, task: ScheduledTask) -> TaskResult:
        """単一タスクを実行"""
        start_time = datetime.now()
        task.status = TaskStatus.RUNNING
        task.last_run = start_time
        task.run_count += 1
        
        result = TaskResult(
            task_id=task.id,
            status=TaskStatus.RUNNING,
            start_time=start_time,
            end_time=None,
            duration_seconds=0.0
        )
        
        try:
            # 登録済み関数を取得
            func = self.task_registry.get_function(task.function_name)
            if not func:
                raise ValueError(f"未登録の関数: {task.function_name}")
            
            # タイムアウト付きで実行
            if asyncio.iscoroutinefunction(func):
                task_result = await asyncio.wait_for(
                    func(*task.args, **task.kwargs),
                    timeout=task.timeout_seconds
                )
            else:
                # 同期関数を非同期で実行
                task_result = await asyncio.get_event_loop().run_in_executor(
                    None, func, *task.args, **task.kwargs
                )
            
            # 成功
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result.status = TaskStatus.COMPLETED
            result.end_time = end_time
            result.duration_seconds = duration
            result.result = task_result
            
            task.status = TaskStatus.COMPLETED
            task.retry_count = 0  # 成功時はリトライカウントリセット
            
            # 次回実行時間を更新（定期実行の場合）
            if task.trigger_type == TriggerType.INTERVAL:
                task.next_run = self._calculate_next_run(task.trigger_type, task.trigger_config)
                task.status = TaskStatus.PENDING  # 再度実行待ちに
            
            self.stats["completed_tasks"] += 1
            logger.info(f"タスク実行成功: {task.name} ({duration:.2f}秒)")
            
        except asyncio.TimeoutError:
            # タイムアウト
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result.status = TaskStatus.FAILED
            result.end_time = end_time
            result.duration_seconds = duration
            result.error = f"タイムアウト ({task.timeout_seconds}秒)"
            
            task.status = TaskStatus.FAILED
            self.stats["failed_tasks"] += 1
            
            logger.error(f"タスクタイムアウト: {task.name}")
            
        except Exception as e:
            # その他のエラー
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result.status = TaskStatus.FAILED
            result.end_time = end_time
            result.duration_seconds = duration
            result.error = str(e)
            
            # リトライ判定
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                task.next_run = datetime.now() + timedelta(minutes=5)  # 5分後にリトライ
                logger.warning(f"タスク失敗、リトライします: {task.name} ({task.retry_count}/{task.max_retries})")
            else:
                task.status = TaskStatus.FAILED
                self.stats["failed_tasks"] += 1
                logger.error(f"タスク失敗（リトライ上限）: {task.name} - {str(e)}")
        
        # 結果を保存
        self.task_results[task.id] = result
        self.stats["last_run"] = datetime.now()
        
        # 平均実行時間を更新
        total_completed = self.stats["completed_tasks"]
        if total_completed > 0:
            self.stats["avg_execution_time"] = (
                (self.stats["avg_execution_time"] * (total_completed - 1) + result.duration_seconds) 
                / total_completed
            )
        
        return result
    
    async def run_scheduler_loop(self):
        """スケジューラーのメインループ"""
        logger.info("スケジューラーを開始しました")
        
        while self.is_running:
            try:
                current_time = datetime.now()
                
                # 実行すべきタスクを取得
                ready_tasks = [
                    task for task in self.tasks.values()
                    if (task.status == TaskStatus.PENDING and 
                        task.next_run and 
                        task.next_run <= current_time)
                ]
                
                # 優先度順でソート
                ready_tasks.sort(key=lambda t: (t.priority.value, t.next_run), reverse=True)
                
                # タスクを並列実行
                if ready_tasks:
                    logger.info(f"{len(ready_tasks)}個のタスクを実行します")
                    
                    # 最大同時実行数を制限
                    max_concurrent = 5
                    for i in range(0, len(ready_tasks), max_concurrent):
                        batch = ready_tasks[i:i + max_concurrent]
                        
                        # バッチ実行
                        await asyncio.gather(
                            *[self.execute_task(task) for task in batch],
                            return_exceptions=True
                        )
                
                # 1秒待機
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"スケジューラーエラー: {e}")
                await asyncio.sleep(5)  # エラー時は少し長めに待機
    
    def start(self):
        """スケジューラーを開始"""
        if self.is_running:
            logger.warning("スケジューラーは既に実行中です")
            return
        
        self.is_running = True
        
        # 新しいイベントループでスケジューラーを実行
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.run_scheduler_loop())
            finally:
                loop.close()
        
        self.scheduler_thread = threading.Thread(target=run_in_thread, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("スケジューラーを開始しました")
    
    def stop(self):
        """スケジューラーを停止"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("スケジューラーを停止しました")
    
    def get_task_status(self, task_id: str) -> Optional[ScheduledTask]:
        """タスク状況を取得"""
        return self.tasks.get(task_id)
    
    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """タスク実行結果を取得"""
        return self.task_results.get(task_id)
    
    def list_tasks(self, status_filter: Optional[TaskStatus] = None) -> List[ScheduledTask]:
        """タスク一覧を取得"""
        tasks = list(self.tasks.values())
        
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    def get_statistics(self) -> Dict[str, Any]:
        """スケジューラー統計を取得"""
        pending_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        running_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.RUNNING])
        
        return {
            **self.stats,
            "pending_tasks": pending_tasks,
            "running_tasks": running_tasks,
            "is_running": self.is_running,
            "registered_functions": len(self.task_registry.registered_functions)
        }
    
    def export_tasks(self) -> Dict[str, Any]:
        """タスク設定をエクスポート"""
        return {
            "export_time": datetime.now().isoformat(),
            "tasks": [
                {
                    **asdict(task),
                    "created_at": task.created_at.isoformat(),
                    "next_run": task.next_run.isoformat() if task.next_run else None,
                    "last_run": task.last_run.isoformat() if task.last_run else None,
                    "trigger_type": task.trigger_type.value,
                    "priority": task.priority.value,
                    "status": task.status.value
                }
                for task in self.tasks.values()
            ],
            "statistics": self.get_statistics()
        }

# グローバルスケジューラーインスタンス
marketing_scheduler = MarketingScheduler()

# 便利な関数
def schedule_daily_social_posts(project_id: str, hour: int = 9, minute: int = 0):
    """毎日のソーシャル投稿をスケジュール"""
    return marketing_scheduler.add_task(
        name=f"Daily Social Posts - {project_id}",
        description="毎日のソーシャルメディア投稿",
        function_name="generate_social_content",
        args=[project_id, ["twitter", "linkedin"]],
        trigger_type=TriggerType.CRON,
        trigger_config={"hour": hour, "minute": minute},
        priority=TaskPriority.HIGH
    )

def schedule_weekly_competitor_analysis(project_id: str):
    """週次競合分析をスケジュール"""
    return marketing_scheduler.add_task(
        name=f"Weekly Competitor Analysis - {project_id}",
        description="週次競合分析レポート",
        function_name="analyze_competitors",
        args=[project_id],
        trigger_type=TriggerType.INTERVAL,
        trigger_config={"days": 7},
        priority=TaskPriority.MEDIUM
    )

def schedule_monthly_performance_report(project_id: str):
    """月次パフォーマンスレポートをスケジュール"""
    return marketing_scheduler.add_task(
        name=f"Monthly Performance Report - {project_id}",
        description="月次パフォーマンスレポート生成",
        function_name="generate_performance_report",
        args=[project_id],
        trigger_type=TriggerType.INTERVAL,
        trigger_config={"days": 30},
        priority=TaskPriority.LOW
    )

# テスト用関数
async def test_scheduler():
    """スケジューラーのテスト"""
    print("=== マーケティングスケジューラーテスト ===")
    
    # スケジューラー開始
    marketing_scheduler.start()
    
    # テストタスクを追加
    task_id1 = marketing_scheduler.add_task(
        name="テスト投稿生成",
        description="テスト用のソーシャル投稿生成",
        function_name="generate_social_content",
        args=["test_project", ["twitter"]],
        trigger_type=TriggerType.ONE_TIME
    )
    
    task_id2 = schedule_daily_social_posts("test_project", hour=10)
    
    print(f"タスク追加: {task_id1}, {task_id2}")
    
    # 少し待機
    await asyncio.sleep(5)
    
    # 統計確認
    stats = marketing_scheduler.get_statistics()
    print(f"統計: {stats}")
    
    # タスク一覧
    tasks = marketing_scheduler.list_tasks()
    print(f"タスク数: {len(tasks)}")
    
    # スケジューラー停止
    marketing_scheduler.stop()

if __name__ == "__main__":
    asyncio.run(test_scheduler())