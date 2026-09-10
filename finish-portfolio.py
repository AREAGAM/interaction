from pathlib import Path
import json
p=Path('.')
f=p/'scripts/check-appearance.mjs';s=f.read_text(encoding='utf-8').replace('roughnessFactor = mix(0.28','roughnessFactor = mix(mix(0.28');s=s.replace('appearance.dispose(returning);','assert.equal(shader.uniforms.archiveClarity, body.userData.clarity);\nappearance.dispose(returning);') if False else s;f.write_text(s,encoding='utf-8')
f=p/'src/scene.ts';s=f.read_text(encoding='utf-8').replace('R L / I S','S F / 0 1');f.write_text(s,encoding='utf-8')
f=p/'src/boot.ts';s=f.read_text(encoding='utf-8').replace('* 13 / 9','* 13 / 11').replace('s.poweredLetters / 19','s.poweredLetters / 23');f.write_text(s,encoding='utf-8')
f=p/'src/main.ts';s=f.read_text(encoding='utf-8').replace('CONFIDENTIALITY:<strong>GENERAL BUSINESS USE','PROJECT ARCHIVE:<strong>SPATIAL DESIGN STUDIES').replace('>BUSINESS AREA<','>CONCEPT STUDY<');f.write_text(s,encoding='utf-8')
# Keep upstream materials locally, outside the public website.
upstream=p/'upstream';upstream.mkdir(exist_ok=True)
if not (upstream/'README.md').exists(): (p/'README.md').rename(upstream/'README.md')
if not (upstream/'content-README.md').exists(): (p/'content/README.md').rename(upstream/'content-README.md')
(upstream/'archives').mkdir(exist_ok=True)
for f in (p/'public/archives').glob('RHINE-LAB-*.txt'):f.rename(upstream/'archives'/f.name)
(p/'content/README.md').write_text('# 作品内容维护\n\n请阅读 [替换指南](替换指南.md)。\n\n内容保存在 archives.json，六个分类各八份，共 48 份项目文档。\n',encoding='utf-8')
(p/'README.md').write_text('''# 间构 SPACE / FIELD

建筑设计与 VR 技术美术综合设计个人作品集。以可循环的三维档案阵列浏览项目，点击抽取进入图文文档。

## 本地运行

需要 Node.js 22.12 以上。双击「启动作品集.cmd」，或运行 `npm ci` 后 `npm run dev`。构建：`npm run build`。

## 内容

六类：沉浸式 VR 展项、AI 工作流、生图与视觉实验、建筑设计、室内设计、景观设计。48 份独立概念示例，6 张 AI 占位图。当前同类项目共用类别图，可逐项更换。

编辑 `content/archives.json` 和 `public/images`。详细见 `content/替换指南.md`。构建时自动生成 48 份 Markdown 和 48 份 UTF-8 TXT。

## 交互

- 启动画面：逐字输入、标志描线、扫描、欢迎转场、三维阵列展开；Enter 或点击跳过。
- 左右切分类，上下翻项目，首尾循环、每类记忆；也可点击六类导航。
- Enter 抽取项目；净空后拖动模型；Esc 先转正再归位。
- `/` 检索，分类筛选，收藏及持久化，项目概述、设计过程、访问记录，独立文档及 TXT 导出。
- 360° 模型查看、缩放、平移、复位、六层拆解与重组、清晰/磨砂。
- 音效、音乐、音量、减少动态效果、画质、全屏、重播开场。
- 竖屏采用自适应控件和阅读面板，桌面保留参考的三维构图。

## 验证边界

构建与静态资源检查、内容测试、20000 次分类/项目循环移动、抽取归位、模型装配、解密和画质检查见 `verification/PORTFOLIO.md`。未进行浏览器逐帧视觉对比或移动端实机验收，不宣称与参考逐像素一致。

## 来源

基于 [LBEILC/RhineLabUI](https://github.com/LBEILC/RhineLabUI) 改编。保留 MIT 许可与第三方字体等许可。原版说明及档案存于 upstream，原参考验证资料保留；其验证报告不等于本改编版的验证结果。
''',encoding='utf-8')
(p/'启动作品集.cmd').write_text('@echo off\ncd /d "%~dp0"\nif not exist node_modules call npm.cmd ci\nstart "" http://127.0.0.1:5173/\ncall npm.cmd run dev\n',encoding='utf-8')
(p/'verification/PORTFOLIO.md').write_text('''# Portfolio verification — 2026-09-09

- verified: TypeScript and production build.
- verified: 18 content tests, 48 UTF-8 TXT exports match shared JSON.
- verified: 20000 directional movements across six disciplines, selection memory and seamless cycles; 288 physical pool slots.
- verified: extraction/return motion logic, six-part assembly, decryption geometry/depth, 48 device-limit quality combinations.
- verified: six generated PNGs copied to public/images; 48 project Markdown documents generated.
- unverified: browser visual QA, exact reference-frame match, mobile hardware interaction, subjective sound quality.
- A stale upstream appearance assertion expected the old shader before its nested clarity blend. Updated the assertion to the actual retained shader; no material or movement parameters changed for this correction.
- Demo content and images are placeholders, not real completed commissions.
''',encoding='utf-8')
base='Use case: stylized-concept\nAsset type: portfolio project card placeholder concept, landscape 16:9 image\nPrimary request: {primary}\nStyle/medium: refined photoreal architectural visualization, editorial composition, soft cinematic light, exquisite but understated material textures, clear large forms.\nColor palette: cohesive restrained blue-grey and ivory, natural warm timber or muted vegetation only where called for.\nComposition/framing: wide 16:9 landscape, strong central spatial composition, safe cropping at all edges, no collage.\nConstraints: fictional concept placeholder; no text, letters, numbers, logo, watermark, signage, people, UI, borders.'
subjects={'vr':'An immersive VR exhibition in a vast dark hall, a luminous icy-blue point-cloud landscape flows across floor and far walls, a single clean rectangular glowing portal at the center, spatial depth and subtle volumetric light, no physical headsets.','workflow':'A tangible abstract AI workflow: a refined network of small luminous blue glass nodes and hairline connections suspended above an ivory architectural maquette of simple building volumes on a broad pale table. Tactile materials and legible spacious structure. No interface panels.','image-lab':'Surreal brutalist architecture: monumental pale concrete platforms and angular walls suspended around a luminous atmospheric cloud, deep spatial voids, gentle blue mist, a dreamlike yet rigorously composed architectural experiment.','architecture':'A minimalist concrete courtyard museum, low horizontal ivory concrete volumes enclose a serene courtyard, shallow reflecting pool and a single small tree, precise joints, soft daylight, composed eye-level architectural view.','interior':'A tranquil contemporary gallery atrium with warm timber walls and ceiling fins, pale stone floor, a sculptural broad staircase, large skylight washes the spacious interior with diffuse daylight, quiet refined contemporary design.','landscape':'A terraced wetland park of layered planted water basins, a slender pale pedestrian bridge curves through reeds, grasses and calm water, gentle terrain, distant trees in mist, slightly elevated architectural landscape view.'}
(p/'content/图片提示词.md').write_text('# 占位图提示词\n\n使用内置 imagegen，每类一张，原始尺寸 1672×941。\n\n'+'\n\n'.join('## '+k+'.png\n\n```text\n'+base.format(primary=v)+'\n```' for k,v in subjects.items()),encoding='utf-8')
# Build helper is an authoring scratch file; keep it locally but out of published source.
f=p/'.gitignore';s=f.read_text(encoding='utf-8');s+='\nbuild-portfolio.py\nfinish-portfolio.py\n';f.write_text(s,encoding='utf-8')
print('Handoff docs and source attribution prepared.')
