#!/usr/bin/env python3
"""
競合インテリジェンス＆ベンチマーク策定システム
競合の品質基準を分析し、それを超える施策を自動生成
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import requests

class QualityMetric(Enum):
    """品質評価指標"""
    DESIGN = "デザイン品質"
    MESSAGING = "メッセージング"
    TARGETING = "ターゲティング精度"
    ENGAGEMENT = "エンゲージメント率"
    CONVERSION = "コンバージョン率"
    BRAND_CONSISTENCY = "ブランド一貫性"
    INNOVATION = "革新性"
    USER_EXPERIENCE = "ユーザー体験"

@dataclass
class CompetitorAnalysis:
    """競合分析結果"""
    name: str
    product: str
    strengths: List[Dict[str, Any]]
    weaknesses: List[Dict[str, Any]]
    marketing_channels: List[str]
    quality_scores: Dict[QualityMetric, float]
    best_practices: List[str]
    estimated_budget: str
    market_position: int

@dataclass
class QualityBenchmark:
    """品質ベンチマーク"""
    metric: QualityMetric
    industry_average: float
    top_performer: float
    our_target: float
    gap_analysis: str
    improvement_tactics: List[str]

@dataclass
class StrategicCampaign:
    """戦略的キャンペーン"""
    campaign_type: str
    quality_targets: Dict[QualityMetric, float]
    tactics: List[str]
    creative_concepts: List[Dict[str, Any]]
    budget_allocation: Dict[str, float]
    expected_performance: Dict[str, Any]
    timeline: Dict[str, Any]

class CompetitiveIntelligence:
    """競合インテリジェンスシステム"""
    
    def __init__(self):
        self.results_dir = '/Users/fukushimashouhei/dev/marketing-automation-tools/outputs/competitive'
        os.makedirs(self.results_dir, exist_ok=True)
        
        # 業界別の品質基準データベース
        self.industry_standards = self._load_industry_standards()
        
    def _load_industry_standards(self) -> Dict[str, Dict[str, float]]:
        """業界標準を読み込み"""
        return {
            "タスク管理": {
                QualityMetric.DESIGN: 7.5,
                QualityMetric.MESSAGING: 7.0,
                QualityMetric.TARGETING: 8.0,
                QualityMetric.ENGAGEMENT: 6.5,
                QualityMetric.CONVERSION: 5.0,
                QualityMetric.BRAND_CONSISTENCY: 7.5,
                QualityMetric.INNOVATION: 6.0,
                QualityMetric.USER_EXPERIENCE: 8.0
            },
            "情報収集・配信": {
                QualityMetric.DESIGN: 7.0,
                QualityMetric.MESSAGING: 8.0,
                QualityMetric.TARGETING: 8.5,
                QualityMetric.ENGAGEMENT: 7.0,
                QualityMetric.CONVERSION: 6.0,
                QualityMetric.BRAND_CONSISTENCY: 7.0,
                QualityMetric.INNOVATION: 7.5,
                QualityMetric.USER_EXPERIENCE: 7.5
            },
            "ビジネスツール": {
                QualityMetric.DESIGN: 8.0,
                QualityMetric.MESSAGING: 8.5,
                QualityMetric.TARGETING: 9.0,
                QualityMetric.ENGAGEMENT: 6.0,
                QualityMetric.CONVERSION: 7.0,
                QualityMetric.BRAND_CONSISTENCY: 8.5,
                QualityMetric.INNOVATION: 7.0,
                QualityMetric.USER_EXPERIENCE: 8.5
            }
        }
    
    def analyze_competitors(self, product_info: Dict[str, Any]) -> List[CompetitorAnalysis]:
        """競合を詳細分析"""
        
        print(f"🔍 {product_info['name']}の競合を詳細分析中...")
        
        # カテゴリに基づいて競合を特定
        competitors = self._identify_competitors(product_info)
        
        analyzed_competitors = []
        for comp in competitors:
            analysis = self._deep_analyze_competitor(comp, product_info)
            analyzed_competitors.append(analysis)
            print(f"  ✓ {analysis.name}の分析完了")
        
        # 市場ポジション計算
        analyzed_competitors = self._calculate_market_positions(analyzed_competitors)
        
        return analyzed_competitors
    
    def _identify_competitors(self, product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """競合を特定"""
        
        # カテゴリ別の主要競合データベース（実際はAPI/スクレイピング）
        competitor_db = {
            "タスク管理": [
                {"name": "Notion", "product": "Notion", "market_share": 25},
                {"name": "Asana", "product": "Asana", "market_share": 20},
                {"name": "Trello", "product": "Trello", "market_share": 15}
            ],
            "情報収集・配信": [
                {"name": "Feedly", "product": "Feedly", "market_share": 30},
                {"name": "Pocket", "product": "Pocket", "market_share": 20},
                {"name": "Flipboard", "product": "Flipboard", "market_share": 15}
            ],
            "ビジネスツール": [
                {"name": "Salesforce", "product": "Sales Cloud", "market_share": 35},
                {"name": "HubSpot", "product": "CRM", "market_share": 20},
                {"name": "Sansan", "product": "名刺管理", "market_share": 25}
            ]
        }
        
        category = product_info.get('category', 'その他')
        return competitor_db.get(category, [])[:3]  # Top 3
    
    def _deep_analyze_competitor(self, competitor: Dict[str, Any], 
                               product_info: Dict[str, Any]) -> CompetitorAnalysis:
        """競合の深層分析"""
        
        # 品質スコアを評価（実際はWeb分析、広告分析など）
        quality_scores = self._evaluate_quality_scores(competitor)
        
        # マーケティングチャネル分析
        channels = self._analyze_marketing_channels(competitor)
        
        # 強み・弱み分析
        strengths, weaknesses = self._swot_analysis(competitor, quality_scores)
        
        # ベストプラクティス抽出
        best_practices = self._extract_best_practices(competitor, quality_scores)
        
        return CompetitorAnalysis(
            name=competitor['name'],
            product=competitor['product'],
            strengths=strengths,
            weaknesses=weaknesses,
            marketing_channels=channels,
            quality_scores=quality_scores,
            best_practices=best_practices,
            estimated_budget=self._estimate_budget(competitor),
            market_position=0  # 後で計算
        )
    
    def _evaluate_quality_scores(self, competitor: Dict[str, Any]) -> Dict[QualityMetric, float]:
        """品質スコアを評価（10点満点）"""
        
        # 実際は画像認識、テキスト分析、UX評価などを実施
        # ここではデモ用の仮想スコア
        
        base_scores = {
            "Notion": {
                QualityMetric.DESIGN: 9.0,
                QualityMetric.MESSAGING: 8.5,
                QualityMetric.TARGETING: 8.0,
                QualityMetric.ENGAGEMENT: 8.5,
                QualityMetric.CONVERSION: 7.5,
                QualityMetric.BRAND_CONSISTENCY: 9.0,
                QualityMetric.INNOVATION: 9.5,
                QualityMetric.USER_EXPERIENCE: 9.0
            },
            "Asana": {
                QualityMetric.DESIGN: 8.5,
                QualityMetric.MESSAGING: 9.0,
                QualityMetric.TARGETING: 9.0,
                QualityMetric.ENGAGEMENT: 7.5,
                QualityMetric.CONVERSION: 8.0,
                QualityMetric.BRAND_CONSISTENCY: 8.5,
                QualityMetric.INNOVATION: 7.5,
                QualityMetric.USER_EXPERIENCE: 8.5
            },
            "Feedly": {
                QualityMetric.DESIGN: 8.0,
                QualityMetric.MESSAGING: 7.5,
                QualityMetric.TARGETING: 8.5,
                QualityMetric.ENGAGEMENT: 8.0,
                QualityMetric.CONVERSION: 7.0,
                QualityMetric.BRAND_CONSISTENCY: 8.0,
                QualityMetric.INNOVATION: 7.0,
                QualityMetric.USER_EXPERIENCE: 8.0
            }
        }
        
        # デフォルトスコア
        default = {metric: 7.0 for metric in QualityMetric}
        
        return base_scores.get(competitor['name'], default)
    
    def _analyze_marketing_channels(self, competitor: Dict[str, Any]) -> List[str]:
        """マーケティングチャネル分析"""
        
        # 実際はSimilarWeb API、広告ライブラリなどを使用
        channels_db = {
            "Notion": ["コンテンツマーケティング", "YouTube", "Twitter", "ProductHunt", "SEO"],
            "Asana": ["Google Ads", "LinkedIn", "ウェビナー", "パートナーシップ", "イベント"],
            "Feedly": ["ブログ", "Twitter", "メールマーケティング", "アフィリエイト", "Chrome拡張"]
        }
        
        return channels_db.get(competitor['name'], ["Web", "SNS", "広告"])
    
    def _swot_analysis(self, competitor: Dict[str, Any], 
                      quality_scores: Dict[QualityMetric, float]) -> Tuple[List[Dict], List[Dict]]:
        """SWOT分析"""
        
        strengths = []
        weaknesses = []
        
        # 品質スコアから強み・弱みを抽出
        avg_score = sum(quality_scores.values()) / len(quality_scores)
        
        for metric, score in quality_scores.items():
            if score >= avg_score + 1.0:
                strengths.append({
                    "area": metric.value,
                    "score": score,
                    "impact": "高" if score >= 9.0 else "中"
                })
            elif score <= avg_score - 1.0:
                weaknesses.append({
                    "area": metric.value,
                    "score": score,
                    "opportunity": "改善の余地あり"
                })
        
        return strengths, weaknesses
    
    def _extract_best_practices(self, competitor: Dict[str, Any], 
                              quality_scores: Dict[QualityMetric, float]) -> List[str]:
        """ベストプラクティス抽出"""
        
        practices = []
        
        # 高スコアの項目からベストプラクティスを抽出
        for metric, score in quality_scores.items():
            if score >= 8.5:
                if metric == QualityMetric.DESIGN:
                    practices.append("ミニマルで直感的なUIデザイン")
                elif metric == QualityMetric.MESSAGING:
                    practices.append("価値提案の明確な言語化")
                elif metric == QualityMetric.TARGETING:
                    practices.append("ペルソナ別のメッセージング最適化")
                elif metric == QualityMetric.INNOVATION:
                    practices.append("AI/自動化機能の積極的活用")
        
        return practices
    
    def _estimate_budget(self, competitor: Dict[str, Any]) -> str:
        """マーケティング予算推定"""
        
        # 企業規模と市場シェアから推定
        budget_map = {
            "Notion": "年間5000万円以上",
            "Asana": "年間1億円以上",
            "Feedly": "年間2000万円以上"
        }
        
        return budget_map.get(competitor['name'], "年間1000万円以上")
    
    def _calculate_market_positions(self, competitors: List[CompetitorAnalysis]) -> List[CompetitorAnalysis]:
        """市場ポジション計算"""
        
        # 総合スコアで順位付け
        for comp in competitors:
            comp.total_score = sum(comp.quality_scores.values()) / len(comp.quality_scores)
        
        sorted_comps = sorted(competitors, key=lambda x: x.total_score, reverse=True)
        
        for i, comp in enumerate(sorted_comps):
            comp.market_position = i + 1
        
        return sorted_comps
    
    def create_quality_benchmarks(self, product_info: Dict[str, Any], 
                                competitors: List[CompetitorAnalysis]) -> List[QualityBenchmark]:
        """品質ベンチマーク策定"""
        
        print("\n📊 品質ベンチマークを策定中...")
        
        benchmarks = []
        category = product_info.get('category', 'その他')
        industry_avg = self.industry_standards.get(category, {})
        
        for metric in QualityMetric:
            # 競合の最高スコアを取得
            competitor_scores = [c.quality_scores.get(metric, 0) for c in competitors]
            top_performer = max(competitor_scores) if competitor_scores else 7.0
            
            # 業界平均
            industry_average = industry_avg.get(metric, 7.0)
            
            # 目標設定（トップ企業を10%上回る）
            our_target = min(top_performer * 1.1, 10.0)
            
            # ギャップ分析
            gap = our_target - industry_average
            if gap > 2:
                gap_analysis = "大幅な改善が必要"
            elif gap > 1:
                gap_analysis = "改善の余地あり"
            else:
                gap_analysis = "業界水準を維持"
            
            # 改善戦術
            improvement_tactics = self._generate_improvement_tactics(metric, our_target)
            
            benchmarks.append(QualityBenchmark(
                metric=metric,
                industry_average=industry_average,
                top_performer=top_performer,
                our_target=our_target,
                gap_analysis=gap_analysis,
                improvement_tactics=improvement_tactics
            ))
        
        return benchmarks
    
    def _generate_improvement_tactics(self, metric: QualityMetric, target: float) -> List[str]:
        """改善戦術を生成"""
        
        tactics_db = {
            QualityMetric.DESIGN: [
                "プロのUIデザイナーによるリデザイン",
                "A/Bテストによるデザイン最適化",
                "モバイルファーストアプローチ",
                "アクセシビリティ改善"
            ],
            QualityMetric.MESSAGING: [
                "コピーライターによるメッセージ改善",
                "顧客インタビューに基づく言語最適化",
                "価値提案の明確化ワークショップ",
                "競合との差別化ポイント強調"
            ],
            QualityMetric.TARGETING: [
                "詳細なペルソナ分析",
                "行動データに基づくセグメンテーション",
                "リターゲティング戦略の精緻化",
                "ルックアライクオーディエンス活用"
            ],
            QualityMetric.ENGAGEMENT: [
                "インタラクティブコンテンツ導入",
                "ソーシャルメディア戦略強化",
                "コミュニティビルディング",
                "インフルエンサーコラボ"
            ],
            QualityMetric.CONVERSION: [
                "ランディングページ最適化",
                "CRO（コンバージョン率最適化）施策",
                "フリートライアル期間延長",
                "オンボーディング改善"
            ]
        }
        
        base_tactics = tactics_db.get(metric, ["品質改善施策を実施"])
        
        # ターゲットスコアに応じて優先順位付け
        if target >= 9.0:
            return base_tactics[:4]  # 全施策実施
        elif target >= 8.0:
            return base_tactics[:3]  # 主要施策
        else:
            return base_tactics[:2]  # 基本施策
    
    def generate_strategic_campaigns(self, product_info: Dict[str, Any],
                                   benchmarks: List[QualityBenchmark],
                                   competitors: List[CompetitorAnalysis]) -> List[StrategicCampaign]:
        """戦略的キャンペーン生成"""
        
        print("\n🎯 ベンチマーク達成のための戦略的キャンペーンを設計中...")
        
        campaigns = []
        
        # 1. ブランド認知キャンペーン
        brand_campaign = self._create_brand_awareness_campaign(product_info, benchmarks, competitors)
        campaigns.append(brand_campaign)
        
        # 2. 差別化キャンペーン
        differentiation_campaign = self._create_differentiation_campaign(product_info, benchmarks, competitors)
        campaigns.append(differentiation_campaign)
        
        # 3. コンバージョン最適化キャンペーン
        conversion_campaign = self._create_conversion_campaign(product_info, benchmarks)
        campaigns.append(conversion_campaign)
        
        # 4. 季節性キャンペーン
        seasonal_campaign = self._create_seasonal_campaign(product_info, benchmarks)
        campaigns.append(seasonal_campaign)
        
        return campaigns
    
    def _create_brand_awareness_campaign(self, product_info: Dict[str, Any],
                                       benchmarks: List[QualityBenchmark],
                                       competitors: List[CompetitorAnalysis]) -> StrategicCampaign:
        """ブランド認知キャンペーン作成"""
        
        # 品質目標設定
        quality_targets = {}
        for benchmark in benchmarks:
            if benchmark.metric in [QualityMetric.DESIGN, QualityMetric.MESSAGING, QualityMetric.BRAND_CONSISTENCY]:
                quality_targets[benchmark.metric] = benchmark.our_target
        
        # クリエイティブコンセプト
        creative_concepts = [
            {
                "type": "ビジュアル広告",
                "concept": f"{product_info['name']}で変わる、新しい{product_info['category']}体験",
                "channels": ["Instagram", "YouTube", "Twitter"],
                "visual_style": "モダン・ミニマル・プロフェッショナル"
            },
            {
                "type": "動画広告",
                "concept": "実際のユーザーストーリー",
                "channels": ["YouTube", "TikTok"],
                "duration": "15-30秒",
                "message": product_info.get('unique_value', 'ユニークな価値')
            }
        ]
        
        # 競合のベストプラクティスを参考に戦術設定
        tactics = ["インフルエンサーマーケティング", "コンテンツマーケティング強化"]
        for comp in competitors[:2]:  # Top 2競合
            tactics.extend(comp.best_practices[:1])
        
        return StrategicCampaign(
            campaign_type="ブランド認知向上",
            quality_targets=quality_targets,
            tactics=tactics,
            creative_concepts=creative_concepts,
            budget_allocation={
                "広告": 0.4,
                "コンテンツ": 0.3,
                "インフルエンサー": 0.2,
                "PR": 0.1
            },
            expected_performance={
                "reach": "目標到達: 10万人/月",
                "impressions": "インプレッション: 100万回/月",
                "brand_lift": "ブランド認知度: +25%"
            },
            timeline={
                "準備期間": "2週間",
                "実行期間": "3ヶ月",
                "効果測定": "継続的"
            }
        )
    
    def _create_differentiation_campaign(self, product_info: Dict[str, Any],
                                       benchmarks: List[QualityBenchmark],
                                       competitors: List[CompetitorAnalysis]) -> StrategicCampaign:
        """差別化キャンペーン作成"""
        
        # 差別化ポイントを特定
        unique_features = self._identify_differentiation_points(product_info, competitors)
        
        quality_targets = {}
        for benchmark in benchmarks:
            if benchmark.metric in [QualityMetric.INNOVATION, QualityMetric.USER_EXPERIENCE]:
                quality_targets[benchmark.metric] = benchmark.our_target
        
        creative_concepts = [
            {
                "type": "比較広告",
                "concept": f"なぜ{product_info['name']}が選ばれるのか",
                "channels": ["Google Ads", "Facebook"],
                "comparison_points": unique_features
            },
            {
                "type": "デモ動画",
                "concept": "独自機能の実演",
                "channels": ["YouTube", "LinkedIn"],
                "focus": product_info.get('unique_value', '')
            }
        ]
        
        return StrategicCampaign(
            campaign_type="競合差別化",
            quality_targets=quality_targets,
            tactics=[
                "機能比較コンテンツ",
                "ユーザー事例紹介",
                "独自価値の可視化",
                "専門家による推薦"
            ],
            creative_concepts=creative_concepts,
            budget_allocation={
                "検索広告": 0.35,
                "SNS広告": 0.25,
                "コンテンツ": 0.25,
                "PR": 0.15
            },
            expected_performance={
                "consideration_rate": "検討率: +40%",
                "preference": "ブランド選好度: +30%",
                "share_of_voice": "シェアオブボイス: 15%"
            },
            timeline={
                "準備期間": "3週間",
                "実行期間": "2ヶ月",
                "最適化": "週次"
            }
        )
    
    def _create_conversion_campaign(self, product_info: Dict[str, Any],
                                  benchmarks: List[QualityBenchmark]) -> StrategicCampaign:
        """コンバージョン最適化キャンペーン"""
        
        quality_targets = {}
        for benchmark in benchmarks:
            if benchmark.metric in [QualityMetric.CONVERSION, QualityMetric.TARGETING]:
                quality_targets[benchmark.metric] = benchmark.our_target
        
        creative_concepts = [
            {
                "type": "リターゲティング広告",
                "concept": "期間限定オファー",
                "channels": ["Google Display", "Facebook"],
                "offer": "初月無料トライアル"
            },
            {
                "type": "メールシーケンス",
                "concept": "段階的な価値訴求",
                "sequence": ["機能紹介", "ユーザー事例", "限定オファー"]
            }
        ]
        
        return StrategicCampaign(
            campaign_type="コンバージョン最適化",
            quality_targets=quality_targets,
            tactics=[
                "ランディングページA/Bテスト",
                "CROファネル最適化",
                "リターゲティング強化",
                "アップセル/クロスセル"
            ],
            creative_concepts=creative_concepts,
            budget_allocation={
                "リターゲティング": 0.4,
                "検索広告": 0.3,
                "メール": 0.2,
                "最適化ツール": 0.1
            },
            expected_performance={
                "conversion_rate": "コンバージョン率: 5%→8%",
                "cac": "顧客獲得コスト: -30%",
                "ltv": "顧客生涯価値: +50%"
            },
            timeline={
                "準備期間": "1週間",
                "実行期間": "継続的",
                "最適化サイクル": "2週間"
            }
        )
    
    def _create_seasonal_campaign(self, product_info: Dict[str, Any],
                                benchmarks: List[QualityBenchmark]) -> StrategicCampaign:
        """季節性キャンペーン"""
        
        # 現在の月に応じた季節性キャンペーン
        current_month = datetime.now().month
        
        if current_month in [3, 4]:
            campaign_theme = "新年度スタートダッシュ"
            target_message = "新しい環境で効率アップ"
        elif current_month in [6, 7]:
            campaign_theme = "夏の生産性向上"
            target_message = "暑い夏も快適に作業"
        elif current_month in [11, 12]:
            campaign_theme = "年末総決算"
            target_message = "来年への準備を今から"
        else:
            campaign_theme = "期間限定キャンペーン"
            target_message = "今がチャンス"
        
        quality_targets = {
            benchmark.metric: benchmark.our_target 
            for benchmark in benchmarks 
            if benchmark.metric in [QualityMetric.MESSAGING, QualityMetric.ENGAGEMENT]
        }
        
        return StrategicCampaign(
            campaign_type=f"季節性キャンペーン: {campaign_theme}",
            quality_targets=quality_targets,
            tactics=[
                "季節限定オファー",
                "タイムリーなメッセージング",
                "イベント連動施策",
                "期間限定コンテンツ"
            ],
            creative_concepts=[
                {
                    "type": "季節広告",
                    "concept": campaign_theme,
                    "channels": ["SNS", "メール"],
                    "message": target_message
                }
            ],
            budget_allocation={
                "SNS広告": 0.5,
                "メール": 0.3,
                "コンテンツ": 0.2
            },
            expected_performance={
                "seasonal_lift": "期間中売上: +35%",
                "engagement": "エンゲージメント率: +50%"
            },
            timeline={
                "準備期間": "2週間",
                "実行期間": "1ヶ月",
                "フォローアップ": "2週間"
            }
        )
    
    def _identify_differentiation_points(self, product_info: Dict[str, Any],
                                       competitors: List[CompetitorAnalysis]) -> List[str]:
        """差別化ポイントを特定"""
        
        # 競合の弱みから機会を発見
        opportunities = []
        for comp in competitors:
            for weakness in comp.weaknesses:
                if weakness['score'] < 7.0:
                    opportunities.append(f"{weakness['area']}での優位性")
        
        # 独自価値の強調
        if product_info.get('unique_value'):
            opportunities.append(product_info['unique_value'])
        
        return opportunities[:3]  # Top 3
    
    def generate_comprehensive_report(self, product_info: Dict[str, Any],
                                    competitors: List[CompetitorAnalysis],
                                    benchmarks: List[QualityBenchmark],
                                    campaigns: List[StrategicCampaign]) -> Dict[str, Any]:
        """包括的レポート生成"""
        
        report = {
            "executive_summary": self._create_executive_summary(product_info, competitors, benchmarks),
            "competitive_landscape": {
                "competitors": [self._summarize_competitor(c) for c in competitors],
                "market_insights": self._extract_market_insights(competitors),
                "opportunity_areas": self._identify_opportunities(competitors, benchmarks)
            },
            "quality_benchmarks": {
                "targets": {b.metric.value: b.our_target for b in benchmarks},
                "improvement_roadmap": self._create_improvement_roadmap(benchmarks),
                "investment_priorities": self._prioritize_investments(benchmarks)
            },
            "campaign_strategy": {
                "campaigns": [self._summarize_campaign(c) for c in campaigns],
                "timeline": self._create_master_timeline(campaigns),
                "budget_allocation": self._calculate_total_budget(campaigns),
                "expected_roi": self._calculate_expected_roi(campaigns)
            },
            "action_plan": self._create_action_plan(product_info, benchmarks, campaigns),
            "success_metrics": self._define_success_metrics(benchmarks, campaigns)
        }
        
        # レポート保存
        self._save_report(product_info['name'], report)
        
        return report
    
    def _create_executive_summary(self, product_info: Dict[str, Any],
                                competitors: List[CompetitorAnalysis],
                                benchmarks: List[QualityBenchmark]) -> str:
        """エグゼクティブサマリー作成"""
        
        top_competitor = competitors[0] if competitors else None
        avg_target = sum(b.our_target for b in benchmarks) / len(benchmarks) if benchmarks else 8.0
        
        summary = f"""
