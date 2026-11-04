import re

HTML_PATH = "/Users/tunyuan/Library/CloudStorage/GoogleDrive-asc103138@st.tc.edu.tw/我的雲端硬碟/115四上期中社會複習遊戲/index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove the mindmap section inside openZone
target_mm_render = """      const maps = MINDMAPS.filter(m => m.zones.includes(z.id));
      if (maps.length) body.append(el('section', { class: 'mm-zone' },
        el('h3', {}, '📜 本課重點圖卡・可重新下載'),
        el('div', { class: `cards mm-cards n${maps.length}` }, ...maps.map(mindmapCard))));"""
if target_mm_render in html:
    html = html.replace(target_mm_render, "")
    print("Removed mm-zone rendering inside openZone!")
else:
    # regex fallback
    html = re.sub(r'const maps = MINDMAPS\.filter\(.*?\);\s*if \(maps\.length\) body\.append\(.*?\);', '', html, flags=re.DOTALL)
    print("Regex removed mm-zone rendering!")

# 2. Remove purchaseNotice from body.append(questBox, purchaseNotice());
html = html.replace("body.append(questBox, purchaseNotice());", "body.append(questBox);")
html = html.replace("body.append(purchaseNotice());", "")

# 3. Remove mindmapCard, openMindmaps and purchaseNotice functions
target_funcs = """// 圖卡項目
function mindmapCard(m) {
  return el('article', { class: 'card mm-card' },
    el('a', { class: 'img-wrap', href: m.article, target: '_blank', rel: 'noopener', 'aria-label': `${m.title}（開新分頁）` },
      el('img', { src: m.image, alt: `${m.title} 課文整理封面`, width: '923', height: '1000' })),
    el('div', { class: 'card-text' },
      el('span', { class: `mm-lesson ${m.unit}` }, `${UNITS[m.unit].tag}・${m.id}`),
      el('h3', {}, m.title),
      el('p', {}, m.summary),
      el('div', { class: 'mm-actions' },
        el('a', { class: 'tool mm-open', href: m.article, target: '_blank', rel: 'noopener' }, m.paid ? '看整理' : '看整理・下載'),
        el('a', { class: 'mm-file', href: m.file, target: '_blank', rel: 'noopener' }, m.paid ? `購買${m.kind}` : `直接開啟${m.kind}`))));
}

function openMindmaps() {}
// mindmaps removed

// 講義免費索取：每個面板都提示加入 LINE 官方帳號
function purchaseNotice() { return document.createComment(''); }"""

if target_funcs in html:
    html = html.replace(target_funcs, "")
    print("Removed target_funcs cleanly!")
else:
    html = re.sub(r'function mindmapCard\(m\) \{.*?\n\}\n*', '', html, flags=re.DOTALL)
    html = re.sub(r'function openMindmaps\(\) \{\}\n*', '', html, flags=re.DOTALL)
    html = re.sub(r'function purchaseNotice\(\) \{.*?\n\}\n*', '', html, flags=re.DOTALL)
    print("Regex removed target_funcs!")

# 4. In HTML header, replace buy-long and buy-short with clean text
html = html.replace('<span class="buy-long">十站清單</span><span class="buy-short">地點</span>', '十站地點')

# 5. Clean CSS for buy and mm
html = re.sub(r'/\* ---------- 學習指引提示 ---------- \*/.*?(?=/\* ---------- 自然島)', '', html, flags=re.DOTALL)
html = re.sub(r'html\[data-mode="night"\] \.buy-notice \{.*?\}', '', html)
html = re.sub(r'html\[data-mode="night"\] \.buy-notice p \{.*?\}', '', html)
html = re.sub(r'html\[data-mode="night"\] \.buy-link, html\[data-mode="night"\] \.buy-cta \{.*?\}', '', html)
html = re.sub(r'html\[data-mode="night"\] \.buy-link:hover, html\[data-mode="night"\] \.buy-cta:hover \{.*?\}', '', html)
html = re.sub(r'/\* 圖卡列表樣式 \*/.*?(?=/\* ---------- 關卡面板)', '', html, flags=re.DOTALL)

# 6. Ensure const MINDMAPS and const PURCHASE are completely removed from JS
html = re.sub(r'const PURCHASE = \{.*?\};\n*', '', html, flags=re.DOTALL)
html = re.sub(r'const MINDMAPS = \[.*?\];\n*', '', html, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Purge completed successfully! New index.html size:", len(html))
