#!/usr/bin/env python3
"""
AIチェーンパイプライン - 自動連鎖処理システム
プロジェクト概要から自動的に複数のAI分析を連鎖実行
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, AsyncIterator
from dataclasses import dataclass, field
import streamlit as st
import google.generativeai as genai
import os
from enum import Enum
import logging

# ロギング設定
logger = logging.getLogger(__name__)

class ChainStatus(Enum):
    """チェーン実行状態"""
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ChainStage:
    """パイプラインの各ステージ定義"""
    id: str
    name: str
    prompt_template: str
    required_inputs: List[str]
    output_key: str
    description: str
    max_retries: int = 3
    
    def build_prompt(self, context: Dict[str, Any]) -> str:
        """コンテキストからプロンプトを生成"""
        prompt = self.prompt_template
        for key, value in context.items():
            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False, indent=2)
            elif isinstance(value, list):
                value = "\n".join(str(item) for item in value)
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt

@dataclass
class ChainResult:
    """各ステージの実行結果"""
    stage_id: str
    stage_name: str
    status: ChainStatus
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class AIChainPipeline:
    """AI連鎖処理パイプライン"""
    
    def __init__(self):
        # Gemini API設定
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY または GOOGLE_API_KEY が設定されていません")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # パイプラインステージの定義
        self.stages = self._define_stages()
        self.results = []
    
    def _define_stages(self) -> List[ChainStage]:
        """パイプラインステージを定義"""
        return [
            ChainStage(
                id="market_analysis",
                name="市場分析",
                prompt_template="""あなたは市場分析の専門家です。以下のプロジェクト概要に基づいて、詳細な市場分析を行ってください。

【プロジェクト概要】
{project_overview}

【分析項目】
1. 市場規模と成長性
   - 国内市場規模（具体的な金額）
   - グローバル市場規模
   - 年間成長率（CAGR）
   - 主要な成長要因

2. ターゲット市場セグメント
   - 主要セグメントの特定
   - 各セグメントの規模と特徴
   - 最も有望なセグメント

3. 市場トレンド
   - 技術トレンド
   - 消費者行動の変化
   - 規制・政策の動向

4. 市場参入の機会と脅威
   - 参入障壁
   - 成功要因
   - リスク要因

できるだけ具体的な数値とデータを含めて分析してください。""",
                required_inputs=["project_overview"],
                output_key="market_analysis",
                description="市場規模、成長性、トレンドを分析"
            ),
            
            ChainStage(
                id="competitor_analysis",
                name="競合分析",
                prompt_template="""あなたは競合分析の専門家です。以下の情報に基づいて、詳細な競合分析を行ってください。

【プロジェクト概要】
{project_overview}

【市場分析結果】
{market_analysis}

【分析項目】
1. 主要競合企業（5社以上）
   - 企業名と概要
   - 市場シェア
   - 主力製品/サービス
   - 価格帯
   - 強みと弱み

2. 競合マップ
   - 直接競合
   - 間接競合
   - 代替品/サービス

3. 競合の戦略分析
   - マーケティング戦略
   - 価格戦略
   - 技術戦略
   - 顧客獲得戦略

4. 差別化ポイント
   - 自社の競争優位性
   - 独自の価値提案
   - 防御可能な差別化要素

具体的な企業名と数値を含めて分析してください。""",
                required_inputs=["project_overview", "market_analysis"],
                output_key="competitor_analysis",
                description="競合企業と差別化ポイントを分析"
            ),
            
            ChainStage(
                id="persona_generation",
                name="ターゲットペルソナ生成",
                prompt_template="""あなたはマーケティングペルソナ作成の専門家です。以下の情報に基づいて、詳細なターゲットペルソナを作成してください。

【プロジェクト概要】
{project_overview}

【市場分析結果】
{market_analysis}

【競合分析結果】
{competitor_analysis}

【ペルソナ作成項目】
3つの主要ペルソナを作成し、それぞれについて以下を含めてください：

1. 基本属性
   - 名前（仮名）
   - 年齢・性別
   - 職業・役職
   - 年収
   - 居住地
   - 家族構成

2. サイコグラフィック
   - 価値観
   - ライフスタイル
   - 興味・関心
   - 情報収集方法

