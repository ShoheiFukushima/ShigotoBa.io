#!/usr/bin/env python3
"""
自動化セットアップウィザード
APIキーの設定と自動化レベルの選択を支援
"""

import os
import json
import sys
from typing import Dict, Any

def setup_automation():
    """自動化環境をセットアップ"""
    
    print("""
╔══════════════════════════════════════════════════════════╗
║        マーケティング完全自動化セットアップ              ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    
    # 1. 自動化レベル選択
    print("\n📊 自動化レベルを選択してください：\n")
    print("1. 【生成のみ】コンテンツを生成して表示（手動でコピペ）")
    print("2. 【半自動】生成後、承認してから自動投稿")
    print("3. 【完全自動】スケジュール通りに自動投稿＆最適化")
    
    level = input("\n選択 (1-3): ").strip()
    
    level_map = {
        "1": "手動（生成のみ）",
        "2": "半自動（承認後投稿）", 
        "3": "完全自動"
    }
    
    config["automation_level"] = level_map.get(level, "手動（生成のみ）")
    
    # レベル2以上の場合、API設定
    if level in ["2", "3"]:
        print("\n🔐 API連携設定")
        print("-" * 40)
        
        # Twitter/X設定
        print("\n【Twitter/X API】")
        use_twitter = input("Twitter自動投稿を使用しますか？ (y/n): ").lower() == 'y'
        
        if use_twitter:
            print("\nTwitter Developer Portalから取得した情報を入力:")
            print("（取得方法: https://developer.twitter.com/）")
            
            twitter_config = {
                "enabled": True,
                "api_key": input("API Key: ").strip(),
                "api_secret": input("API Secret: ").strip(),
                "access_token": input("Access Token: ").strip(),
                "access_token_secret": input("Access Token Secret: ").strip()
            }
            
            # 環境変数として保存
            env_content = f"""
# Twitter API
export TWITTER_API_KEY="{twitter_config['api_key']}"
export TWITTER_API_SECRET="{twitter_config['api_secret']}"
export TWITTER_ACCESS_TOKEN="{twitter_config['access_token']}"
export TWITTER_ACCESS_TOKEN_SECRET="{twitter_config['access_token_secret']}"
"""
            
            with open('.env', 'a') as f:
                f.write(env_content)
            
            print("✅ Twitter API設定完了")
        
        # WordPress設定
        print("\n【WordPress自動投稿】")
        use_wordpress = input("WordPress自動投稿を使用しますか？ (y/n): ").lower() == 'y'
        
        if use_wordpress:
            wp_config = {
                "enabled": True,
                "url": input("WordPressサイトURL: ").strip(),
                "username": input("ユーザー名: ").strip(),
                "password": input("アプリケーションパスワード: ").strip()
            }
            
            env_content = f"""
# WordPress
export WORDPRESS_URL="{wp_config['url']}"
export WORDPRESS_USER="{wp_config['username']}"
export WORDPRESS_PASS="{wp_config['password']}"
"""
            
            with open('.env', 'a') as f:
                f.write(env_content)
            
            print("✅ WordPress設定完了")
        
        # メール設定
        print("\n【メール自動配信】")
        use_email = input("メール自動配信を使用しますか？ (y/n): ").lower() == 'y'
        
        if use_email:
            print("\nメールサーバー設定:")
            email_config = {
                "enabled": True,
                "smtp_server": input("SMTPサーバー (Gmail: smtp.gmail.com): ").strip() or "smtp.gmail.com",
                "username": input("メールアドレス: ").strip(),
                "password": input("アプリパスワード: ").strip()
            }
            
            env_content = f"""
# Email
export SMTP_SERVER="{email_config['smtp_server']}"
export EMAIL_USER="{email_config['username']}"
export EMAIL_PASS="{email_config['password']}"
export FROM_EMAIL="{email_config['username']}"
"""
            
            with open('.env', 'a') as f:
                f.write(env_content)
            
            print("✅ メール設定完了")
    
    # 3. スケジュール設定（レベル3の場合）
    if level == "3":
        print("\n⏰ 投稿スケジュール設定")
        print("-" * 40)
        
        print("\nデフォルトのスケジュール:")
        print("- Twitter: 9:00, 12:00, 19:00（平日）")
        print("- ブログ: 10:00（火・木）")
        print("- メール: 8:00（月）")
        
        use_default = input("\nデフォルト設定を使用しますか？ (y/n): ").lower() == 'y'
        
        if not use_default:
            # カスタムスケジュール設定
            pass
    
    # 設定ファイル保存
    config_path = '/Users/fukushimashouhei/dev/marketing-automation-tools/automation_config.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("\n✅ セットアップ完了！")
    print(f"設定ファイル: {config_path}")
    
    if level != "1":
        print("\n📌 次のステップ:")
        print("1. source .env  # 環境変数を読み込み")
        print("2. python3 main_auto.py  # 自動化モードで実行")
    
    print("\n🎉 準備完了！プロダクト情報を入力して自動化を開始しましょう。")


if __name__ == "__main__":
    setup_automation()