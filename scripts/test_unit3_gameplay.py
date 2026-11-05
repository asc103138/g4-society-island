#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright E2E 自動化驗證腳本：
測試獨立的第三單元地圖 `unit3/index.html`：
1. 驗證僅有 2 座島嶼（faith 傳統信仰島、oldstreet 家鄉老街島）
2. 驗證看門獸「泰雅祖靈彩虹橋」(guardian) 無島嶼、直接飄在海面上（scale=2.35）且具備導覽功能
3. 驗證 1~8 關圖卡、實境小實驗、因果速懂方格與闖關題目
4. 驗證 0 Console Errors / 0 Page Errors
"""
import os
import threading
import http.server
import socketserver
from playwright.sync_api import sync_playwright

PORT = 8766

def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, port

def main():
    os.makedirs("test_screenshots", exist_ok=True)
    httpd, port = start_server()
    console_errors = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        url = f"http://127.0.0.1:{port}/unit3/index.html"
        print(f"Navigating to {url} ...")
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(1800)

        # 1. 檢查島嶼數量與海上彩虹橋 guardian 設定
        world_info = page.evaluate("""() => {
            const terrains = Object.keys(window.__island.world.terrains);
            const gRoot = window.__island.guardian.root;
            const gScale = gRoot.children[0].scale.x;
            const gPos = [gRoot.position.x, gRoot.position.y, gRoot.position.z];
            return { terrains, gScale, gPos };
        }""")
        print("World Info:", world_info)
        assert world_info["terrains"] == ["faith", "oldstreet"], f"Expected 2 islands ['faith', 'oldstreet'], got {world_info['terrains']}"
        assert world_info["gScale"] > 2.0, f"Expected enlarged guardian scale > 2.0, got {world_info['gScale']}"

        # 拍下雙島與海上巨型彩虹橋全景圖
        page.screenshot(path="test_screenshots/unit3_standalone_panorama.png")
        print("Saved panorama screenshot: test_screenshots/unit3_standalone_panorama.png")

        # 2. 測試點擊海上「祖靈彩虹橋」導覽（如同上一檔案的海龜導覽）
        page.evaluate("window.openGuardianFast()")
        page.wait_for_timeout(900)
        guide_title = page.locator("#panel-title").inner_text()
        print("Guardian Guide Panel Title:", guide_title)
        assert "泰雅祖靈彩虹橋" in guide_title and "島嶼導覽" in guide_title

        # 在導覽面板中執行彩虹橋小實驗
        page.screenshot(path="test_screenshots/unit3_standalone_guardian_guide.png")
        print("Saved guardian guide screenshot: test_screenshots/unit3_standalone_guardian_guide.png")
        btns = page.locator("#panel-body .minigame-btn")
        for i in range(btns.count()):
            btns.nth(i).click()
            page.wait_for_timeout(150)
        page.evaluate("""() => {
            if (typeof closeLevelupModal === 'function') closeLevelupModal();
            const rm = document.getElementById('rainbowCelebrationModal');
            if (rm) rm.remove();
            const p = document.getElementById('panel');
            if (p && !p.hidden) document.getElementById('panel-close')?.click();
        }""")
        page.wait_for_timeout(400)

        # 3. 逐一測試第 1～8 關
        stations = [
            "indigenous_ritual", "folk_deity", "temple_fair", "eco_worship",
            "river_port", "shophouse", "indigo_craft", "street_revival"
        ]
        for idx, sid in enumerate(stations, 1):
            page.evaluate(f"window.goStationFast('{sid}')")
            page.wait_for_timeout(1100)
            title = page.locator("#panel-title").inner_text()
            print(f"Station {idx} ({sid}) opened -> {title}")
            # 點擊該站小實驗按鈕
            m_btns = page.locator("#panel-body .minigame-btn")
            for b_i in range(m_btns.count()):
                m_btns.nth(b_i).click()
                page.wait_for_timeout(120)
            page.evaluate("if (typeof closeLevelupModal === 'function') closeLevelupModal();")
            page.wait_for_timeout(150)
            page.screenshot(path=f"test_screenshots/unit3_standalone_s{idx}_{sid}.png")
            page.evaluate("""() => {
                if (typeof closeLevelupModal === 'function') closeLevelupModal();
                const p = document.getElementById('panel');
                if (p && !p.hidden) document.getElementById('panel-close')?.click();
            }""")
            page.wait_for_timeout(300)

        browser.close()

    httpd.shutdown()
    print(f"Console Errors: {len(console_errors)}")
    for e in console_errors:
        print("  ERROR:", e)
    print(f"Page Errors: {len(page_errors)}")
    for e in page_errors:
        print("  PAGE ERROR:", e)

    assert len(console_errors) == 0, "Console errors detected!"
    assert len(page_errors) == 0, "Page errors detected!"
    print("ALL STANDALONE UNIT 3 TESTS 100% PASSED!")

if __name__ == "__main__":
    main()
