#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
將 temp_unit3_base.html 轉換為獨立的「康軒四上社會 第三單元：家鄉的信仰與老街」3D 島嶼地圖：
- 輸出至 unit3/index.html 與 unit3.html
- 地圖僅含兩座島嶼：「傳統信仰島」(faith, 1~4關) 與「家鄉老街島」(oldstreet, 5~8關)
- 「泰雅祖靈彩虹橋」(guardian) 不設島嶼，直接以巨型規模飄浮於海面上進行全島導覽（如同前一檔案之方向標海龜）
"""
import os
import re

with open("temp_unit3_base.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. 更新 <title> 與頂部品牌標題、星星總數 (8關 = 24 ★)、按鈕文字
html = html.replace(
    "<title>康軒四上 社會島・家鄉時空英雄傳 3D 沉浸 RPG 冒險</title>",
    "<title>康軒四上 社會島（第三單元）・傳統信仰島 ✕ 家鄉老街島 ✕ 海上祖靈彩虹橋導覽</title>"
)
html = html.replace(
    "<strong>康軒四上 社會島・家鄉時空英雄傳</strong>\n        <small>期中全單元實境複習｜第一單元 家鄉環境 ✕ 第二單元 傳統生活</small>",
    "<strong>康軒四上 社會島・第三單元時空英雄傳</strong>\n        <small>第三單元實境複習｜傳統信仰島 ✕ 家鄉老街島 ✕ 海上彩虹橋導覽</small>"
)
html = html.replace(
    '<span id="hudStarsText">0 / 72 ★</span>',
    '<span id="hudStarsText">0 / 24 ★</span>'
)
html = html.replace(
    '>二十四站全島地點</button>',
    '>八大關卡與彩虹橋</button>'
)
html = html.replace(
    '<span class="rpg-name-text" id="hudTitleText">小航【海線見習生】</span>',
    '<span class="rpg-name-text" id="hudTitleText">小航【信仰見習生】</span>'
)

# 2. 更新 CSS 以支援 faith 與 oldstreet 標籤顏色
css_target = """.scene-label.faction-change .badge, .place-list .change .badge, .panel-kicker .tag.change { background: color-mix(in srgb, var(--change) 68%, #062a3a); }"""
css_replacement = """.scene-label.faction-change .badge, .place-list .change .badge, .panel-kicker .tag.change { background: color-mix(in srgb, var(--change) 68%, #062a3a); }
.scene-label.faction-faith .badge, .place-list .faith .badge, .panel-kicker .tag.faith { background: #c84b31; color: #fff; }
.scene-label.faction-oldstreet .badge, .place-list .oldstreet .badge, .panel-kicker .tag.oldstreet { background: #24587a; color: #fff; }
.scene-label.faction-guardian .badge { background: linear-gradient(135deg, #e85d56, #f2994a, #4ea871, #6b7fd7); color: #fff; }"""
assert css_target in html, "CSS target not found"
html = html.replace(css_target, css_replacement, 1)

# 3. 更新底部快捷列 (1~8關 + 彩虹橋導覽)
footer_pattern = re.compile(
    r'<footer class="bottombar".*?</footer>',
    re.DOTALL
)
new_footer = """<footer class="bottombar" style="gap:6px; flex-wrap:wrap; height:auto; min-height:var(--bottom); padding:6px 14px;">
    <div style="display:flex; gap:5px; align-items:center; overflow-x:auto; max-width:calc(100vw - 260px); padding-bottom:2px;">
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('indigenous_ritual')">1.原民祭儀</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('folk_deity')">2.守護神廟宇</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('temple_fair')">3.迎神賽會</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('eco_worship')">4.環保祭祀</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('river_port')">5.河運渡口</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('shophouse')">6.長條街屋</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('indigo_craft')">7.三峽藍染</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 10px;" onclick="window.goStationFast('street_revival')">8.老街保存</button>
      <button type="button" class="tool" style="font-size:12.5px; padding:4px 11px; font-weight:800; background:#fdf2f8; border-color:#db2777; color:#9d174d;" onclick="window.openGuardianFast()">🌈 祖靈彩虹橋（導覽）</button>
    </div>
    <div class="controls">
      <button type="button" class="tool" id="btn-home">↺ 全景</button>
      <button type="button" class="tool" id="btn-pause" aria-pressed="false">暫停</button>
      <div class="zoom" role="group" aria-label="縮放">
        <button type="button" class="tool icon" id="btn-zoom-out" aria-label="縮小">−</button>
        <button type="button" class="tool icon" id="btn-zoom-in" aria-label="放大">＋</button>
      </div>
    </div>
  </footer>"""
assert footer_pattern.search(html), "Footer pattern not found"
html = footer_pattern.sub(new_footer, html, count=1)

# 4. 更新 __content：僅保留第三單元兩課 (faith, oldstreet) 與第 1~8 關，並將 RAINBOW_GUIDE_DATA 獨立供導覽使用
content_start = html.index("const __content = (() => {")
content_end = html.index("// ---- src/runtime-kit/terrain.mjs ----")

# 從原本 html 中擷取 indigenous_ritual 到 rainbow_bridge 的區塊
z16_idx = html.index("  {\n    id: 'indigenous_ritual'")
z_end_idx = html.index("const ISLANDS = [", z16_idx)
unit3_zones_raw = html[z16_idx:z_end_idx]

# 將 order 16..23 改為 1..8，並分離 rainbow_bridge 作為 RAINBOW_GUIDE_DATA
rb_split_idx = unit3_zones_raw.index("  {\n    id: 'rainbow_bridge'")
eight_zones_str = unit3_zones_raw[:rb_split_idx].rstrip()
if eight_zones_str.endswith(","):
    eight_zones_str = eight_zones_str[:-1]

rainbow_zone_str = unit3_zones_raw[rb_split_idx:].strip()
# 移除最後的 ];
if rainbow_zone_str.endswith("];"):
    rainbow_zone_str = rainbow_zone_str[:-2].strip()
if rainbow_zone_str.endswith(","):
    rainbow_zone_str = rainbow_zone_str[:-1].strip()

for old_ord, new_ord in [(16, 1), (17, 2), (18, 3), (19, 4), (20, 5), (21, 6), (22, 7), (23, 8)]:
    eight_zones_str = eight_zones_str.replace(f"order: {old_ord},", f"order: {new_ord},")

new_content_module = f"""const __content = (() => {{
const UNITS = {{
  faith: {{ name: '家鄉的傳統信仰', tag: '第三單元 第1課' }},
  oldstreet: {{ name: '家鄉的老街', tag: '第三單元 第2課' }},
}};

const ZONES = [
{eight_zones_str}
];

const RAINBOW_GUIDE = {rainbow_zone_str};

const ISLANDS = [
  {{ id: 'faith', name: '傳統信仰島', note: '第三單元第 1 課（第 1～4 關）：原住民族歲時祭儀、漢人守護神與廟宇、迎神賽會陣頭文化、現代環保誠心祭祀' }},
  {{ id: 'oldstreet', name: '家鄉老街島', note: '第三單元第 2 課（第 5～8 關）：河運渡口與老街起源、紅磚長條街屋與騎樓、三峽傳統藍染工坊、老街轉型與文創保存' }},
];

return {{ UNITS, ZONES, ISLANDS, RAINBOW_GUIDE }};
}})();
"""

html = html[:content_start] + new_content_module + html[content_end:]

# 5. 更新 __world：僅建立傳統信仰島 (faith, 西島) 與家鄉老街島 (oldstreet, 東島)，無彩虹橋島！
world_start = html.index("const __world = (() => {")
world_end = html.index("// ---- src/residents.js ----")

new_world_module = """const __world = (() => {
// 世界布局（第三單元專屬地圖）：
// 西邊「傳統信仰島」是第三單元第 1 課四站：原民歲時祭儀、漢人守護神與廟宇、迎神賽會陣頭、現代環保祭祀；
// 東邊「家鄉老街島」是第三單元第 2 課四站：河運渡口起源、紅磚長條街屋、三峽傳統藍染、老街保存與文創。
// 兩座島以跨海拱橋相連；南方海面則直接飄浮著巨型看門獸「Hakaw Utux 泰雅祖靈彩虹橋」負責全島導覽。
const { createIslandTerrain } = __terrain;
const { createIslandPath, validateIslandConnections } = __paths;
const {
  mat, fixedMat, at, ball, cyl, tree, mountain, cloud,
  indigenousRitual, folkDeityTemple, templeFair, ecoWorship,
  riverPort, shophouseBaroque, indigoDyeWorkshop, streetRevival,
} = __models;

const WATER_LEVEL = -0.24;
const S = 1.3;
const LANDMARK_SCALE = 1.45;

// 微微起伏的自然島嶼海岸線
const blob = (cx, cz, r, wobble, phase, count = 18) => Array.from({ length: count }, (_, i) => {
  const a = i / count * Math.PI * 2;
  const rr = r + wobble * Math.sin(3 * a + phase) + wobble * 0.5 * Math.sin(5 * a + phase * 2);
  return [cx + Math.cos(a) * rr, cz + Math.sin(a) * rr];
});

const LAYOUT = {
  faith: {
    outline: blob(-7.8, -0.8, 6.6, 0.35, 0.8),
    plateaus: [
      { position: [-11.0, 1.4, -3.8], radius: 1.5 },   // 1 原民歲時祭儀（北側山麓）
      { position: [-4.6, 1.4, -3.8], radius: 1.6 },    // 2 守護神與廟宇
      { position: [-4.6, 1.4, 2.2], radius: 1.5 },     // 3 廟會陣頭文化
      { position: [-11.0, 1.4, 2.2], radius: 1.5 },    // 4 現代環保祭祀
      { position: [-7.8, 1.4, -0.8], radius: 1.1 },    // 信仰中央廣場 fj
      { position: [-2.2, 1.4, -0.8], radius: 0.85 },   // 東岸跨海橋頭
    ],
  },
  oldstreet: {
    outline: blob(7.8, -0.8, 6.6, 0.35, 1.6),
    plateaus: [
      { position: [4.6, 1.4, 2.4], radius: 1.5 },      // 5 河運渡口起源（西南臨水灣）
      { position: [11.0, 1.4, -3.8], radius: 1.6 },    // 6 紅磚長條街屋
      { position: [4.6, 1.4, -3.8], radius: 1.5 },     // 7 三峽傳統藍染
      { position: [11.0, 1.4, 2.2], radius: 1.5 },     // 8 老街保存文創
      { position: [7.8, 1.4, -0.8], radius: 1.1 },     // 老街中央廣場 oj
      { position: [2.2, 1.4, -0.8], radius: 0.85 },    // 西岸跨海橋頭
    ],
  },
};
for (const def of Object.values(LAYOUT)) {
  def.outline = def.outline.map(([x, z]) => [x * S, z * S]);
  def.plateaus = def.plateaus.map(({ position: [x, y, z], radius }) => ({ position: [x * S, y, z * S], radius: radius * S }));
}
const sxz = ([x, z]) => [x * S, z * S];

// 地點節點（前庭）與地標位置；地標正面朝向節點
const SITES = {
  indigenous_ritual: { building: indigenousRitual, at: [-11.0, -3.8], node: [-9.4, -2.4], island: 'faith', scale: 1.0 },
  folk_deity: { building: folkDeityTemple, at: [-4.6, -3.8], node: [-6.2, -2.4], island: 'faith', scale: 1.0 },
  temple_fair: { building: templeFair, at: [-4.6, 2.2], node: [-6.2, 0.8], island: 'faith', scale: 1.0 },
  eco_worship: { building: ecoWorship, at: [-11.0, 2.2], node: [-9.4, 0.8], island: 'faith', scale: 1.0 },
  river_port: { building: riverPort, at: [4.6, 2.4], node: [6.2, 0.9], island: 'oldstreet', scale: 1.0 },
  shophouse: { building: shophouseBaroque, at: [11.0, -3.8], node: [9.4, -2.4], island: 'oldstreet', scale: 1.0 },
  indigo_craft: { building: indigoDyeWorkshop, at: [4.6, -3.8], node: [6.2, -2.4], island: 'oldstreet', scale: 1.0 },
  street_revival: { building: streetRevival, at: [11.0, 2.2], node: [9.4, 0.8], island: 'oldstreet', scale: 1.0 },
};
const JUNCTIONS = { fj: [-7.8, -0.8], oj: [7.8, -0.8] };

// 跨海通道：[id, 起島, 起點種子, 終島, 終點種子]
const BRIDGES = [
  ['faith-oldstreet', 'faith', [-2.0, -0.8], 'oldstreet', [2.0, -0.8]],
];

// 島內道路（自然曲線，經過中途點）
const ROADS = [
  ['indigenous_ritual', 'fj', []],
  ['folk_deity', 'fj', []],
  ['temple_fair', 'fj', []],
  ['eco_worship', 'fj', []],
  ['fj', 'faith-oldstreet:a', [[-4.8, -0.8]]],
  ['faith-oldstreet:b', 'oj', [[4.8, -0.8]]],
  ['oj', 'river_port', []],
  ['oj', 'shophouse', []],
  ['oj', 'indigo_craft', []],
  ['oj', 'street_revival', []],
];

// 信仰島北側山巒（呼應原住民族山林祭儀背景）
const MOUNTAINS = [[-12.2, -5.6, 1.05, 2.2], [-7.8, -6.0, 1.25, 2.6]]
  .map(([x, z, r, h]) => [x * S, z * S, r * S, h * 1.3]);
for (const s of Object.values(SITES)) { s.at = sxz(s.at); s.node = sxz(s.node); s.scale *= LANDMARK_SCALE; }
for (const k of Object.keys(JUNCTIONS)) JUNCTIONS[k] = sxz(JUNCTIONS[k]);
for (const r of ROADS) r[2] = r[2].map(sxz);

function buildWorld(scene, palette) {
  const world = new THREE.Group();
  world.name = 'world-root';
  scene.add(world);

  const terrains = {};
  for (const [id, def] of Object.entries(LAYOUT)) {
    let gColor = palette.lawn, bColor = palette.shore;
    if (id === 'faith') { gColor = '#d4b886'; bColor = '#9c7a4c'; }
    else if (id === 'oldstreet') { gColor = '#c79d79'; bColor = '#8c6244'; }
    terrains[id] = createIslandTerrain(THREE, {
      id, outline: def.outline, plateaus: def.plateaus, waterLevel: WATER_LEVEL,
      groundColor: gColor, bankColor: bColor,
      gridSize: 0.25,
    });
    world.add(terrains[id].group);
  }
  const islandOf = (x, z) => Object.keys(terrains).find(id => terrains[id].contains(x, z));
  const surface = (x, z) => {
    const id = islandOf(x, z);
    return id ? terrains[id].surfaceAt(x, z) : null;
  };

  // ---------- 橋：從兩岸實際可走地面找落點 ----------
  const shoreToward = (terrain, from, to) => {
    const dir = new THREE.Vector2(to[0] - from[0], to[1] - from[1]).normalize();
    const p = new THREE.Vector2(...from);
    while (terrain.contains(p.x, p.y)) p.addScaledVector(dir, 0.05);
    p.addScaledVector(dir, -0.4);
    return [p.x, terrain.surfaceAt(p.x, p.y), p.y];
  };
  const nodes = {};
  const bridges = [];
  for (const [id, fromId, fromSeed, toId, toSeed] of BRIDGES) {
    const a = shoreToward(terrains[fromId], sxz(fromSeed), sxz(toSeed));
    const b = shoreToward(terrains[toId], sxz(toSeed), sxz(fromSeed));
    const bridge = createIslandPath(THREE, {
      id, fromIslandId: fromId, toIslandId: toId, from: a, to: b, width: 1.6, kind: 'bridge', archHeight: 0.55,
      colors: { deck: '#b85d3b', rail: '#fff8eb', post: '#d97706' },
    });
    world.add(bridge.group);
    bridges.push(bridge);
    nodes[`${id}:a`] = { id: `${id}:a`, x: a[0], z: a[2] };
    nodes[`${id}:b`] = { id: `${id}:b`, x: b[0], z: b[2] };
    // 橋頭傳統宮燈路燈
    for (const end of [bridge.start, bridge.end]) {
      const toward = (end === bridge.start ? bridge.end : bridge.start).clone().sub(end).setY(0).normalize();
      const side = new THREE.Vector3(-toward.z, 0, toward.x);
      for (const s of [-1, 1]) {
        const post = new THREE.Group();
        post.add(at(cyl(0.06, 0.07, 1.35, 6, fixedMat('#9b2f22')), 0, 0.67, 0));
        const lamp = ball(0.2, fixedMat('#ffedd5', { emissive: '#f59e0b', emissiveIntensity: 0.6 }), 10, 8);
        post.add(at(lamp, 0, 1.45, 0));
        post.position.copy(end).addScaledVector(side, s * 0.95).addScaledVector(toward, 0.15);
        world.add(post);
      }
    }
  }
  const connectionCheck = validateIslandConnections(Object.keys(LAYOUT), bridges, 'faith');

  // ---------- 節點與路網 ----------
  for (const [id, s] of Object.entries(SITES)) nodes[id] = { id, x: s.node[0], z: s.node[1] };
  for (const [id, p] of Object.entries(JUNCTIONS)) nodes[id] = { id, x: p[0], z: p[1] };

  const edges = [];
  const roadMaterial = mat('path', { side: THREE.DoubleSide });
  roadMaterial.polygonOffset = true;
  roadMaterial.polygonOffsetFactor = -2;
  const addPolyline = (a, b, points, kind) => {
    const cum = [0];
    for (let i = 1; i < points.length; i++) cum.push(cum[i - 1] + points[i].distanceTo(points[i - 1]));
    const edge = { id: `${a}~${b}`, a, b, points, cum, length: cum[cum.length - 1], kind };
    edges.push(edge);
    return edge;
  };
  for (const [a, b, via] of ROADS) {
    const ctrl = [[nodes[a].x, nodes[a].z], ...via, [nodes[b].x, nodes[b].z]].map(([x, z]) => new THREE.Vector3(x, 0, z));
    const curve = new THREE.CatmullRomCurve3(ctrl, false, 'centripetal');
    const n = Math.max(8, Math.ceil(curve.getLength() / 0.18));
    const pts = curve.getSpacedPoints(n).map(p => {
      const y = surface(p.x, p.z);
      return new THREE.Vector3(p.x, (y ?? 0.8) + 0.02, p.z);
    });
    const edge = addPolyline(a, b, pts, 'road');
    world.add(roadRibbon(pts, 1.05, surface, roadMaterial, edge.id));
  }
  for (const bridge of bridges) {
    const pts = [];
    const steps = Math.ceil(bridge.start.distanceTo(bridge.end) / 0.04);
    for (let i = 0; i <= steps; i++) pts.push(bridge.pointAt(i / steps));
    addPolyline(`${bridge.id}:a`, `${bridge.id}:b`, pts, 'bridge');
  }

  for (const n of Object.values(nodes)) n.y = surface(n.x, n.z);
  const graph = { nodes, edges, adjacency: new Map() };
  for (const e of edges) {
    for (const [from, to] of [[e.a, e.b], [e.b, e.a]]) {
      if (!graph.adjacency.has(from)) graph.adjacency.set(from, []);
      graph.adjacency.get(from).push({ edge: e, to, forward: from === e.a });
    }
  }

  // 前庭小廣場
  const plazaMat = mat('path');
  for (const id of [...Object.keys(SITES), ...Object.keys(JUNCTIONS)]) {
    const n = nodes[id];
    const plaza = new THREE.Mesh(new THREE.CircleGeometry(1.1, 22), plazaMat);
    plaza.rotation.x = -Math.PI / 2;
    plaza.position.set(n.x, n.y + 0.022, n.z);
    plaza.receiveShadow = true;
    world.add(plaza);
  }

  // ---------- 地標 ----------
  const zoneObjects = {};
  const pickables = [];
  const footprints = [];
  for (const [zoneId, s] of Object.entries(SITES)) {
    const model = s.building();
    const [bx, bz] = s.at;
    const y = terrains[s.island].surfaceAt(bx, bz);
    if (y === null) throw new Error(`Landmark ${zoneId} is off its island.`);
    model.position.set(bx, y, bz);
    model.rotation.y = Math.atan2(s.node[0] - bx, s.node[1] - bz);
    model.scale.setScalar(s.scale);
    model.name = `landmark:${zoneId}`;
    model.traverse(o => { o.userData.zoneId = zoneId; if (o.isMesh) pickables.push(o); });
    world.add(model);
    const box = new THREE.Box3().setFromObject(model);
    zoneObjects[zoneId] = { model, box, anchor: new THREE.Vector3((box.min.x + box.max.x) / 2, box.max.y, (box.min.z + box.max.z) / 2) };
    footprints.push({ x: bx, z: bz, r: Math.max(box.max.x - box.min.x, box.max.z - box.min.z) / 2 + 0.25 });
  }

  // ---------- 傳統信仰島北側的山 ----------
  const mountainMeshes = [];
  for (const [mx, mz, r0, h] of MOUNTAINS) {
    let r = r0;
    const fits = rr => Array.from({ length: 8 }, (_, i) => terrains.faith.contains(mx + Math.cos(i * Math.PI / 4) * rr, mz + Math.sin(i * Math.PI / 4) * rr)).every(Boolean);
    while (r > 0.5 && !fits(r)) r -= 0.08;
    const base = Math.min(...Array.from({ length: 8 }, (_, i) => terrains.faith.surfaceAt(mx + Math.cos(i * Math.PI / 4) * r * 0.9, mz + Math.sin(i * Math.PI / 4) * r * 0.9)));
    const m = mountain(r, h * (r / r0) ** 0.5);
    m.position.set(mx, base - 0.05, mz);
    m.rotation.y = mx * 1.7;
    world.add(m);
    mountainMeshes.push(m);
    footprints.push({ x: mx, z: mz, r: r + 0.15 });
  }

  // ---------- 樹木：避開道路、地標與山 ----------
  const rand = mulberry32(20261105);
  const roadPts = edges.filter(e => e.kind === 'road').flatMap(e => e.points.filter((_, i) => i % 2 === 0));
  const nearRoad = (x, z, d) => roadPts.some(p => (p.x - x) ** 2 + (p.z - z) ** 2 < d * d);
  const nearNode = (x, z, d) => Object.values(nodes).some(n => (n.x - x) ** 2 + (n.z - z) ** 2 < d * d);
  const treeSpots = [];
  for (let i = 0; i < 1200 && treeSpots.length < 30; i++) {
    const x = (-16 + rand() * 32) * S, z = (-9 + rand() * 18) * S;
    const id = islandOf(x, z);
    if (!id) continue;
    const terrain = terrains[id];
    const edgeSafe = [[0.45, 0], [-0.45, 0], [0, 0.45], [0, -0.45]].every(([dx, dz]) => terrain.contains(x + dx, z + dz));
    if (!edgeSafe || nearRoad(x, z, 0.9) || nearNode(x, z, 1.4)) continue;
    if (footprints.some(f => (f.x - x) ** 2 + (f.z - z) ** 2 < f.r * f.r)) continue;
    if (treeSpots.some(t => (t[0] - x) ** 2 + (t[1] - z) ** 2 < 1.4)) continue;
    treeSpots.push([x, z]);
    const t = tree(Math.floor(rand() * 3), 1.25 + rand() * 0.5);
    t.position.set(x, terrain.surfaceAt(x, z) - 0.02, z);
    t.rotation.y = rand() * Math.PI * 2;
    world.add(t);
  }

  // ---------- 遠景：漂浮的雲、遠方沙洲 ----------
  const clouds = [];
  for (const [x, y, z, s] of [[-24, 7.5, -16, 1.6], [18, 8, -16, 1.3], [22, 7, 14, 1.4], [-26, 6.5, 12, 1.2]]) {
    const c = cloud(s);
    c.position.set(x, y, z);
    c.userData.base = x;
    world.add(c);
    clouds.push(c);
  }
  for (const [x, z, r] of [[-24, 18, 1.5], [24, -10, 1.1], [22, 18, 1.3]]) {
    const isle = new THREE.Mesh(new THREE.CylinderGeometry(r, r * 1.15, 0.5, 14), mat('sand'));
    isle.position.set(x, WATER_LEVEL, z);
    isle.receiveShadow = true;
    world.add(isle);
    const t = tree(0, 0.9);
    t.position.set(x, WATER_LEVEL + 0.25, z);
    world.add(t);
  }

  // ---------- 科技夜景特效 ----------
  const techFx = new THREE.Group();
  techFx.name = 'tech-fx';
  const glowLine = new THREE.LineBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.9 });
  const glowLine2 = new THREE.LineBasicMaterial({ color: 0xa78bfa, transparent: true, opacity: 0.75 });
  for (const t of Object.values(terrains)) {
    const pts = t.group.userData.outline.map(([x, z]) => {
      const y = t.surfaceAt(x * 0.995, z * 0.995) ?? t.surfaceAt(x, z) ?? 1;
      return new THREE.Vector3(x, y + 0.04, z);
    });
    techFx.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), glowLine));
    const low = t.group.userData.outline.map(([x, z]) => new THREE.Vector3(x, WATER_LEVEL + 0.05, z));
    techFx.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(low), glowLine2));
  }
  for (const e of edges) {
    const pts = e.points.filter((_, i) => i % 2 === 0).map(p => p.clone().setY(p.y + (e.kind === 'bridge' ? 0.06 : 0.05)));
    techFx.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), glowLine));
  }
  const grid = new THREE.GridHelper(180, 90, 0x22d3ee, 0x22d3ee);
  grid.material.transparent = true;
  grid.material.opacity = 0.22;
  grid.material.depthWrite = false;
  grid.position.y = WATER_LEVEL + 0.02;
  techFx.add(grid);
  const sparkCount = 260;
  const sparkPos = new Float32Array(sparkCount * 3);
  for (let i = 0; i < sparkCount; i++) {
    sparkPos[i * 3] = (rand() - 0.5) * 65;
    sparkPos[i * 3 + 1] = 1 + rand() * 12;
    sparkPos[i * 3 + 2] = (rand() - 0.5) * 55 + 4;
  }
  const sparkGeo = new THREE.BufferGeometry();
  sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
  const sparks = new THREE.Points(sparkGeo, new THREE.PointsMaterial({ color: 0x9be7ff, size: 0.16, transparent: true, opacity: 0.8, depthWrite: false }));
  techFx.add(sparks);
  techFx.visible = false;
  world.add(techFx);

  const bounds = new THREE.Box3();
  for (const t of Object.values(terrains)) bounds.expandByObject(t.group);
  const movers = { spin: [], spinZ: [], bob: [], sway: [], glow: [] };
  world.traverse(o => { for (const k of Object.keys(movers)) if (o.userData[k] !== undefined) movers[k].push(o); });

  function update(time) {
    clouds.forEach((c, i) => { c.position.x = c.userData.base + Math.sin(time * 0.03 + i) * 3; });
    for (const o of movers.spin) o.rotation.y = time * o.userData.spin;
    for (const o of movers.spinZ) o.rotation.z = time * o.userData.spinZ;
    for (const o of movers.bob) { o.userData.baseY ??= o.position.y; o.position.y = o.userData.baseY + Math.sin(time * 1.4 + o.id) * o.userData.bob; }
    for (const o of movers.sway) o.rotation.z = Math.sin(time * 1.2 + o.id) * o.userData.sway;
    for (const o of movers.glow) o.material.emissiveIntensity = 0.75 + Math.sin(time * 2.4) * 0.25;
    if (techFx.visible) {
      sparks.rotation.y = time * 0.01;
      glowLine.opacity = 0.75 + Math.sin(time * 1.6) * 0.2;
    }
  }

  function setColors(p) {
    if (terrains.faith) terrains.faith.setColors({ groundColor: p.mode === 'night' ? '#3d342b' : '#d4b886', bankColor: '#9c7a4c' });
    if (terrains.oldstreet) terrains.oldstreet.setColors({ groundColor: p.mode === 'night' ? '#3a2d27' : '#c79d79', bankColor: '#8c6244' });
    techFx.visible = p.mode === 'night';
    if (p.glow) glowLine.color.set(p.glow);
    if (p.glow2) glowLine2.color.set(p.glow2);
  }

  return { world, terrains, surface, graph, zoneObjects, pickables, mountainMeshes, bridges, connectionCheck, bounds, update, setColors };
}

function roadRibbon(points, width, surface, material, id) {
  const pos = [], idx = [];
  for (let i = 0; i < points.length; i++) {
    const p = points[i];
    const q = points[Math.min(points.length - 1, i + 1)], o = points[Math.max(0, i - 1)];
    const dir = new THREE.Vector2(q.x - o.x, q.z - o.z).normalize();
    for (const s of [-1, 1]) {
      const x = p.x - dir.y * s * width / 2, z = p.z + dir.x * s * width / 2;
      pos.push(x, (surface(x, z) ?? p.y - 0.02) + 0.025, z);
    }
    if (i) { const a = (i - 1) * 2; idx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx);
  g.computeVertexNormals();
  const mesh = new THREE.Mesh(g, material);
  mesh.receiveShadow = true;
  mesh.name = `road:${id}`;
  return mesh;
}

function mulberry32(seed) {
  return function () {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

return { WATER_LEVEL, S, LAYOUT, buildWorld, mulberry32 };
})();
"""

html = html[:world_start] + new_world_module + html[world_end:]

# 6. 更新 __residents 裡的 ROLES，讓 10 位第三單元在地居民在傳統信仰島與家鄉老街島之間過橋走動！
roles_start = html.index("const ROLES = [")
roles_end = html.index("];", roles_start) + 2

new_roles = """const ROLES = [
  { id: 'indigenous-elder', label: '原住民族頭目', coat: 'stone*0.45', hat: 'feather', hatColor: '#d63a2a', stops: ['indigenous_ritual', 'fj', 'folk_deity'], speed: 0.78 },
  { id: 'temple-keeper', label: '老廟祝伯伯', coat: 'demo', hat: 'cap', hatColor: '#b45309', stops: ['folk_deity', 'fj', 'temple_fair', 'eco_worship'], speed: 0.75 },
  { id: 'troupe-youth', label: '廟會陣頭青年', coat: 'accent', hat: 'band', hatColor: '#dc2626', stops: ['temple_fair', 'fj', 'folk_deity', 'oj', 'river_port'], speed: 0.88 },
  { id: 'eco-volunteer', label: '環保祭祀志工', coat: 'leaf2', hat: 'cap', hatColor: '#15803d', stops: ['eco_worship', 'fj', 'oj', 'street_revival'], speed: 0.85 },
  { id: 'boatman', label: '渡口老船長', coat: 'wall', hat: 'straw', hatColor: '#e8cf8a', stops: ['river_port', 'oj', 'shophouse'], speed: 0.76 },
  { id: 'merchant', label: '老街商號掌櫃', coat: 'change', hat: 'brim', hatColor: '#a16207', stops: ['shophouse', 'oj', 'river_port', 'indigo_craft'], speed: 0.80 },
  { id: 'indigo-master', label: '三峽藍染阿زما', coat: 'demo*1.1', hat: 'bun', stops: ['indigo_craft', 'oj', 'shophouse', 'street_revival'], speed: 0.74 },
  { id: 'cultural-guide', label: '老街文史導覽員', coat: 'change*1.15', hat: 'helmet', hatColor: '#f2c14e', stops: ['street_revival', 'oj', 'fj', 'folk_deity'], speed: 0.86 },
  { id: 'student-a', label: '學生小航', coat: 'demo*1.2', hat: 'cap', hatColor: '#2563eb', stops: ['indigenous_ritual', 'fj', 'oj', 'indigo_craft'], speed: 0.94 },
  { id: 'student-b', label: '學生小雅', coat: 'change*1.2', hat: 'bun', stops: ['temple_fair', 'fj', 'oj', 'street_revival'], speed: 0.92 },
];"""

html = html[:roles_start] + new_roles + html[roles_end:]

# 7. 更新 __guardian：將看門獸改為飄在海面上的巨型「Hakaw Utux 泰雅祖靈彩虹橋」（無島嶼，直接浮在海上，規模調大！）
guardian_start = html.index("const __guardian = (() => {")
guardian_end = html.index("// ---- src/labels.js ----")

new_guardian_module = """const __guardian = (() => {
// 看門獸／全島導覽「Hakaw Utux 泰雅祖靈彩虹橋」：
// 不設陸地島嶼，像上一檔案的方向標海龜一樣直接飄浮在雙島南側前方海面上，並放大尺寸（scale: 2.35）！
// 兩端由海面祥雲浮座與擴散水波紋托起，立有泰雅族「祖靈之眼」紅白黑菱形紋圖騰柱與發光晶石，
// 橋頂站著泰雅族大頭目守護者與「祖靈彩虹橋」導覽牌，身旁海面漂著泰雅傳統織布機，點擊即可開啟全島導覽與彩虹橋傳說挑戰。
const { fixedMat, at, sc, ball, cyl, cone, rbox, signBoard } = __models;

const GUARDIAN = {
  anchor: [0.0, 12.2],      // 世界座標 x, z（雙島正南方海面中央，全景視野最醒目處）
  facing: [-1.5, 24.0],     // 微斜朝向全景相機，完美展現五彩彩虹拱橋弧度與雙柱
  scale: 2.35,              // 大幅調大尺寸，橫跨海面氣勢磅礴
};

function createGuardian(scene, waterLevel) {
  const root = new THREE.Group();
  root.name = 'guardian-root';
  const body = new THREE.Group();
  body.scale.setScalar(GUARDIAN.scale);
  root.add(body);

  // 1. 雙端海面祥雲浮台（托起彩虹橋兩端，直接飄在海上）
  const cloudMat = fixedMat('#fffdf9');
  const cloudShadowMat = fixedMat('#dceefb');
  const cloudClusters = [];
  for (const side of [-1, 1]) {
    const cg = new THREE.Group();
    cg.position.set(side * 2.85, 0.18, 0);
    cg.add(sc(ball(0.95, cloudMat, 16, 12), 1.35, 0.55, 1.15));
    cg.add(at(sc(ball(0.72, cloudMat, 14, 10), 1.1, 0.6, 1.0), -0.55 * side, 0.12, 0.35));
    cg.add(at(sc(ball(0.75, cloudMat, 14, 10), 1.15, 0.6, 1.0), 0.5 * side, 0.15, -0.3));
    cg.add(at(sc(ball(0.62, cloudShadowMat, 12, 8), 1.4, 0.3, 1.2), 0, -0.18, 0));
    body.add(cg);
    cloudClusters.push(cg);
  }

  // 2. 巨型五色粉柔自發光彩虹拱橋（橫跨海面）
  const archGroup = new THREE.Group();
  archGroup.position.set(0, 0.25, 0);
  const rainbowColors = ['#e85d56', '#f2994a', '#f2c94c', '#4ea871', '#6b7fd7'];
  const bandMats = [];
  rainbowColors.forEach((col, idx) => {
    const radius = 3.15 - idx * 0.16;
    const curvePts = [];
    for (let i = 0; i <= 32; i++) {
      const theta = (i / 32) * Math.PI;
      curvePts.push(new THREE.Vector3(-Math.cos(theta) * radius, Math.sin(theta) * radius * 0.92, 0));
    }
    const curve = new THREE.CatmullRomCurve3(curvePts);
    const tubeGeo = new THREE.TubeGeometry(curve, 36, 0.11, 10, false);
    const m = fixedMat(col, { emissive: col, emissiveIntensity: 0.32, roughness: 0.35 }).clone();
    bandMats.push({ mat: m, baseCol: col });
    const mesh = new THREE.Mesh(tubeGeo, m);
    archGroup.add(mesh);
  });

  // 彩虹橋面半透明晶亮階梯踏板與欄杆光柱
  const stepMat = fixedMat('#fffbeb', { emissive: '#fde68a', emissiveIntensity: 0.25 });
  for (let i = 2; i <= 18; i++) {
    const theta = (i / 20) * Math.PI;
    const sx = -Math.cos(theta) * 2.85;
    const sy = Math.sin(theta) * 2.85 * 0.92;
    const step = rbox(0.32, 0.06, 0.95, stepMat, 0.02);
    step.position.set(sx, sy + 0.04, 0);
    step.rotation.z = theta - Math.PI / 2;
    archGroup.add(step);
  }
  body.add(archGroup);

  // 3. 左右兩端「泰雅族祖靈之眼（菱形紋）」守護圖騰柱
  const woodDark = fixedMat('#5c3a21');
  const crimson = fixedMat('#be123c');
  const cream = fixedMat('#fffbeb');
  const ink = fixedMat('#1e293b');
  const gemMat = fixedMat('#38bdf8', { emissive: '#0284c7', emissiveIntensity: 0.6 }).clone();
  const crystals = [];

  for (const side of [-1, 1]) {
    const pillar = new THREE.Group();
    pillar.position.set(side * 2.95, 0.35, 0.55);
    pillar.add(at(cyl(0.24, 0.28, 2.2, 10, woodDark), 0, 1.1, 0));
    // 柱身三層泰雅菱形「祖靈之眼」圖騰雕刻
    for (const py of [0.55, 1.15, 1.75]) {
      const diamondOuter = rbox(0.32, 0.32, 0.12, crimson, 0.02);
      diamondOuter.rotation.z = Math.PI / 4;
      pillar.add(at(diamondOuter, 0, py, 0.22));
      const diamondMid = rbox(0.20, 0.20, 0.14, cream, 0.02);
      diamondMid.rotation.z = Math.PI / 4;
      pillar.add(at(diamondMid, 0, py, 0.23));
      const eyePupil = ball(0.06, ink, 8, 6);
      pillar.add(at(eyePupil, 0, py, 0.30));
    }
    // 柱頂懸浮旋轉的祖靈菱形晶石
    const crystal = new THREE.Group();
    crystal.position.set(0, 2.55, 0);
    crystal.add(at(cone(0.22, 0.38, 4, gemMat), 0, 0.19, 0));
    const lowerCone = cone(0.22, 0.38, 4, gemMat);
    lowerCone.rotation.x = Math.PI;
    crystal.add(at(lowerCone, 0, -0.19, 0));
    pillar.add(crystal);
    crystals.push(crystal);
    body.add(pillar);
  }

  // 4. 橋頂中央：泰雅族大頭目守護者與「祖靈彩虹橋」導覽旗標
  const crest = new THREE.Group();
  crest.position.set(0, 2.95, 0);

  // 守護者半身雕像（帶眨眼動畫與泰雅羽冠、紅白菱形披肩）
  const skin = fixedMat('#f2c9a0');
  const white = fixedMat('#fffdf8');
  const pupil = fixedMat('#1d2630');
  const chief = new THREE.Group();
  chief.position.set(-0.55, 0, 0.25);
  // 泰雅紅白菱形織紋披肩軀幹
  chief.add(at(rbox(0.62, 0.72, 0.42, crimson, 0.08), 0, 0.36, 0));
  chief.add(at(rbox(0.42, 0.68, 0.45, cream, 0.04), 0, 0.36, 0));
  // 頭部
  const head = new THREE.Group();
  head.position.set(0, 0.92, 0);
  head.add(ball(0.32, skin, 16, 12));
  // 泰雅傳統額帶與三根高聳羽冠
  head.add(at(cyl(0.33, 0.33, 0.1, 14, crimson), 0, 0.12, 0));
  for (const [fx, fc] of [[-0.1, '#f2c14e'], [0, '#ffffff'], [0.1, '#e85d56']]) {
    const f = rbox(0.07, 0.42, 0.03, fixedMat(fc), 0.01);
    f.rotation.z = fx * 2.5;
    head.add(at(f, fx, 0.38, -0.12));
  }
  const lids = [];
  for (const s of [-1, 1]) {
    const eye = new THREE.Group();
    eye.position.set(s * 0.13, 0.02, 0.28);
    eye.add(ball(0.055, white, 10, 8));
    eye.add(at(ball(0.032, pupil, 8, 6), 0, 0, 0.035));
    const lid = ball(0.06, skin, 10, 8);
    lid.visible = false;
    eye.add(lid);
    lids.push(lid);
    head.add(eye);
  }
  chief.add(head);
  crest.add(chief);

  // 橋頂導覽旗桿與招牌
  const mast = new THREE.Group();
  mast.position.set(0.55, 0, 0.15);
  mast.add(at(cyl(0.05, 0.06, 1.45, 8, fixedMat('#fffbeb')), 0, 0.72, 0));
  mast.add(at(signBoard('🌈 祖靈彩虹橋', 1.75, 0.56, { bg: '#9d174d', fg: '#ffffff', frame: '#fde047' }), 0, 1.15, 0.08));
  crest.add(mast);
  body.add(crest);

  // 5. 海面伴隨漂浮物：泰雅傳統紅白菱形織布台（如同上一檔案海龜身旁漂著的魚筌）
  const loom = new THREE.Group();
  loom.position.set(4.1, 0.08, 1.15);
  loom.add(at(sc(ball(0.75, cloudMat, 12, 8), 1.3, 0.35, 1.0), 0, 0.05, 0));
  // 織布木架與紅白菱形紋布匹
  loom.add(at(rbox(0.95, 0.08, 0.65, woodDark, 0.02), 0, 0.25, 0));
  const cloth = rbox(0.72, 0.85, 0.05, crimson, 0.01);
  cloth.rotation.x = -0.35;
  loom.add(at(cloth, 0, 0.62, 0));
  for (const dy of [0.48, 0.72]) {
    const dm = rbox(0.22, 0.22, 0.07, cream, 0.01);
    dm.rotation.z = Math.PI / 4;
    dm.rotation.x = -0.35;
    loom.add(at(dm, 0, dy, 0.02));
  }
  loom.add(at(signBoard('祖靈之眼織紋', 1.35, 0.42, { bg: '#be123c', fg: '#ffffff', frame: '#fde68a' }), 0, 1.32, 0));
  body.add(loom);

  // 6. 海面擴散水波圈（強化飄在海上的視覺感）
  const ripples = [];
  for (let i = 0; i < 4; i++) {
    const ring = new THREE.Mesh(
      new THREE.RingGeometry(0.96, 1.0, 56),
      new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.4, depthWrite: false })
    );
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.025;
    root.add(ring);
    ripples.push(ring);
  }

  root.position.set(GUARDIAN.anchor[0], waterLevel, GUARDIAN.anchor[1]);
  root.rotation.y = Math.atan2(GUARDIAN.facing[0] - GUARDIAN.anchor[0], GUARDIAN.facing[1] - GUARDIAN.anchor[1]);
  const pickables = [];
  body.traverse(o => { if (o.isMesh) { o.castShadow = true; o.userData.guardian = true; pickables.push(o); } });
  scene.add(root);

  let state = 'idle', stateTime = 0;
  function trigger(kind = 'interaction') {
    if (state === 'greeting' || state === 'interaction') return false;
    state = kind; stateTime = 0;
    return true;
  }

  function update(dt, time, animate) {
    stateTime += dt;
    let nod = 0, rise = 0, turn = 0;
    if (state === 'greeting' || state === 'interaction') {
      const k = Math.min(1, stateTime / 1.8);
      nod = Math.sin(k * Math.PI * 2) * 0.22;
      turn = Math.sin(k * Math.PI);
      if (animate) rise = Math.sin(k * Math.PI) * 0.55;
      if (k >= 1) { state = 'returning'; stateTime = 0; }
    } else if (state === 'returning' && stateTime > 0.4) {
      state = 'idle';
    }
    const t = animate ? time : 0;
    const blink = animate && (time % 4.2) < 0.15 ? 1 : 0;
    for (const lid of lids) lid.visible = !!blink;

    // 整座彩虹橋隨海浪輕柔上下浮動
    body.position.y = (Math.sin(t * 0.75) * 0.08 + rise) * GUARDIAN.scale;
    body.rotation.z = Math.sin(t * 0.45) * 0.022;
    head.rotation.x = -nod;
    head.rotation.y = turn * 0.45 + Math.sin(t * 0.5) * 0.15;
    mast.rotation.y = Math.sin(t * 0.6) * 0.1 + turn * Math.PI * 2;

    // 雙柱頂端祖靈晶石旋轉與上下浮動
    crystals.forEach((c, idx) => {
      c.rotation.y = t * 1.4 + idx * Math.PI + turn * Math.PI * 2;
      c.position.y = 2.55 + Math.sin(t * 2.0 + idx) * 0.08;
    });

    // 祥雲呼吸律動與織布浮台隨波搖曳
    cloudClusters.forEach((cg, idx) => {
      cg.position.y = 0.18 + Math.sin(t * 1.1 + idx * 2) * 0.04;
    });
    loom.position.y = 0.08 + Math.sin(t * 1.15 + 1.2) * 0.07;
    loom.rotation.y = Math.sin(t * 0.5) * 0.16;

    // 水波圈向外擴散
    ripples.forEach((r, i) => {
      const p = animate ? ((time * 0.16 + i / 4) % 1) : 0.35 + i * 0.18;
      const s = 7.5 + p * 6.5;
      r.scale.set(s, s * 0.72, 1);
      r.material.opacity = 0.42 * (1 - p);
    });
  }

  function setNight(night) {
    bandMats.forEach(({ mat }) => {
      mat.emissiveIntensity = night ? 0.88 : 0.32;
    });
    gemMat.emissiveIntensity = night ? 1.2 : 0.6;
  }

  root.updateMatrixWorld(true);
  const local = [];
  for (let i = 0; i < 16; i++) {
    const a = i / 16 * Math.PI * 2;
    local.push([Math.cos(a) * 3.8, 0, Math.sin(a) * 2.2]);
  }
  local.push([0, 3.6, 0], [-3.2, 2.8, 0.5], [3.2, 2.8, 0.5], [0, 4.3, 0.2], [4.2, 1.5, 1.1], [-3.5, 0, 0]);
  const bbox = new THREE.Box3();
  const outlinePoints = local.map(([x, y, z]) => { const p = body.localToWorld(new THREE.Vector3(x, y, z)); bbox.expandByPoint(p); return p; });
  const anchor = body.localToWorld(new THREE.Vector3(0, 4.35, 0.1));
  return { root, pickables, update, trigger, setNight, get state() { return state; }, box: bbox, anchor, outlinePoints };
}

return { GUARDIAN, createGuardian };
})();
"""

html = html[:guardian_start] + new_guardian_module + html[guardian_end:]

# 8. 更新 __main 內部的儲存 key、RPG 狀態、8 枚徽章、快速導覽函數、標籤與 openGuide 導覽面板
html = html.replace(
    "const { ZONES, UNITS, ISLANDS } = __content;",
    "const { ZONES, UNITS, ISLANDS, RAINBOW_GUIDE } = __content;"
)
html = html.replace(
    "const ISLAND_KEY = 'g4-society-island:v1';",
    "const ISLAND_KEY = 'g4-society-island-unit3:v1';"
)

# 更新 TITLES 與 gameState
old_titles_block = """const TITLES = [
  "海線見習生", "地圖測量士", "地形探勘家", "山川漫遊者", "氣候觀測員",
  "水資源衛士", "時空穿越者", "三合院掌門", "石板屋守護者", "家鄉時空英雄"
];"""
new_titles_block = """const TITLES = [
  "信仰見習生", "祭儀文化員", "廟宇建築師", "藝陣小傳人", "綠色信仰家",
  "渡口領航員", "老街保存者", "三峽藍染師", "泰雅彩虹守護者", "家鄉時空英雄"
];"""
assert old_titles_block in html, "TITLES block not found"
html = html.replace(old_titles_block, new_titles_block, 1)

old_inv_block = """  inventory: [
    { id: "potato", name: "炭火悶烤地瓜", icon: "🍠", count: 3, desc: "大灶柴灰餘溫燜烤！食用回復 40 HP。" },
    { id: "tea", name: "丘陵高山烏龍茶", icon: "🍵", count: 2, desc: "苗栗丘陵排水良好特產！飲用回復 25 MP。" },
    { id: "compass", name: "傳奇指北羅盤", icon: "🧭", count: 1, desc: "地圖四要素之方位指針裝備。" },
    { id: "fishTrap", name: "工匠竹編魚筌", icon: "🎋", count: 1, desc: "順流水中捕魚，留縫隙讓小魚游走。" }
  ],
  stamps: Array(24).fill(false)"""
new_inv_block = """  inventory: [
    { id: "croissant", name: "三峽金牛角麵包", icon: "🥐", count: 3, desc: "三峽老街排隊名產！外酥內軟，食用回復 45 HP。" },
    { id: "milletRice", name: "阿美族香Q竹筒飯", icon: "🎋", count: 2, desc: "歲時祭儀傳統美食，散發竹膜清香！食用回復 30 MP。" },
    { id: "mazuCharm", name: "大甲鎮瀾宮平安符", icon: "🧧", count: 1, desc: "海上守護神媽祖庇佑出入平安之護身符。" },
    { id: "indigoScarf", name: "三峽大菁藍染方巾", icon: "🧣", count: 1, desc: "經浸染與空氣氧化而成的美麗天然藍染布巾。" }
  ],
  stamps: Array(9).fill(false)"""
assert old_inv_block in html, "Inventory block not found"
html = html.replace(old_inv_block, new_inv_block, 1)

# 更新 useInventoryItem 支援新道具與修復 sfx.playVictory
html = html.replace('if (itemId === "potato")', 'if (itemId === "potato" || itemId === "croissant")')
html = html.replace('if (itemId === "tea")', 'if (itemId === "tea" || itemId === "milletRice")')
html = html.replace('sfx.playVictory();', 'sfx.playCorrect();')
html = html.replace('👑 彩虹時空守護者 (全 72 ★)', '👑 彩虹時空守護者 (全 24 ★)')

# 更新 STAMP_DEFINITIONS 為第三單元專屬 8 站 + 彩虹橋導覽徽章 (共 9 枚)
stamps_start = html.index("const STAMP_DEFINITIONS = [")
stamps_end = html.index("];", stamps_start) + 2
new_stamps_def = """const STAMP_DEFINITIONS = [
  { name: "原民歲時祭儀徽章", icon: "🏹" },
  { name: "守護神與廟宇徽章", icon: "🏮" },
  { name: "廟會陣頭文化徽章", icon: "🦁" },
  { name: "環保誠心祭祀徽章", icon: "🌾" },
  { name: "河運渡口老街徽章", icon: "⛵" },
  { name: "紅磚長條街屋徽章", icon: "🏛️" },
  { name: "三峽傳統藍染徽章", icon: "🧣" },
  { name: "老街文創活化徽章", icon: "🥐" },
  { name: "泰雅祖靈彩虹橋徽章", icon: "🌈" }
];"""
html = html[:stamps_start] + new_stamps_def + html[stamps_end:]

# 更新 renderEncyclopedia 的標籤文字
html = html.replace(
    "<span class=\"tag ${z.unit}\">${z.unit === 'demo' ? '單元一' : '單元二'}</span>",
    "<span class=\"tag ${z.unit}\">${z.unit === 'faith' ? '第三單元 第1課' : '第三單元 第2課'}</span>"
)

# 更新證書標題文字
html = html.replace(
    'ctx.fillText("🏆 期中全單元通關探險大師榮譽證書 🏆", 400, 118);',
    'ctx.fillText("🏆 第三單元：家鄉的信仰與老街 探險大師榮譽證書 🏆", 400, 118);'
)
html = html.replace(
    'ctx.fillText("已完成【第一單元：家鄉的環境】與【第二單元：家鄉的傳統生活】", 400, 290);',
    'ctx.fillText("已完成【傳統信仰島】、【家鄉老街島】與【泰雅祖靈彩虹橋】", 400, 290);'
)

# 新增 window.openGuardianFast 並讓 goStationFast('rainbow_bridge') 也能飛向海上彩虹橋並開啟導覽
old_go_fast = """// 快速飛向特定站點
window.goStationFast = function(id) {
  sfx.playClick();
  goStation(id);
};"""
new_go_fast = """// 快速飛向特定站點或海上彩虹橋看門獸
window.openGuardianFast = function() {
  sfx.playClick();
  closePanel();
  const toZ = Math.max(camera.zoom, homeZoom * 1.5);
  const toT = guardian.anchor.clone();
  flight = { t: paused ? 1 : 0, fromT: controls.target.clone(), toT, fromP: camera.position.clone(), fromZ: camera.zoom, toZ };
  setTimeout(() => openGuide(true), paused ? 0 : 650);
};
window.goStationFast = function(id) {
  if (id === 'rainbow_bridge' || id === 'guardian') {
    window.openGuardianFast();
    return;
  }
  sfx.playClick();
  goStation(id);
};"""
assert old_go_fast in html, "goStationFast not found"
html = html.replace(old_go_fast, new_go_fast, 1)

# 更新 hullSources 中 mountainMeshes 掛載的島 ID (由 'demo' 改為 'faith')
html = html.replace(
    ".concat(id === 'demo' ? world.mountainMeshes.map(m => new THREE.Box3().setFromObject(m)) : [])),",
    ".concat(id === 'faith' ? world.mountainMeshes.map(m => new THREE.Box3().setFromObject(m)) : [])),"
)

# 更新看門獸場景標籤：由「海龜」改為「祖靈彩虹橋」
html = html.replace(
    "labelDefs.push({ id: 'guardian', text: '海龜', badge: '導', faction: 'guardian', anchor: guardian.anchor.clone(), hullId: 'guardian' });",
    "labelDefs.push({ id: 'guardian', text: '祖靈彩虹橋', badge: '導', faction: 'guardian', anchor: guardian.anchor.clone(), hullId: 'guardian' });"
)

# 更新通關慶祝文字
html = html.replace(
    "totalStars() === ZONES.length * 3 ? '全部三星，方向標海龜幫你蓋上「家鄉小達人」章！' : '想拿滿三星？回到星星較少的關卡再挑戰一次吧！'",
    "totalStars() === ZONES.length * 3 ? '全部三星，海上的泰雅祖靈彩虹橋為你綻放七彩光芒，蓋上「信仰老街小達人」章！' : '想拿滿三星？回到星星較少的關卡再挑戰一次吧！'"
)

# 更新 openGuide：改為「泰雅祖靈彩虹橋的島嶼導覽」，並內建彩虹橋傳說圖卡、小實驗與互動問答！
open_guide_start = html.index("function openGuide(fromGuardian = false) {")
open_guide_end = html.index("document.getElementById('btn-guide').addEventListener('click'", open_guide_start)

new_open_guide = """function openGuide(fromGuardian = false) {
  if (fromGuardian) guardian.trigger('interaction');
  labels.setSelected('guardian');
  needsLayout = true;
  openPanel({
    title: '🌈 泰雅祖靈彩虹橋（Hakaw Utux）的島嶼導覽',
    kicker: '<span class="tag" style="background:linear-gradient(135deg,#e85d56,#f2994a,#4ea871,#6b7fd7);color:#fff;">海上看門獸導覽</span><span>飄浮於南方海面・守護雙島</span>',
    className: 'is-guide',
    build(body) {
      body.append(el('p', { class: 'intro' },
        '歡迎來到康軒四上社會島【第三單元：家鄉的信仰與老街】！我是飄浮在海面上的「泰雅祖靈彩虹橋（Hakaw Utux）」，橋身兩端立著紅白黑菱形紋的「祖靈之眼」守護柱，身旁漂著泰雅傳統織布機。先在西邊的「傳統信仰島」（第 1～4 關）認識原住民族歲時祭儀、漢人守護神廟宇、迎神賽會陣頭與現代環保祭祀；再跨橋到東邊的「家鄉老街島」（第 5～8 關），探索河運渡口、紅磚長條街屋、三峽藍染與老街文創活化！'
      ));

      body.append(el('h3', {}, `🗺️ 雙島闖關路線：第 1 關到第 ${ZONES.length} 關`));
      const route = el('div', { class: 'route' });
      ZONES.forEach((z, i) => {
        if (i) route.append(el('span', { class: 'arrow', 'aria-hidden': 'true' }, '→'));
        route.append(el('button', { type: 'button', onclick: () => goStation(z.id) },
          `${z.order} ${z.shortName}${isCleared(z.id) ? ' ' + '★'.repeat(quest[z.id].stars) : isUnlocked(z) ? '' : ' 🔒'}`
        ));
      });
      body.append(route);

      body.append(el('ul', { class: 'guide-list' },
        ...ISLANDS.map(i => el('li', {}, el('strong', {}, i.name), `：${i.note}`)),
        el('li', {}, '兩座島以朱紅跨海拱橋相連，原住民族頭目、老廟祝、陣頭青年、環保志工、渡口船長、商號掌櫃、三峽藍染師傅、文史導覽員和學生們會在各站之間走動。')
      ));

      // 內嵌「泰雅祖靈彩虹橋」傳說圖卡與品格試煉小實驗（讓海面彩虹橋同時兼具導覽與文化體驗）
      if (RAINBOW_GUIDE) {
        const divider = el('hr', { style: 'border:none; border-top:1.5px dashed var(--line); margin:18px 0;' });
        body.append(divider);
        body.append(el('h3', { style: 'color:#9d174d; font-size:16px;' }, '✨ 海上看門獸傳說：Hakaw Utux 泰雅彩虹橋文化圖卡'));
        body.append(el('p', { style: 'font-size:13.5px; color:var(--muted); margin:4px 0 10px;' }, RAINBOW_GUIDE.intro));
        const grid = el('div', { class: 'cards n3' });
        for (const c of RAINBOW_GUIDE.cards) {
          grid.append(el('article', { class: 'card' },
            el('img', { src: illustrationUrl(c.illustration), width: ILLUSTRATION_SIZE.w, height: ILLUSTRATION_SIZE.h, alt: c.title, loading: 'lazy' }),
            el('div', { class: 'card-body' }, el('h3', {}, c.title), el('p', {}, c.summary))
          ));
        }
        body.append(grid);
        body.append(el('div', { class: 'trap' }, '⚠️ ', RAINBOW_GUIDE.trap));
        body.append(buildMinigame({ ...RAINBOW_GUIDE, order: 9 }));
      }
    },
  });
}
"""

html = html[:open_guide_start] + new_open_guide + html[open_guide_end:]

# 更新地點清單抽屜中的看門獸名稱
html = html.replace(
    "'方向標海龜（島嶼導覽）'",
    "'🌈 泰雅祖靈彩虹橋（海上導覽）'"
)

# 更新抽屜標題與三階漏斗審查文字
html = html.replace(
    "<h3>🎖️ 十五大關卡探索徽章冊</h3>",
    "<h3>🎖️ 第三單元八大關卡與彩虹橋徽章冊</h3>"
)
html = html.replace(
    "依據康軒四上社會課本第一單元（P.8~31）與第二單元（P.32~51）嚴格命題",
    "依據康軒四上社會課本第三單元「家鄉的信仰與老街」（P.52~69）嚴格命題"
)

# 寫出至 unit3.html 與 unit3/index.html
os.makedirs("unit3", exist_ok=True)
with open("unit3/index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("unit3.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully built unit3/index.html and unit3.html! Size:", len(html))
