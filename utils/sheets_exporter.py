#!/usr/bin/env python3
"""
Google Sheets専用出力モジュール
サマリーダッシュボードからの高度な出力機能
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional
import streamlit as st
from .google_sheets_db import get_db

class SheetsExporter:
    """Google Sheets出力専用クラス"""
    
    def __init__(self):
        self.db = get_db()
        
    def create_summary_export(self, project_data: Dict[str, Any], options: List[str]) -> Dict[str, Any]:
        """サマリー出力用のデータを作成"""
        export_data = {
            'メタ情報': {
                '出力日時': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'プロジェクト名': project_data.get('name', ''),
                'プロジェクトID': project_data.get('id', ''),
                '出力オプション': ', '.join(options)
            }
        }
        
        # 基本情報
        if "プロジェクト基本情報" in options:
            export_data['基本情報'] = {
                'プロジェクト名': project_data.get('name', ''),
                'カテゴリ': project_data.get('type', ''),
                'ステータス': project_data.get('status', ''),
                '作成日': project_data.get('created_at', ''),
                '説明': project_data.get('description', '')
            }
            
            # 技術スタック
            if 'tech_stack' in project_data:
                tech_stack = project_data['tech_stack']
                export_data['技術スタック'] = {
                    'フロントエンド': tech_stack.get('frontend', ''),
                    'バックエンド': tech_stack.get('backend', ''),
                    'データベース': tech_stack.get('database', ''),
                    'デプロイ': tech_stack.get('deploy', '')
                }
        
        # AI分析結果
        if 'ai_analysis' in project_data:
            ai_analysis = project_data['ai_analysis']
            
            if "市場分析" in options and 'market_analysis' in ai_analysis:
                export_data['市場分析'] = self._parse_analysis_text(ai_analysis['market_analysis'])
            
            if "競合分析" in options and 'competitor_analysis' in ai_analysis:
                export_data['競合分析'] = self._parse_analysis_text(ai_analysis['competitor_analysis'])
            
            if "ターゲットペルソナ" in options and 'target_personas' in ai_analysis:
                export_data['ターゲットペルソナ'] = self._parse_analysis_text(ai_analysis['target_personas'])
            
            if "機能設計" in options and 'feature_design' in ai_analysis:
                export_data['機能設計'] = self._parse_analysis_text(ai_analysis['feature_design'])
            
            if "価格戦略" in options and 'pricing_strategy' in ai_analysis:
                export_data['価格戦略'] = self._parse_analysis_text(ai_analysis['pricing_strategy'])
            
            if "Go-to-Market戦略" in options and 'go_to_market_strategy' in ai_analysis:
                export_data['GTM戦略'] = self._parse_analysis_text(ai_analysis['go_to_market_strategy'])
        
        return export_data
    
    def _parse_analysis_text(self, text: str) -> Dict[str, str]:
        """分析テキストを構造化されたデータに変換"""
        if not text:
            return {'内容': ''}
        
        # セクション分割を試みる
        sections = {}
        current_section = 'メイン内容'
        current_content = []
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            
            # セクションヘッダーの検出（【】または##で囲まれた部分）
            if line.startswith('【') and line.endswith('】'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('【】')
                current_content = []
            elif line.startswith('##'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.replace('#', '').strip()
                current_content = []
            else:
                if line:  # 空行でない場合のみ追加
                    current_content.append(line)
        
        # 最後のセクションを追加
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections if sections else {'内容': text}
    
    def export_to_structured_sheet(self, project_data: Dict[str, Any], options: List[str], 
                                 sheet_name: str) -> bool:
        """構造化されたシートとして出力"""
        try:
            # データ準備
            export_data = self.create_summary_export(project_data, options)
            
            # 新しいワークシートを作成
            worksheet = self.db.spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=10)
            
            # ヘッダー設定
            headers = ['カテゴリ', 'セクション', '項目', '内容', '詳細']
            worksheet.update('A1:E1', [headers])
            
            # ヘッダーのフォーマット
            worksheet.format('A1:E1', {
                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True}
            })
            
            # データ行の追加
            row = 2
            for category, content in export_data.items():
                if isinstance(content, dict):
                    for section, details in content.items():
                        if isinstance(details, dict):
                            for item, value in details.items():
                                worksheet.update(f'A{row}:E{row}', [[
                                    category, section, item, str(value)[:100], str(value)
                                ]])
                                row += 1
                        else:
                            worksheet.update(f'A{row}:E{row}', [[
                                category, section, '', str(details)[:100], str(details)
                            ]])
                            row += 1
                else:
                    worksheet.update(f'A{row}:E{row}', [[
                        category, '', '', str(content)[:100], str(content)
                    ]])
                    row += 1
            
            # 列幅の自動調整
            worksheet.columns_auto_resize(0, 4)
            
            return True
            
        except Exception as e:
            st.error(f"構造化出力エラー: {str(e)}")
            return False
    
    def export_to_analysis_dashboard(self, project_data: Dict[str, Any]) -> bool:
        """分析ダッシュボード形式で出力"""
        try:
            sheet_name = f"分析ダッシュボード_{datetime.now().strftime('%Y%m%d_%H%M')}"
            worksheet = self.db.spreadsheet.add_worksheet(title=sheet_name, rows=50, cols=15)
            
            # ダッシュボードレイアウト
            # タイトル
            worksheet.update('A1', f"📊 {project_data.get('name', 'プロジェクト')} 分析ダッシュボード")
            worksheet.merge_cells('A1:O1')
            worksheet.format('A1', {
                'backgroundColor': {'red': 0.1, 'green': 0.3, 'blue': 0.7},
                'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 
                             'bold': True, 'fontSize': 16},
                'horizontalAlignment': 'CENTER'
            })
            
            # 基本情報セクション
            row = 3
            worksheet.update(f'A{row}', '📋 基本情報')
            worksheet.format(f'A{row}', {'textFormat': {'bold': True, 'fontSize': 12}})
            row += 1
            
            basic_info = [
                ['プロジェクト名', project_data.get('name', '')],
                ['カテゴリ', project_data.get('type', '')],
                ['ステータス', project_data.get('status', '')],
                ['作成日', project_data.get('created_at', '')]
            ]
            
            for info in basic_info:
                worksheet.update(f'A{row}:B{row}', [info])
                row += 1
            
            # 分析結果セクション
            if 'ai_analysis' in project_data:
                ai_analysis = project_data['ai_analysis']
                
                # 市場分析
                if 'market_analysis' in ai_analysis:
                    row += 2
                    worksheet.update(f'A{row}', '🏪 市場分析')
                    worksheet.format(f'A{row}', {'textFormat': {'bold': True, 'fontSize': 12}})
                    row += 1
                    
                    market_text = ai_analysis['market_analysis'][:500] + "..." if len(ai_analysis['market_analysis']) > 500 else ai_analysis['market_analysis']
                    worksheet.update(f'A{row}:O{row+5}', market_text)
                    worksheet.merge_cells(f'A{row}:O{row+5}')
                    row += 7
                
                # 競合分析
                if 'competitor_analysis' in ai_analysis:
                    worksheet.update(f'A{row}', '🎯 競合分析')
                    worksheet.format(f'A{row}', {'textFormat': {'bold': True, 'fontSize': 12}})
                    row += 1
                    
                    competitor_text = ai_analysis['competitor_analysis'][:500] + "..." if len(ai_analysis['competitor_analysis']) > 500 else ai_analysis['competitor_analysis']
                    worksheet.update(f'A{row}:O{row+5}', competitor_text)
                    worksheet.merge_cells(f'A{row}:O{row+5}')
                    row += 7
            
            # フッター
            row += 2
            worksheet.update(f'A{row}', f"出力日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            worksheet.format(f'A{row}', {'textFormat': {'italic': True, 'fontSize': 10}})
            
            return True
            
        except Exception as e:
            st.error(f"ダッシュボード出力エラー: {str(e)}")
            return False
    
    def export_to_csv_format(self, project_data: Dict[str, Any], options: List[str]) -> pd.DataFrame:
        """CSV形式のDataFrameとして出力"""
        export_data = self.create_summary_export(project_data, options)
        
        rows = []
        for category, content in export_data.items():
            if isinstance(content, dict):
                for section, details in content.items():
                    if isinstance(details, dict):
                        for item, value in details.items():
                            rows.append({
                                'カテゴリ': category,
                                'セクション': section,
                                '項目': item,
                                '内容': str(value)
                            })
                    else:
                        rows.append({
                            'カテゴリ': category,
                            'セクション': section,
                            '項目': '',
                            '内容': str(details)
                        })
            else:
                rows.append({
                    'カテゴリ': category,
                    'セクション': '',
                    '項目': '',
                    '内容': str(content)
                })
        
        return pd.DataFrame(rows)
    
    def get_available_sheets(self) -> List[str]:
        """利用可能なシート名の一覧を取得"""
        try:
            worksheets = self.db.spreadsheet.worksheets()
            return [ws.title for ws in worksheets]
        except:
            return []
    
    def delete_sheet(self, sheet_name: str) -> bool:
        """指定されたシートを削除"""
        try:
            worksheet = self.db.spreadsheet.worksheet(sheet_name)
            self.db.spreadsheet.del_worksheet(worksheet)
            return True
        except:
            return False

# シングルトンインスタンス
_exporter_instance = None

def get_sheets_exporter():
    """SheetsExporterのシングルトンインスタンスを取得"""
    global _exporter_instance
    if _exporter_instance is None:
        _exporter_instance = SheetsExporter()
    return _exporter_instance