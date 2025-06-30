#!/usr/bin/env python3
"""
Google Sheets データベース連携モジュール
個人利用向けのシンプルなデータ永続化ソリューション
"""

import os
import json
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st
import time
from functools import wraps

# スコープ設定
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class GoogleSheetsDB:
    """Google Sheetsをデータベースとして使用するクラス"""
    
    def __init__(self, spreadsheet_id: Optional[str] = None):
        """
        初期化
        
        Args:
            spreadsheet_id: Google SheetsのID（URLから取得可能）
        """
        self.spreadsheet_id = spreadsheet_id or os.getenv('GOOGLE_SHEETS_ID')
        self.client = None
        self.spreadsheet = None
        self._connect()
    
    def _connect(self):
        """Google Sheetsに接続"""
        try:
            # サービスアカウント認証（推奨）
            if os.path.exists('credentials.json'):
                creds = service_account.Credentials.from_service_account_file(
                    'credentials.json', scopes=SCOPES
                )
            # 環境変数から認証情報を取得
            elif os.getenv('GOOGLE_SHEETS_CREDENTIALS'):
                creds_dict = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))
                creds = service_account.Credentials.from_service_account_info(
                    creds_dict, scopes=SCOPES
                )
            else:
                st.error("Google Sheets認証情報が見つかりません")
                return
            
            self.client = gspread.authorize(creds)
            
            # スプレッドシートを開く（なければ作成）
            if self.spreadsheet_id:
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            else:
                # 新しいスプレッドシートを作成
                self.spreadsheet = self.client.create('Marketing Automation Data')
                self.spreadsheet_id = self.spreadsheet.id
                st.info(f"新しいスプレッドシートを作成しました: {self.spreadsheet_id}")
                
                # 必要なシートを作成
                self._initialize_sheets()
                
        except Exception as e:
            st.error(f"Google Sheets接続エラー: {str(e)}")
    
    def _initialize_sheets(self):
        """必要なシートを初期化"""
        sheets = {
            'projects': ['id', 'name', 'type', 'status', 'flow_stage', 'created_at', 'updated_at', 'data'],
            'todos': ['id', 'text', 'done', 'priority', 'created_at', 'updated_at'],
            'ai_outputs': ['id', 'project_id', 'type', 'content', 'created_at'],
            'settings': ['key', 'value', 'updated_at']
        }
        
        for sheet_name, headers in sheets.items():
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except:
                worksheet = self.spreadsheet.add_worksheet(sheet_name, rows=1000, cols=20)
                worksheet.update('A1', [headers])
    
    def retry_on_error(max_retries=3, delay=1):
        """リトライデコレーター"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if i == max_retries - 1:
                            raise e
                        time.sleep(delay * (i + 1))
                return None
            return wrapper
        return decorator
    
    @retry_on_error()
    def save_projects(self, projects: Dict[str, Dict[str, Any]]):
        """プロジェクトデータを保存"""
        if not self.spreadsheet:
            return
        
        try:
            worksheet = self.spreadsheet.worksheet('projects')
            
            # 既存データをクリア
            worksheet.clear()
            worksheet.update('A1', [['id', 'name', 'type', 'status', 'flow_stage', 'created_at', 'updated_at', 'data']])
            
            # データを準備
            rows = []
            for project_id, project_data in projects.items():
                row = [
                    project_id,
                    project_data.get('name', ''),
                    project_data.get('type', ''),
                    project_data.get('status', ''),
                    str(project_data.get('flow_stage', 0)),
                    project_data.get('created_at', datetime.now().isoformat()),
                    datetime.now().isoformat(),
                    json.dumps(project_data)  # 全データをJSON形式で保存
                ]
                rows.append(row)
            
            # バッチ更新
            if rows:
                worksheet.update(f'A2:H{len(rows)+1}', rows)
                
        except Exception as e:
            st.error(f"プロジェクト保存エラー: {str(e)}")
    
    @retry_on_error()
    def load_projects(self) -> Dict[str, Dict[str, Any]]:
        """プロジェクトデータを読み込み"""
        if not self.spreadsheet:
            return {}
        
        try:
            worksheet = self.spreadsheet.worksheet('projects')
            records = worksheet.get_all_records()
            
            projects = {}
            for record in records:
                if record.get('id'):
                    # JSONデータをパース
                    project_data = json.loads(record.get('data', '{}'))
                    # 基本フィールドを更新
                    project_data.update({
                        'name': record.get('name', ''),
                        'type': record.get('type', ''),
                        'status': record.get('status', ''),
                        'flow_stage': int(record.get('flow_stage', 0))
                    })
                    projects[record['id']] = project_data
            
            return projects
            
        except Exception as e:
            st.error(f"プロジェクト読み込みエラー: {str(e)}")
            return {}
    
    @retry_on_error()
    def save_todos(self, todos: List[Dict[str, Any]]):
        """TODOリストを保存"""
        if not self.spreadsheet:
            return
        
        try:
            worksheet = self.spreadsheet.worksheet('todos')
            
            # 既存データをクリア
            worksheet.clear()
            worksheet.update('A1', [['id', 'text', 'done', 'priority', 'created_at', 'updated_at']])
            
            # データを準備
            rows = []
            for todo in todos:
                row = [
                    str(todo.get('id', '')),
                    todo.get('text', ''),
                    str(todo.get('done', False)),
                    todo.get('priority', 'medium'),
                    todo.get('created_at', datetime.now().isoformat()),
                    datetime.now().isoformat()
                ]
                rows.append(row)
            
            # バッチ更新
            if rows:
                worksheet.update(f'A2:F{len(rows)+1}', rows)
                
        except Exception as e:
            st.error(f"TODO保存エラー: {str(e)}")
    
    @retry_on_error()
    def load_todos(self) -> List[Dict[str, Any]]:
        """TODOリストを読み込み"""
        if not self.spreadsheet:
            return []
        
        try:
            worksheet = self.spreadsheet.worksheet('todos')
            records = worksheet.get_all_records()
            
            todos = []
            for record in records:
                if record.get('id'):
                    todos.append({
                        'id': int(record.get('id', 0)),
                        'text': record.get('text', ''),
                        'done': record.get('done', 'False') == 'True',
                        'priority': record.get('priority', 'medium')
                    })
            
            return todos
            
        except Exception as e:
            st.error(f"TODO読み込みエラー: {str(e)}")
            return []
    
    @retry_on_error()
    def save_ai_output(self, project_id: str, output_type: str, content: Any):
        """AI出力を保存"""
        if not self.spreadsheet:
            return
        
        try:
            worksheet = self.spreadsheet.worksheet('ai_outputs')
            
            # 新しい行を追加
            row = [
                str(datetime.now().timestamp()),  # ID
                project_id,
                output_type,
                json.dumps(content) if isinstance(content, dict) else str(content),
                datetime.now().isoformat()
            ]
            
            worksheet.append_row(row)
            
        except Exception as e:
            st.error(f"AI出力保存エラー: {str(e)}")
    
    @retry_on_error()
    def load_ai_outputs(self, project_id: str) -> List[Dict[str, Any]]:
        """特定プロジェクトのAI出力を読み込み"""
        if not self.spreadsheet:
            return []
        
        try:
            worksheet = self.spreadsheet.worksheet('ai_outputs')
            records = worksheet.get_all_records()
            
            outputs = []
            for record in records:
                if record.get('project_id') == project_id:
                    content = record.get('content', '')
                    try:
                        content = json.loads(content)
                    except:
                        pass
                    
                    outputs.append({
                        'id': record.get('id', ''),
                        'type': record.get('type', ''),
                        'content': content,
                        'created_at': record.get('created_at', '')
                    })
            
            return outputs
            
        except Exception as e:
            st.error(f"AI出力読み込みエラー: {str(e)}")
            return []
    
    def get_spreadsheet_url(self) -> str:
        """スプレッドシートのURLを取得"""
        if self.spreadsheet:
            return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
        return ""

# Streamlitのキャッシュを使用してシングルトンを実装
@st.cache_resource
def get_db() -> GoogleSheetsDB:
    """データベースインスタンスを取得（キャッシュされたシングルトン）"""
    return GoogleSheetsDB()

def sync_session_to_sheets():
    """セッション状態をGoogle Sheetsに同期"""
    db = get_db()
    
    # プロジェクトを保存
    if 'projects' in st.session_state:
        db.save_projects(st.session_state.projects)
    
    # TODOを保存
    if 'todos' in st.session_state:
        db.save_todos(st.session_state.todos)

def sync_sheets_to_session():
    """Google Sheetsからセッション状態に同期"""
    db = get_db()
    
    # プロジェクトを読み込み
    projects = db.load_projects()
    if projects:
        # 既存のプロジェクトと比較して、変更がある場合のみ更新
        current_projects = st.session_state.get('projects', {})
        if projects != current_projects:
            st.session_state.projects = projects
    
    # TODOを読み込み
    todos = db.load_todos()
    if todos:
        # 既存のTODOと比較して、変更がある場合のみ更新
        current_todos = st.session_state.get('todos', [])
        if todos != current_todos:
            st.session_state.todos = todos