3. 行動特性
   - 購買行動パターン
   - 意思決定プロセス
   - 利用デバイス・チャネル
   - ブランドとの接点

4. ニーズと課題
   - 現在抱えている課題
   - 求めている解決策
   - 購買の動機
   - 購買の障壁

各ペルソナに優先順位をつけ、なぜそのペルソナが重要かを説明してください。""",
                required_inputs=["project_overview", "market_analysis", "competitor_analysis"],
                output_key="target_personas",
                description="詳細なターゲットペルソナを生成"
            ),
            
            ChainStage(
                id="feature_design",
                name="機能設計・MVP定義",
                prompt_template="""あなたはプロダクト設計の専門家です。以下の情報に基づいて、MVP（Minimum Viable Product）の機能設計を行ってください。

【プロジェクト概要】
{project_overview}

【市場分析結果】
{market_analysis}

【競合分析結果】
{competitor_analysis}

【ターゲットペルソナ】
{target_personas}

【設計項目】
1. コア機能（MVP必須機能）
   - 機能名と詳細説明
   - なぜ必須なのか
   - 技術的実装の概要
   - 開発工数の見積もり

2. Nice to Have機能（フェーズ2）
   - 機能名と詳細説明
   - 追加する価値
   - 優先順位

3. 将来の拡張機能（フェーズ3以降）
   - 長期ビジョンに基づく機能
   - 市場の成熟に合わせた機能

4. 技術スタック推奨
   - フロントエンド
   - バックエンド
   - データベース
   - インフラ
   - 選定理由

5. 開発ロードマップ
   - MVP完成まで：○週間
   - フェーズ2まで：○ヶ月
   - 各マイルストーン

ユーザー価値を最大化しつつ、最小限の機能で市場検証できる設計を提案してください。""",
                required_inputs=["project_overview", "market_analysis", "competitor_analysis", "target_personas"],
                output_key="feature_design",
                description="MVP機能と技術スタックを設計"
            ),
            
            ChainStage(
                id="pricing_strategy",
                name="価格戦略・ビジネスモデル",
                prompt_template="""あなたはプライシング戦略の専門家です。以下の情報に基づいて、最適な価格戦略とビジネスモデルを提案してください。

【プロジェクト概要】
{project_overview}

【市場分析結果】
{market_analysis}

【競合分析結果】
{competitor_analysis}

【ターゲットペルソナ】
{target_personas}

【機能設計】
{feature_design}

【戦略策定項目】
1. 価格モデル
   - 推奨モデル（サブスク/従量課金/買い切り等）
   - 選定理由
   - 競合との比較

2. 価格プラン詳細
   - 各プランの名称
   - 価格（月額/年額）
   - 含まれる機能
   - ユーザー数/使用量制限
   - サポートレベル

3. 価格設定の根拠
   - コスト構造分析
   - 価値ベース価格分析
   - 競合価格分析
   - 価格感度分析

4. 収益予測
   - 想定顧客数
   - 平均単価
   - MRR/ARR予測
   - ユニットエコノミクス
   - 損益分岐点

5. 価格戦略
   - 導入期の戦略
   - 成長期の戦略
   - 割引・プロモーション戦略
   - アップセル/クロスセル戦略

各ペルソナに対する価格の妥当性も検証してください。""",
                required_inputs=["project_overview", "market_analysis", "competitor_analysis", "target_personas", "feature_design"],
                output_key="pricing_strategy",
                description="最適な価格戦略とビジネスモデルを策定"
            ),
            
            ChainStage(
                id="go_to_market",
                name="Go-to-Market戦略",
                prompt_template="""あなたはGo-to-Market戦略の専門家です。以下の情報に基づいて、包括的なGTM戦略を策定してください。

【プロジェクト概要】
{project_overview}

【これまでの分析結果】
- 市場分析：{market_analysis}
- 競合分析：{competitor_analysis}
- ペルソナ：{target_personas}
- 機能設計：{feature_design}
- 価格戦略：{pricing_strategy}

【GTM戦略項目】
1. ポジショニング
   - ブランドポジショニング
   - バリュープロポジション
   - キーメッセージ

