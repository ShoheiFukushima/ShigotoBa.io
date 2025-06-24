#!/usr/bin/env python3
"""
Gemini API接続テスト
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# 環境変数の読み込み
load_dotenv()

def test_gemini_connection():
    """Gemini APIへの接続テスト"""
    print("🔧 Gemini API接続テスト開始...\n")
    
    # APIキーの確認
    api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ エラー: GOOGLE_API_KEY または GEMINI_API_KEY が設定されていません")
        return False
    
    print(f"✅ APIキーが見つかりました: {api_key[:8]}...")
    
    try:
        # Gemini APIの設定
        genai.configure(api_key=api_key)
        
        # 利用可能なモデルの確認
        print("\n📋 利用可能なモデル:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # テスト生成
        print("\n🧪 テスト生成中...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("こんにちは！私はマーケティング自動化ツールです。")
        
        print(f"\n✅ 応答: {response.text[:100]}...")
        print("\n🎉 Gemini API接続成功！")
        return True
        
    except Exception as e:
        print(f"\n❌ エラー: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_connection()