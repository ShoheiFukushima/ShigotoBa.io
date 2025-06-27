# Shigotoba.io 開発ルール

## 🎯 プロジェクトの核心
**1プロンプト = 1モジュール** の原則で、個人開発者が大企業のマーケティング部門と同等の成果を出せるシステム

## 📏 開発の基本ルール

### 1. シンプルさを最優先
- 複雑な機能より動くものを優先
- 1つの関数は1つの目的
- プロンプトで解決できることはプロンプトで

### 2. AIコーディングの活用
```python
# 良い例：シンプルなプロンプト呼び出し
def analyze_competitors(app_name, category):
    prompt = f"{category}カテゴリの{app_name}の競合TOP5を教えて"
    return call_ai(prompt)

# 悪い例：複雑なロジック
def analyze_competitors_complex(app_name, category):
    # 100行のデータ処理...
```

### 3. モジュール設計
- **入力**: 明確で最小限
- **処理**: 1つのAIプロンプト
- **出力**: 構造化された結果

### 4. UIの方針
- Streamlitの標準機能を使う
- カスタムCSSは最小限
- 機能 > 見た目

### 5. データ管理
- セッション状態で管理
- 永続化はGoogle Sheets（将来）
- 複雑なDBは避ける

### 6. エラーハンドリング
- シンプルなリトライ
- ユーザーへの明確なメッセージ
- 致命的エラーは避ける設計

## 🚀 実装の順序

### Phase 1: MVP（現在）
1. 企画書入力フォーム
2. 基本的なAIモジュール5個
3. 承認画面
4. 実行フロー

### Phase 2: 拡張
5. 残りのAIモジュール
6. Google Sheets連携
7. 自動実行

### Phase 3: 最適化
8. パフォーマンス改善
9. UI/UX向上

## 💡 開発のコツ

### やること
- ✅ 動くプロトタイプを素早く作る
- ✅ ユーザー（自分）のフィードバックを即反映
- ✅ AIに処理を任せる

### やらないこと
- ❌ 完璧を求める
- ❌ 複雑な抽象化
- ❌ 過度な最適化

## 🔧 技術スタック
- **Frontend**: Streamlit
- **AI**: OpenAI API (or Claude API)
- **Storage**: Session State → Google Sheets
- **Deploy**: Streamlit Cloud (将来)

## 📝 命名規則
- ファイル: `snake_case.py`
- 関数: `snake_case()`
- クラス: `PascalCase`
- 定数: `UPPER_SNAKE_CASE`

## 🎨 コーディングスタイル
- PEP 8準拠
- 日本語コメントOK（わかりやすさ優先）
- 型ヒントは任意

## 🚦 コミットメッセージ
- 日本語OK
- 何をしたか明確に
- 例: "企画書入力フォームを追加"

---

**Remember**: このプロジェクトの目的は「動くもの」を作ること。完璧より進捗を優先！