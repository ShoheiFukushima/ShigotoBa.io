"""
Pytest設定ファイル
PlaywrightのE2Eテスト用フィクスチャ
"""

import pytest
from playwright.sync_api import sync_playwright
import subprocess
import time
import os
import signal


@pytest.fixture(scope="session")
def browser():
    """ブラウザインスタンスを提供"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # ヘッドレスモードで実行
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """各テスト用の新しいページを提供"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="ja-JP"
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session", autouse=True)
def streamlit_server():
    """Streamlitサーバーを起動・停止"""
    # Streamlitサーバーを起動
    process = subprocess.Popen(
        ["python", "-m", "streamlit", "run", "dashboard/home.py", 
         "--server.port", "8501", 
         "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid  # プロセスグループを作成
    )
    
    # サーバーの起動を待つ
    time.sleep(5)
    
    yield
    
    # テスト終了後、プロセスグループ全体を終了
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except:
        process.terminate()
    
    process.wait()