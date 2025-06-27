#!/usr/bin/env python3
"""
Gemini CLI - Google AI Geminiとの対話用CLIツール
"""

import os
import sys
import argparse
import google.generativeai as genai
from typing import Optional

class GeminiCLI:
    def __init__(self, api_key: Optional[str] = None):
        """
        Gemini CLIの初期化
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            print("エラー: GEMINI_API_KEYが設定されていません")
            print("環境変数を設定するか、--api-keyオプションを使用してください")
            sys.exit(1)
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def prompt(self, question: str) -> str:
        """
        Geminiに質問を送信して回答を取得
        """
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"
    
    def interactive_mode(self):
        """
        対話モード
        """
        print("Gemini CLI - 対話モード")
        print("終了するには 'exit' または 'quit' を入力してください")
        print("-" * 50)
        
        while True:
            try:
                question = input("\nあなた: ")
                if question.lower() in ['exit', 'quit']:
                    print("さようなら！")
                    break
                
                print("\nGemini: ", end="", flush=True)
                response = self.prompt(question)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\nさようなら！")
                break
            except Exception as e:
                print(f"\nエラー: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Gemini CLI - Google AI Geminiとの対話ツール')
    parser.add_argument('-p', '--prompt', type=str, help='Geminiへの質問')
    parser.add_argument('--api-key', type=str, help='Gemini API Key')
    parser.add_argument('-i', '--interactive', action='store_true', help='対話モード')
    
    args = parser.parse_args()
    
    cli = GeminiCLI(api_key=args.api_key)
    
    if args.interactive:
        cli.interactive_mode()
    elif args.prompt:
        response = cli.prompt(args.prompt)
        print(response)
    else:
        # 引数なしの場合は対話モード
        cli.interactive_mode()

if __name__ == "__main__":
    main()