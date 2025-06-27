# 🚀 AI Pipeline Development Plan

## 👥 開発チーム体制

### PM (Project Manager)
**担当**: 全体管理・API設計・統合テスト
**ウィンドウ**: `multiagent:0 (PM-Main)`

### Worker1 - AI Creative Studio
**担当**: モック削除・Gemini API統合
**ウィンドウ**: `multiagent:1 (Worker1-Creative)`
**ファイル**: `pages/_ai_creative_studio.py`

### Worker2 - 広告最適化エンジン  
**担当**: リアルタイム最適化AI実装
**ウィンドウ**: `multiagent:2 (Worker2-AdOptimizer)`
**ファイル**: `pages/_realtime_ad_optimizer.py`

### Worker3 - データパイプライン
**担当**: ツール間連携・ワークフロー基盤
**ウィンドウ**: `multiagent:3 (Worker3-Pipeline)`
**ファイル**: 新規作成予定 `utils/pipeline.py`

---

## 📋 タスク分割

### Phase 1: 個別AI実装 (並行作業)

#### Worker1 タスク
1. `generate_ai_creative_content` をモックから実AIに移行
2. Gemini APIを使った実際のクリエイティブ生成
3. プロンプトエンジニアリング
4. エラーハンドリング実装

#### Worker2 タスク
1. `generate_optimization_recommendations` を実AI化
2. パフォーマンスデータの分析ロジック
3. 最適化アルゴリズムの実装
4. リアルタイムデータ処理

#### Worker3 タスク
1. 統一データフォーマット設計
2. `PipelineManager` クラス作成
3. ワークフロー定義システム
4. ツール間データ受け渡し機能

### Phase 2: 統合テスト
- 各AIツールの連携確認
- エンドツーエンドテスト
- パフォーマンステスト

### Phase 3: パイプライン実装
- ワークフロー実行エンジン
- 自動化フロー設定画面
- 進捗モニタリング機能

---

## 🔧 共通インターフェース

### データフォーマット標準
```python
{
    "tool_id": "ai_creative_studio",
    "timestamp": "2025-06-27T10:00:00Z",
    "input": {
        "campaign_type": "SNS広告",
        "theme": "夏のセール",
        "target_audience": "20-30代女性"
    },
    "output": {
        "status": "success",
        "data": {
            "creatives": [...],
            "metadata": {...}
        }
    },
    "next_tools": ["realtime_ad_optimizer", "ab_testing"]
}
```

### セッション状態管理
```python
st.session_state.pipeline_data = {
    "current_workflow": "campaign_automation",
    "step": 2,
    "results": {
        "ai_creative_studio": {...},
        "realtime_ad_optimizer": {...}
    }
}
```

---

## 🚦 開発ルール

1. **ブランチ戦略**
   - main: 本番環境
   - develop: 統合ブランチ
   - feature/worker1-creative: Worker1作業
   - feature/worker2-optimizer: Worker2作業
   - feature/worker3-pipeline: Worker3作業

2. **コミットメッセージ**
   - feat: 新機能追加
   - fix: バグ修正
   - refactor: リファクタリング
   - test: テスト追加

3. **レビュープロセス**
   - 各Workerは自己テスト実施
   - PMが統合テスト実施
   - 本番デプロイ前に全体確認

---

## 📅 スケジュール

### Day 1-2: 個別AI実装
- 各Workerが並行作業
- 日次進捗確認

### Day 3: 統合テスト
- ツール間連携確認
- バグ修正

### Day 4-5: パイプライン構築
- ワークフローエンジン実装
- UI作成

### Day 6: 本番デプロイ
- 最終テスト
- デプロイ実行

---

## 🎯 成功基準

1. **各AIツールが実データで動作**
   - モック完全削除
   - 実際のAI応答

2. **ツール間の自動連携**
   - データの自動受け渡し
   - エラーハンドリング

3. **エンドツーエンドの自動化**
   - キャンペーン作成から配信まで
   - 人間の介入最小化

---

*最終更新: 2025-06-27 by PM*