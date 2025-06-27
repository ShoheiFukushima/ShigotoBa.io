#!/usr/bin/env python3
"""
Shigotoba.io テストスイート
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import json

# テスト対象のインポート
from shigotoba_modules import ShigotobaAIModules
from app_shigotoba import ProjectPlan, Phase

# フィクスチャ
@pytest.fixture
def test_project_data():
    """テスト用プロジェクトデータ"""
    return {
        'app_name': 'TestApp',
        'category': '仕事効率化',
        'platforms': ['iOS', 'Android'],
        'concept_oneline': 'テスト用のアプリコンセプト',
        'problems': ['問題1', '問題2', '問題3'],
        'target_users': 'テストユーザー層',
        'usage_scenes': 'テスト利用シーン',
        'core_features': ['機能1', '機能2', '機能3'],
        'unique_features': ['差別化1', '差別化2'],
        'monetization': 'フリーミアム',
        'price_range': '基本無料、プレミアム月額1000円'
    }

@pytest.fixture
def ai_modules():
    """AIモジュールのインスタンス"""
    return ShigotobaAIModules()

class TestShigotobaAIModules:
    """AIモジュールのテスト"""
    
    @pytest.mark.asyncio
    async def test_generate_competitor_list(self, ai_modules):
        """競合リスト生成のテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # モックレスポンス
            mock_response = Mock()
            mock_response.content = """
            1. Todoist
            2. Notion
            3. Asana
            4. Trello
            5. Monday.com
            """
            mock_response.cost = 0.01
            mock_response.model = 'test-model'
            mock_generate.return_value = mock_response
            
            # テスト実行
            competitors = await ai_modules.generate_competitor_list('TestApp', '仕事効率化')
            
            # 検証
            assert len(competitors) == 5
            assert 'Todoist' in competitors[0]
            assert mock_generate.called
    
    @pytest.mark.asyncio
    async def test_market_analysis_ai(self, ai_modules, test_project_data):
        """マーケット分析AIのテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # モックレスポンス
            mock_response = Mock()
            mock_response.content = json.dumps({
                'competitors': ['競合A', '競合B', '競合C'],
                'market_size': {
                    'TAM': '1000億円',
                    'SAM': '100億円',
                    'SOM': '10億円'
                },
                'risks': ['リスク1', 'リスク2']
            })
            mock_response.cost = 0.02
            mock_response.model = 'test-model'
            mock_generate.return_value = mock_response
            
            # テスト実行
            result = await ai_modules.market_analysis_ai(test_project_data)
            
            # 検証
            assert result['status'] == 'completed'
            assert 'result' in result
            assert 'competitors' in result['result']
            assert result['cost'] == 0.02
    
    @pytest.mark.asyncio
    async def test_copywriting_ai(self, ai_modules, test_project_data):
        """コピーライティングAIのテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # モックレスポンス
            mock_response = Mock()
            mock_response.content = "魅力的なコピー文章"
            mock_response.cost = 0.015
            mock_response.model = 'test-model'
            mock_generate.return_value = mock_response
            
            # マーケット分析結果（モック）
            market_analysis = {
                'result': {
                    'competitors': ['競合A', '競合B'],
                    'market_size': {'TAM': '1000億円'}
                }
            }
            
            # テスト実行
            result = await ai_modules.copywriting_ai(test_project_data, market_analysis)
            
            # 検証
            assert result['status'] == 'completed'
            assert 'headlines' in result['result']
            assert 'body_copy' in result['result']
            assert result['cost'] == 0.015
    
    @pytest.mark.asyncio
    async def test_humanist_ai(self, ai_modules):
        """人文学者AIのテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # モックレスポンス
            mock_response = Mock()
            mock_response.content = "深い哲学的洞察"
            mock_response.cost = 0.02
            mock_response.model = 'test-model'
            mock_generate.return_value = mock_response
            
            # テスト戦略データ
            strategy_data = {
                'growth': '成長戦略',
                'pricing': '価格戦略'
            }
            
            # テスト実行
            result = await ai_modules.humanist_ai(strategy_data)
            
            # 検証
            assert result['status'] == 'completed'
            assert 'cultural_analysis' in result['result']
            assert 'philosophical_insights' in result['result']
            assert 'full_analysis' in result['result']
    
    @pytest.mark.asyncio
    async def test_ai_conference_system(self, ai_modules):
        """AI専門家会議システムのテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # モックレスポンス
            mock_response = Mock()
            mock_response.content = "統合戦略レポート"
            mock_response.cost = 0.025
            mock_response.model = 'test-model'
            mock_generate.return_value = mock_response
            
            # テストデータ
            growth_strategy = {'acquisition': 'オーガニック成長'}
            pricing_strategy = {'price': '月額1000円'}
            market_analysis = {'competitors': ['競合A']}
            
            # テスト実行
            result = await ai_modules.ai_conference_system(
                growth_strategy, pricing_strategy, market_analysis
            )
            
            # 検証
            assert result['status'] == 'completed'
            assert 'executive_summary' in result['result']
            assert 'integrated_strategy' in result['result']
            assert 'execution_plan' in result['result']
    
    @pytest.mark.asyncio
    async def test_revision_ai(self, ai_modules):
        """修正反映AIのテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # モックレスポンス
            mock_response = Mock()
            mock_response.content = "修正済み成果物"
            mock_response.cost = 0.01
            mock_response.model = 'test-model'
            mock_generate.return_value = mock_response
            
            # テストデータ
            original_outputs = {'copy': 'オリジナルコピー'}
            revision_instructions = "もっとキャッチーに"
            
            # テスト実行
            result = await ai_modules.revision_ai(original_outputs, revision_instructions)
            
            # 検証
            assert result['status'] == 'completed'
            assert 'revised_outputs' in result['result']
            assert 'changes_summary' in result['result']
    
    def test_log_execution(self, ai_modules):
        """実行ログ記録のテスト"""
        # ログ記録
        ai_modules.log_execution('test_module', {'input': 'data'}, {'output': 'result'})
        
        # 検証
        assert len(ai_modules.execution_log) == 1
        assert ai_modules.execution_log[0]['module'] == 'test_module'
        assert 'timestamp' in ai_modules.execution_log[0]
        assert ai_modules.execution_log[0]['input'] == {'input': 'data'}
        assert ai_modules.execution_log[0]['output'] == {'output': 'result'}

class TestProjectPlan:
    """ProjectPlanデータクラスのテスト"""
    
    def test_project_plan_creation(self):
        """ProjectPlanの作成テスト"""
        project = ProjectPlan(
            app_name="TestApp",
            category="仕事効率化",
            platforms=["iOS", "Android"],
            concept_oneline="テストコンセプト",
            problems=["問題1", "問題2"],
            target_users="テストユーザー",
            usage_scenes="テストシーン",
            core_features=["機能1", "機能2", "機能3"],
            unique_features=["差別化1"],
            monetization="フリーミアム",
            price_range="基本無料"
        )
        
        assert project.app_name == "TestApp"
        assert len(project.platforms) == 2
        assert len(project.core_features) == 3
        assert project.created_at != ""
    
    def test_project_plan_optional_fields(self):
        """ProjectPlanのオプショナルフィールドテスト"""
        project = ProjectPlan(
            app_name="TestApp",
            category="仕事効率化",
            platforms=["iOS"],
            concept_oneline="テスト",
            problems=["問題1"],
            target_users="ユーザー",
            usage_scenes="シーン",
            core_features=["機能1", "機能2", "機能3"],
            unique_features=["差別化1"],
            monetization="フリーミアム",
            price_range="無料",
            competitors="競合A, 競合B",
            budget="50万円以下",
            release_date="2024-12-31"
        )
        
        assert project.competitors == "競合A, 競合B"
        assert project.budget == "50万円以下"
        assert project.release_date == "2024-12-31"

class TestPhaseEnum:
    """Phaseenumのテスト"""
    
    def test_phase_values(self):
        """フェーズ値のテスト"""
        assert Phase.PLANNING.value == "planning"
        assert Phase.PHASE1.value == "phase1_strategy"
        assert Phase.APPROVAL1.value == "approval1"
        assert Phase.PHASE2.value == "phase2_execution"
        assert Phase.APPROVAL2.value == "approval2"
        assert Phase.MONITORING.value == "monitoring"

# エラーケースのテスト
class TestErrorCases:
    """エラーケースのテスト"""
    
    @pytest.mark.asyncio
    async def test_market_analysis_ai_error(self, ai_modules, test_project_data):
        """マーケット分析AIのエラーテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # エラーを発生させる
            mock_generate.side_effect = Exception("API Error")
            
            # テスト実行
            result = await ai_modules.market_analysis_ai(test_project_data)
            
            # 検証
            assert result['status'] == 'error'
            assert 'error' in result
            assert "API Error" in result['error']
    
    @pytest.mark.asyncio
    async def test_competitor_list_error(self, ai_modules):
        """競合リスト生成のエラーテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # エラーを発生させる
            mock_generate.side_effect = Exception("API Error")
            
            # テスト実行
            competitors = await ai_modules.generate_competitor_list('TestApp', '仕事効率化')
            
            # 検証
            assert len(competitors) == 1
            assert 'エラー' in competitors[0]

# 統合テスト
class TestIntegration:
    """統合テスト"""
    
    @pytest.mark.asyncio
    async def test_full_phase1_flow(self, ai_modules, test_project_data):
        """フェーズ1の完全フローテスト"""
        with patch('shigotoba_modules.ai_client.generate_content') as mock_generate:
            # 各AIのモックレスポンスを設定
            mock_responses = [
                Mock(content=json.dumps({'competitors': ['A', 'B', 'C']}), cost=0.02, model='test'),
                Mock(content="統合戦略", cost=0.025, model='test'),
                Mock(content="コピー文章", cost=0.015, model='test'),
                Mock(content="哲学的分析", cost=0.02, model='test'),
            ]
            mock_generate.side_effect = mock_responses
            
            # マーケット分析
            market_result = await ai_modules.market_analysis_ai(test_project_data)
            assert market_result['status'] == 'completed'
            
            # AI会議（モックデータで）
            conference_result = await ai_modules.ai_conference_system(
                {'growth': 'strategy'}, {'price': '1000円'}, market_result['result']
            )
            assert conference_result['status'] == 'completed'
            
            # コピーライティング
            copy_result = await ai_modules.copywriting_ai(test_project_data, market_result)
            assert copy_result['status'] == 'completed'
            
            # 人文学者AI
            humanist_result = await ai_modules.humanist_ai(conference_result['result'])
            assert humanist_result['status'] == 'completed'
            
            # ログ確認
            assert len(ai_modules.execution_log) == 4

if __name__ == "__main__":
    pytest.main([__file__, "-v"])