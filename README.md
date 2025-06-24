# 🚀 shigotoba.io

**AI-Powered Marketing Automation Platform**

マーケティング業務を革新する次世代自動化プラットフォーム

## ✨ 主な機能

- 🤖 **AIチャット**: Gemini APIを活用したリアルタイムマーケティング支援
- 📊 **プロジェクト管理**: マーケティングプロジェクトの一元管理
- 🔍 **市場分析**: AI駆動の競合分析とSWOT分析
- 📝 **コンテンツ生成**: SNS投稿、ブログ記事、プレスリリースの自動生成
- 📈 **パフォーマンス追跡**: リアルタイムでのKPI監視
- 🎯 **自動投稿**: ソーシャルメディアへの予約投稿（拡張機能）

## 🛠️ 技術スタック

- **フロントエンド**: Streamlit
- **AI/LLM**: Google Gemini API
- **データ可視化**: Plotly, Pandas
- **言語**: Python 3.10+

## 📦 インストール

### 1. リポジトリのクローン
```bash
git clone https://github.com/YOUR_USERNAME/marketing-automation-tools.git
cd marketing-automation-tools
```

### 2. 仮想環境の作成（推奨）
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# または
venv\Scripts\activate  # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
`.env`ファイルを作成し、APIキーを設定:
```env
GOOGLE_API_KEY=your-gemini-api-key
GEMINI_API_KEY=your-gemini-api-key
```

## 🚀 起動方法

```bash
cd dashboard
streamlit run home.py
```

ブラウザで http://localhost:8501 にアクセス

## 📱 スマートフォンからのアクセス

### ローカルネットワーク経由
1. PCとスマホを同じWi-Fiに接続
2. PCのIPアドレスを確認
3. スマホで `http://YOUR_PC_IP:8501` にアクセス

### Streamlit Cloud経由（推奨）
1. Streamlit Cloudにデプロイ
2. 生成されたURLにスマホからアクセス
3. ホーム画面に追加してアプリのように使用

## 🔧 設定

### 機能の有効化/無効化
`.env`ファイルで機能フラグを設定:
```env
ENABLE_AI_CHAT=true
ENABLE_SOCIAL_POSTING=false
ENABLE_EMAIL_MARKETING=false
```

### APIキーの追加
必要に応じて`.env`ファイルのコメントを外してAPIキーを追加

## 📚 使用方法

1. **プロジェクト作成**: 「開発室」から新規プロジェクトを作成
2. **プロダクト情報入力**: 製品の基本情報を入力
3. **AI分析**: 市場分析・競合分析を実行
4. **コンテンツ生成**: マーケティングコンテンツを自動生成
5. **実行・監視**: キャンペーンの実行と効果測定

## 🤝 貢献

プルリクエストを歓迎します！

## 📄 ライセンス

MIT License

## 🔗 関連リンク

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [デプロイガイド](./deploy_guide.md)

---

Made with ❤️ by Marketing Automation Team