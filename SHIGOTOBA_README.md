# 🏭 Shigotoba.io - 個人開発者向け全自動マーケティング代理店

## 概要
Shigotoba.ioは、14個のAI専門家モジュールが協力して、アプリの企画から広告配信、改善まで全自動で実行するシステムです。個人開発者が大企業のマーケティング部門と同等の成果を出せるように設計されています。

## 🚀 特徴
- **14個のAI専門家**: 各分野のスペシャリストAIが協力
- **企画から配信まで全自動**: 人間は承認するだけ
- **工場レーン型プロセス**: 明確で効率的なワークフロー
- **1プロンプト = 1モジュール**: シンプルで拡張性の高い設計

## 📦 必要な環境
- Python 3.12+
- Streamlit
- OpenAI API キー または Anthropic API キー
- pytest（テスト実行用）
- Playwright（E2Eテスト用）

## 🛠️ インストール
```bash
# 1. リポジトリをクローン
git clone https://github.com/your-repo/marketing-automation-tools.git
cd marketing-automation-tools

# 2. 必要なパッケージをインストール
pip install -r requirements.txt

# 3. 環境変数を設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

## 🎯 使い方

### アプリケーションの起動
```bash
streamlit run app_shigotoba.py
```

ブラウザで http://localhost:8501 にアクセスしてください。

### 基本的な使用フロー
1. **企画書入力**: アプリのアイデアを入力
2. **AI分析**: 14個のAIが自動で市場分析・戦略立案
3. **承認ゲート1**: 戦略を確認して承認
4. **制作・配信**: 広告素材の制作と配信
5. **承認ゲート2**: 制作物を確認して配信開始
6. **継続改善**: データ分析と最適化

## 🤖 AIモジュール一覧

### フェーズ1: 基礎戦略（7モジュール）
1. **マーケット分析AI**: 競合調査、市場規模算出
2. **グロースハッカーAI**: 成長戦略立案
3. **価格戦略AI**: 最適価格設計
4. **AI専門家会議システム**: 戦略統合
5. **コピーライティングAI**: 魅力的な文章生成
6. **ビジュアルクリエイティブAI**: デザイン戦略
7. **SEO/ASO専門AI**: 検索最適化

### フェーズ2: 実行戦略（6モジュール）
8. **修正反映AI**: 人間の修正指示を反映
9. **クリエイター実行AI**: 実際の制作
10. **広告配信AI**: 配信戦略と実行
11. **データアナリストAI**: パフォーマンス分析
12. **カスタマーサクセスAI**: ユーザー対応
13. **デプロイメントAI**: 技術的実装

### 特別な役割
14. **人文学者AI**: 戦略の文化的・社会的分析

## 🧪 テスト

### ユニットテスト
```bash
pytest test_shigotoba.py -v
```

### E2Eテスト
```bash
npx playwright test tests/shigotoba_e2e.spec.js
```

## 📁 プロジェクト構成
```
marketing-automation-tools/
├── app_shigotoba.py          # メインアプリケーション
├── shigotoba_modules.py      # AIモジュール実装
├── test_shigotoba.py         # ユニットテスト
├── tests/
│   └── shigotoba_e2e.spec.js # E2Eテスト
├── config/
│   ├── ai_client.py          # AI統一クライアント
│   └── ai_models.py          # AIモデル設定
├── SHIGOTOBA_AI_MODULES_SPEC.md   # 詳細仕様書
├── SHIGOTOBA_DEVELOPMENT_RULES.md # 開発ルール
└── SHIGOTOBA_README.md       # このファイル
```

## 🔧 設定

### AIプロバイダーの設定
`config/ai_models.py`でAIモデルを設定できます：
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)

### 環境変数
```bash
# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key

# Google
GOOGLE_API_KEY=your-google-api-key
```

## 📝 開発ガイドライン

### 基本原則
- **1プロンプト = 1モジュール**: 各AIモジュールは単一の責任を持つ
- **シンプル最優先**: 複雑な機能より動くものを
- **AIに任せる**: できるだけAIに処理を委ねる

### 新しいAIモジュールの追加
1. `shigotoba_modules.py`に新しいメソッドを追加
2. 入力・処理・出力を明確に定義
3. エラーハンドリングを実装
4. テストケースを追加

## 🚨 トラブルシューティング

### よくある問題
1. **APIキーエラー**: 環境変数が正しく設定されているか確認
2. **モジュール import エラー**: `pip install -r requirements.txt`を再実行
3. **Streamlitエラー**: `streamlit run`コマンドで起動しているか確認

### デバッグモード
```python
# ログレベルを設定
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 貢献方法
1. Forkする
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにPush (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

## 📄 ライセンス
このプロジェクトはMITライセンスの下で公開されています。

## 🙏 謝辞
- AIコーディングの可能性を示してくれたClaudeに感謝
- 個人開発者コミュニティの皆様に感謝

---

**Remember**: このプロジェクトの目的は「動くもの」を作ること。完璧より進捗を優先！

## 📞 サポート
質問や問題がある場合は、GitHubのIssueを作成してください。