#!/usr/bin/env python3
"""
市場分析ツール - Gemini APIを使用した市場調査と競合分析
"""

import os
import sys
import asyncio
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

# パス追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.ai_client import ai_client
from config.ai_models import TaskType

class MarketAnalyzer:
    """市場分析クラス"""
    
    def __init__(self):
        self.ai_client = ai_client
    
    async def analyze_market(
        self,
        product_info: Dict[str, str],
        analysis_depth: str = "standard"
    ) -> Dict[str, Any]:
        """
        市場分析を実行
        
        Args:
            product_info: 製品情報
            analysis_depth: 分析の深度（simple/standard/detailed）
        
        Returns:
            分析結果
        """
        prompt = self._create_market_analysis_prompt(product_info, analysis_depth)
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.MARKET_ANALYSIS.value,
            temperature=0.3,
            max_tokens=2000
        )
        
        try:
            # レスポンスからJSON部分を抽出
            content = response.get('content', '')
            # JSON部分を探して解析
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content
            
            return json.loads(json_str)
        except:
            # JSON解析に失敗した場合は構造化されたデータを返す
            return self._parse_text_response(content)
    
    async def analyze_competitors(
        self,
        product_info: Dict[str, str],
        num_competitors: int = 3
    ) -> List[Dict[str, Any]]:
        """
        競合分析を実行
        
        Args:
            product_info: 製品情報
            num_competitors: 分析する競合数
        
        Returns:
            競合情報のリスト
        """
        prompt = f"""
        以下の製品の主要競合を{num_competitors}社分析してください：
        
        製品名: {product_info.get('name', 'N/A')}
        カテゴリ: {product_info.get('category', 'N/A')}
        ターゲット: {product_info.get('target', 'N/A')}
        価格帯: {product_info.get('price', 'N/A')}
        
        各競合について以下の情報をJSON形式で提供してください：
        {{
            "competitors": [
                {{
                    "name": "競合名",
                    "description": "簡単な説明",
                    "strengths": ["強み1", "強み2"],
                    "weaknesses": ["弱み1", "弱み2"],
                    "market_share": "推定市場シェア",
                    "price_range": "価格帯",
                    "target_audience": "ターゲット層"
                }}
            ]
        }}
        """
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.MARKET_ANALYSIS.value,
            temperature=0.3,
            max_tokens=1500
        )
        
        try:
            content = response.get('content', '')
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content
            
            data = json.loads(json_str)
            return data.get('competitors', [])
        except:
            return []
    
    async def generate_swot_analysis(
        self,
        product_info: Dict[str, str],
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[str]]:
        """
        SWOT分析を生成
        
        Args:
            product_info: 製品情報
            market_data: 市場データ（オプション）
        
        Returns:
            SWOT分析結果
        """
        context = f"""
        製品情報:
        - 名前: {product_info.get('name', 'N/A')}
        - カテゴリ: {product_info.get('category', 'N/A')}
        - ターゲット: {product_info.get('target', 'N/A')}
        - 独自性: {product_info.get('uniqueness', 'N/A')}
        """
        
        if market_data:
            context += f"\n\n市場データ: {json.dumps(market_data, ensure_ascii=False)}"
        
        prompt = f"""
        {context}
        
        上記の製品についてSWOT分析を行い、JSON形式で返してください：
        {{
            "strengths": ["強み1", "強み2", "強み3"],
            "weaknesses": ["弱み1", "弱み2", "弱み3"],
            "opportunities": ["機会1", "機会2", "機会3"],
            "threats": ["脅威1", "脅威2", "脅威3"]
        }}
        """
        
        response = await self.ai_client.generate_content(
            prompt=prompt,
            task_type=TaskType.MARKET_ANALYSIS.value,
            temperature=0.4,
            max_tokens=1000
        )
        
        try:
            content = response.get('content', '')
            if '```json' in content:
                json_start = content.find('```json') + 7
                json_end = content.find('```', json_start)
                json_str = content[json_start:json_end].strip()
            else:
                json_str = content
            
            return json.loads(json_str)
        except:
            # フォールバック
            return {
                "strengths": ["イノベーティブな機能", "使いやすいUI", "競争力のある価格"],
                "weaknesses": ["ブランド認知度", "限定的な機能", "サポート体制"],
                "opportunities": ["市場の成長", "デジタル化の加速", "新規顧客層"],
                "threats": ["競合の参入", "技術の陳腐化", "規制の変化"]
            }
    
    def _create_market_analysis_prompt(
        self,
        product_info: Dict[str, str],
        analysis_depth: str
    ) -> str:
        """市場分析用のプロンプトを作成"""
        
        base_prompt = f"""
        以下の製品について市場分析を行ってください：
        
        製品名: {product_info.get('name', 'N/A')}
        カテゴリ: {product_info.get('category', 'N/A')}
        ターゲット顧客: {product_info.get('target', 'N/A')}
        価格帯: {product_info.get('price', 'N/A')}
        独自の価値提案: {product_info.get('uniqueness', 'N/A')}
        """
        
        if analysis_depth == "simple":
            base_prompt += """
            
            以下の項目について簡潔に分析し、JSON形式で回答してください：
            {
                "market_size": "市場規模の推定",
                "growth_rate": "年間成長率",
                "key_trends": ["主要トレンド1", "主要トレンド2"],
                "target_segments": ["セグメント1", "セグメント2"]
            }
            """
        elif analysis_depth == "detailed":
            base_prompt += """
            
            以下の項目について詳細に分析し、JSON形式で回答してください：
            {
                "market_overview": {
                    "size": "市場規模（具体的な数値）",
                    "growth_rate": "成長率（過去3年と今後3年の予測）",
                    "maturity": "市場の成熟度"
                },
                "trends": {
                    "current": ["現在のトレンド1", "現在のトレンド2", "現在のトレンド3"],
                    "emerging": ["新興トレンド1", "新興トレンド2"],
                    "declining": ["衰退トレンド1", "衰退トレンド2"]
                },
                "customer_analysis": {
                    "segments": ["セグメント1", "セグメント2", "セグメント3"],
                    "pain_points": ["課題1", "課題2", "課題3"],
                    "buying_behavior": "購買行動の特徴"
                },
                "competitive_landscape": {
                    "market_leaders": ["リーダー1", "リーダー2"],
                    "market_share_distribution": "シェア分布の説明",
                    "entry_barriers": ["参入障壁1", "参入障壁2"]
                },
                "opportunities": ["機会1", "機会2", "機会3"],
                "risks": ["リスク1", "リスク2", "リスク3"]
            }
            """
        else:  # standard
            base_prompt += """
            
            以下の項目について分析し、JSON形式で回答してください：
            {
                "market_size": "市場規模の推定",
                "growth_rate": "年間成長率",
                "key_trends": ["トレンド1", "トレンド2", "トレンド3"],
                "target_segments": ["セグメント1", "セグメント2", "セグメント3"],
                "competitive_intensity": "競争の激しさ（低/中/高）",
                "opportunities": ["機会1", "機会2"],
                "challenges": ["課題1", "課題2"]
            }
            """
        
        return base_prompt
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """テキストレスポンスを構造化データに変換"""
        # シンプルなフォールバック実装
        return {
            "market_size": "分析中",
            "growth_rate": "分析中",
            "key_trends": ["AIの活用", "自動化の進展", "パーソナライゼーション"],
            "analysis_text": text
        }

# シングルトンインスタンス
market_analyzer = MarketAnalyzer()