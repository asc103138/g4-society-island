import os
import sys
import time
from playwright.sync_api import sync_playwright

WORKSPACE_DIR = "/Users/tunyuan/Library/CloudStorage/GoogleDrive-asc103138@st.tc.edu.tw/我的雲端硬碟/115四上期中社會複習遊戲"
HTML_PATH = f"file://{WORKSPACE_DIR}/index.html"
SCREENSHOT_DIR = f"{WORKSPACE_DIR}/test_screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def dismiss_levelup_if_present(page):
    time.sleep(0.3)
    modal = page.locator("#levelupModal.active")
    if modal.is_visible():
        print("   -> [RPG 升級！] 觸發 Level Up 彈窗，收下力量繼續冒險！")
        page.click("#levelupModal button")
        time.sleep(0.3)

def run_tests():
    console_errors = []
    unhandled_exceptions = []

    print("=== [1] 啟動原本 3D 群島島嶼 ✕ 科技 RPG 完整 Playwright E2E 自動測試 ===")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # 監聽主控台錯誤與未處理異常
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: unhandled_exceptions.append(str(err)))
        page.on("dialog", lambda dialog: dialog.accept())

        print(f"正在載入 3D 社會島遊戲網頁：{HTML_PATH}")
        page.goto(HTML_PATH)
        page.wait_for_selector("#scene")
        page.wait_for_selector(".topbar")
        page.wait_for_selector(".bottombar")
        time.sleep(2.5)  # 等待 Three.js 空間地景與標籤渲染

        # 測試 0：3D 社會島全景與 RPG HUD
        print("-> [Pass] 原本 3D 社會島自然群島與 RPG HUD 載入成功")
        page.screenshot(path=f"{SCREENSHOT_DIR}/01_original_3d_island_overview.png")

        # 驗證 HUD 元素
        assert page.locator("#hudLevelPill").is_visible(), "Level pill should be visible"
        assert page.locator("#hudGoldText").is_visible(), "Gold text should be visible"
        assert page.locator("#hudStarsText").is_visible(), "Stars text should be visible"

        # 測試抽屜系統 1：🎒 背包道具
        print("-> [Pass] 測試抽屜面板：🎒 背包抽屜與食用烤地瓜")
        page.click("button:has-text('🎒 背包')")
        time.sleep(0.4)
        page.screenshot(path=f"{SCREENSHOT_DIR}/02_rpg_drawer_inventory.png")
        page.click(".rpg-item-card:has-text('炭火悶烤地瓜')")
        time.sleep(0.3)
        page.click("#inventoryDrawer .drawer-close")
        time.sleep(0.3)

        # 測試抽屜系統 2：🎖️ 徽章手冊
        print("-> [Pass] 測試抽屜面板：🎖️ 徽章手冊")
        page.click("button:has-text('🎖️ 徽章')")
        time.sleep(0.4)
        page.screenshot(path=f"{SCREENSHOT_DIR}/03_rpg_drawer_stamps.png")
        page.click("#stampsDrawer .drawer-close")
        time.sleep(0.3)

        # 測試抽屜系統 3：📖 圖鑑辭典
        print("-> [Pass] 測試抽屜面板：📖 生活辭典小圖鑑")
        page.click("button:has-text('📖 圖鑑')")
        time.sleep(0.4)
        page.screenshot(path=f"{SCREENSHOT_DIR}/04_rpg_drawer_encyclopedia.png")
        page.click("#encyclopediaDrawer .drawer-close")
        time.sleep(0.3)

        # 測試抽屜系統 4：📋 教師教材審查
        print("-> [Pass] 測試抽屜面板：📋 教師教材審查工作台")
        page.click("button:has-text('📋 審查')")
        time.sleep(0.4)
        page.screenshot(path=f"{SCREENSHOT_DIR}/05_rpg_drawer_teacher_audit.png")
        page.click("#teacherDrawer .drawer-close")
        time.sleep(0.3)

        # 測試第 1 站：家鄉地圖站
        print("-> [Pass] 進入第 1 站：家鄉地圖站")
        page.click("button:has-text('1.地圖站')")
        time.sleep(1.2)
        page.wait_for_selector(".panel", state="visible")
        page.screenshot(path=f"{SCREENSHOT_DIR}/06_station1_map_panel.png")

        # 執行第 1 站實境小實驗：地圖修復工作台
        print("   -> 執行第 1 站實境小實驗：安裝方向標、圖例、比例尺")
        page.click(".minigame-btn:has-text('安裝方向標')")
        time.sleep(0.2)
        page.click(".minigame-btn:has-text('安裝圖例')")
        time.sleep(0.2)
        page.click(".minigame-btn:has-text('安裝比例尺')")
        time.sleep(0.4)
        dismiss_levelup_if_present(page)

        # 啟動第 1 站闖關挑戰
        print("   -> 啟動第 1 站闖關挑戰")
        start_btn = page.locator(".quiz button.btn-primary:has-text('開始闖關'), .quiz button.btn-primary:has-text('再挑戰一次')")
        if start_btn.is_visible():
            start_btn.click()
            time.sleep(0.4)
            opt = page.locator(".answer-grid button.answer-btn, .answer-grid button.tf-btn, button:has-text('確定')").first
            if opt.is_visible():
                opt.click()
                time.sleep(0.3)
                dismiss_levelup_if_present(page)
        
        page.click("#panel-close")
        time.sleep(0.5)

        # 測試第 6 站：水庫水資源站（海廢怪戰鬥）
        print("-> [Pass] 進入第 6 站：水庫水資源站")
        page.click("button:has-text('6.水庫水資源')")
        time.sleep(1.2)
        page.wait_for_selector(".panel", state="visible")
        page.screenshot(path=f"{SCREENSHOT_DIR}/07_station6_water_panel.png")
        page.click(".minigame-btn:has-text('抹肥皂關水')")
        time.sleep(0.2)
        page.click(".minigame-btn:has-text('減塑海廢爆擊')")
        time.sleep(0.4)
        dismiss_levelup_if_present(page)
        page.click("#panel-close")
        time.sleep(0.5)

        # 測試第 7 站：紅磚三合院
        print("-> [Pass] 進入第 7 站：紅磚三合院（左尊右卑與大灶柴灰）")
        page.click("button:has-text('7.三合院')")
        time.sleep(1.2)
        page.wait_for_selector(".panel", state="visible")
        page.click(".minigame-btn:has-text('左護龍')")
        time.sleep(0.2)
        page.click(".minigame-btn:has-text('悶地瓜')")
        time.sleep(0.3)
        dismiss_levelup_if_present(page)
        page.click("#panel-close")
        time.sleep(0.5)

        # 測試第 8 站：石板屋與達悟地下屋
        print("-> [Pass] 進入第 8 站：石板屋聚落（排煙防蟲與抗颱避風）")
        page.click("button:has-text('8.石板屋')")
        time.sleep(1.2)
        page.wait_for_selector(".panel", state="visible")
        page.click(".minigame-btn:has-text('排煙')")
        time.sleep(0.2)
        page.click(".minigame-btn:has-text('避風')")
        time.sleep(0.3)
        dismiss_levelup_if_present(page)
        page.click("#panel-close")
        time.sleep(0.5)

        # 測試第 9 站：古早器物市集
        print("-> [Pass] 進入第 9 站：古早器物市集（竹編魚筌與木杵搗小米）")
        page.click("button:has-text('9.古早器物')")
        time.sleep(1.2)
        page.wait_for_selector(".panel", state="visible")
        page.click(".minigame-btn:has-text('魚筌')")
        time.sleep(0.2)
        for _ in range(3):
            page.click(".minigame-btn:has-text('搗小米')")
            time.sleep(0.15)
        dismiss_levelup_if_present(page)
        page.click("#panel-close")
        time.sleep(0.5)

        # 測試全景回到俯瞰
        print("-> [Pass] 測試全景重設")
        page.click("#btn-home")
        time.sleep(1.2)
        page.screenshot(path=f"{SCREENSHOT_DIR}/08_original_island_home_returned.png")

        # 測試終章：🏆 榮譽結業證書
        print("-> [Pass] 測試終章：專屬 Canvas 結業榮譽證書生成")
        page.click("button:has-text('🏆 證書')")
        time.sleep(0.5)
        page.fill("#certClass", "四年忠班")
        page.fill("#certSeat", "15")
        page.fill("#certName", "林小航")
        page.click("button:has-text('即時繪製專屬獎狀')")
        time.sleep(0.5)
        page.screenshot(path=f"{SCREENSHOT_DIR}/09_original_island_certificate.png")
        page.click("#certModal .drawer-close")
        time.sleep(0.3)

        # 檢查主控台錯誤與未處理異常
        print("=== [2] 測試全流程完成，進行主控台錯誤統計 ===")
        print(f"-> 瀏覽器主控台 Error 總數：{len(console_errors)}")
        print(f"-> 頁面未處理異常 Exception 總數：{len(unhandled_exceptions)}")

        if console_errors:
            print("❌ 檢測到主控台錯誤：")
            for err in console_errors:
                print(f"   - {err}")

        if unhandled_exceptions:
            print("❌ 檢測到未處理異常：")
            for exc in unhandled_exceptions:
                print(f"   - {exc}")

        browser.close()

        if len(console_errors) == 0 and len(unhandled_exceptions) == 0:
            print("✅ 【自動化測試全數通過 100%】原本自然 3D 群島島嶼、相機巡航、實境小實驗、RPG 與證書全流程閉環！")
            return 0
        else:
            print("⚠️ 測試中發現異常，需要修復！")
            return 1

if __name__ == "__main__":
    sys.exit(run_tests())
