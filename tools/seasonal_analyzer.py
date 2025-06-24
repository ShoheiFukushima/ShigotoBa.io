#!/usr/bin/env python3
"""
季節性分析・消費者行動予測モジュール
日本の月別消費者行動と業界トレンドを分析
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class BusinessSector(Enum):
    """業界セクター"""
    B2C_GENERAL = "B2C一般"
    B2C_STUDENT = "B2C学生向け"
    B2B_ENTERPRISE = "B2B企業向け"
    B2B_SMB = "B2B中小企業向け"
    EDUCATION = "教育"
    ENTERTAINMENT = "エンタメ"
    HEALTH_FITNESS = "健康・フィットネス"
    TRAVEL = "旅行"

@dataclass
class SeasonalInsight:
    """季節性インサイト"""
    month: int
    consumer_behavior: List[str]
    opportunities: List[str]
    risks: List[str]
    recommended_campaigns: List[str]
    budget_allocation_factor: float  # 1.0が標準、1.5なら50%増

class SeasonalAnalyzer:
    """日本の季節性と消費者行動を分析"""
    
    def __init__(self):
        self.japan_calendar = self._init_japan_calendar()
        self.sector_patterns = self._init_sector_patterns()
        
    def _init_japan_calendar(self) -> Dict[int, Dict[str, Any]]:
        """日本の年間カレンダーと消費者行動パターン"""
        return {
            1: {
                "name": "1月 - 新年・仕事始め",
                "events": ["正月", "成人の日", "仕事始め"],
                "consumer_mood": "新年の決意・目標設定",
                "spending_level": "中",
                "business_activity": "低（正月休み明け）",
                "trends": ["健康・ダイエット", "学習・自己啓発", "新年の抱負"]
            },
            2: {
                "name": "2月 - 受験・バレンタイン",
                "events": ["節分", "バレンタインデー", "受験シーズン"],
                "consumer_mood": "集中・準備期間",
                "spending_level": "中",
                "business_activity": "中",
                "trends": ["受験対策", "ギフト", "恋愛関連"]
            },
            3: {
                "name": "3月 - 年度末・卒業",
                "events": ["ひな祭り", "卒業式", "年度末", "春休み開始"],
                "consumer_mood": "変化・準備",
                "spending_level": "高",
                "business_activity": "高（年度末）",
                "trends": ["引っ越し", "新生活準備", "卒業記念"]
            },
            4: {
                "name": "4月 - 新年度・新生活",
                "events": ["入学式", "入社式", "新年度開始", "花見"],
                "consumer_mood": "新しいスタート",
                "spending_level": "非常に高",
                "business_activity": "高",
                "trends": ["新生活グッズ", "ビジネスツール", "学習教材"]
            },
            5: {
                "name": "5月 - GW・五月病",
                "events": ["ゴールデンウィーク", "母の日", "五月病"],
                "consumer_mood": "リフレッシュ・調整期",
                "spending_level": "高（GW）",
                "business_activity": "低（GW）→中",
                "trends": ["旅行", "レジャー", "ストレス解消", "母の日ギフト"]
            },
            6: {
                "name": "6月 - 梅雨・ボーナス前",
                "events": ["梅雨入り", "父の日", "ボーナス前"],
                "consumer_mood": "室内活動・期待感",
                "spending_level": "中低",
                "business_activity": "中",
                "trends": ["室内エンタメ", "梅雨対策", "父の日ギフト"]
            },
            7: {
                "name": "7月 - 夏休み・ボーナス",
                "events": ["七夕", "海の日", "夏休み開始", "夏のボーナス"],
                "consumer_mood": "開放的・アクティブ",
                "spending_level": "高",
                "business_activity": "中",
                "trends": ["夏のレジャー", "旅行", "夏期講習", "エアコン・涼感グッズ"]
            },
            8: {
                "name": "8月 - 夏本番・お盆",
                "events": ["お盆", "夏祭り", "花火大会", "夏休み"],
                "consumer_mood": "リラックス・帰省",
                "spending_level": "高",
                "business_activity": "低（お盆休み）",
                "trends": ["帰省", "レジャー", "夏の思い出作り", "受験勉強追い込み"]
            },
            9: {
                "name": "9月 - 秋の始まり・防災",
                "events": ["防災の日", "敬老の日", "秋分の日", "新学期"],
                "consumer_mood": "気持ちの切り替え",
                "spending_level": "中",
                "business_activity": "高",
                "trends": ["防災グッズ", "秋物衣類", "敬老の日ギフト", "学習再開"]
            },
            10: {
                "name": "10月 - スポーツ・文化",
                "events": ["体育の日", "ハロウィン", "紅葉シーズン"],
                "consumer_mood": "活動的・文化的",
                "spending_level": "中",
                "business_activity": "高",
                "trends": ["スポーツ", "読書", "ハロウィン", "秋の行楽"]
            },
            11: {
                "name": "11月 - 年末準備開始",
                "events": ["文化の日", "勤労感謝の日", "ブラックフライデー"],
                "consumer_mood": "年末に向けた準備",
                "spending_level": "中高",
                "business_activity": "高",
                "trends": ["年末準備", "お歳暮選び", "セール", "受験ラストスパート"]
            },
            12: {
                "name": "12月 - 年末・ボーナス",
                "events": ["冬のボーナス", "クリスマス", "大晦日", "冬休み"],
                "consumer_mood": "お祝い・締めくくり",
                "spending_level": "非常に高",
                "business_activity": "高→低（年末）",
                "trends": ["クリスマス", "忘年会", "年末セール", "お正月準備"]
            }
        }
    
    def _init_sector_patterns(self) -> Dict[BusinessSector, Dict[int, float]]:
        """業界別の月別活性度（1.0が標準）"""
        return {
            BusinessSector.B2C_STUDENT: {
                1: 0.8, 2: 1.2, 3: 1.5, 4: 1.8, 5: 1.0,
                6: 0.8, 7: 1.3, 8: 1.2, 9: 1.1, 10: 1.0,
                11: 1.2, 12: 1.0
            },
            BusinessSector.B2B_ENTERPRISE: {
                1: 0.7, 2: 1.0, 3: 1.3, 4: 1.2, 5: 0.8,
                6: 1.1, 7: 1.0, 8: 0.6, 9: 1.2, 10: 1.3,
                11: 1.2, 12: 0.9
            },
            BusinessSector.HEALTH_FITNESS: {
                1: 1.8, 2: 1.3, 3: 1.2, 4: 1.5, 5: 1.3,
                6: 1.0, 7: 1.2, 8: 1.0, 9: 1.1, 10: 1.0,
                11: 0.9, 12: 0.7
            },
            BusinessSector.ENTERTAINMENT: {
                1: 1.2, 2: 1.0, 3: 1.1, 4: 1.0, 5: 1.4,
                6: 0.9, 7: 1.5, 8: 1.6, 9: 1.0, 10: 1.1,
                11: 1.0, 12: 1.3
            }
        }
    
    def analyze_seasonal_opportunity(self, product_info: Dict[str, Any], 
                                   target_month: int = None) -> Dict[str, Any]:
        """製品の季節性機会を分析"""
        
        if target_month is None:
            target_month = datetime.now().month
        
        # 業界セクターを判定
        sector = self._determine_sector(product_info)
        
        # 3ヶ月先まで分析
        insights = []
        for i in range(3):
            month = ((target_month - 1 + i) % 12) + 1
            insight = self._analyze_month(month, sector, product_info)
            insights.append(insight)
        
        # 年間トレンドも分析
        yearly_trend = self._analyze_yearly_trend(sector, product_info)
        
        return {
            "current_month": target_month,
            "sector": sector.value,
            "next_3_months": insights,
            "yearly_trend": yearly_trend,
            "best_launch_months": self._find_best_launch_months(sector, product_info),
            "seasonal_campaigns": self._generate_seasonal_campaigns(insights, product_info)
        }
    
    def _determine_sector(self, product_info: Dict[str, Any]) -> BusinessSector:
        """製品情報から業界セクターを判定"""
        
        target = product_info.get('target', '').lower()
        category = product_info.get('category', '').lower()
        
        if '学生' in target or '教育' in category:
            return BusinessSector.B2C_STUDENT
        elif '企業' in target and '大' in target:
            return BusinessSector.B2B_ENTERPRISE
        elif '企業' in target:
            return BusinessSector.B2B_SMB
        elif '健康' in category or 'フィットネス' in category:
            return BusinessSector.HEALTH_FITNESS
        elif 'エンタメ' in category or 'ゲーム' in category:
            return BusinessSector.ENTERTAINMENT
        elif '旅行' in category:
            return BusinessSector.TRAVEL
        else:
            return BusinessSector.B2C_GENERAL
    
    def _analyze_month(self, month: int, sector: BusinessSector, 
                      product_info: Dict[str, Any]) -> SeasonalInsight:
        """特定の月の分析"""
        
        calendar = self.japan_calendar[month]
        sector_factor = self.sector_patterns.get(sector, {}).get(month, 1.0)
        
        # 製品特性に基づいた機会とリスクを分析
        opportunities = []
        risks = []
        campaigns = []
        
        # カレンダーイベントから機会を抽出
        for event in calendar['events']:
            if '新' in event and '始' in event:
                opportunities.append(f"{event}に合わせた新規ユーザー獲得")
                campaigns.append(f"「{event}応援キャンペーン」")
            elif 'ボーナス' in event:
                opportunities.append(f"{event}時期の購買意欲向上")
                campaigns.append(f"「{event}特別プラン」")
        
        # 消費者行動からインサイトを生成
        if calendar['spending_level'] in ['高', '非常に高']:
            opportunities.append("消費意欲が高い時期")
        else:
            risks.append("消費が控えめな時期")
        
        # 業界別の追加インサイト
        if sector == BusinessSector.B2C_STUDENT:
            if month in [3, 4]:
                opportunities.append("新入生向けプロモーション最適期")
            elif month in [7, 8]:
                opportunities.append("夏休み期間の利用促進")
        
        return SeasonalInsight(
            month=month,
            consumer_behavior=calendar['trends'],
            opportunities=opportunities,
            risks=risks,
            recommended_campaigns=campaigns,
            budget_allocation_factor=sector_factor
        )
    
    def _analyze_yearly_trend(self, sector: BusinessSector, 
                            product_info: Dict[str, Any]) -> Dict[str, Any]:
        """年間トレンド分析"""
        
        # 四半期ごとの特徴
        quarters = {
            "Q1 (1-3月)": {
                "theme": "新年の抱負・年度末準備",
                "focus": "目標設定、準備、変化",
                "budget": "中〜高"
            },
            "Q2 (4-6月)": {
                "theme": "新生活・梅雨対策",
                "focus": "スタート、適応、室内活動",
                "budget": "高〜中"
            },
            "Q3 (7-9月)": {
                "theme": "夏のアクティビティ・秋の準備",
                "focus": "レジャー、リフレッシュ、再始動",
                "budget": "高〜中"
            },
            "Q4 (10-12月)": {
                "theme": "年末商戦・締めくくり",
                "focus": "イベント、ギフト、総括",
                "budget": "中〜非常に高"
            }
        }
        
        return {
            "quarters": quarters,
            "peak_seasons": self._identify_peak_seasons(sector),
            "off_seasons": self._identify_off_seasons(sector)
        }
    
    def _identify_peak_seasons(self, sector: BusinessSector) -> List[str]:
        """ピークシーズンを特定"""
        
        peak_map = {
            BusinessSector.B2C_STUDENT: ["3-4月（新学期）", "7-8月（夏休み）"],
            BusinessSector.B2B_ENTERPRISE: ["3月（年度末）", "4月（新年度）", "10月（下期開始）"],
            BusinessSector.HEALTH_FITNESS: ["1月（新年）", "4-5月（薄着の季節前）"],
            BusinessSector.ENTERTAINMENT: ["5月（GW）", "8月（夏休み）", "12月（年末）"]
        }
        
        return peak_map.get(sector, ["4月", "7-8月", "12月"])
    
    def _identify_off_seasons(self, sector: BusinessSector) -> List[str]:
        """オフシーズンを特定"""
        
        off_map = {
            BusinessSector.B2C_STUDENT: ["6月（梅雨）", "11月（受験準備）"],
            BusinessSector.B2B_ENTERPRISE: ["8月（お盆）", "年末年始"],
            BusinessSector.HEALTH_FITNESS: ["12月（忘年会シーズン）"],
            BusinessSector.ENTERTAINMENT: ["2月", "6月（梅雨）"]
        }
        
        return off_map.get(sector, ["2月", "6月"])
    
    def _find_best_launch_months(self, sector: BusinessSector, 
                                product_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """最適なローンチ時期を提案"""
        
        sector_patterns = self.sector_patterns.get(sector, {})
        
        # 活性度の高い月を抽出
        high_activity_months = [
            month for month, factor in sector_patterns.items() 
            if factor >= 1.2
        ]
        
        recommendations = []
        for month in high_activity_months[:3]:  # Top 3
            calendar = self.japan_calendar[month]
            recommendations.append({
                "month": f"{month}月",
                "reason": f"{calendar['name']}で{calendar['consumer_mood']}",
                "activity_score": sector_patterns[month]
            })
        
        return sorted(recommendations, 
                     key=lambda x: x['activity_score'], 
                     reverse=True)
    
    def _generate_seasonal_campaigns(self, insights: List[SeasonalInsight], 
                                   product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """季節性を考慮したキャンペーン案を生成"""
        
        campaigns = []
        
        for insight in insights:
            month_name = self.japan_calendar[insight.month]['name']
            
            # 各月のキャンペーン案
            for campaign_name in insight.recommended_campaigns:
                campaigns.append({
                    "month": insight.month,
                    "name": campaign_name,
                    "timing": month_name,
                    "budget_factor": insight.budget_allocation_factor,
                    "expected_impact": "高" if insight.budget_allocation_factor > 1.2 else "中"
                })
        
        return campaigns


def main():
    """使用例"""
    analyzer = SeasonalAnalyzer()
    
    # サンプル製品
    product_info = {
        "name": "StudyMaster",
        "category": "教育",
        "target": "学生"
    }
    
    # 季節性分析
    results = analyzer.analyze_seasonal_opportunity(product_info)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()