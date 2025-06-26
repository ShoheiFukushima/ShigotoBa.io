# Streamlit Cloud デプロイメントガイド

## 本番環境でのナビゲーションメニュー非表示化

### 1. Streamlit Cloud の設定

Streamlit Cloudの管理画面で以下の設定を行ってください：

1. **Advanced settings** → **Secrets** に以下を追加：
```toml
[client]
showSidebarNavigation = false
```

2. **Advanced settings** → **Python dependencies** で以下を確認：
- `requirements.txt` が正しく読み込まれていること

### 2. 環境変数の設定

Streamlit Cloudの **Secrets** セクションに以下を追加：
```toml
HIDE_STREAMLIT_NAV = "true"
```

### 3. コマンドライン引数の設定（オプション）

もし上記の方法で解決しない場合、Streamlit Cloudの **Advanced settings** で：
- **Main file path**: `app.py`
- **Custom subdomain**: 任意のサブドメイン
- **Python version**: 3.10

### 4. 最終手段：カスタムコンポーネント

それでも解決しない場合は、`components/sidebar_enhanced.py` を使用してください。
この強化版サイドバーは、JavaScriptとCSSで完全にカスタマイズされており、
Streamlitのデフォルトナビゲーションを上書きします。

### 実装済みの対策

1. **`.streamlit/config.toml`**:
   ```toml
   [client]
   showSidebarNavigation = false
   ```

2. **`.streamlit/pages.toml`**:
   ```toml
   pages = []
   ```

3. **CSS による強制非表示**:
   - `app.py` 内のカスタムCSSで、ナビゲーション要素を `display: none`

4. **環境検出による動的制御**:
   - 本番環境を検出して設定を動的に変更

### トラブルシューティング

もしまだナビゲーションが表示される場合：

1. **ブラウザのキャッシュをクリア**
2. **Streamlit Cloudでアプリを再起動**
3. **別のブラウザで確認**

### 推奨される最終構成

左サイドバーには以下のみを表示：
- 📁 プロジェクト選択（ドロップダウン）
- 🏗️ 新規開発（アコーディオン）
- 📊 運営・分析（アコーディオン）
- 🎨 広告・マーケ（アコーディオン）

これらはすべて `components/sidebar.py` または `components/sidebar_enhanced.py` で管理されています。