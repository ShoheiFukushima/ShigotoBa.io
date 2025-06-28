# Google Sheets データベース設定ガイド

このガイドでは、Marketing Automation ToolsアプリでGoogle Sheetsをデータベースとして使用するための設定方法を説明します。

## 1. Google Cloud Consoleでのプロジェクト設定

### 1.1 プロジェクトの作成または選択
1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 既存のプロジェクトを選択するか、新しいプロジェクトを作成

### 1.2 Google Sheets APIの有効化
1. 「APIとサービス」→「ライブラリ」に移動
2. 「Google Sheets API」を検索
3. 「有効にする」をクリック
4. 同様に「Google Drive API」も有効化

## 2. サービスアカウントの作成

### 2.1 サービスアカウント作成
1. 「APIとサービス」→「認証情報」に移動
2. 「認証情報を作成」→「サービスアカウント」を選択
3. 以下の情報を入力：
   - サービスアカウント名: `marketing-automation-sheets`
   - サービスアカウントID: 自動生成されたものを使用
   - 説明: `Marketing Automation Tools用のGoogle Sheets接続`

### 2.2 キーの作成
1. 作成したサービスアカウントをクリック
2. 「キー」タブに移動
3. 「鍵を追加」→「新しい鍵を作成」
4. 「JSON」を選択して「作成」
5. JSONファイルがダウンロードされます（重要：このファイルは安全に保管してください）

## 3. アプリケーションの設定

### 3.1 認証情報の配置
ダウンロードしたJSONファイルを以下のいずれかの方法で設定：

#### 方法1: ファイルとして配置（ローカル開発用）
```bash
# プロジェクトルートに配置
cp ~/Downloads/your-service-account-key.json ./credentials.json
```

#### 方法2: 環境変数として設定（本番環境用）
```bash
# .envファイルに追加
GOOGLE_SHEETS_CREDENTIALS='{"type": "service_account", "project_id": "your-project", ...}'
```

### 3.2 スプレッドシートIDの設定
```bash
# .envファイルに追加
GOOGLE_SHEETS_ID=your-spreadsheet-id
```

スプレッドシートIDは、Google SheetsのURLから取得できます：
`https://docs.google.com/spreadsheets/d/[ここがスプレッドシートID]/edit`

## 4. Google Sheetsの準備

### 4.1 新規スプレッドシートの作成
1. [Google Sheets](https://sheets.google.com)にアクセス
2. 新しいスプレッドシートを作成
3. スプレッドシート名を「Marketing Automation Data」に変更

### 4.2 サービスアカウントへの権限付与
1. スプレッドシートの「共有」ボタンをクリック
2. サービスアカウントのメールアドレスを入力
   （JSONファイル内の`client_email`の値）
3. 「編集者」権限を付与
4. 「送信」をクリック

## 5. 初回起動と確認

### 5.1 アプリケーションの起動
```bash
streamlit run app.py
```

### 5.2 接続確認
アプリケーション起動時に以下のメッセージが表示されれば成功：
- 「Google Sheets接続成功」
- スプレッドシートのURLが表示される

エラーが表示される場合は、以下を確認：
- APIが有効化されているか
- 認証情報が正しく設定されているか
- スプレッドシートへの権限が付与されているか

## 6. データ構造

自動的に以下のシートが作成されます：

### projects シート
| 列名 | 説明 |
|------|------|
| id | プロジェクトID |
| name | プロジェクト名 |
| type | プロジェクトタイプ |
| status | ステータス |
| flow_stage | フロー段階 |
| created_at | 作成日時 |
| updated_at | 更新日時 |
| data | JSON形式の詳細データ |

### todos シート
| 列名 | 説明 |
|------|------|
| id | TODO ID |
| text | TODOテキスト |
| done | 完了フラグ |
| priority | 優先度 |
| created_at | 作成日時 |
| updated_at | 更新日時 |

### ai_outputs シート
| 列名 | 説明 |
|------|------|
| id | 出力ID |
| project_id | プロジェクトID |
| type | 出力タイプ |
| content | 出力内容 |
| created_at | 作成日時 |

### settings シート
| 列名 | 説明 |
|------|------|
| key | 設定キー |
| value | 設定値 |
| updated_at | 更新日時 |

## 7. トラブルシューティング

### よくあるエラーと対処法

#### "Google Sheets認証情報が見つかりません"
- `credentials.json`ファイルが存在するか確認
- 環境変数`GOOGLE_SHEETS_CREDENTIALS`が設定されているか確認

#### "APIが有効化されていません"
- Google Cloud ConsoleでSheets APIとDrive APIが有効化されているか確認

#### "権限がありません"
- サービスアカウントのメールアドレスがスプレッドシートに編集者として追加されているか確認

#### "スプレッドシートが見つかりません"
- `GOOGLE_SHEETS_ID`が正しく設定されているか確認
- スプレッドシートが削除されていないか確認

## 8. セキュリティに関する注意事項

1. **認証情報の管理**
   - `credentials.json`ファイルは絶対にGitにコミットしないでください
   - `.gitignore`に`credentials.json`が含まれていることを確認

2. **アクセス制限**
   - サービスアカウントには必要最小限の権限のみ付与
   - 本番環境では環境変数を使用

3. **データの暗号化**
   - 機密情報は別途暗号化して保存することを推奨

## 9. Cloud Run デプロイ時の設定

Cloud Runにデプロイする際は、以下の手順で環境変数を設定：

```bash
# シークレットの作成
gcloud secrets create google-sheets-credentials --data-file=credentials.json

# Cloud Runサービスの更新
gcloud run deploy shigotoba-io \
  --update-secrets=GOOGLE_SHEETS_CREDENTIALS=google-sheets-credentials:latest \
  --update-env-vars=GOOGLE_SHEETS_ID=your-spreadsheet-id
```

## 10. データのバックアップ

定期的にGoogle Sheetsのデータをバックアップすることを推奨：

1. Google Sheetsの「ファイル」→「コピーを作成」
2. または、「ファイル」→「ダウンロード」→「Microsoft Excel」

---

問題が発生した場合は、アプリケーション内のエラーメッセージを確認し、このガイドに従って設定を見直してください。