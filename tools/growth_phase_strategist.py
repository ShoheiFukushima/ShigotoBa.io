#!/usr/bin/env python3
"""
成長フェーズ別戦略エンジン
知名度ゼロから市場リーダーまでの成長戦略を管理
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class GrowthPhase(Enum):
    """成長フェーズ"""
    STEALTH = "ステルス期"
    LAUNCH = "ローンチ期"
    EARLY_GROWTH = "初期成長期"
    GROWTH = "成長期"
    EXPANSION = "拡大期"
    MATURITY = "成熟期"
    RENEWAL = "再成長期"

class MetricType(Enum):
    """KPI種別"""
    AWARENESS = "認知度"
    ACQUISITION = "新規獲得"
    ACTIVATION = "アクティベーション"
    RETENTION = "継続率"
    REVENUE = "収益"
    REFERRAL = "紹介"

@dataclass
class PhaseStrategy:
    """フェーズ別戦略"""
    phase: GrowthPhase
    duration_weeks: int
    primary_goals: List[str]
    key_metrics: List[MetricType]
    marketing_focus: List[str]
    budget_allocation: Dict[str, float]
    expected_milestones: List[str]
    risk_factors: List[str]

@dataclass
class GrowthRoadmap:
    """成長ロードマップ"""
    product_name: str
    total_duration_months: int
    phases: List[PhaseStrategy]
    quarterly_reviews: List[Dict[str, Any]]
    success_criteria: Dict[str, Any]

class GrowthPhaseStrategist:
    """成長フェーズに応じた戦略を策定"""
    
    def __init__(self):
        self.phase_templates = self._init_phase_templates()
        self.channel_effectiveness = self._init_channel_effectiveness()
        
    def _init_phase_templates(self) -> Dict[GrowthPhase, Dict[str, Any]]:
        """フェーズ別のテンプレート戦略"""
        return {
            GrowthPhase.STEALTH: {
                "duration_weeks": 4,
                "description": "製品開発とテストマーケティング",
                "user_target": 10,
                "primary_goals": [
                    "コアバリューの検証",
                    "初期ユーザーフィードバック収集",
                    "プロダクトマーケットフィット探索"
                ],
                "channels": {
                    "closed_beta": 0.4,
                    "direct_outreach": 0.3,
                    "community": 0.2,
                    "content": 0.1
                },
                "content_strategy": [
                    "ブログ記事（週1本）",
                    "開発者ブログ",
                    "限定的なSNS活動"
                ]
            },
            GrowthPhase.LAUNCH: {
                "duration_weeks": 8,
                "description": "正式リリースと初期ユーザー獲得",
                "user_target": 1000,
                "primary_goals": [
                    "製品認知度の確立",
                    "初期ユーザーベース構築",
                    "フィードバックループ確立"
                ],
                "channels": {
                    "pr": 0.3,
                    "content_marketing": 0.25,
                    "social_media": 0.25,
                    "paid_ads": 0.2
                },
                "content_strategy": [
                    "プレスリリース",
                    "ローンチ記事（主要メディア）",
                    "製品デモ動画",
                    "SNS集中投稿"
                ]
            },
            GrowthPhase.EARLY_GROWTH: {
                "duration_weeks": 12,
                "description": "ユーザーベース拡大と最適化",
                "user_target": 10000,
                "primary_goals": [
                    "継続的なユーザー増加",
                    "収益化モデルの確立",
                    "プロダクト改善サイクル"
                ],
                "channels": {
                    "content_marketing": 0.3,
                    "paid_ads": 0.25,
                    "seo": 0.2,
                    "email": 0.15,
                    "referral": 0.1
                },
                "content_strategy": [
                    "SEO最適化コンテンツ（週2-3本）",
                    "ユーザー事例紹介",
                    "ウェビナー開催",
                    "メールニュースレター"
                ]
            },
            GrowthPhase.GROWTH: {
                "duration_weeks": 24,
                "description": "スケール拡大と市場浸透",
                "user_target": 100000,
                "primary_goals": [
                    "市場シェア拡大",
                    "ブランド確立",
                    "収益最大化"
                ],
                "channels": {
                    "paid_ads": 0.35,
                    "content_marketing": 0.2,
                    "partnerships": 0.15,
                    "events": 0.15,
                    "influencer": 0.15
                },
                "content_strategy": [
                    "大規模コンテンツ制作",
                    "インフルエンサーコラボ",
                    "業界イベント参加",
                    "TV/ラジオ広告検討"
                ]
            },
            GrowthPhase.EXPANSION: {
                "duration_weeks": 36,
                "description": "新市場開拓と多角化",
                "user_target": 500000,
                "primary_goals": [
                    "新セグメント開拓",
                    "国際展開",
                    "プロダクトライン拡充"
                ],
                "channels": {
                    "partnerships": 0.25,
                    "enterprise_sales": 0.2,
                    "paid_ads": 0.2,
                    "events": 0.2,
                    "content": 0.15
                },
                "content_strategy": [
                    "多言語コンテンツ",
                    "業界別ソリューション",
                    "大型カンファレンス登壇",
                    "戦略的提携発表"
                ]
            }
        }
    
    def _init_channel_effectiveness(self) -> Dict[str, Dict[GrowthPhase, float]]:
        """チャネル別・フェーズ別の効果性（0-1.0）"""
        return {
            "content_marketing": {
                GrowthPhase.STEALTH: 0.3,
                GrowthPhase.LAUNCH: 0.6,
                GrowthPhase.EARLY_GROWTH: 0.8,
                GrowthPhase.GROWTH: 0.9,
                GrowthPhase.EXPANSION: 0.7
            },
            "paid_ads": {
                GrowthPhase.STEALTH: 0.1,
                GrowthPhase.LAUNCH: 0.5,
                GrowthPhase.EARLY_GROWTH: 0.7,
                GrowthPhase.GROWTH: 0.9,
                GrowthPhase.EXPANSION: 0.8
            },
            "social_media": {
                GrowthPhase.STEALTH: 0.4,
                GrowthPhase.LAUNCH: 0.8,
                GrowthPhase.EARLY_GROWTH: 0.7,
                GrowthPhase.GROWTH: 0.6,
                GrowthPhase.EXPANSION: 0.5
            },
            "pr": {
                GrowthPhase.STEALTH: 0.2,
                GrowthPhase.LAUNCH: 0.9,
                GrowthPhase.EARLY_GROWTH: 0.6,
                GrowthPhase.GROWTH: 0.5,
                GrowthPhase.EXPANSION: 0.7
            }
        }
    
    def create_growth_roadmap(self, product_info: Dict[str, Any], 
                            starting_phase: GrowthPhase = GrowthPhase.STEALTH,
                            target_duration_months: int = 18) -> GrowthRoadmap:
        """成長ロードマップを作成"""
        
        phases = []
        current_phase = starting_phase
        total_weeks = 0
        
        # フェーズ順序
        phase_order = [
            GrowthPhase.STEALTH,
            GrowthPhase.LAUNCH,
            GrowthPhase.EARLY_GROWTH,
            GrowthPhase.GROWTH,
            GrowthPhase.EXPANSION
        ]
        
        # 開始フェーズのインデックスを取得
        start_idx = phase_order.index(starting_phase)
        
        # 各フェーズの戦略を生成
        for phase in phase_order[start_idx:]:
            if total_weeks >= target_duration_months * 4:
                break
                
            strategy = self._create_phase_strategy(phase, product_info)
            phases.append(strategy)
            total_weeks += strategy.duration_weeks
        
        # 四半期レビュー計画
        quarterly_reviews = self._create_quarterly_reviews(phases, product_info)
        
        # 成功基準
        success_criteria = self._define_success_criteria(phases, product_info)
        
        return GrowthRoadmap(
            product_name=product_info['name'],
            total_duration_months=total_weeks // 4,
            phases=phases,
            quarterly_reviews=quarterly_reviews,
            success_criteria=success_criteria
        )
    
    def _create_phase_strategy(self, phase: GrowthPhase, 
                             product_info: Dict[str, Any]) -> PhaseStrategy:
        """特定フェーズの戦略を作成"""
        
        template = self.phase_templates[phase]
        
        # フェーズ別のKPI
        key_metrics = self._determine_key_metrics(phase)
        
        # リスク要因
        risk_factors = self._identify_risks(phase, product_info)
        
        # マイルストーン
        milestones = self._generate_milestones(phase, template['user_target'])
        
        return PhaseStrategy(
            phase=phase,
            duration_weeks=template['duration_weeks'],
            primary_goals=template['primary_goals'],
            key_metrics=key_metrics,
            marketing_focus=template['content_strategy'],
            budget_allocation=template['channels'],
            expected_milestones=milestones,
            risk_factors=risk_factors
        )
    
    def _determine_key_metrics(self, phase: GrowthPhase) -> List[MetricType]:
        """フェーズに応じた重要指標を決定"""
        
        metric_priority = {
            GrowthPhase.STEALTH: [
                MetricType.ACTIVATION,
                MetricType.RETENTION
            ],
            GrowthPhase.LAUNCH: [
                MetricType.AWARENESS,
                MetricType.ACQUISITION,
                MetricType.ACTIVATION
            ],
            GrowthPhase.EARLY_GROWTH: [
                MetricType.ACQUISITION,
                MetricType.RETENTION,
                MetricType.REVENUE
            ],
            GrowthPhase.GROWTH: [
                MetricType.REVENUE,
                MetricType.RETENTION,
                MetricType.REFERRAL
            ],
            GrowthPhase.EXPANSION: [
                MetricType.REVENUE,
                MetricType.REFERRAL,
                MetricType.ACQUISITION
            ]
        }
        
        return metric_priority.get(phase, [MetricType.ACQUISITION])
    
    def _identify_risks(self, phase: GrowthPhase, 
                       product_info: Dict[str, Any]) -> List[str]:
        """フェーズ別のリスク要因を特定"""
        
        common_risks = {
            GrowthPhase.STEALTH: [
                "プロダクトマーケットフィット未達成",
                "初期資金枯渇",
                "競合の先行リリース"
            ],
            GrowthPhase.LAUNCH: [
                "初期バグによる評判低下",
                "PR効果の不発",
                "サーバー負荷対応"
            ],
            GrowthPhase.EARLY_GROWTH: [
                "CAC（顧客獲得コスト）の上昇",
                "競合の攻勢",
                "スケーラビリティ問題"
            ],
            GrowthPhase.GROWTH: [
                "市場飽和",
                "大手参入",
                "組織スケール課題"
            ],
            GrowthPhase.EXPANSION: [
                "新市場での文化的不適合",
                "リソース分散",
                "ブランド希薄化"
            ]
        }
        
        return common_risks.get(phase, ["予期せぬ市場変化"])
    
    def _generate_milestones(self, phase: GrowthPhase, 
                           user_target: int) -> List[str]:
        """フェーズ別のマイルストーンを生成"""
        
        milestones = []
        
        if phase == GrowthPhase.STEALTH:
            milestones = [
                "クローズドベータ開始",
                f"初期ユーザー{user_target}人獲得",
                "主要機能の検証完了"
            ]
        elif phase == GrowthPhase.LAUNCH:
            milestones = [
                "プレスリリース配信",
                f"ユーザー{user_target}人達成",
                "初月のリテンション率40%以上"
            ]
        elif phase == GrowthPhase.EARLY_GROWTH:
            milestones = [
                f"月間アクティブユーザー{user_target}人",
                "有料転換率5%達成",
                "NPS 50以上"
            ]
        elif phase == GrowthPhase.GROWTH:
            milestones = [
                f"ユーザー{user_target}人突破",
                "月間収益1000万円達成",
                "チャーンレート5%以下"
            ]
        elif phase == GrowthPhase.EXPANSION:
            milestones = [
                "新市場参入",
                f"グローバルユーザー{user_target}人",
                "年間収益10億円"
            ]
        
        return milestones
    
    def _create_quarterly_reviews(self, phases: List[PhaseStrategy], 
                                product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """四半期レビュー計画を作成"""
        
        reviews = []
        total_weeks = 0
        quarter = 1
        
        for phase in phases:
            total_weeks += phase.duration_weeks
            
            if total_weeks >= quarter * 12:  # 12週間 = 1四半期
                reviews.append({
                    "quarter": f"Q{quarter}",
                    "week": quarter * 12,
                    "phase": phase.phase.value,
                    "review_items": [
                        "KPI達成状況",
                        "予算消化率",
                        "次四半期の戦略調整",
                        "リスク評価"
                    ],
                    "decision_points": [
                        "フェーズ移行の可否",
                        "予算配分の見直し",
                        "チャネル戦略の修正"
                    ]
                })
                quarter += 1
        
        return reviews
    
    def _define_success_criteria(self, phases: List[PhaseStrategy], 
                               product_info: Dict[str, Any]) -> Dict[str, Any]:
        """成功基準を定義"""
        
        # 最終フェーズの目標を基に設定
        final_phase = phases[-1] if phases else None
        
        if not final_phase:
            return {}
        
        final_user_target = self.phase_templates[final_phase.phase]['user_target']
        
        return {
            "quantitative": {
                "total_users": final_user_target,
                "monthly_revenue": f"{final_user_target * 0.05 * 1000}円",  # 5%有料化×1000円
                "retention_rate": "40%以上",
                "nps_score": "50以上"
            },
            "qualitative": {
                "brand_recognition": "業界内での認知度確立",
                "product_quality": "主要機能の安定性",
                "team_growth": "必要人材の確保",
                "market_position": "カテゴリートップ5入り"
            },
            "timeline": f"{sum(p.duration_weeks for p in phases)}週間"
        }
    
    def generate_phase_transition_criteria(self, current_phase: GrowthPhase, 
                                         next_phase: GrowthPhase) -> Dict[str, Any]:
        """フェーズ移行の判断基準を生成"""
        
        criteria = {
            "quantitative_criteria": [],
            "qualitative_criteria": [],
            "readiness_checklist": [],
            "risk_assessment": []
        }
        
        # フェーズ別の移行基準
        if current_phase == GrowthPhase.STEALTH:
            criteria["quantitative_criteria"] = [
                "ベータユーザー50人以上",
                "週次アクティブ率60%以上",
                "主要機能の完成度90%"
            ]
            criteria["qualitative_criteria"] = [
                "コアバリューの検証完了",
                "ユーザーフィードバックの収束"
            ]
        elif current_phase == GrowthPhase.LAUNCH:
            criteria["quantitative_criteria"] = [
                "ユーザー1,000人達成",
                "Day 7 リテンション40%以上",
                "クラッシュ率1%以下"
            ]
            criteria["qualitative_criteria"] = [
                "メディア露出の成功",
                "初期ユーザーの満足度"
            ]
        
        criteria["readiness_checklist"] = [
            "次フェーズの予算確保",
            "必要人材の採用完了",
            "インフラのスケール準備",
            "マーケティング素材の準備"
        ]
        
        return criteria


def main():
    """使用例"""
    strategist = GrowthPhaseStrategist()
    
    # サンプル製品
    product_info = {
        "name": "TaskMaster Pro",
        "category": "生産性",
        "target": "個人・中小企業",
        "launch_readiness": "mvp_complete"
    }
    
    # 成長ロードマップ作成
    roadmap = strategist.create_growth_roadmap(
        product_info,
        starting_phase=GrowthPhase.STEALTH,
        target_duration_months=18
    )
    
    # 結果を表示
    print(f"🚀 {roadmap.product_name} 成長ロードマップ")
    print(f"期間: {roadmap.total_duration_months}ヶ月\n")
    
    for phase in roadmap.phases:
        print(f"\n【{phase.phase.value}】（{phase.duration_weeks}週間）")
        print(f"主要目標: {', '.join(phase.primary_goals[:2])}")
        print(f"重要指標: {', '.join([m.value for m in phase.key_metrics])}")
        print(f"予算配分: {list(phase.budget_allocation.keys())[:3]}")


if __name__ == "__main__":
    main()