【{product_info['name']} 競合分析・品質ベンチマークレポート】

1. 市場状況
- 主要競合: {', '.join([c.name for c in competitors[:3]])}
- 市場リーダー: {top_competitor.name if top_competitor else 'N/A'}（品質スコア: {top_competitor.total_score:.1f}/10）
- 業界平均品質: {sum(b.industry_average for b in benchmarks) / len(benchmarks):.1f}/10

2. 品質目標
- 総合目標スコア: {avg_target:.1f}/10（業界トップを10%上回る）
- 最重要改善領域: {', '.join([b.metric.value for b in benchmarks if b.gap_analysis == '大幅な改善が必要'][:3])}

3. 戦略的推奨事項
- 短期（1-3ヶ月）: ブランド認知向上とメッセージング最適化
- 中期（3-6ヶ月）: 差別化強化とコンバージョン最適化
- 長期（6-12ヶ月）: 市場リーダーポジション確立

4. 投資優先順位
- 第1優先: クリエイティブ品質向上（デザイン・メッセージング）
- 第2優先: ターゲティング精度向上
- 第3優先: エンゲージメント施策強化
"""
        
        return summary
    
    def _summarize_competitor(self, competitor: CompetitorAnalysis) -> Dict[str, Any]:
        """競合サマリー"""
        return {
            "name": competitor.name,
            "market_position": competitor.market_position,
            "overall_quality": round(competitor.total_score, 1),
            "key_strengths": [s['area'] for s in competitor.strengths[:3]],
            "main_channels": competitor.marketing_channels[:3],
            "estimated_budget": competitor.estimated_budget
        }
    
    def _extract_market_insights(self, competitors: List[CompetitorAnalysis]) -> List[str]:
        """市場インサイト抽出"""
        insights = []
        
        # 共通の強みを発見
        all_strengths = []
        for comp in competitors:
            all_strengths.extend([s['area'] for s in comp.strengths])
        
        # 頻出する強みは業界標準
        from collections import Counter
        strength_counts = Counter(all_strengths)
        for strength, count in strength_counts.most_common(3):
            if count >= 2:
                insights.append(f"{strength}は業界標準として確立")
        
        # 共通の弱み＝市場機会
        all_weaknesses = []
        for comp in competitors:
            all_weaknesses.extend([w['area'] for w in comp.weaknesses])
        
        weakness_counts = Counter(all_weaknesses)
        for weakness, count in weakness_counts.most_common(2):
            if count >= 2:
                insights.append(f"{weakness}は業界全体の改善機会")
        
        return insights
    
    def _identify_opportunities(self, competitors: List[CompetitorAnalysis],
                              benchmarks: List[QualityBenchmark]) -> List[Dict[str, str]]:
        """機会領域特定"""
        opportunities = []
        
        # 競合の弱み×自社の目標
        for benchmark in benchmarks:
            if benchmark.our_target >= 8.0:
                weak_competitors = [
                    c.name for c in competitors 
                    if c.quality_scores.get(benchmark.metric, 0) < 7.0
                ]
                if weak_competitors:
                    opportunities.append({
                        "area": benchmark.metric.value,
                        "opportunity": f"{', '.join(weak_competitors)}に対する優位性確立",
                        "priority": "高"
                    })
        
        return opportunities[:5]  # Top 5
    
    def _create_improvement_roadmap(self, benchmarks: List[QualityBenchmark]) -> List[Dict[str, Any]]:
        """改善ロードマップ作成"""
        roadmap = []
        
        # 優先順位付け（ギャップが大きい順）
        sorted_benchmarks = sorted(
            benchmarks, 
            key=lambda b: b.our_target - b.industry_average, 
            reverse=True
        )
        
        for i, benchmark in enumerate(sorted_benchmarks[:5]):
            phase = "Phase 1" if i < 2 else "Phase 2" if i < 4 else "Phase 3"
            roadmap.append({
                "phase": phase,
                "metric": benchmark.metric.value,
                "current": benchmark.industry_average,
                "target": benchmark.our_target,
                "tactics": benchmark.improvement_tactics[:2],
                "timeline": f"{(i+1)*4}週間"
            })
        
        return roadmap
    
    def _prioritize_investments(self, benchmarks: List[QualityBenchmark]) -> List[Dict[str, Any]]:
        """投資優先順位付け"""
        priorities = []
        
        for benchmark in benchmarks:
            gap = benchmark.our_target - benchmark.industry_average
            roi_potential = "高" if gap > 2 else "中" if gap > 1 else "低"
            
            if roi_potential in ["高", "中"]:
                priorities.append({
                    "area": benchmark.metric.value,
                    "investment_level": f"{int(gap * 20)}%増",
                    "expected_roi": roi_potential,
                    "recommended_budget": f"{int(gap * 100)}万円/月"
                })
        
        return sorted(priorities, key=lambda p: p['expected_roi'], reverse=True)
    
    def _summarize_campaign(self, campaign: StrategicCampaign) -> Dict[str, Any]:
        """キャンペーンサマリー"""
        return {
            "type": campaign.campaign_type,
            "main_tactics": campaign.tactics[:3],
            "channels": list(campaign.budget_allocation.keys())[:3],
            "duration": campaign.timeline.get('実行期間', 'N/A'),
            "key_metrics": list(campaign.expected_performance.keys())[:3]
        }
    
    def _create_master_timeline(self, campaigns: List[StrategicCampaign]) -> Dict[str, List[str]]:
        """マスタータイムライン作成"""
        timeline = {
            "Month 1": ["ブランド認知キャンペーン準備", "ベンチマーク測定開始"],
            "Month 2": ["ブランド認知キャンペーン開始", "差別化キャンペーン準備"],
            "Month 3": ["差別化キャンペーン開始", "初期成果測定"],
            "Month 4": ["コンバージョン最適化開始", "季節キャンペーン準備"],
            "Month 5": ["全キャンペーン最適化", "ROI分析"],
            "Month 6": ["成果評価", "次期戦略立案"]
        }
        
        return timeline
    
    def _calculate_total_budget(self, campaigns: List[StrategicCampaign]) -> Dict[str, float]:
        """総予算計算"""
        total_budget = {}
        
        for campaign in campaigns:
            for channel, allocation in campaign.budget_allocation.items():
                if channel in total_budget:
                    total_budget[channel] += allocation
                else:
                    total_budget[channel] = allocation
        
        # 正規化
        total = sum(total_budget.values())
        return {k: round(v/total * 100, 1) for k, v in total_budget.items()}
    
    def _calculate_expected_roi(self, campaigns: List[StrategicCampaign]) -> Dict[str, str]:
        """期待ROI計算"""
        return {
            "3ヶ月後": "ROI 150%（1.5倍）",
            "6ヶ月後": "ROI 250%（2.5倍）",
            "12ヶ月後": "ROI 400%（4倍）",
            "ブレークイーブン": "2.5ヶ月"
        }
    
    def _create_action_plan(self, product_info: Dict[str, Any],
                          benchmarks: List[QualityBenchmark],
                          campaigns: List[StrategicCampaign]) -> List[Dict[str, Any]]:
        """アクションプラン作成"""
        
        action_plan = [
            {
                "week": "Week 1-2",
                "actions": [
                    "クリエイティブチーム編成",
                    "ベンチマーク詳細測定",
                    "競合広告素材収集"
                ],
                "deliverables": ["品質基準書", "クリエイティブブリーフ"],
                "owner": "マーケティングチーム"
            },
            {
                "week": "Week 3-4",
                "actions": [
                    "初期クリエイティブ制作",
                    "A/Bテスト設計",
                    "メディアプランニング"
                ],
                "deliverables": ["広告素材v1", "テスト計画書"],
                "owner": "クリエイティブチーム"
            },
            {
                "week": "Week 5-8",
                "actions": [
                    "キャンペーン実行",
                    "日次モニタリング",
                    "最適化実施"
                ],
                "deliverables": ["週次レポート", "最適化提案"],
                "owner": "メディアチーム"
            }
        ]
        
        return action_plan
    
    def _define_success_metrics(self, benchmarks: List[QualityBenchmark],
                              campaigns: List[StrategicCampaign]) -> Dict[str, Any]:
        """成功指標定義"""
        return {
            "quality_metrics": {
                b.metric.value: {
                    "target": b.our_target,
                    "measurement": "月次ブランド調査"
                }
                for b in benchmarks[:5]
            },
            "business_metrics": {
                "brand_awareness": {"target": "+50%", "baseline": "現在の認知度"},
                "market_share": {"target": "+5%", "timeline": "12ヶ月"},
                "customer_acquisition": {"target": "月間1000人", "cac_target": "5000円以下"},
                "revenue_growth": {"target": "+200%", "timeline": "12ヶ月"}
            },
            "campaign_metrics": {
                "reach": "月間10万人",
                "engagement_rate": "5%以上",
                "conversion_rate": "3%以上",
                "roi": "250%以上"
            }
        }
    
    def _save_report(self, product_name: str, report: Dict[str, Any]):
        """レポート保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{product_name}_competitive_intelligence_{timestamp}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        # Markdownサマリーも生成
        md_filename = f"{product_name}_competitive_summary_{timestamp}.md"
        md_filepath = os.path.join(self.results_dir, md_filename)
        
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(self._generate_markdown_summary(report))
        
        print(f"\n📊 レポートを保存しました:")
        print(f"  - 詳細: {filepath}")
        print(f"  - サマリー: {md_filepath}")
    
    def _generate_markdown_summary(self, report: Dict[str, Any]) -> str:
        """Markdownサマリー生成"""
        md = f"""# 競合インテリジェンス＆品質ベンチマークレポート

{report['executive_summary']}

## 品質ベンチマーク目標

| 指標 | 目標スコア |
|------|-----------|
"""
        
        for metric, target in report['quality_benchmarks']['targets'].items():
            md += f"| {metric} | {target:.1f}/10 |\n"
        
        md += "\n## 推奨キャンペーン\n\n"
        
        for campaign in report['campaign_strategy']['campaigns']:
            md += f"### {campaign['type']}\n"
            md += f"- 主要施策: {', '.join(campaign['main_tactics'])}\n"
            md += f"- チャネル: {', '.join(campaign['channels'])}\n"
            md += f"- 期間: {campaign['duration']}\n\n"
        
        return md


def main():
    """デモ実行"""
    
    ci = CompetitiveIntelligence()
    
    # サンプル製品
    product_info = {
        "name": "TaskMaster Pro",
        "category": "タスク管理",
        "target": "個人・中小企業",
        "price": "月額980円",
        "unique_value": "AI自動スケジューリング",
        "users": 100
    }
    
    print("🎯 競合インテリジェンス分析を開始します...\n")
    
    # 1. 競合分析
    competitors = ci.analyze_competitors(product_info)
    
    # 2. ベンチマーク策定
    benchmarks = ci.create_quality_benchmarks(product_info, competitors)
    
    # 3. 戦略的キャンペーン生成
    campaigns = ci.generate_strategic_campaigns(product_info, benchmarks, competitors)
    
    # 4. 包括的レポート作成
    report = ci.generate_comprehensive_report(product_info, competitors, benchmarks, campaigns)
    
    print("\n✅ 分析完了！")
    print("\n" + "="*60)
    print(report['executive_summary'])
    print("="*60)


if __name__ == "__main__":
    main()