2. マーケティングチャネル戦略
   - 優先チャネル（なぜそのチャネルか）
   - チャネル別の施策
   - 予算配分の推奨

3. ローンチ戦略
   - プレローンチ（ティザー、事前登録）
   - ローンチイベント/キャンペーン
   - ポストローンチ（定着化施策）

4. コンテンツ戦略
   - コンテンツテーマ
   - コンテンツカレンダー（3ヶ月分）
   - 各ペルソナ向けコンテンツ

5. 成長戦略
   - 顧客獲得戦略
   - リテンション戦略
   - 拡大戦略

6. KPIと成功指標
   - 3ヶ月後の目標
   - 6ヶ月後の目標
   - 1年後の目標
   - 測定方法

実行可能で具体的なアクションプランを含めてください。""",
                required_inputs=["project_overview", "market_analysis", "competitor_analysis", "target_personas", "feature_design", "pricing_strategy"],
                output_key="go_to_market_strategy",
                description="包括的なGo-to-Market戦略を策定"
            )
        ]
    
    async def execute_stage(self, stage: ChainStage, context: Dict[str, Any]) -> ChainResult:
        """単一ステージを実行"""
        start_time = datetime.now()
        
        try:
            # 必要な入力があるか確認
            for required_input in stage.required_inputs:
                if required_input not in context:
                    raise ValueError(f"必要な入力 '{required_input}' がありません")
            
            # プロンプト生成
            prompt = stage.build_prompt(context)
            
            # Gemini APIを呼び出し
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            
            # 実行時間計算
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ChainResult(
                stage_id=stage.id,
                stage_name=stage.name,
                status=ChainStatus.COMPLETED,
                output=response.text,
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"ステージ {stage.name} でエラー: {str(e)}")
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ChainResult(
                stage_id=stage.id,
                stage_name=stage.name,
                status=ChainStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_chain(self, project_overview: str) -> AsyncIterator[Dict[str, Any]]:
        """チェーン全体を実行し、進捗をストリーミング"""
        context = {"project_overview": project_overview}
        total_stages = len(self.stages)
        
        for i, stage in enumerate(self.stages):
            # 進捗状況を通知
            yield {
                "type": "progress",
                "stage": stage.name,
                "stage_id": stage.id,
                "progress": i / total_stages,
                "status": "running",
                "description": stage.description
            }
            
            # ステージ実行
            result = await self.execute_stage(stage, context)
            self.results.append(result)
            
            if result.status == ChainStatus.COMPLETED:
                # 成功時は結果をコンテキストに追加
                context[stage.output_key] = result.output
                
                yield {
                    "type": "result",
                    "stage": stage.name,
                    "stage_id": stage.id,
                    "status": "completed",
                    "output": result.output,
                    "execution_time": result.execution_time
                }
            else:
                # 失敗時はエラーを通知して中断
                yield {
                    "type": "error",
                    "stage": stage.name,
                    "stage_id": stage.id,
                    "error": result.error
                }
                break
        
        # 最終的な完了通知
        yield {
            "type": "complete",
            "total_execution_time": sum(r.execution_time for r in self.results),
            "context": context
        }
    
    def generate_final_report(self) -> Dict[str, Any]:
        """最終レポートを生成"""
        report = {
            "execution_summary": {
                "total_stages": len(self.stages),
                "completed_stages": sum(1 for r in self.results if r.status == ChainStatus.COMPLETED),
                "failed_stages": sum(1 for r in self.results if r.status == ChainStatus.FAILED),
                "total_execution_time": sum(r.execution_time for r in self.results)
            },
            "stage_results": {}
        }
        
        for result in self.results:
            if result.status == ChainStatus.COMPLETED:
                report["stage_results"][result.stage_id] = {
                    "name": result.stage_name,
                    "output": result.output,
                    "execution_time": result.execution_time
                }
        
        return report

# Streamlit用のヘルパー関数
def get_ai_chain_pipeline() -> AIChainPipeline:
    """シングルトンのAIChainPipelineを取得"""
    if 'ai_chain_pipeline' not in st.session_state:
        st.session_state.ai_chain_pipeline = AIChainPipeline()
    return st.session_state.ai_chain_pipeline