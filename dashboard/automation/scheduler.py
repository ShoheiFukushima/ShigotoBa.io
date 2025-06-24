#!/usr/bin/env python3
"""
スケジューラーモジュール（スタブ実装）
将来的にCronジョブやタスクキューと連携
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
import uuid

class TaskStatus(Enum):
    """タスクステータス"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    """タスクタイプ"""
    SOCIAL_POST = "social_post"
    CONTENT_GENERATION = "content_generation"
    REPORT_GENERATION = "report_generation"
    DATA_ANALYSIS = "data_analysis"

class ScheduledTask:
    """スケジュールされたタスク"""
    
    def __init__(
        self,
        name: str,
        task_type: TaskType,
        schedule: str,
        config: Dict[str, Any],
        enabled: bool = True
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.task_type = task_type
        self.schedule = schedule  # Cron形式
        self.config = config
        self.enabled = enabled
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.last_run = None
        self.next_run = self._calculate_next_run()
    
    def _calculate_next_run(self) -> datetime:
        """次回実行時刻を計算（簡易実装）"""
        # 実際にはcronライブラリを使用
        if "daily" in self.schedule.lower():
            return datetime.now() + timedelta(days=1)
        elif "hourly" in self.schedule.lower():
            return datetime.now() + timedelta(hours=1)
        elif "weekly" in self.schedule.lower():
            return datetime.now() + timedelta(weeks=1)
        else:
            return datetime.now() + timedelta(hours=1)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            "id": self.id,
            "name": self.name,
            "task_type": self.task_type.value,
            "schedule": self.schedule,
            "config": self.config,
            "enabled": self.enabled,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat()
        }

class Scheduler:
    """スケジューラークラス（スタブ）"""
    
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self._init_sample_tasks()
    
    def _init_sample_tasks(self):
        """サンプルタスクを初期化"""
        sample_tasks = [
            ScheduledTask(
                name="毎日のSNS投稿",
                task_type=TaskType.SOCIAL_POST,
                schedule="0 9 * * *",  # 毎日9時
                config={
                    "platforms": ["twitter", "linkedin"],
                    "content_type": "daily_update"
                }
            ),
            ScheduledTask(
                name="週次レポート生成",
                task_type=TaskType.REPORT_GENERATION,
                schedule="0 10 * * MON",  # 毎週月曜10時
                config={
                    "report_type": "weekly_performance",
                    "recipients": ["user@example.com"]
                },
                enabled=False
            )
        ]
        
        for task in sample_tasks:
            self.tasks[task.id] = task
    
    def create_task(
        self,
        name: str,
        task_type: TaskType,
        schedule: str,
        config: Dict[str, Any]
    ) -> ScheduledTask:
        """新しいタスクを作成"""
        task = ScheduledTask(name, task_type, schedule, config)
        self.tasks[task.id] = task
        return task
    
    def get_all_tasks(self) -> List[ScheduledTask]:
        """すべてのタスクを取得"""
        return list(self.tasks.values())
    
    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """特定のタスクを取得"""
        return self.tasks.get(task_id)
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[ScheduledTask]:
        """タスクを更新"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # 更新可能なフィールドのみ更新
        if "name" in updates:
            task.name = updates["name"]
        if "schedule" in updates:
            task.schedule = updates["schedule"]
            task.next_run = task._calculate_next_run()
        if "config" in updates:
            task.config.update(updates["config"])
        if "enabled" in updates:
            task.enabled = updates["enabled"]
        
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """タスクを削除"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def toggle_task(self, task_id: str) -> Optional[ScheduledTask]:
        """タスクの有効/無効を切り替え"""
        task = self.tasks.get(task_id)
        if task:
            task.enabled = not task.enabled
        return task
    
    def get_upcoming_tasks(self, hours: int = 24) -> List[ScheduledTask]:
        """今後実行予定のタスクを取得"""
        cutoff_time = datetime.now() + timedelta(hours=hours)
        upcoming = []
        
        for task in self.tasks.values():
            if task.enabled and task.next_run <= cutoff_time:
                upcoming.append(task)
        
        return sorted(upcoming, key=lambda t: t.next_run)
    
    def run_task_manually(self, task_id: str) -> Dict[str, Any]:
        """タスクを手動実行（スタブ）"""
        task = self.tasks.get(task_id)
        if not task:
            return {"success": False, "error": "タスクが見つかりません"}
        
        # スタブ実装：成功を返す
        task.last_run = datetime.now()
        task.status = TaskStatus.COMPLETED
        task.next_run = task._calculate_next_run()
        
        return {
            "success": True,
            "task_id": task_id,
            "message": f"タスク '{task.name}' を実行しました（テストモード）",
            "next_run": task.next_run.isoformat()
        }
    
    def start(self) -> Dict[str, Any]:
        """スケジューラーを開始（スタブ）"""
        return {
            "success": True,
            "message": "スケジューラーが開始されました（テストモード）",
            "started_at": datetime.now().isoformat(),
            "active_tasks": len([t for t in self.tasks.values() if t.enabled])
        }
    
    def stop(self) -> Dict[str, Any]:
        """スケジューラーを停止（スタブ）"""
        return {
            "success": True,
            "message": "スケジューラーが停止されました（テストモード）",
            "stopped_at": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """スケジューラーのステータスを取得"""
        return {
            "running": True,  # スタブでは常にTrue
            "total_tasks": len(self.tasks),
            "active_tasks": len([t for t in self.tasks.values() if t.enabled]),
            "last_check": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """スケジューラーの統計情報を取得"""
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        pending_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        failed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED])
        
        return {
            "total_tasks": len(self.tasks),
            "active_tasks": len([t for t in self.tasks.values() if t.enabled]),
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": (completed_tasks / max(1, len(self.tasks))) * 100,
            "last_updated": datetime.now().isoformat()
        }
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """タスク一覧を取得（辞書形式）"""
        return [task.to_dict() for task in self.get_all_tasks()]

# グローバルインスタンス
scheduler = Scheduler()

# エクスポート用の関数
def get_all_scheduled_tasks() -> List[Dict[str, Any]]:
    """すべてのスケジュールタスクを取得"""
    return [task.to_dict() for task in scheduler.get_all_tasks()]

def create_scheduled_task(
    name: str,
    task_type: str,
    schedule: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """スケジュールタスクを作成"""
    try:
        task_type_enum = TaskType(task_type)
        task = scheduler.create_task(name, task_type_enum, schedule, config)
        return {"success": True, "task": task.to_dict()}
    except ValueError:
        return {"success": False, "error": f"不明なタスクタイプ: {task_type}"}

def toggle_scheduled_task(task_id: str) -> Dict[str, Any]:
    """スケジュールタスクの有効/無効を切り替え"""
    task = scheduler.toggle_task(task_id)
    if task:
        return {"success": True, "task": task.to_dict()}
    return {"success": False, "error": "タスクが見つかりません"}

def run_task_now(task_id: str) -> Dict[str, Any]:
    """タスクを今すぐ実行"""
    return scheduler.run_task_manually(task_id)