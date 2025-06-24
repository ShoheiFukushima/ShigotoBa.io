#!/usr/bin/env python3
"""
ダッシュボード監視ツール
エラーを自動検出して報告
"""

import time
import subprocess
import sys
import os
import requests
from datetime import datetime

class DashboardMonitor:
    """ダッシュボードの健全性を監視"""
    
    def __init__(self):
        self.dashboard_url = "http://localhost:8501"
        self.log_file = "dashboard/logs/monitor.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
    def log(self, message, level="INFO"):
        """ログ記録"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_message.strip())
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
    
    def check_health(self):
        """ヘルスチェック"""
        try:
            response = requests.get(self.dashboard_url, timeout=5)
            if response.status_code == 200:
                self.log("✅ ダッシュボードは正常に動作しています")
                return True
            else:
                self.log(f"⚠️ 異常なステータスコード: {response.status_code}", "WARNING")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ ダッシュボードに接続できません", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ ヘルスチェックエラー: {str(e)}", "ERROR")
            return False
    
    def check_resources(self):
        """リソース使用状況チェック"""
        try:
            # メモリ使用量（簡易チェック）
            import psutil
            
            memory = psutil.virtual_memory()
            if memory.percent > 80:
                self.log(f"⚠️ メモリ使用率が高い: {memory.percent}%", "WARNING")
                
            # ディスク容量
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                self.log(f"⚠️ ディスク使用率が高い: {disk.percent}%", "WARNING")
                
        except ImportError:
            # psutilがない場合はスキップ
            pass
        except Exception as e:
            self.log(f"リソースチェックエラー: {str(e)}", "WARNING")
    
    def check_files(self):
        """重要ファイルの存在チェック"""
        critical_files = [
            "dashboard/app.py",
            "dashboard/config/projects.json",
            ".streamlit/config.toml"
        ]
        
        for file_path in critical_files:
            if not os.path.exists(file_path):
                self.log(f"⚠️ 重要ファイルが見つかりません: {file_path}", "WARNING")
    
    def auto_restart(self):
        """問題検出時の自動再起動"""
        self.log("🔄 ダッシュボードを再起動します...", "INFO")
        
        try:
            # 既存のプロセスを終了
            subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
            time.sleep(2)
            
            # 再起動
            subprocess.Popen([
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "dashboard/app.py",
                "--server.headless=true"
            ])
            
            time.sleep(5)  # 起動待機
            
            if self.check_health():
                self.log("✅ 再起動成功", "INFO")
                return True
            else:
                self.log("❌ 再起動失敗", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ 再起動エラー: {str(e)}", "ERROR")
            return False
    
    def monitor_loop(self, interval=60):
        """監視ループ"""
        self.log("🚀 ダッシュボード監視を開始します")
        
        consecutive_failures = 0
        
        while True:
            try:
                # ヘルスチェック
                if self.check_health():
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    
                    # 3回連続失敗で再起動
                    if consecutive_failures >= 3:
                        self.log("⚠️ 3回連続でヘルスチェック失敗", "WARNING")
                        if self.auto_restart():
                            consecutive_failures = 0
                
                # リソースチェック
                self.check_resources()
                
                # ファイルチェック
                self.check_files()
                
                # 待機
                time.sleep(interval)
                
            except KeyboardInterrupt:
                self.log("👋 監視を終了します")
                break
            except Exception as e:
                self.log(f"❌ 監視エラー: {str(e)}", "ERROR")
                time.sleep(interval)

def main():
    """メイン実行"""
    monitor = DashboardMonitor()
    
    print("🔍 ダッシュボード監視ツール")
    print("="*50)
    print("監視間隔: 60秒")
    print("自動再起動: 3回連続失敗時")
    print("終了: Ctrl+C")
    print("="*50)
    
    monitor.monitor_loop()

if __name__ == "__main__":
    main()