from pathlib import Path
import json
p=Path('.')
# Six disciplines, eight independent sample documents per discipline.
briefs=[
 ('沉浸式VR展项','VR / IMMERSIVE','vr','Unity · HDRP · OpenXR',[
 ('零重力档案馆','ZERO GRAVITY ARCHIVE','以悬浮档案与点云空间构成可行走的记忆展馆。观众靠近光环时唤醒一段空间叙事，以抓取、旋转和归位完成探索。'),
 ('深海回声','ABYSSAL ECHO','以深海声场和发光生物群构成沉浸环境，让观众的手势改变粒子流向与声音距离。'),
 ('消失的城市','VANISHING CITY','通过尺度切换阅读城市的日常痕迹，在街道、建筑与房间之间形成连续的空间转场。'),
 ('光之温室','LIGHT CONSERVATORY','把虚拟植物生长与观众停留时间连接，探索缓慢动作带来的沉浸式反馈。'),
 ('记忆地层','MEMORY STRATA','把不同年代的空间碎片叠成可剥离的地层，使用空间音频提示隐藏线索。'),
 ('无界剧场','BOUNDLESS THEATRE','围绕一场没有固定座位的演出设计视线引导，让叙事事件在观众周围依次发生。'),
 ('粒子气候','PARTICLE CLIMATE','把风、雨、雾的视觉参数转译为可操作的气候场，研究 GPU 粒子与体积光的组合。'),
 ('身体的边界','BODY BOUNDARIES','以手部追踪与虚拟化身探索身体尺度变化，使用渐变空间提示动作与安全边界。')]),
 ('AI工作流','AI / WORKFLOW','workflow','ComfyUI · Python · Blender',[
 ('从草图到空间','SKETCH TO SPACE','从手绘草图提取构图约束，经深度与线稿控制生成方案，再回到三维场景核对空间关系。'),
 ('概念分镜流水线','STORYBOARD PIPELINE','将脚本文本拆成稳定镜头编号，用统一视觉规范与参考图约束多镜头生成。'),
 ('材质研究助手','MATERIAL RESEARCH','把材质参考、无缝纹理与 PBR 通道检查组织成可重复的研究流程。'),
 ('建筑方案变体','DESIGN VARIATIONS','固定场地边界与体量关系，仅对立面节奏、材质和光照生成受控变体。'),
 ('展项内容工厂','EXHIBIT CONTENT','将展项知识目标、观众动作与反馈画面关联，形成可复用的内容模块。'),
 ('资产自动归档','ASSET LIBRARY','按项目、镜头与版本组织图像和模型，使每次生成结果都能回溯到输入参数。'),
 ('实时场景桥接','REALTIME BRIDGE','把图像概念转成可在实时引擎中调整的灯光、材质与摄像机设置。'),
 ('设计复核回路','DESIGN REVIEW LOOP','在生成、人工筛选、结构检查和实机验证之间建立反馈回路，保留失败与修订记录。')]),
 ('生图与视觉实验','AI / IMAGE LAB','image-lab','生成式影像 · 构图 · 氛围研究',[
 ('漂浮的混凝土','FLOATING CONCRETE','在超现实的重力关系中研究粗粝混凝土、柔软云雾与冷光之间的张力。'),
 ('后数字考古','POST DIGITAL RUINS','用废弃终端、玻璃残片与沉积地貌构造数字文明遗址的视觉母题。'),
 ('液态地景','LIQUID LANDSCAPE','研究流体形态与建筑边界的相互侵入，形成可用于动态影像的构图草案。'),
 ('合成植物志','SYNTHETIC BOTANY','将自然生长规律与机械细节并置，探索一组非写实的未来植物。'),
 ('雾中的构筑物','STRUCTURES IN FOG','通过低对比度光照与局部清晰细节，研究建筑在雾中的层次和方向感。'),
 ('异星室内','OTHERWORLD INTERIOR','在熟悉的房间比例中引入陌生材质，测试空间尺度与感知的变化。'),
 ('光谱实验','SPECTRAL STUDIES','以折射、色散与透明材料形成连续影像，比较静态首帧和动态形变的关系。'),
 ('未建成的未来','UNBUILT FUTURES','为尚未建造的空间制作概念气氛图，探索视觉叙事与设计意图的对应。')]),
 ('建筑设计','ARCHITECTURE','architecture','Rhino · Grasshopper · 建筑表达',[
 ('间庭美术馆','COURTYARD MUSEUM','围绕一处下沉庭院组织展厅、回廊与公共空间，让自然光成为参观动线的节奏。'),
 ('山地阅读所','HILLSIDE LIBRARY','以顺应等高线的错层体量减少场地扰动，在坡地中形成连续阅读空间。'),
 ('城市缝隙','URBAN INFILL','在紧凑街区的空隙中插入共享工作与公共活动空间，研究新旧建筑的连接。'),
 ('光井住宅','LIGHTWELL HOUSE','利用内院和垂直光井改善进深较大的居住空间，平衡开放与私密。'),
 ('滨水文化站','WATERFRONT STATION','把屋顶、步道与公共看台组合成滨水界面，让建筑连接城市与河岸。'),
 ('可生长的校园','GROWING CAMPUS','使用可重复的教学单元与共享庭院，研究分期建设中的完整空间体验。'),
 ('再生工坊','REGENERATIVE WORKSHOP','保留旧厂房结构并植入新的生产与展览功能，强调材料再利用。'),
 ('雨的屋檐','RAIN PAVILION','以集雨屋面和连廊组织小型公共建筑，让天气变化成为空间的一部分。')]),
 ('室内设计','INTERIOR DESIGN','interior','空间叙事 · 材质 · 灯光',[
 ('静默艺廊','QUIET GALLERY','通过温润木材、连续天光与留白墙面营造安静的展览空间，使观者专注于作品。'),
 ('复合工作室','HYBRID STUDIO','把专注工作、材料试验与小型展示安排在同一开放平面中，以家具界定边界。'),
 ('旧屋新生','HOUSE REIMAGINED','保留旧住宅的时间痕迹，以新的收纳、采光和通行关系适应当代生活。'),
 ('微型剧场','MICRO THEATRE','以可变座席和灯光轨道组织有限面积中的演出、排练与交流。'),
 ('材料图书馆','MATERIAL LIBRARY','通过可触摸样本、抽屉与工作台构成材料研究空间，兼顾展示和使用。'),
 ('云端客厅','SKY LOUNGE','用低矮家具和轻质隔断保持开阔视线，研究高层公共空间的舒适尺度。'),
 ('缓慢的商店','SLOW RETAIL','以曲折但清晰的动线和停留节点，让小型零售空间容纳阅读与交流。'),
 ('光的居所','HOME OF LIGHT','把一天中不同方向的自然光转译为空间分区，建立材质与生活节奏的联系。')]),
 ('景观设计','LANDSCAPE','landscape','地形 · 植物 · 雨洪策略',[
 ('潮汐公园','TIDAL PARK','以阶梯湿地、雨水花园和轻型步桥修复滨水边界，形成可感知水位变化的公共地景。'),
 ('城市绿脉','GREEN CORRIDOR','连接被道路切断的绿地与慢行路径，研究通勤和日常游憩共享的线性空间。'),
 ('雨水花园','RAIN GARDEN','将汇水路径变成可阅读的景观，把蓄水、渗透和植物群落组成连续系统。'),
 ('山谷步道','VALLEY WALK','通过轻触地面的栈道与观景节点组织山谷游览，减少对原有地表的干扰。'),
 ('屋顶森林','ROOFTOP FOREST','在承载条件约束下研究轻量化种植与休憩空间，创造城市上方的绿色层次。'),
 ('四季庭园','SEASONAL GARDEN','用花期、叶色和枝干形态安排四季变化，构成日常可使用的小尺度庭园。'),
 ('废墟花园','RUIN GARDEN','让自生植物与保留的工业构筑物共存，通过路径揭示场地记忆。'),
 ('河岸慢行','RIVERSIDE LOOP','组织步行、骑行与亲水停留节点，让线性河岸成为连续的日常公共空间。')])]
