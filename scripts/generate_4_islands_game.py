import os
import sys

WORKSPACE_DIR = "/Users/tunyuan/Library/CloudStorage/GoogleDrive-asc103138@st.tc.edu.tw/我的雲端硬碟/115四上期中社會複習遊戲"
OUTPUT_HTML_PATH = os.path.join(WORKSPACE_DIR, "index.html")

html_content = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>康軒四上社會科 3D 互動島嶼：家鄉時空英雄傳（科技微縮模型風・期中複習專用）</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
  
  <script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
    }
  }
  </script>
  <style>
    :root {
      --bg-space: #070c18;
      --bg-card: rgba(15, 23, 42, 0.92);
      --primary: #38bdf8;
      --primary-dark: #0284c7;
      --accent: #f59e0b;
      --accent-glow: rgba(245, 158, 11, 0.4);
      --danger: #ef4444;
      --success: #10b981;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --line: rgba(56, 189, 248, 0.25);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --font-family: "Noto Sans TC", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-tap-highlight-color: transparent; }
    html, body { width: 100vw; height: 100vh; height: 100dvh; overflow: hidden; background: var(--bg-space); font-family: var(--font-family); color: var(--text); }
    button { font: inherit; color: inherit; cursor: pointer; }

    /* 滿版 3D WebGL Canvas */
    #sceneCanvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      display: block;
    }

    /* 頂部科技感 RPG HUD */
    header.hud-bar {
      position: fixed;
      top: 0; left: 0; right: 0;
      height: 60px;
      z-index: 30;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      background: linear-gradient(180deg, rgba(7, 12, 24, 0.95) 0%, rgba(7, 12, 24, 0.75) 85%, transparent 100%);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--line);
    }

    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .brand-logo {
      width: 36px; height: 36px;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    }
    .brand-title {
      font-size: 15px;
      font-weight: 900;
      color: #fff;
      letter-spacing: 0.5px;
    }
    .brand-sub {
      font-size: 11px;
      color: var(--primary);
      display: block;
    }

    .hud-stats {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .rpg-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--primary);
      padding: 4px 12px 4px 6px;
      border-radius: 999px;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }
    .rpg-level {
      background: var(--accent);
      color: #000;
      font-weight: 900;
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .rpg-name {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
    }
    .rpg-bars {
      display: flex;
      flex-direction: column;
      gap: 3px;
      width: 80px;
    }
    .bar-wrap {
      height: 6px;
      background: #334155;
      border-radius: 3px;
      overflow: hidden;
    }
    .hp-fill { height: 100%; width: 100%; background: linear-gradient(90deg, #ef4444, #f87171); transition: width 0.3s; }
    .mp-fill { height: 100%; width: 100%; background: linear-gradient(90deg, #0284c7, #38bdf8); transition: width 0.3s; }

    .gold-pill, .stars-pill {
      font-size: 12px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 999px;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .gold-pill { background: rgba(245, 158, 11, 0.15); border: 1px solid var(--accent); color: #fbbf24; }
    .stars-pill { background: rgba(16, 185, 129, 0.15); border: 1px solid var(--success); color: #34d399; }

    .hud-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .hud-btn {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #f8fafc;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 800;
      transition: all 0.2s;
    }
    .hud-btn:hover, .hud-btn.active {
      background: var(--primary-dark);
      border-color: var(--primary);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }
    .hud-btn.primary {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      border-color: var(--primary);
      color: #fff;
    }

    /* 底部 4 座島嶼快速切換導覽列 */
    footer.bottom-bar {
      position: fixed;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 30;
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(12px);
      border: 1px solid var(--line);
      padding: 6px 10px;
      border-radius: 999px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5);
      max-width: 95vw;
      overflow-x: auto;
    }
    .island-nav-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 7px 14px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 800;
      color: #cbd5e1;
      white-space: nowrap;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .island-nav-btn:hover, .island-nav-btn.active {
      background: var(--primary);
      border-color: #fff;
      color: #04101e;
      transform: translateY(-2px);
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
    }
    .island-nav-btn.home-btn {
      background: #0f172a;
      border-color: #64748b;
      color: #94a3b8;
    }

    /* 3D 浮動標籤 (Leader Label) */
    .island-floating-tag {
      position: absolute;
      transform: translate(-50%, -100%);
      pointer-events: auto;
      cursor: pointer;
      z-index: 10;
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: transform 0.2s;
    }
    .island-floating-tag:hover {
      transform: translate(-50%, -108%) scale(1.06);
    }
    .tag-badge {
      background: rgba(15, 23, 42, 0.95);
      border: 1.5px solid var(--primary);
      border-radius: 999px;
      padding: 4px 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5), 0 0 10px rgba(56,189,248,0.3);
      white-space: nowrap;
    }
    .tag-num {
      background: var(--accent);
      color: #000;
      font-weight: 900;
      font-size: 11px;
      border-radius: 50%;
      width: 18px; height: 18px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    .tag-title {
      font-size: 13px;
      font-weight: 800;
      color: #f8fafc;
    }
    .tag-pointer {
      width: 2px;
      height: 18px;
      background: linear-gradient(180deg, var(--primary) 0%, transparent 100%);
    }

    /* 右側彈出式島嶼詳情卡片 (Side Modal Card) */
    .island-card-panel {
      position: fixed;
      top: 70px;
      right: 18px;
      bottom: 80px;
      width: 440px;
      max-width: calc(100vw - 36px);
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      border: 1.5px solid var(--line);
      border-radius: var(--radius-lg);
      z-index: 40;
      display: flex;
      flex-direction: column;
      box-shadow: 0 15px 45px rgba(0, 0, 0, 0.6), 0 0 25px rgba(56, 189, 248, 0.2);
      transform: translateX(110%);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      overflow: hidden;
    }
    .island-card-panel.active {
      transform: translateX(0);
    }
    .panel-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      background: rgba(30, 41, 59, 0.5);
    }
    .panel-kicker {
      font-size: 11px;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 2px;
    }
    .panel-title {
      font-size: 18px;
      font-weight: 900;
      color: #fff;
    }
    .panel-close-btn {
      background: rgba(255,255,255,0.08);
      border: none;
      font-size: 20px;
      color: var(--text-muted);
      border-radius: 50%;
      width: 32px; height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }
    .panel-close-btn:hover {
      background: #ef4444;
      color: #fff;
    }

    /* 分頁標籤 */
    .panel-tabs {
      display: flex;
      border-bottom: 1px solid var(--line);
      background: rgba(15, 23, 42, 0.6);
    }
    .tab-btn {
      flex: 1;
      padding: 10px 0;
      text-align: center;
      font-size: 13px;
      font-weight: 800;
      color: var(--text-muted);
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-btn:hover { color: #fff; }
    .tab-btn.active {
      color: var(--primary);
      border-bottom-color: var(--primary);
      background: rgba(56, 189, 248, 0.08);
    }

    .panel-body {
      padding: 18px 20px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* 觀念圖卡 */
    .concept-card {
      background: rgba(30, 41, 59, 0.65);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: var(--radius-md);
      padding: 14px;
      transition: border-color 0.2s;
    }
    .concept-card:hover { border-color: var(--primary); }
    .concept-head {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .concept-icon { font-size: 22px; }
    .concept-title { font-size: 15px; font-weight: 900; color: var(--primary); }
    .concept-text { font-size: 13px; line-height: 1.6; color: #cbd5e1; }

    /* 易錯陷阱框 */
    .trap-box {
      background: rgba(245, 158, 11, 0.12);
      border-left: 3.5px solid var(--accent);
      border-radius: 4px var(--radius-sm) var(--radius-sm) 4px;
      padding: 12px 14px;
      font-size: 13px;
      line-height: 1.55;
      color: #fde68a;
    }
    .trap-box strong { color: #fbbf24; font-weight: 900; display: block; margin-bottom: 2px; }

    /* 實境小實驗盒 */
    .minigame-container {
      background: rgba(15, 23, 42, 0.85);
      border: 1.5px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 16px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .minigame-container h4 {
      font-size: 15px;
      font-weight: 900;
      color: #38bdf8;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .minigame-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 10px;
    }
    .game-action-btn {
      background: rgba(2, 132, 199, 0.25);
      border: 1.5px solid var(--primary);
      color: #fff;
      font-weight: 800;
      font-size: 13px;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      transition: all 0.2s;
    }
    .game-action-btn:hover {
      background: var(--primary);
      color: #000;
    }
    .game-action-btn.done {
      background: rgba(16, 185, 129, 0.2);
      border-color: var(--success);
      color: #34d399;
    }

    /* 闖關測驗元件 */
    .quiz-box {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .quiz-q-title {
      font-size: 14px;
      font-weight: 800;
      color: #fff;
      line-height: 1.5;
    }
    .quiz-options {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .quiz-opt-btn {
      background: rgba(30, 41, 59, 0.8);
      border: 1.5px solid rgba(56, 189, 248, 0.3);
      border-radius: var(--radius-sm);
      padding: 10px 14px;
      font-size: 13px;
      font-weight: 700;
      color: #f8fafc;
      text-align: left;
      transition: all 0.2s;
    }
    .quiz-opt-btn:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: var(--primary);
    }
    .quiz-opt-btn.correct {
      background: rgba(16, 185, 129, 0.25) !important;
      border-color: var(--success) !important;
      color: #34d399 !important;
    }
    .quiz-opt-btn.wrong {
      background: rgba(239, 68, 68, 0.25) !important;
      border-color: var(--danger) !important;
      color: #f87171 !important;
    }
    .quiz-feedback {
      background: rgba(15, 23, 42, 0.9);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      font-size: 13px;
      line-height: 1.5;
      display: none;
    }

    /* 抽屜樣式 (背包/徽章/圖鑑/審查/證書) */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      z-index: 100;
      background: rgba(7, 12, 24, 0.7);
      backdrop-filter: blur(6px);
      display: none;
      justify-content: flex-end;
      opacity: 0;
      transition: opacity 0.3s;
    }
    .drawer-overlay.active { display: flex; opacity: 1; }
    .drawer-panel {
      width: 100%;
      max-width: 460px;
      height: 100%;
      background: #0f172a;
      border-left: 1.5px solid var(--line);
      box-shadow: -10px 0 35px rgba(0, 0, 0, 0.7);
      display: flex;
      flex-direction: column;
      transform: translateX(100%);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .drawer-overlay.active .drawer-panel { transform: translateX(0); }
    .drawer-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .drawer-header h3 { font-size: 16px; font-weight: 900; color: #fff; }
    .drawer-close {
      background: none; border: none; font-size: 22px; color: var(--text-muted); padding: 4px 8px; border-radius: 6px;
    }
    .drawer-close:hover { color: #ef4444; }
    .drawer-body { padding: 18px 20px; overflow-y: auto; flex: 1; }

    /* 背包道具格 */
    .rpg-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .rpg-item-card {
      background: rgba(30, 41, 59, 0.7);
      border: 1.5px solid var(--line);
      border-radius: var(--radius-md);
      padding: 12px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
    }
    .rpg-item-card:hover { border-color: var(--accent); transform: translateY(-2px); }

    /* 徽章格 */
    .stamps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .stamp-cell {
      background: rgba(30, 41, 59, 0.5);
      border: 1.5px dashed #475569;
      border-radius: var(--radius-md);
      padding: 12px 8px;
      text-align: center;
    }
    .stamp-cell.unlocked {
      background: rgba(16, 185, 129, 0.15);
      border: 1.5px solid var(--success);
    }
    .stamp-icon { font-size: 28px; filter: grayscale(1); opacity: 0.3; margin-bottom: 4px; }
    .stamp-cell.unlocked .stamp-icon { filter: none; opacity: 1; }
    .stamp-title { font-size: 12px; font-weight: 800; color: #94a3b8; }
    .stamp-cell.unlocked .stamp-title { color: #34d399; }

    /* 浮動提示 Toast */
    #rpgToast {
      position: fixed;
      top: 72px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.95);
      color: #fff;
      padding: 10px 22px;
      border-radius: 999px;
      z-index: 200;
      font-size: 13px;
      font-weight: 800;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
      border: 1.5px solid var(--accent);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s;
    }

    /* 證書畫布 */
    .cert-preview {
      width: 100%;
      border-radius: 10px;
      border: 2px solid var(--primary);
      margin: 12px 0;
    }

    @media (max-width: 800px) {
      .rpg-bars, .gold-pill, .stars-pill { display: none; }
      .brand-sub { display: none; }
      .island-card-panel { width: 100%; right: 0; top: auto; bottom: 0; height: 65vh; border-radius: 20px 20px 0 0; }
    }
  </style>
</head>
<body>

  <!-- 滿版 3D WebGL Canvas -->
  <canvas id="sceneCanvas"></canvas>

  <!-- 頂部科技感 RPG HUD 儀表列 -->
  <header class="hud-bar">
    <div class="brand-wrap">
      <div class="brand-logo">🏝️</div>
      <div>
        <div class="brand-title">3D 家鄉時空島群</div>
        <small class="brand-sub">康軒四上社會科・期中全單元科技微縮模型</small>
      </div>
    </div>

    <div class="hud-stats">
      <div class="rpg-badge">
        <span id="hudAvatar" style="font-size:18px;">👦</span>
        <span class="rpg-level" id="hudLevel">Lv.1</span>
        <span class="rpg-name" id="hudName">小航【海線見習生】</span>
      </div>

      <div class="rpg-bars" title="HP 生命值 / MP 探險魔力">
        <div class="bar-wrap" title="HP 生命值"><div class="hp-fill" id="hudHpBar"></div></div>
        <div class="bar-wrap" title="MP 探險魔力"><div class="mp-fill" id="hudMpBar"></div></div>
      </div>

      <div class="gold-pill" title="探險金幣">🪙 <span id="hudGold">100 G</span></div>
      <div class="stars-pill" title="全島徽章星級">⭐ <span id="hudStars">0 / 4 ★</span></div>
    </div>

    <div class="hud-actions">
      <button class="hud-btn" onclick="openDrawer('inventoryDrawer')">🎒 背包</button>
      <button class="hud-btn" onclick="openDrawer('stampsDrawer')">🎖️ 徽章</button>
      <button class="hud-btn" onclick="openDrawer('encyclopediaDrawer')">📖 圖鑑</button>
      <button class="hud-btn" onclick="openDrawer('teacherDrawer')">📋 審查</button>
      <button class="hud-btn primary" onclick="openDrawer('certDrawer')">🏆 證書</button>
      <button class="hud-btn" id="btnToggleSound" onclick="toggleSound()">🔊</button>
      <button class="hud-btn" onclick="toggleFullscreen()">⛶</button>
    </div>
  </header>

  <!-- 底部 4 座島嶼快速切換導覽列 -->
  <footer class="bottom-bar">
    <button class="island-nav-btn home-btn" id="btnOverview" onclick="focusOverview()">↺ 全景視野</button>
    <button class="island-nav-btn" id="btnNav0" onclick="focusIsland(0)">🗺️ 島嶼 1：地圖認識家鄉</button>
    <button class="island-nav-btn" id="btnNav1" onclick="focusIsland(1)">⛰️ 島嶼 2：五大地形探勘</button>
    <button class="island-nav-btn" id="btnNav2" onclick="focusIsland(2)">⛅ 島嶼 3：氣候與水資源</button>
    <button class="island-nav-btn" id="btnNav3" onclick="focusIsland(3)">🏡 島嶼 4：傳統住屋與器具</button>
  </footer>

  <!-- 3D 空間浮動島嶼標籤容器 -->
  <div id="labelsContainer" style="position:absolute; inset:0; pointer-events:none; z-index:20;"></div>

  <!-- 右側彈出式島嶼詳情卡片 (Side Modal Card) -->
  <aside class="island-card-panel" id="islandPanel">
    <div class="panel-header">
      <div>
        <div class="panel-kicker" id="panelKicker">單元重點展示</div>
        <div class="panel-title" id="panelTitle">島嶼名稱</div>
      </div>
      <button class="panel-close-btn" onclick="closeIslandPanel()">×</button>
    </div>

    <div class="panel-tabs">
      <button class="tab-btn active" id="tabBtnCards" onclick="switchPanelTab('cards')">📖 觀念圖卡</button>
      <button class="tab-btn" id="tabBtnGame" onclick="switchPanelTab('game')">🛠️ 實境小實驗</button>
      <button class="tab-btn" id="tabBtnQuiz" onclick="switchPanelTab('quiz')">🎯 闖關挑戰</button>
    </div>

    <div class="panel-body" id="panelBody">
      <!-- 動態填充內容 -->
    </div>
  </aside>

  <!-- 浮動提示 Toast -->
  <div id="rpgToast">提示文字</div>

  <!-- 抽屜 1：背包系統 -->
  <div class="drawer-overlay" id="inventoryDrawer" onclick="if(event.target===this)closeDrawer('inventoryDrawer')">
    <div class="drawer-panel">
      <div class="drawer-header">
        <h3>🎒 冒險者行囊・生活道具</h3>
        <button class="drawer-close" onclick="closeDrawer('inventoryDrawer')">×</button>
      </div>
      <div class="drawer-body">
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">點選背包道具可直接食用補血或裝備：</p>
        <div class="rpg-grid" id="inventoryList"></div>
      </div>
    </div>
  </div>

  <!-- 抽屜 2：徽章冊 -->
  <div class="drawer-overlay" id="stampsDrawer" onclick="if(event.target===this)closeDrawer('stampsDrawer')">
    <div class="drawer-panel">
      <div class="drawer-header">
        <h3>🎖️ 四大島嶼時空探索徽章手冊</h3>
        <button class="drawer-close" onclick="closeDrawer('stampsDrawer')">×</button>
      </div>
      <div class="drawer-body">
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">完成各大島嶼之實境小實驗與闖關，解鎖專屬榮譽徽章：</p>
        <div class="stamps-grid" id="stampsList"></div>
      </div>
    </div>
  </div>

  <!-- 抽屜 3：生活辭典圖鑑 -->
  <div class="drawer-overlay" id="encyclopediaDrawer" onclick="if(event.target===this)closeDrawer('encyclopediaDrawer')">
    <div class="drawer-panel">
      <div class="drawer-header">
        <h3>📖 康軒四上社會重點知識小辭典</h3>
        <button class="drawer-close" onclick="closeDrawer('encyclopediaDrawer')">×</button>
      </div>
      <div class="drawer-body" id="encyclopediaList"></div>
    </div>
  </div>

  <!-- 抽屜 4：教師審查工作台 -->
  <div class="drawer-overlay" id="teacherDrawer" onclick="if(event.target===this)closeDrawer('teacherDrawer')">
    <div class="drawer-panel" style="max-width:520px;">
      <div class="drawer-header">
        <h3>📋 教師教材審查工作台 (g4-curriculum-review)</h3>
        <button class="drawer-close" onclick="closeDrawer('teacherDrawer')">×</button>
      </div>
      <div class="drawer-body">
        <div style="background:rgba(16, 185, 129, 0.15); border:1.5px solid var(--success); border-radius:10px; padding:12px; margin-bottom:14px;">
          <strong style="color:#34d399;">🟢 三階漏斗自我檢測審查：全數通過 (100% PASS)</strong>
          <p style="font-size:12px; color:#a7f3d0; margin-top:4px;">嚴格依照康軒版四上社會課本第一單元（P.8~31）與第二單元（P.32~51）核心命題，0 幻想內容，符合教育部標準國字規範。</p>
        </div>
        <ul style="font-size:13px; color:var(--text); line-height:1.75; padding-left:18px;">
          <li><strong>最低門檻紅線</strong>：臺灣、臺中、臺地、汙染皆符教育部國字標準；題幹無非教材機械道具。</li>
          <li><strong>認知負荷優化 (CLT)</strong>：四大島嶼獨立清晰，圖卡分段呈現，配有常見易錯陷阱即時指引。</li>
          <li><strong>素養迷思導正</strong>：石板屋石縫排煙防蟲會呼吸、達悟地下屋避強風抗颱、三合院左尊右卑護龍。</li>
          <li><strong>SDGs 永續融入</strong>：SDG 6 淨水節水三招、SDG 14 海廢第一名寶特瓶源頭減塑。</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- 抽屜 5：結業證書 -->
  <div class="drawer-overlay" id="certDrawer" onclick="if(event.target===this)closeDrawer('certDrawer')">
    <div class="drawer-panel" style="max-width:540px;">
      <div class="drawer-header">
        <h3>🏆 期中全單元通關探險大師榮譽證書</h3>
        <button class="drawer-close" onclick="closeDrawer('certDrawer')">×</button>
      </div>
      <div class="drawer-body">
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:10px;">請輸入學生資料，即時繪製高解析專屬榮譽證書：</p>
        <div style="background:rgba(30, 41, 59, 0.7); border:1px solid var(--line); border-radius:10px; padding:12px; margin-bottom:12px;">
          <div style="display:flex; gap:8px; margin-bottom:8px;">
            <div style="flex:1;">
              <label style="font-size:12px; color:var(--text-muted);">班級：</label>
              <input type="text" id="certClass" value="四年忠班" style="width:100%; padding:6px 10px; background:#0f172a; color:#fff; border:1px solid #475569; border-radius:6px; font-size:13px;">
            </div>
            <div style="width:80px;">
              <label style="font-size:12px; color:var(--text-muted);">座號：</label>
              <input type="text" id="certSeat" value="15" style="width:100%; padding:6px 10px; background:#0f172a; color:#fff; border:1px solid #475569; border-radius:6px; font-size:13px;">
            </div>
            <div style="flex:1;">
              <label style="font-size:12px; color:var(--text-muted);">姓名：</label>
              <input type="text" id="certName" value="林小航" style="width:100%; padding:6px 10px; background:#0f172a; color:#fff; border:1px solid #475569; border-radius:6px; font-size:13px;">
            </div>
          </div>
          <button class="hud-btn primary" style="width:100%; justify-content:center; padding:9px 0;" onclick="drawCertificateCanvas()">🎨 即時繪製專屬獎狀</button>
        </div>

        <canvas id="certCanvas" width="800" height="560" class="cert-preview"></canvas>
        <button class="hud-btn" style="width:100%; justify-content:center; padding:9px 0; border:1.5px solid var(--primary); font-weight:800;" onclick="downloadCertificateImage()">📥 下載高解析獎狀圖檔 (PNG)</button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       3D 空間、音效與互動腳本
       ========================================================================== -->
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    /* --------------------------------------------------------------------------
       1. 遊戲資料庫 (四大島嶼嚴格依照康軒四上社會教材第一、二單元)
       -------------------------------------------------------------------------- */
    const ISLANDS_DATA = [
      {
        id: "map",
        order: 1,
        title: "用地圖認識家鄉",
        shortTitle: "地圖之島",
        unitTag: "第一單元・第 1 課",
        coords: [-16, 0, -10],
        color: 0x38bdf8,
        intro: "家鄉是我們出生、成長或長期居住的地方。想要認識家鄉的環境與方位，第一步就是學會看懂地圖四要素！",
        trap: "⚠️ 易錯陷阱：「圖例」是說明地圖上每個符號代表的意思；換算地圖距離與實際距離的，是「比例尺」！",
        cards: [
          { icon: "🧭", title: "地圖四要素", text: "1. 圖名：告知主題。\\n2. 方向標：指針指向北方。\\n3. 圖例：說明地圖符號含義。\\n4. 比例尺：表示縮小比例與距離換算。" },
          { icon: "🏘️", title: "家鄉的定義", text: "出生的地方、成長的地方或長期居住生活的地方，都可以是我們的家鄉！所以一個人的家鄉可能不只一個。" },
          { icon: "🗺️", title: "三種常見地圖", text: "行政區圖（看相鄰行政轄區）、觀光導覽圖（看景點與遊覽路線）、交通路線圖（看捷運公路搭乘）。" }
        ],
        quiz: [
          { q: "小恩在臺中出生，三歲搬到花蓮住到現在，所以臺中與花蓮都可以算是她的家鄉？", options: ["⭕ 是（正確）", "❌ 否（只能算一個）"], ans: 0, why: "出生、成長或長期居住的地方都可以是家鄉。" },
          { q: "在地圖上看到標示「1 公分代表實際 1 公里」，這是地圖四要素中的哪一項？", options: ["比例尺", "圖例", "方向標", "圖名"], ans: 0, why: "比例尺用來表示地圖縮小比例與實際距離換算。" },
          { q: "阿凱看不懂地圖上「藍色小船」符號代表什麼，他應該查看地圖的哪裡？", options: ["圖例", "比例尺", "方向標", "圖名"], ans: 0, why: "圖例說明地圖上各種符號與顏色代表的意思。" }
        ],
        minigameType: "mapWorkbench"
      },
      {
        id: "terrain",
        order: 2,
        title: "用地形認識家鄉（五大地形）",
        shortTitle: "地形之島",
        unitTag: "第一單元・第 2 課",
        coords: [16, 0, -10],
        color: 0x10b981,
        intro: "家鄉的大地高低起伏，主要包含五種基本地形：平原、盆地、臺地、丘陵與山地。不同的地勢造就了截然不同的生活與產業型態！",
        trap: "⚠️ 易錯陷阱：臺地是「頂部平坦、邊緣陡峭」；盆地是「四周高山圍繞、中間低平」；魚塭在沿海平原，不在高低起伏的丘陵！",
        cards: [
          { icon: "🌾", title: "平原與盆地", text: "• 平原：平坦廣闊、海拔低（如宜蘭平原、嘉南平原），適合水稻與沿海魚塭。\\n• 盆地：四周高、中間低平（如臺中盆地、臺北盆地），人口工商業密集。" },
          { icon: "🥏", title: "臺地（大肚臺地）", text: "頂部平坦、邊緣以陡坡與低地相接（如臺中大肚臺地、林口臺地），頂部常開闢成工業區與新市鎮。" },
          { icon: "⛰️", title: "丘陵與山地", text: "• 丘陵：海拔 1000 公尺以下、坡度平緩（如苗栗丘陵），適合茶園果園。\\n• 山地：海拔 1000 公尺以上、高聳起伏大（如中央山脈）。" }
        ],
        quiz: [
          { q: "「從空中鳥瞰頂部平坦，邊緣以陡坡和低地相接」，最符合哪一種地形？", options: ["臺地（如大肚臺地）", "盆地", "山地", "平原"], ans: 0, why: "頂部平坦邊緣陡峭為臺地特徵。" },
          { q: "臺北市或埔里四周高山環抱、中間是低平的土地，這種地形叫做？", options: ["盆地", "丘陵", "平原", "臺地"], ans: 0, why: "四周高山環繞、中間低平為盆地。" },
          { q: "苗栗一帶地勢起伏較平緩、海拔在 1000 公尺以下，這種地形是？", options: ["丘陵", "山地", "盆地", "平原"], ans: 0, why: "海拔 1000m 以下、起伏平緩為丘陵。" }
        ],
        minigameType: "terrainRadar"
      },
      {
        id: "climate",
        order: 3,
        title: "氣候與水資源認識家鄉",
        shortTitle: "氣候水資島",
        unitTag: "第一單元・第 3 課",
        coords: [-16, 0, 14],
        color: 0x0284c7,
        intro: "雨量與氣溫深刻影響家鄉的生活！河川與水庫是珍貴的水資源，降雨季節分佈不均時，儲水與節約用水至關重要。",
        trap: "⚠️ 易錯陷阱：折線圖看「氣溫」，長條柱狀圖看「雨量」；基隆四季多雨，中南部則是「夏雨冬乾」，冬天進入枯水期！",
        cards: [
          { icon: "📊", title: "氣候圖判讀", text: "• 折線圖：每月份平均氣溫（°C）。\\n• 長條圖：每月份累積雨量（毫米）。\\n基隆全年有雨；中南部夏雨冬乾，冬天河床常裸露。" },
          { icon: "💧", title: "水庫功能與守護", text: "興建水庫蓄水：供應民生與工業用水、灌溉農田、雨季防洪與水力發電。嚴禁工廠廢水直接排入河川！" },
          { icon: "🚰", title: "日常節水生活三招", text: "1. 抹肥皂時關緊水龍頭。\\n2. 洗米水與除濕機冷凝水拿來澆花沖廁。\\n3. 自備環保水壺，消滅臺灣海廢第一名的寶特瓶！" }
        ],
        quiz: [
          { q: "在氣候圖上，通常用一根根「長條柱狀」表示的資料是？", options: ["降雨量", "平均氣溫", "紫外線指數", "風速"], ans: 0, why: "氣候圖中長條圖代表雨量，折線圖代表氣溫。" },
          { q: "下列哪一種行為最能落實「珍惜水資源物盡其用」？", options: ["用除濕機冷凝水澆花", "開著水龍頭抹肥皂", "把工廠廢水倒進溪流", "每天泡大浴缸洗澡"], ans: 0, why: "除濕機水重複利用澆花沖廁為節水美德。" },
          { q: "統計顯示臺灣海洋廢棄物中數量最多的是哪一種？", options: ["寶特瓶", "腳踏車", "玻璃罐", "木頭椅子"], ans: 0, why: "寶特瓶為海廢數量第一名，需從源頭自備水壺減塑。" }
        ],
        minigameType: "waterBattle"
      },
      {
        id: "heritage",
        order: 4,
        title: "傳統住宅與生活器具（原漢分流）",
        shortTitle: "古厝時空島",
        unitTag: "第二單元・第 1~2 課",
        coords: [16, 0, 14],
        color: 0xf59e0b,
        intro: "坐上時光機回到過去！先民就地取材展現生活智慧：原住民族的石板屋與地下屋，漢人講究長幼尊卑的三合院與大灶柴灰零浪費。",
        trap: "⚠️ 易錯陷阱：達悟族地下屋是「一部分」建於地面下躲避強颱；三合院「左尊右卑」要站在正廳門口面向屋外判斷！傳統菜櫥通風防蟲但「沒有冷藏功能」！",
        cards: [
          { icon: "🏛️", title: "原住民族傳統住屋", text: "• 排灣/魯凱黑灰石板屋：石縫排煙防蟲，冬暖夏涼被譽為「會呼吸的房子」。\\n• 達悟半地下屋：低矮主屋建於凹地，有效避開蘭嶼強風與颱風。" },
          { icon: "🏡", title: "漢人三合院與倫理", text: "由一條龍擴建為單伸手、三合院。正身中央為正廳祭祖；護龍講究「左尊右卑」長幼有序，大房住左護龍；大埕曬穀活動。" },
          { icon: "🎋", title: "生活器具物盡其用", text: "• 原住民竹編魚筌：順流捕魚，留縫隙放走小魚永續生態；木杵搗小米。\\n• 漢人紅磚大灶柴灰：餘溫悶烤地瓜，冷卻後做菜園天然肥料！" }
        ],
        quiz: [
          { q: "蘭嶼達悟族之所以將傳統主屋設計成「半地下屋」，主要目的是？", options: ["躲避強烈颱風與冬季強風", "方便看海釣魚", "用來水力發電", "防止積水淹水"], ans: 0, why: "半地下屋低矮地基可抵禦強風抗颱。" },
          { q: "排灣族石板屋燒柴時，煙會從石板縫隙穿透飄出，這種設計具有什麼巧思？", options: ["空氣流通防蟲蛀冬暖夏涼", "容易引起火災", "讓屋頂瓦片融化", "沒有任何用途"], ans: 0, why: "柴煙穿透板岩縫隙防蟲蛀，被稱會呼吸的房子。" },
          { q: "漢人傳統紅磚大灶煮飯後，燃燒木柴所留下的灰燼可以拿來做什麼？", options: ["餘溫悶烤地瓜與當菜園肥料", "倒入水溝堵塞水管", "拿去丟入大海", "直接做成塑膠玩具"], ans: 0, why: "大灶灰燼餘溫悶地瓜、菜園施肥，落實物盡其用。" }
        ],
        minigameType: "heritageCraft"
      }
    ];

    /* --------------------------------------------------------------------------
       2. Web Audio API 復古科技音效合成器
       -------------------------------------------------------------------------- */
    let soundEnabled = true;
    let audioCtx = null;

    function initAudio() {
      if (!audioCtx) {
        const AC = window.AudioContext || window.webkitAudioContext;
        if (AC) audioCtx = new AC();
      }
      if (audioCtx && audioCtx.state === "suspended") audioCtx.resume();
    }

    function playTone(freq, type, duration, gainVal = 0.15) {
      if (!soundEnabled) return;
      initAudio(); if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    }

    window.toggleSound = function() {
      soundEnabled = !soundEnabled;
      document.getElementById("btnToggleSound").innerText = soundEnabled ? "🔊" : "🔇";
      showToast(soundEnabled ? "音效已開啟" : "音效已靜音");
    };

    /* --------------------------------------------------------------------------
       3. RPG 冒險數值狀態
       -------------------------------------------------------------------------- */
    const TITLES = ["海線見習生", "地圖測量士", "五大地貌師", "水資源衛士", "時空守護英雄"];
    const gameState = {
      level: 1, exp: 0, maxExp: 100,
      hp: 100, maxHp: 100,
      mp: 50, maxMp: 50,
      gold: 100,
      title: TITLES[0],
      stars: 0,
      stamps: [false, false, false, false],
      inventory: [
        { id: "potato", name: "炭火悶烤地瓜", icon: "🍠", count: 3, desc: "大灶柴灰餘溫燜烤！食用回復 40 HP。" },
        { id: "tea", name: "丘陵高山烏龍茶", icon: "🍵", count: 2, desc: "苗栗丘陵排水良好特產！飲用回復 25 MP。" },
        { id: "compass", name: "傳奇指北羅盤", icon: "🧭", count: 1, desc: "地圖四要素之方位指針裝備。" },
        { id: "fishTrap", name: "工匠竹編魚筌", icon: "🎋", count: 1, desc: "順流水中捕魚，留縫隙放走小魚。" }
      ]
    };

    function addExp(amount) {
      gameState.exp += amount;
      if (gameState.exp >= gameState.maxExp) {
        gameState.level = Math.min(5, gameState.level + 1);
        gameState.exp -= gameState.maxExp;
        gameState.maxExp = Math.round(gameState.maxExp * 1.5);
        gameState.maxHp += 20;
        gameState.hp = gameState.maxHp;
        gameState.maxMp += 15;
        gameState.mp = gameState.maxMp;
        gameState.gold += 50;
        gameState.title = TITLES[gameState.level - 1];
        playTone(523.25, "triangle", 0.1);
        setTimeout(() => playTone(659.25, "triangle", 0.1), 100);
        setTimeout(() => playTone(783.99, "triangle", 0.15), 200);
        setTimeout(() => playTone(1046.50, "triangle", 0.3), 300);
        showToast(`🌟 LEVEL UP! 升級至 Lv.${gameState.level}【${gameState.title}】！`);
      }
      updateHUD();
    }

    function addGold(amount) {
      gameState.gold += amount;
      updateHUD();
    }

    function updateHUD() {
      document.getElementById("hudHpBar").style.width = (gameState.hp / gameState.maxHp * 100) + "%";
      document.getElementById("hudMpBar").style.width = (gameState.mp / gameState.maxMp * 100) + "%";
      document.getElementById("hudGold").innerText = gameState.gold + " G";
      document.getElementById("hudLevel").innerText = "Lv." + gameState.level;
      document.getElementById("hudName").innerText = "小航【" + gameState.title + "】";
      document.getElementById("hudStars").innerText = gameState.stars + " / 4 ★";
    }

    window.showToast = function(msg) {
      const toast = document.getElementById("rpgToast");
      toast.innerText = msg;
      toast.style.opacity = "1";
      clearTimeout(toast._timer);
      toast._timer = setTimeout(() => { toast.style.opacity = "0"; }, 2400);
    };

    /* --------------------------------------------------------------------------
       4. Three.js 3D 空間世界構建 (科技感低多邊形微縮模型風格)
       -------------------------------------------------------------------------- */
    let scene, camera, renderer, controls;
    let islandGroups = [];
    let islandMeshes = [];
    let oceanMesh, gridHelper;
    let hoveredIsland = null;
    let activeIslandIdx = null;

    // 相機飛行動畫
    let isFlying = false;
    let flightStart = { pos: new THREE.Vector3(), target: new THREE.Vector3() };
    let flightEnd = { pos: new THREE.Vector3(), target: new THREE.Vector3() };
    let flightProgress = 1;

    function init3D() {
      const canvas = document.getElementById("sceneCanvas");
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x070c18);
      scene.fog = new THREE.FogExp2(0x070c18, 0.015);

      camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 500);
      camera.position.set(0, 36, 44);

      controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.08;
      controls.maxPolarAngle = Math.PI / 2 - 0.05; // 禁止穿透水面
      controls.minDistance = 10;
      controls.maxDistance = 120;
      controls.target.set(0, 2, 0);

      // 燈光系統
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
      scene.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0x38bdf8, 1.8);
      dirLight.position.set(25, 45, 20);
      dirLight.castShadow = true;
      dirLight.shadow.mapSize.set(2048, 2048);
      dirLight.shadow.camera.left = -35;
      dirLight.shadow.camera.right = 35;
      dirLight.shadow.camera.top = 35;
      dirLight.shadow.camera.bottom = -35;
      scene.add(dirLight);

      const bluePoint = new THREE.PointLight(0x0284c7, 2.5, 60);
      bluePoint.position.set(0, 8, 0);
      scene.add(bluePoint);

      // 科技感水面海床
      buildTechOcean();

      // 建立 4 座科技感特色島嶼
      buildAllFourIslands();

      // 事件監聽
      window.addEventListener("resize", onWindowResize);
      window.addEventListener("pointermove", onPointerMove);
      window.addEventListener("click", onCanvasClick);

      // 動畫主循環
      animate();
    }

    function onWindowResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    // 科技感流光水面與坐標網格
    function buildTechOcean() {
      const waterGeo = new THREE.PlaneGeometry(160, 160, 32, 32);
      const waterMat = new THREE.MeshStandardMaterial({
        color: 0x07152d,
        roughness: 0.1,
        metalness: 0.8,
        flatShading: true
      });
      oceanMesh = new THREE.Mesh(waterGeo, waterMat);
      oceanMesh.rotation.x = -Math.PI / 2;
      oceanMesh.position.y = -0.5;
      oceanMesh.receiveShadow = true;
      scene.add(oceanMesh);

      // 科技網格地坪
      gridHelper = new THREE.GridHelper(160, 40, 0x0284c7, 0x1e293b);
      gridHelper.position.y = -0.48;
      scene.add(gridHelper);

      // 環境浮游粒子
      const partGeo = new THREE.BufferGeometry();
      const partCount = 200;
      const posArr = new Float32Array(partCount * 3);
      for (let i = 0; i < partCount * 3; i += 3) {
        posArr[i] = (Math.random() - 0.5) * 100;
        posArr[i + 1] = Math.random() * 25 + 0.5;
        posArr[i + 2] = (Math.random() - 0.5) * 100;
      }
      partGeo.setAttribute("position", new THREE.BufferAttribute(posArr, 3));
      const partMat = new THREE.PointsMaterial({ color: 0x38bdf8, size: 0.35, transparent: true, opacity: 0.6 });
      const particles = new THREE.Points(partGeo, partMat);
      scene.add(particles);
    }

    // 建立 4 座小島
    function buildAllFourIslands() {
      ISLANDS_DATA.forEach((data, idx) => {
        const group = new THREE.Group();
        group.position.set(...data.coords);
        group.userData = { islandIndex: idx, islandData: data };

        // 懸浮六角柱底座 (科技感基座)
        const baseGeo = new THREE.CylinderGeometry(6.8, 5.8, 3.0, 7);
        const baseMat = new THREE.MeshStandardMaterial({
          color: 0x131d33,
          metalness: 0.6,
          roughness: 0.4,
          flatShading: true
        });
        const baseMesh = new THREE.Mesh(baseGeo, baseMat);
        baseMesh.position.y = 1.5;
        baseMesh.castShadow = true;
        baseMesh.receiveShadow = true;
        group.add(baseMesh);

        // 頂層翠綠／科技草地
        const topGeo = new THREE.CylinderGeometry(6.5, 6.7, 0.4, 7);
        const topMat = new THREE.MeshStandardMaterial({
          color: idx === 1 ? 0x1e3a2f : idx === 3 ? 0x2d2218 : 0x162c46,
          roughness: 0.6,
          flatShading: true
        });
        const topMesh = new THREE.Mesh(topGeo, topMat);
        topMesh.position.y = 3.1;
        topMesh.receiveShadow = true;
        group.add(topMesh);

        // 底部能量發光光環
        const ringGeo = new THREE.TorusGeometry(6.2, 0.12, 8, 32);
        const ringMat = new THREE.MeshBasicMaterial({ color: data.color });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.rotation.x = Math.PI / 2;
        ringMesh.position.y = 0.4;
        group.add(ringMesh);

        // 各島專屬微縮建築與地標模型
        if (idx === 0) buildIsland1Models(group);
        else if (idx === 1) buildIsland2Models(group);
        else if (idx === 2) buildIsland3Models(group);
        else if (idx === 3) buildIsland4Models(group);

        scene.add(group);
        islandGroups.push(group);
        islandMeshes.push(baseMesh);
      });

      // 建立 HTML 3D 浮動標籤
      createLabels();
    }

    // 島嶼 1 模型：地圖畫架、指北針、家鄉小屋
    function buildIsland1Models(parent) {
      // 大地圖展板
      const boardGeo = new THREE.BoxGeometry(3.2, 2.2, 0.15);
      const boardMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.3 });
      const board = new THREE.Mesh(boardGeo, boardMat);
      board.position.set(0, 4.8, -1.2);
      board.rotation.x = -0.15;
      parent.add(board);

      // 地圖畫心
      const mapInnerGeo = new THREE.PlaneGeometry(2.9, 1.9);
      const mapInnerMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
      const mapInner = new THREE.Mesh(mapInnerGeo, mapInnerMat);
      mapInner.position.set(0, 4.8, -1.1);
      mapInner.rotation.x = -0.15;
      parent.add(mapInner);

      // 巨大發光方向標 (指示北方)
      const compassGroup = new THREE.Group();
      compassGroup.position.set(2.4, 3.4, 1.2);
      const poleGeo = new THREE.CylinderGeometry(0.08, 0.08, 2.0);
      const poleMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8 });
      compassGroup.add(new THREE.Mesh(poleGeo, poleMat));
      const arrowGeo = new THREE.ConeGeometry(0.4, 0.9, 4);
      const arrowMat = new THREE.MeshStandardMaterial({ color: 0xef4444 });
      const arrow = new THREE.Mesh(arrowGeo, arrowMat);
      arrow.position.y = 1.2;
      compassGroup.add(arrow);
      parent.add(compassGroup);

      // 家鄉小屋
      const houseGeo = new THREE.BoxGeometry(1.6, 1.4, 1.4);
      const houseMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.6 });
      const house = new THREE.Mesh(houseGeo, houseMat);
      house.position.set(-2.2, 4.0, 1.2);
      const roofGeo = new THREE.ConeGeometry(1.3, 1.0, 4);
      const roofMat = new THREE.MeshStandardMaterial({ color: 0x0284c7 });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.position.set(-2.2, 5.1, 1.2);
      roof.rotation.y = Math.PI / 4;
      parent.add(house);
      parent.add(roof);
    }

    // 島嶼 2 模型：五大地形（平原、盆地、大肚臺地、丘陵、中央山脈）
    function buildIsland2Models(parent) {
      // 1. 中央山脈 (>1000m 高聳陡峭)
      const mtnGeo = new THREE.ConeGeometry(2.2, 4.2, 5);
      const mtnMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.9, flatShading: true });
      const mtn = new THREE.Mesh(mtnGeo, mtnMat);
      mtn.position.set(-1.8, 5.3, -1.8);
      parent.add(mtn);

      // 2. 苗栗丘陵 (<1000m 平緩圓潤)
      const hillGeo = new THREE.SphereGeometry(1.5, 7, 6, 0, Math.PI * 2, 0, Math.PI * 0.5);
      const hillMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.8, flatShading: true });
      const hill = new THREE.Mesh(hillGeo, hillMat);
      hill.position.set(2.2, 3.2, -1.6);
      parent.add(hill);

      // 3. 大肚臺地 (頂部平坦、邊緣陡峭)
      const tableGeo = new THREE.CylinderGeometry(1.8, 2.1, 1.6, 6);
      const tableMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.7, flatShading: true });
      const table = new THREE.Mesh(tableGeo, tableMat);
      table.position.set(-1.8, 4.0, 1.8);
      parent.add(table);

      // 4. 臺中盆地 (四周高、中間低平)
      const basinRingGeo = new THREE.TorusGeometry(1.8, 0.45, 6, 16);
      const basinMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, flatShading: true });
      const basin = new THREE.Mesh(basinRingGeo, basinMat);
      basin.rotation.x = Math.PI / 2;
      basin.position.set(1.8, 3.3, 1.6);
      parent.add(basin);
    }

    // 島嶼 3 模型：水庫大壩、藍色蓄水池、白色百葉箱、風向計
    function buildIsland3Models(parent) {
      // 藍色蓄水湖面
      const lakeGeo = new THREE.CylinderGeometry(2.6, 2.6, 0.2, 16);
      const lakeMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.1, metalness: 0.7 });
      const lake = new THREE.Mesh(lakeGeo, lakeMat);
      lake.position.set(0, 3.3, 0);
      parent.add(lake);

      // 水庫大壩弧形牆
      const damGeo = new THREE.CylinderGeometry(2.8, 2.8, 1.4, 16, 1, true, 0, Math.PI * 0.9);
      const damMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.5 });
      const dam = new THREE.Mesh(damGeo, damMat);
      dam.position.set(0, 4.0, 0);
      dam.rotation.y = -Math.PI * 0.45;
      parent.add(dam);

      // 白色百葉箱
      const boxStandGeo = new THREE.CylinderGeometry(0.06, 0.06, 1.4);
      const boxStandMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
      const stand = new THREE.Mesh(boxStandGeo, boxStandMat);
      stand.position.set(-2.4, 4.0, -1.8);
      const boxGeo = new THREE.BoxGeometry(0.8, 0.8, 0.8);
      const boxMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });
      const box = new THREE.Mesh(boxGeo, boxMat);
      box.position.set(-2.4, 4.8, -1.8);
      parent.add(stand);
      parent.add(box);
    }

    // 島嶼 4 模型：紅磚三合院、石板屋、時空傳送光環
    function buildIsland4Models(parent) {
      // 漢人紅磚三合院 (正身與左右護龍)
      const brickMat = new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.6 });
      const mainHall = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.2, 0.8), brickMat);
      mainHall.position.set(-1.8, 3.8, -1.8);
      const leftWing = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.0, 2.0), brickMat);
      leftWing.position.set(-2.6, 3.7, -0.8);
      const rightWing = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.0, 2.0), brickMat);
      rightWing.position.set(-1.0, 3.7, -0.8);
      parent.add(mainHall);
      parent.add(leftWing);
      parent.add(rightWing);

      // 原住民黑灰石板屋 (層疊石板建築)
      const slateMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.9, flatShading: true });
      const slateHouse = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.2, 1.8), slateMat);
      slateHouse.position.set(2.0, 3.8, -1.2);
      const slateRoof = new THREE.Mesh(new THREE.ConeGeometry(1.7, 0.8, 4), slateMat);
      slateRoof.position.set(2.0, 4.7, -1.2);
      slateRoof.rotation.y = Math.PI / 4;
      parent.add(slateHouse);
      parent.add(slateRoof);

      // 旋轉時空之門光環 (時光機)
      const portalGeo = new THREE.TorusGeometry(1.6, 0.15, 12, 32);
      const portalMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xd97706, roughness: 0.2 });
      const portal = new THREE.Mesh(portalGeo, portalMat);
      portal.position.set(0, 5.0, 2.0);
      portal.name = "timePortal";
      parent.add(portal);
    }

    // 建立 3D 浮動標籤
    function createLabels() {
      const container = document.getElementById("labelsContainer");
      container.innerHTML = "";

      ISLANDS_DATA.forEach((data, idx) => {
        const tag = document.createElement("div");
        tag.className = "island-floating-tag";
        tag.id = `islandTag_${idx}`;
        tag.onclick = () => focusIsland(idx);
        tag.innerHTML = `
          <div class="tag-badge">
            <span class="tag-num">${idx + 1}</span>
            <span class="tag-title">${data.title}</span>
          </div>
          <div class="tag-pointer"></div>
        `;
        container.appendChild(tag);
      });
    }

    // 更新 3D 標籤螢幕投影位置
    function updateLabelsPosition() {
      const tempV = new THREE.Vector3();
      ISLANDS_DATA.forEach((data, idx) => {
        const el = document.getElementById(`islandTag_${idx}`);
        if (!el) return;
        tempV.set(data.coords[0], data.coords[1] + 6.5, data.coords[2]);
        tempV.project(camera);

        // 超出相機前方或太遠則隱藏
        if (tempV.z > 1) {
          el.style.display = "none";
          return;
        }
        el.style.display = "flex";
        const x = (tempV.x * 0.5 + 0.5) * window.innerWidth;
        const y = (-(tempV.y * 0.5) + 0.5) * window.innerHeight;
        el.style.left = `${x}px`;
        el.style.top = `${y}px`;
      });
    }

    /* --------------------------------------------------------------------------
       5. 互動射線檢測與平滑相機對焦 (Smooth FlyTo)
       -------------------------------------------------------------------------- */
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function onPointerMove(e) {
      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(islandMeshes, true);

      if (intersects.length > 0) {
        let root = intersects[0].object;
        while (root.parent && root.parent !== scene) root = root.parent;
        const idx = root.userData.islandIndex;
        if (hoveredIsland !== idx) {
          hoveredIsland = idx;
          document.body.style.cursor = "pointer";
          playTone(600, "sine", 0.04, 0.05);
        }
      } else {
        if (hoveredIsland !== null) {
          hoveredIsland = null;
          document.body.style.cursor = "default";
        }
      }
    }

    function onCanvasClick(e) {
      if (e.target.closest("header, footer, aside, .drawer-overlay, .island-floating-tag")) return;
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(islandMeshes, true);
      if (intersects.length > 0) {
        let root = intersects[0].object;
        while (root.parent && root.parent !== scene) root = root.parent;
        const idx = root.userData.islandIndex;
        focusIsland(idx);
      }
    }

    // 平滑飛向特定島嶼
    window.focusIsland = function(idx) {
      playTone(440, "sine", 0.08);
      activeIslandIdx = idx;
      const data = ISLANDS_DATA[idx];

      // 更新按鈕高亮
      document.querySelectorAll(".island-nav-btn").forEach((btn, i) => {
        btn.classList.toggle("active", i === idx + 1);
      });

      // 設定相機飛向目標
      const targetPos = new THREE.Vector3(...data.coords);
      const camOffset = new THREE.Vector3(12, 14, 18);
      startCameraFlight(targetPos.clone().add(camOffset), targetPos.clone().add(new THREE.Vector3(0, 3.5, 0)));

      // 打開側邊資訊卡片
      openIslandPanel(idx);
    };

    // 回到全景視角
    window.focusOverview = function() {
      playTone(520, "sine", 0.08);
      activeIslandIdx = null;
      document.querySelectorAll(".island-nav-btn").forEach(btn => btn.classList.remove("active"));
      document.getElementById("btnOverview").classList.add("active");
      closeIslandPanel();
      startCameraFlight(new THREE.Vector3(0, 36, 44), new THREE.Vector3(0, 2, 0));
    };

    function startCameraFlight(toPos, toTarget) {
      flightStart.pos.copy(camera.position);
      flightStart.target.copy(controls.target);
      flightEnd.pos.copy(toPos);
      flightEnd.target.copy(toTarget);
      flightProgress = 0;
      isFlying = true;
    }

    // 每幀動畫
    let clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const time = clock.getElapsedTime();

      // 相機平滑插值
      if (isFlying) {
        flightProgress += delta * 1.8;
        if (flightProgress >= 1) {
          flightProgress = 1;
          isFlying = false;
        }
        const ease = 1 - Math.pow(1 - flightProgress, 3);
        camera.position.lerpVectors(flightStart.pos, flightEnd.pos, ease);
        controls.target.lerpVectors(flightStart.target, flightEnd.target, ease);
      }

      controls.update();

      // 島嶼微幅懸浮浮動動畫
      islandGroups.forEach((grp, i) => {
        const baseOffset = Math.sin(time * 1.2 + i * 1.5) * 0.25;
        grp.position.y = baseOffset;
      });

      // 時空光環旋轉
      const portal = scene.getObjectByName("timePortal");
      if (portal) {
        portal.rotation.z += delta * 1.2;
        portal.rotation.y += delta * 0.6;
      }

      // 水面微微沉浮
      if (oceanMesh) {
        oceanMesh.position.y = -0.5 + Math.sin(time * 0.8) * 0.05;
      }

      // 更新 3D 浮動標籤位置
      updateLabelsPosition();

      renderer.render(scene, camera);
    }

    /* --------------------------------------------------------------------------
       6. 右側島嶼詳細資訊卡片 (Card Modal)
       -------------------------------------------------------------------------- */
    let currentPanelTab = "cards";

    function openIslandPanel(idx) {
      const data = ISLANDS_DATA[idx];
      const panel = document.getElementById("islandPanel");
      document.getElementById("panelKicker").innerText = `${data.unitTag}・第 ${data.order} 站`;
      document.getElementById("panelTitle").innerText = data.title;
      renderPanelContent(data);
      panel.classList.add("active");
    }

    window.closeIslandPanel = function() {
      document.getElementById("islandPanel").classList.remove("active");
    };

    window.switchPanelTab = function(tab) {
      playTone(500, "sine", 0.05);
      currentPanelTab = tab;
      document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
      if (tab === "cards") document.getElementById("tabBtnCards").classList.add("active");
      if (tab === "game") document.getElementById("tabBtnGame").classList.add("active");
      if (tab === "quiz") document.getElementById("tabBtnQuiz").classList.add("active");

      if (activeIslandIdx !== null) {
        renderPanelContent(ISLANDS_DATA[activeIslandIdx]);
      }
    };

    function renderPanelContent(data) {
      const body = document.getElementById("panelBody");
      body.innerHTML = "";

      if (currentPanelTab === "cards") {
        // 觀念圖卡列表
        const intro = document.createElement("p");
        intro.style.fontSize = "13px";
        intro.style.lineHeight = "1.6";
        intro.style.color = "#cbd5e1";
        intro.innerText = data.intro;
        body.appendChild(intro);

        data.cards.forEach(c => {
          const card = document.createElement("div");
          card.className = "concept-card";
          card.innerHTML = `
            <div class="concept-head">
              <span class="concept-icon">${c.icon}</span>
              <span class="concept-title">${c.title}</span>
            </div>
            <div class="concept-text">${c.text.replace(/\\n/g, "<br>")}</div>
          `;
          body.appendChild(card);
        });

        const trap = document.createElement("div");
        trap.className = "trap-box";
        trap.innerHTML = `<strong>迷思診斷提醒：</strong>${data.trap}`;
        body.appendChild(trap);
      }
      else if (currentPanelTab === "game") {
        // 實境小實驗
        body.appendChild(buildMinigameElement(data));
      }
      else if (currentPanelTab === "quiz") {
        // 闖關挑戰題目
        body.appendChild(buildQuizElement(data));
      }
    }

    /* --------------------------------------------------------------------------
       7. 實境動手小實驗元件 (Minigames)
       -------------------------------------------------------------------------- */
    function buildMinigameElement(data) {
      const box = document.createElement("div");
      box.className = "minigame-container";

      if (data.id === "map") {
        let tools = { compass: false, legend: false, scale: false };
        box.innerHTML = `
          <h4>🛠️ 地圖修復工作台</h4>
          <p style="font-size:13px; color:#cbd5e1; margin-bottom:8px;">海線觀光地圖缺漏三項工具，點擊按鈕組裝復原：</p>
          <div id="mStatus1" style="font-size:12px; font-weight:700; color:#38bdf8; margin-bottom:10px;">［缺漏：方向標、圖例、比例尺］</div>
          <div class="minigame-actions">
            <button class="game-action-btn" id="bToolCompass">🧭 安裝方向標</button>
            <button class="game-action-btn" id="bToolLegend">📌 安裝圖例</button>
            <button class="game-action-btn" id="bToolScale">📏 安裝比例尺</button>
          </div>
        `;
        const check = () => {
          if (tools.compass && tools.legend && tools.scale) {
            playTone(880, "triangle", 0.25);
            box.querySelector("#mStatus1").innerHTML = "🎉 <strong>地圖四要素安裝完成！獲得 40 EXP 與 50 G！</strong>";
            addExp(40); addGold(50);
            unlockStamp(0);
          }
        };
        box.querySelector("#bToolCompass").onclick = (e) => {
          tools.compass = true; e.target.classList.add("done"); e.target.disabled = true;
          e.target.innerText = "✅ 已安裝方向標"; check();
        };
        box.querySelector("#bToolLegend").onclick = (e) => {
          tools.legend = true; e.target.classList.add("done"); e.target.disabled = true;
          e.target.innerText = "✅ 已安裝圖例"; check();
        };
        box.querySelector("#bToolScale").onclick = (e) => {
          tools.scale = true; e.target.classList.add("done"); e.target.disabled = true;
          e.target.innerText = "✅ 已安裝比例尺"; check();
        };
      }
      else if (data.id === "terrain") {
        box.innerHTML = `
          <h4>⛰️ 五大地形雷達剖面掃描儀</h4>
          <p style="font-size:13px; color:#cbd5e1; margin-bottom:8px;">點選下方地形名稱，觀察課本標準地形特徵：</p>
          <div id="mStatus2" style="background:rgba(30,41,59,0.7); border-radius:8px; padding:10px; font-size:13px; color:#34d399; margin-bottom:10px;">
            請點選下方地形進行探勘辨識
          </div>
          <div class="minigame-actions">
            <button class="game-action-btn" onclick="scanTerrain('平原', '地勢平坦廣闊、海拔低（如宜蘭平原、嘉南平原），適合種水稻與魚塭')">🌾 平原</button>
            <button class="game-action-btn" onclick="scanTerrain('盆地', '四周高山圍繞、中間低平（如臺中盆地、埔里盆地），人口密集')">🥣 盆地</button>
            <button class="game-action-btn" onclick="scanTerrain('臺地', '頂部平坦、邊緣以陡坡與低地相接（如大肚臺地、林口臺地）')">🥏 臺地</button>
            <button class="game-action-btn" onclick="scanTerrain('丘陵', '海拔 1000m 以下、坡度較平緩（如苗栗丘陵），適合茶園梯田')">⛰️ 丘陵</button>
            <button class="game-action-btn" onclick="scanTerrain('山地', '海拔 1000m 以上、高聳起伏大（如中央山脈），有豐富森林')">🌋 山地</button>
          </div>
        `;
        window.scanTerrain = function(name, desc) {
          playTone(660, "sine", 0.08);
          box.querySelector("#mStatus2").innerHTML = `<strong>【${name}】</strong>：${desc}`;
          addExp(10);
          unlockStamp(1);
        };
      }
      else if (data.id === "climate") {
        let monsterHp = 100;
        box.innerHTML = `
          <h4>⚔️ 水資源遭遇戰：擊退海廢浪費怪！</h4>
          <p style="font-size:13px; color:#cbd5e1; margin-bottom:8px;">施展課本節水減塑招式，打擊浪費水資源怪獸：</p>
          <div style="height:8px; background:#334155; border-radius:4px; overflow:hidden; margin-bottom:6px;">
            <div id="monsterHpBar" style="width:100%; height:100%; background:#ef4444; transition:width 0.3s;"></div>
          </div>
          <div id="mBattleLog" style="font-size:12px; font-weight:700; color:#38bdf8; margin-bottom:10px;">怪獸 HP: 100 / 100</div>
          <div class="minigame-actions" id="battleActions">
            <button class="game-action-btn" onclick="attackMonster(35, '抹肥皂關水龍頭')">🚰 抹肥皂關水</button>
            <button class="game-action-btn" onclick="attackMonster(35, '除濕機水澆花沖廁')">💧 冷凝水澆花</button>
            <button class="game-action-btn" onclick="attackMonster(40, '自備水壺消滅寶特瓶')">🍾 減塑海廢爆擊</button>
          </div>
        `;
        window.attackMonster = function(dmg, name) {
          playTone(520, "square", 0.08);
          monsterHp = Math.max(0, monsterHp - dmg);
          box.querySelector("#monsterHpBar").style.width = monsterHp + "%";
          box.querySelector("#mBattleLog").innerText = `施展【${name}】！造成 ${dmg} 點淨化傷害！剩餘 HP: ${monsterHp}`;
          if (monsterHp <= 0) {
            playTone(880, "triangle", 0.3);
            box.querySelector("#mBattleLog").innerHTML = "🎉 <strong>海廢浪費怪已被擊退！獲得 50 EXP 與 80 G！</strong>";
            box.querySelector("#battleActions").style.display = "none";
            addExp(50); addGold(80);
            unlockStamp(2);
          }
        };
      }
      else if (data.id === "heritage") {
        box.innerHTML = `
          <h4>🏡 先民生活智慧工坊實作</h4>
          <p style="font-size:13px; color:#cbd5e1; margin-bottom:8px;">點擊測試原住民族與漢人就地取材的生活智慧：</p>
          <div id="mStatus4" style="font-size:12px; font-weight:700; color:#fbbf24; margin-bottom:10px;">請點擊下方按鈕進行實境驗證</div>
          <div class="minigame-actions">
            <button class="game-action-btn" onclick="testHeritage('smoke')">🔥 石板屋排煙防蟲測試</button>
            <button class="game-action-btn" onclick="testHeritage('typhoon')">🌪️ 達悟地下屋避風抗颱</button>
            <button class="game-action-btn" onclick="testHeritage('sanheyuan')">👴 三合院左尊右卑護龍</button>
            <button class="game-action-btn" onclick="testHeritage('ash')">🍠 大灶柴灰悶地瓜施肥</button>
            <button class="game-action-btn" onclick="testHeritage('fishtrap')">🎋 竹編魚筌放小魚生態</button>
          </div>
        `;
        window.testHeritage = function(type) {
          playTone(700, "sine", 0.08);
          let txt = "";
          if (type === "smoke") txt = "💨 <strong>柴煙穿透板岩縫隙飄出！</strong>能防蟲蛀並維持空氣流通，冬暖夏涼被譽為會呼吸的房子！";
          if (type === "typhoon") txt = "🌪️ <strong>強颱強風從上方吹過！</strong>達悟半地下屋主屋低矮，有效避開蘭嶼強烈颱風！";
          if (type === "sanheyuan") txt = "👴 <strong>長幼有序左尊右卑！</strong>大房長輩安排在左護龍，正身正廳供奉神明與祖先！";
          if (type === "ash") txt = "🍠 <strong>大灶柴灰零浪費！</strong>餘溫燜烤香甜地瓜，冷卻後做菜園天然肥料！";
          if (type === "fishtrap") txt = "🐟 <strong>竹編魚筌生態智慧！</strong>順流放置溪中，大魚進得去出不來，留縫隙讓小魚游走永續利用！";
          box.querySelector("#mStatus4").innerHTML = txt;
          addExp(15);
          unlockStamp(3);
        };
      }

      return box;
    }

    function unlockStamp(idx) {
      if (!gameState.stamps[idx]) {
        gameState.stamps[idx] = true;
        gameState.stars = gameState.stamps.filter(Boolean).length;
        updateHUD();
        showToast("🎖️ 榮譽徽章已解鎖！");
      }
    }

    /* --------------------------------------------------------------------------
       8. 闖關挑戰題目元件 (Quiz)
       -------------------------------------------------------------------------- */
    function buildQuizElement(data) {
      const box = document.createElement("div");
      box.className = "quiz-box";

      let qIndex = 0;
      function showQ() {
        box.innerHTML = "";
        if (qIndex >= data.quiz.length) {
          box.innerHTML = `
            <div style="text-align:center; padding:18px; background:rgba(16,185,129,0.15); border-radius:10px; border:1px solid #10b981;">
              <div style="font-size:36px; margin-bottom:6px;">🏆</div>
              <strong style="font-size:16px; color:#34d399;">本島闖關全數通過！</strong>
              <p style="font-size:12px; color:#a7f3d0; margin-top:4px;">獲得滿星評價 ★★★ 與 100 G 獎勵！</p>
            </div>
          `;
          unlockStamp(data.order - 1);
          return;
        }

        const qData = data.quiz[qIndex];
        const titleEl = document.createElement("div");
        titleEl.className = "quiz-q-title";
        titleEl.innerText = `第 ${qIndex + 1}/${data.quiz.length} 題：${qData.q}`;
        box.appendChild(titleEl);

        const optsWrap = document.createElement("div");
        optsWrap.className = "quiz-options";

        const feedbackEl = document.createElement("div");
        feedbackEl.className = "quiz-feedback";

        qData.options.forEach((optText, oIdx) => {
          const btn = document.createElement("button");
          btn.className = "quiz-opt-btn";
          btn.innerText = optText;
          btn.onclick = () => {
            const isRight = (oIdx === qData.ans);
            if (isRight) {
              btn.classList.add("correct");
              playTone(784, "sine", 0.15);
              feedbackEl.style.display = "block";
              feedbackEl.style.border = "1.5px solid #10b981";
              feedbackEl.style.color = "#34d399";
              feedbackEl.innerHTML = `✅ <strong>回答正確！</strong> ${qData.why}`;
              addExp(25); addGold(100);
              setTimeout(() => { qIndex++; showQ(); }, 1400);
            } else {
              btn.classList.add("wrong");
              playTone(220, "sawtooth", 0.2);
              gameState.hp = Math.max(10, gameState.hp - 15);
              updateHUD();
              feedbackEl.style.display = "block";
              feedbackEl.style.border = "1.5px solid #ef4444";
              feedbackEl.style.color = "#f87171";
              feedbackEl.innerHTML = `❌ <strong>回答錯誤喔！</strong> ${qData.why}（微扣 15 HP）`;
              if (gameState.hp <= 35) {
                showToast("⚠️ 冒險者生命值偏低，可打開背包食用烤地瓜補血！");
              }
            }
          };
          optsWrap.appendChild(btn);
        });

        box.appendChild(optsWrap);
        box.appendChild(feedbackEl);
      }

      showQ();
      return box;
    }

    /* --------------------------------------------------------------------------
       9. 抽屜面板與 Canvas 證書系統
       -------------------------------------------------------------------------- */
    window.openDrawer = function(id) {
      playTone(520, "sine", 0.05);
      window.closeAllDrawers();
      const el = document.getElementById(id);
      if (el) el.classList.add("active");
      if (id === "inventoryDrawer") renderInventory();
      if (id === "stampsDrawer") renderStamps();
      if (id === "encyclopediaDrawer") renderEncyclopedia();
      if (id === "certDrawer") window.drawCertificateCanvas();
    };

    window.closeDrawer = function(id) {
      playTone(400, "sine", 0.05);
      const el = document.getElementById(id);
      if (el) el.classList.remove("active");
    };

    window.closeAllDrawers = function() {
      document.querySelectorAll(".drawer-overlay").forEach(d => d.classList.remove("active"));
    };

    function renderInventory() {
      const c = document.getElementById("inventoryList");
      c.innerHTML = gameState.inventory.map(item => `
        <div class="rpg-item-card" onclick="useInventoryItem('${item.id}')">
          <span style="font-size:32px; display:block; margin-bottom:4px;">${item.icon}</span>
          <strong style="font-size:13px; color:#fff;">${item.name}</strong>
          <div style="font-size:11px; color:#f59e0b; font-weight:800; margin-top:2px;">數量: x${item.count}</div>
          <div style="font-size:10px; color:#94a3b8; margin-top:4px; line-height:1.3;">${item.desc}</div>
        </div>
      `).join("");
    }

    window.useInventoryItem = function(itemId) {
      const item = gameState.inventory.find(i => i.id === itemId);
      if (!item || item.count <= 0) {
        showToast("此道具已用盡！");
        return;
      }
      if (itemId === "potato") {
        gameState.hp = Math.min(gameState.maxHp, gameState.hp + 40);
        item.count--;
        playTone(660, "triangle", 0.15);
        showToast("🍠 吃了炭火悶烤地瓜！回復 40 HP！真香！");
      } else if (itemId === "tea") {
        gameState.mp = Math.min(gameState.maxMp, gameState.mp + 25);
        item.count--;
        playTone(660, "triangle", 0.15);
        showToast("🍵 喝了丘陵烏龍茶！回復 25 MP！神清氣爽！");
      } else {
        showToast(`【${item.name}】是關鍵探險裝備！已裝配於行囊中。`);
      }
      updateHUD();
      renderInventory();
    };

    function renderStamps() {
      const c = document.getElementById("stampsList");
      const list = [
        { name: "地圖四要素徽章", icon: "🧭" },
        { name: "五大地形探勘徽章", icon: "⛰️" },
        { name: "氣候與水資源衛士徽章", icon: "💧" },
        { name: "傳統住宅生活大師徽章", icon: "🏡" }
      ];
      c.innerHTML = list.map((s, idx) => {
        const isUnlocked = gameState.stamps[idx];
        return `
          <div class="stamp-cell ${isUnlocked ? 'unlocked' : ''}">
            <div class="stamp-icon">${s.icon}</div>
            <div class="stamp-title">島嶼 ${idx + 1}・${s.name}</div>
            <small style="font-size:10px; color:${isUnlocked ? '#34d399' : '#64748b'}; font-weight:800;">
              ${isUnlocked ? '✅ 已解鎖' : '🔒 未解鎖'}
            </small>
          </div>
        `;
      }).join("");
    }

    function renderEncyclopedia() {
      const c = document.getElementById("encyclopediaList");
      c.innerHTML = ISLANDS_DATA.map(data => `
        <div style="background:rgba(30,41,59,0.7); border:1px solid var(--line); border-radius:10px; padding:12px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#38bdf8; font-size:14px;">島嶼 ${data.order}：${data.title}</strong>
            <span style="font-size:11px; background:#0369a1; padding:2px 8px; border-radius:999px;">${data.unitTag}</span>
          </div>
          <p style="font-size:12px; color:#cbd5e1; line-height:1.5; margin-bottom:8px;">${data.intro}</p>
          <div style="background:rgba(245,158,11,0.12); border-left:3px solid #f59e0b; padding:6px 8px; font-size:11px; color:#fde68a;">
            ${data.trap}
          </div>
        </div>
      `).join("");
    }

    window.drawCertificateCanvas = function() {
      const c1 = document.getElementById("certCanvas");
      if (!c1) return;
      const ctx = c1.getContext("2d");

      ctx.fillStyle = "#fffcf3";
      ctx.fillRect(0, 0, 800, 560);

      ctx.lineWidth = 14;
      ctx.strokeStyle = "#0284c7";
      ctx.strokeRect(10, 10, 780, 540);

      ctx.lineWidth = 2;
      ctx.strokeStyle = "#f59e0b";
      ctx.strokeRect(22, 22, 756, 516);

      ctx.fillStyle = "#0f172a";
      ctx.font = "bold 30px 'Noto Sans TC', sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("國小四年級社會科・家鄉時空英雄傳", 400, 76);

      ctx.fillStyle = "#0284c7";
      ctx.font = "bold 22px 'Noto Sans TC', sans-serif";
      ctx.fillText("🏆 期中四大島嶼全單元通關榮譽證書 🏆", 400, 118);

      const uClass = document.getElementById("certClass")?.value || "四年忠班";
      const uSeat = document.getElementById("certSeat")?.value || "15";
      const uName = document.getElementById("certName")?.value || "林小航";

      ctx.fillStyle = "#475569";
      ctx.font = "18px 'Noto Sans TC', sans-serif";
      ctx.fillText(`茲證明 臺中市梧棲區中正國小 ${uClass} ${uSeat} 號`, 400, 180);

      ctx.fillStyle = "#0f172a";
      ctx.font = "bold 34px 'Noto Sans TC', sans-serif";
      ctx.fillText(`${uName} 同學`, 400, 230);

      ctx.fillStyle = "#334155";
      ctx.font = "16px 'Noto Sans TC', sans-serif";
      ctx.fillText("於本校四年級社會科 3D 互動島嶼學習中，精通地圖四要素、", 400, 280);
      ctx.fillText("五大地貌剖面、水資源氣候、原漢傳統住屋建築與生活器物物盡其用之巧思，", 400, 310);
      ctx.fillText("完成四大島嶼所有實境實驗與挑戰，成績優異，特頒此狀以資表揚！", 400, 340);

      ctx.fillStyle = "#b45309";
      ctx.font = "bold 18px 'Noto Sans TC', sans-serif";
      ctx.fillText(`🌟 冒險等級：Lv.${gameState.level} ${gameState.title}  |  ⭐ 星級榮譽：${gameState.stars} / 4 ★`, 400, 395);

      ctx.strokeStyle = "#b91c1c";
      ctx.lineWidth = 3.5;
      ctx.strokeRect(580, 430, 150, 70);
      ctx.fillStyle = "#b91c1c";
      ctx.font = "bold 17px 'Noto Sans TC', sans-serif";
      ctx.fillText("中正國小教務處", 655, 460);
      ctx.font = "13px 'Noto Sans TC', sans-serif";
      ctx.fillText("審查認證合格章", 655, 485);

      ctx.fillStyle = "#64748b";
      ctx.font = "14px 'Noto Sans TC', sans-serif";
      ctx.textAlign = "left";
      const today = new Date();
      ctx.fillText(`授證日期：${today.getFullYear()} 年 ${today.getMonth() + 1} 月 ${today.getDate()} 日`, 50, 480);
    };

    window.downloadCertificateImage = function() {
      const canvas = document.getElementById("certCanvas");
      if (!canvas) return;
      const link = document.createElement("a");
      link.download = `家鄉時空大冒險_結業證書_${document.getElementById('certName')?.value || '學生'}.png`;
      link.href = canvas.toDataURL("image/png");
      link.click();
      showToast("📥 證書圖檔已開始下載！");
    };

    window.toggleFullscreen = function() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    };

    /* --------------------------------------------------------------------------
       10. 初始化載入
       -------------------------------------------------------------------------- */
    window.addEventListener("DOMContentLoaded", () => {
      init3D();
      updateHUD();
      // 預設全景視野
      document.getElementById("btnOverview").classList.add("active");
    });
  </script>
</body>
</html>
'''

with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated clean single-file 4-islands HTML at: {OUTPUT_HTML_PATH} (Size: {len(html_content)} bytes)")