records=[]
for category,en,asset,tools,items in briefs:
 for n,(title,english,abstract) in enumerate(items):
  idx=len(records)+1
  records.append(dict(id=f'X-{idx:03}',title=title,en=english,department=category,category=category,date='概念示例 / 年份待填',lead='个人设计 · 角色待填写',clearance='CONCEPT STUDY',abstract=abstract,findings=[f'01 / 设计起点：{abstract.split("。")[0]}。',f'02 / 方法与工具：{tools}。在真实项目中补充采用的方法、关键参数与个人负责范围。','03 / 过程记录：在此替换调研、草图、迭代对比、空间分析或交互状态图。','04 / 交付与复核：补充最终图纸、影像、模型或实机效果，以及实际完成的验证。当前为占位方案。'],source=f'/projects/X-{idx:03}.md',image=f'/images/{asset}.png',imageAlt=f'{category}占位概念图：{items[0][0]}',tools=tools,placeholder=True))
# Start at VR, at the original camera-centered lane 2.
columns=['建筑设计','室内设计','沉浸式VR展项','AI工作流','生图与视觉实验','景观设计']
content=dict(categories=[b[0] for b in briefs],columns=columns,records=records)
(p/'content/archives.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# All authored text stays independently editable; interaction source remains original.
for rel in ['src/main.ts','src/scene.ts','src/model-viewer.ts','src/boot-motion.ts','index.html','scripts/archive-content.mjs','scripts/export-records.mjs','scripts/check-content.mjs']:
 f=p/rel;s=f.read_text(encoding='utf-8')
 for a,b in [('RHINE-LAB-','SPACE-FIELD-'),('RHINE LAB.LLC.','SPACE / FIELD'),('RHINE LAB, LLC.','SPACE / FIELD'),('RHINE LAB','SPACE / FIELD'),('RHINE·LAB','SPACE·FIELD'),('Rhine Lab — Synthesize Information Analysis OS. 交互式三维研究档案终端。','间构 SPACE / FIELD，建筑设计与 VR 技术美术的综合设计个人作品集。'),('ANALYSIS OS','DESIGN ARCHIVE'),('INTERNAL DATABASE','SELECTED WORKS'),('JOYCE MOORE','VISITOR / 访客'),('莱茵生命内部资料档案','间构设计作品档案'),('莱茵生命','零重力档案馆'),('rhine-saved','space-field-saved'),('rhine-settings','space-field-settings')]:s=s.replace(a,b)
 f.write_text(s,encoding='utf-8')
# New identity uses an architectural frame mark in the same animation geometry slots.
(p/'src/brand.ts').write_text('''const paths = `<path d="M25 125V20H135V125M175 125V20H285V125M25 73H135M175 73H285" fill="none" stroke="currentColor" stroke-width="12"/><path d="M69 45v50M219 70h44" fill="none" stroke="currentColor" stroke-width="6"/>`;
export const labelMarkSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 310 145" color="#171713">${paths}</svg>`;
export const logo = `<svg viewBox="0 0 310 185" aria-label="间构 SPACE / FIELD" role="img">${paths}<text x="155" y="174" text-anchor="middle" font-family="MiSans,sans-serif" font-size="16" font-weight="700" letter-spacing="5">SPACE / FIELD</text></svg>`;
export const bootMarkStrokes = ["M25 125V20H135", "M135 20V125M25 73H135", "M175 125V20H285V125M175 73H285"];
export const brandHeading = `<h1>SPACE / FIELD</h1><div>ARCHITECTURE × DIGITAL EXPERIENCE</div><p><span class="brand-analysis">间构 · 设计档案</span> <b>SF</b></p>`;
''',encoding='utf-8')
f=p/'src/boot.ts';s=f.read_text(encoding='utf-8').replace('this.letters.textContent = s.logoLetters;', 'this.letters.textContent = "SPACE / FIELD".slice(0, Math.ceil(s.logoLetters.length * 13 / 9));');f.write_text(s,encoding='utf-8')
f=p/'src/data.ts';s=f.read_text(encoding='utf-8').replace('  source: string;','  source: string;\n  image: string;\n  imageAlt: string;\n  tools: string;\n  placeholder: boolean;');f.write_text(s,encoding='utf-8')
f=p/'src/scene.ts';s=f.read_text(encoding='utf-8').replace('import { fileAtSlot, fileLocation }','import { fileAtSlot, fileLocation, archiveColumns }').replace('Math.round((this.selectedCell.lane - 2) / 5) * 5','Math.round((this.selectedCell.lane - 2) / archiveColumns.length) * archiveColumns.length');f.write_text(s,encoding='utf-8')
f=p/'scripts/archive-content.mjs';s=f.read_text(encoding='utf-8').replace('names.length !== 5','names.length !== 6').replace('new Set(names).size !== 5','new Set(names).size !== 6').replace('五个','六个').replace('records.length !== 40','records.length !== 48').replace('四十份','四十八份')
s=s.replace('const url = new URL(record.source);','const url = new URL(record.source, "https://portfolio.local");\n      if (!record.source.startsWith("/projects/") && !/^https?:\\/\\//.test(record.source)) throw new Error();')
a=s.index('export function archiveText(r)');s=s[:a]+'''export function archiveText(r) {
  return `\\uFEFFSPACE / FIELD · 设计作品档案\\nPROJECT ${r.id} / ${r.title}\\n${r.en}\\n\\n分类：${r.category}\\n时间：${r.date}\\n个人角色：${r.lead}\\n工具：${r.tools}\\n状态：概念占位，非真实项目履历\\n\\n${r.abstract}\\n\\n设计过程\\n${r.findings.map((f) => f).join("\\n")}\\n\\n本档案与图像为可替换的作品集示例。\\n`;
}
''';f.write_text(s,encoding='utf-8')
f=p/'scripts/check-content.mjs';s=f.read_text(encoding='utf-8').replace('all forty','all forty-eight').replace('四十份','四十八份').replace('五个','六个');f.write_text(s,encoding='utf-8')
f=p/'scripts/check-loop.mjs';s=f.read_text(encoding='utf-8').replace('columnFiles, fileLocation','columnFiles, fileLocation, archiveColumns').replace('wrap(lane, 5)','wrap(lane, archiveColumns.length)').replace('length: 5','length: archiveColumns.length').replace('wrap(lane + direction, 5)','wrap(lane + direction, archiveColumns.length)');f.write_text(s,encoding='utf-8')
f=p/'src/main.ts';s=f.read_text(encoding='utf-8')
for a,b in [('ARCHIVE INDEX','项目索引'),('ENTER SYSTEM','进入作品档案'),('ARCHIVE OVERVIEW','返回作品阵列'),('ACCESS FILE','抽取项目档案'),('FILE NUMBER:','PROJECT FILE:'),('ARCHIVE / SELECT','PROJECT / SELECT'),(' / 05',' / 06'),('机构档案','沉浸式VR展项'),('DEPARTMENT / 科室','DISCIPLINE / 设计领域'),('COLLECTION / 编目范围','YEAR / 项目时间'),('RELATED / 相关人物','ROLE / 个人职责'),('研究记录','设计过程'),('RESEARCH NOTES','DESIGN PROCESS'),('设定参考 ↗','独立项目文档 ↗'),('内部档案检索','跨领域项目索引'),('科室','设计领域'),('已归档 · 可读取','概念占位 · 可替换'),('本次会话已通过身份验证。档案内容以当前终端可访问范围展示。','仅记录本次浏览。当前作品和图像为占位示例，后续可替换为真实项目。'),('PERMISSION AUTHORIZED','PORTFOLIO CONNECTED'),('SESSION AUTHORIZED','PORTFOLIO / CONCEPT EDITION'),('READ AUTHORIZED','PROJECT OPENED')]:s=s.replace(a,b)
s=s.replace('import "./style.css";', 'import "./style.css";\nimport "./portfolio.css";')
s=s.replace('<section id="archive-ui" class="archive-ui" aria-label="档案选择">','''<section id="archive-ui" class="archive-ui" aria-label="档案选择">
    <div class="portfolio-intro"><span>INDEPENDENT DESIGNER / 综合设计个人作品集</span><h2>空间，及其可能。</h2><p>建筑设计 · VR 技术美术 · AI 视觉探索</p><small>48 PROJECT STUDIES / 概念占位集</small></div>
    <nav class="discipline-nav" aria-label="作品分类">${archiveColumns.map((name,lane)=>`<button data-lane="${lane}"><span>${String(lane+1).padStart(2,"0")}</span>${escapeHtml(name)}</button>`).join("")}</nav>''')
s=s.replace('<div class="archive-hint">','<div class="archive-hint">')
s=s.replace('<div class="detail-rule"></div>', '<div class="detail-rule"></div>')
s=s.replace('function overview() {\n  return `<div class="panel-label">ABSTRACT / 摘要</div><p>${escapeHtml(records[selected].abstract)}</p>`;\n}', '''function overview() {
  const r = records[selected];
  return `<figure class="project-figure"><a href="${escapeHtml(r.image)}" target="_blank" rel="noopener" aria-label="查看项目示意图大图"><img src="${escapeHtml(r.image)}" alt="${escapeHtml(r.imageAlt)}" width="1600" height="900" /></a><figcaption>CONCEPT IMAGE / 占位概念图 <span>${escapeHtml(r.category)}</span></figcaption></figure><div class="panel-label">PROJECT BRIEF / 项目概述</div><p>${escapeHtml(r.abstract)}</p><div class="project-tools">${escapeHtml(r.tools)}</div>`;
}''')
s=s.replace('  const scale = Math.min(innerWidth / 1920, innerHeight / 1080);', '  const portrait = innerWidth < 760 && innerHeight > innerWidth;\n  document.documentElement.classList.toggle("portrait", portrait);\n  const scale = portrait ? 1 : Math.min(innerWidth / 1920, innerHeight / 1080);')
s=s.replace('  if (el.dataset.select) {','  if (el.dataset.lane !== undefined) {\n    if (ready && mode === "archive" && !modal) select(columnMemory[Number(el.dataset.lane)]);\n    return;\n  }\n  if (el.dataset.select) {')
s=s.replace('  columnTitle.update({ text: archiveColumns[lane]', '  document.querySelectorAll<HTMLButtonElement>("[data-lane]").forEach(button => { button.classList.toggle("active", Number(button.dataset.lane) === lane); button.setAttribute("aria-pressed", String(Number(button.dataset.lane) === lane)); });\n  columnTitle.update({ text: archiveColumns[lane]')
s=s.replace('  rhine: {','  spatialArchive: {')
s=s.replace('if (action === "skip") {','if (action === "skip" && ready) {')
f.write_text(s,encoding='utf-8')
# Standalone source documents and downloads are produced from the same content.
f=p/'scripts/export-records.mjs';s=f.read_text(encoding='utf-8');s+='''
const projectOutput = new URL("../public/projects/", import.meta.url);
await fs.mkdir(projectOutput, { recursive: true });
for (const r of records) {
  const markdown = `# ${r.title}\\n\\n${r.en} · ${r.id}\\n\\n> 概念占位项目，图像为 AI 生成示意，不代表真实委托或已建成作品。\\n\\n![${r.imageAlt}](../images/${r.image.split("/").pop()})\\n\\n- 分类：${r.category}\\n- 时间：${r.date}\\n- 个人职责：${r.lead}\\n- 工具：${r.tools}\\n\\n## 项目概述\\n\\n${r.abstract}\\n\\n## 设计过程\\n\\n${r.findings.join("\\n\\n")}\\n`;
  await fs.writeFile(new URL(`${r.id}.md`, projectOutput), markdown, "utf8");
}
''';f.write_text(s,encoding='utf-8')
(p/'public/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#e8e5e1"/><path d="M12 51V13H29V51M35 51V13H52V51M12 33H29M35 33H52" fill="none" stroke="#171713" stroke-width="4"/></svg>',encoding='utf-8')
(p/'content/替换指南.md').write_text('''# 作品集内容替换指南

网站暂名「间构 SPACE / FIELD」，可在 src/brand.ts 与 index.html 修改。

## 改项目

编辑 content/archives.json。每份项目对应一个 records 条目，48 份示例分属六类，每类八份。保留 id 和顺序可维持收藏兼容。title 为中文名，en 为英文名，category 为分类，date 为时间，lead 为个人职责，abstract 为概述，findings 为设计过程，tools 为工具，image 为图片路径。纯文本会自动转义，不在文本中写 HTML。

## 换图片

六张 AI 生成占位图在 public/images。每类八份示例暂共用一张图。可直接替换同名图片，也可以新增单项目图片并更新 image，例如 /images/X-001.jpg。推荐横向 16:9。imageAlt 同时改成对应项目描述。

## 独立文档

每次运行 npm run dev 或 npm run build，都从 JSON 自动生成 public/projects/X-001.md 等 48 份项目文档，以及 public/archives/SPACE-FIELD-X-001.txt 等 48 份文本下载。不要只改自动生成的文档，下一次构建会覆盖它们。

## 分类与扩展

categories 控制索引筛选顺序，columns 控制三维阵列列顺序。目前六类为沉浸式 VR 展项、AI 工作流、生图与视觉实验、建筑设计、室内设计、景观设计。「深图」暂按生图理解，可同时修改 categories、columns 和相关 records 的 category。改变每列数量需同步调整内容校验与导航刻度。

## 状态

所有项目均为占位概念，不含真实客户、面积、预算、奖项或落地业绩。替换真实项目后同步更新日期、职责与占位状态文案。

## 来源

交互实现改编自 LBEILC/RhineLabUI，保留 LICENSE、原工程资料与第三方许可。三维档案盒模型用于复刻体验；正式品牌替换时可进一步制作独立模型资产。
''',encoding='utf-8')
print('Authored 48 project records, six categories, portfolio identity and document export.')
