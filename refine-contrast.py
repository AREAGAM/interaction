from pathlib import Path
import shutil
p=Path('.')
backup=p/'backups/blackline-before-contrast';backup.mkdir(parents=True,exist_ok=True)
for name in ['blackline.css','blackline-materials.ts','archive-lighting.ts','scene.ts','model-viewer.ts','appearance.ts','quality-renderer.ts']:
 if not (backup/name).exists():shutil.copy2(p/'src'/name,backup/name)
f=p/'src/blackline-materials.ts';s=f.read_text(encoding='utf-8').replace('envMapIntensity = 1.15','envMapIntensity = .72')
for a,b in [('#454e49','#111813'),('#87918a','#414c43'),('array ? .36 : .18','array ? .22 : .12'),('array ? .24 : .56','array ? .12 : .42'),('array ? .32 : .22','array ? .22 : .16'),('clearcoatRoughness = .22','clearcoatRoughness = .12'),('#7e8881','#78847a'),('#bcc6c0','#d3ddd5'),('.25, .9','.14, .96'),('#171f1b','#030704'),('#111814','#020503'),('#252e28','#09110b'),('#505e54','#28392b'),('#111a13','#020603'),('#58665d','#26382a')]:s=s.replace(a,b)
s=s.replace('case "Champagne_Index": steel(array ? "#829361" : "#baff48", .36, .55); break;', '''case "Champagne_Index":
      steel("#b6ff00", .22, .18);
      material.emissive.set("#99ff00"); material.emissiveIntensity = array ? .85 : 1.6;
      break;''')
s=s.replace('steel("#b7ff3b", .28, .22)','steel("#b6ff00", .18, .1)').replace('material.emissive.set("#89e52b"); material.emissiveIntensity = .32','material.emissive.set("#9dff00"); material.emissiveIntensity = 2.4')
f.write_text(s,encoding='utf-8')
f=p/'src/archive-lighting.ts';s=f.read_text(encoding='utf-8').replace('environmentIntensity = .72','environmentIntensity = .28').replace('"#0a140d", .62','"#000000", .12').replace('"#eef5f1", 2.35','"#f5fff6", 3.1').replace('"#c4d4cb", .85','"#c4d4cb", .18').replace('"#bcff48", .32','"#b6ff00", .8');f.write_text(s,encoding='utf-8')
(p/'src/fluorescence.ts').write_text('''import { Vector2 } from "three";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
// Only HDR highlights bloom: shadows and normal text keep a clean black floor.
export const createFluorescence = () => new UnrealBloomPass(new Vector2(1, 1), .48, .22, 1.05);
''',encoding='utf-8')
f=p/'src/scene.ts';s=f.read_text(encoding='utf-8');s='import { createFluorescence } from "./fluorescence";\n'+s
s=s.replace('"#080c09"','"#000000"').replace('color: "#0b110d", roughness: 0.78, metalness: 0.3','color: "#010302", roughness: 0.96, metalness: 0.05')
s=s.replace('this.composer.addPass(new OutputPass());','this.composer.addPass(createFluorescence());\n    this.composer.addPass(new OutputPass());')
s=s.replace('c.fillStyle = "#101812"','c.fillStyle = "#010402"').replace('c.fillStyle = "#baff48"','c.fillStyle = "#b6ff00"')
f.write_text(s,encoding='utf-8')
f=p/'src/quality-renderer.ts';s=f.read_text(encoding='utf-8');s='import { createFluorescence } from "./fluorescence";\n'+s;s=s.replace('composer.addPass(new OutputPass());','composer.addPass(createFluorescence());\n  composer.addPass(new OutputPass());');f.write_text(s,encoding='utf-8')
f=p/'src/model-viewer.ts';s=f.read_text(encoding='utf-8').replace('"#080c09"','"#000000"').replace('if (this.quality.antialias === "smaa") this.pipeline.composer.render();\n    else this.renderer.render(this.scene, this.camera);','this.pipeline.composer.render();');f.write_text(s,encoding='utf-8')
f=p/'src/appearance.ts';s=f.read_text(encoding='utf-8').replace('mat.color.copy(low.color).lerp(high.color, value);','mat.color.copy(low.color).lerp(high.color, value);\n      mat.emissive.copy(low.emissive).lerp(high.emissive, value);\n      mat.emissiveIntensity = THREE.MathUtils.lerp(low.emissiveIntensity, high.emissiveIntensity, value);');f.write_text(s,encoding='utf-8')
f=p/'src/blackline.css';s=f.read_text(encoding='utf-8-sig').replace('--signal:#bdff3c','--signal:#b6ff00').replace('--surface:#0b100d','--surface:#020403').replace('#080c09','#000000')
s+='''
/* Contrast revision: true black surfaces, crisp fluorescent signals. */
:root,body,#viewport,#stage,.loading,.model-viewer,.boot-background,.boot-white,.welcome-panel { background:#000; }
.scene-atmosphere { background:linear-gradient(180deg,#000 0%,rgba(0,0,0,.8) 12%,transparent 42%),linear-gradient(0deg,#000 0%,transparent 22%); }
.archive-atmosphere::before { background:linear-gradient(180deg,rgba(0,0,0,.65),transparent 40%); }
.archive-atmosphere::after { background:linear-gradient(90deg,transparent 40%,rgba(0,0,0,.25) 58%,rgba(0,0,0,.97) 73%,#000); mask-image:none; }
.brand h1,.portfolio-intro h2,.detail-content h2,.terminal-modal h2 { color:#f6fff3; }
.brand > p > b,.portfolio-intro small,.file-open,.read-file,.viewer-open,.export-button,.skip,.detail-kicker,.viewer-state { color:var(--signal); }
#selected-id,#selected-number,#column-index,.discipline-nav button.active,.detail-tabs button.active,.result-name b { color:var(--signal); text-shadow:0 0 5px #b6ff0060,0 0 18px #9dff0038; }
.brand::before,.status-light,.file-ticks button.selected::before,.tab-indicator,.auth-status i,.loading > i::after { background:var(--signal); box-shadow:0 0 6px #b6ff0090,0 0 17px #a4ff0045; }
.discipline-nav button.active { border-color:var(--signal); }
#selected-title,.file-title,.column-navigation strong,.metadata dd,.detail-title-cn { color:#efffeb; }
#selected-clearance,.panel-label,.project-tools,.detail-kicker span:last-child { color:#b7e987; }
.portfolio-intro p,.tab-panel p,.research-notes li { color:#ccddc9; }
.discipline-nav,.system-footer,.detail-tabs,.project-tools,.result-header,.result-row { border-color:#1e3120; }
.read-file,.solid-button,.viewer-actions button,.category-filters button,select { background:#020702; border-color:#47740c; }
.read-file:hover,.solid-button:hover,.viewer-actions button:hover { background:#0b1801; border-color:var(--signal); box-shadow:0 0 14px #a6ff001b; }
.solid-button[aria-pressed="true"],.viewer-actions button[aria-pressed="true"] { background:#071401; border-color:var(--signal); }
.category-filters button.active,.viewer-surface button[aria-pressed="true"] { background:var(--signal); color:#020900; box-shadow:0 0 14px #a4ff0030; }
.terminal-modal,.portrait .terminal-modal { background:rgba(0,2,0,.99); border-color:#2c451c; border-top-color:var(--signal); }
.modal-backdrop { background:rgba(0,0,0,.85); }
.hover-label,.portrait .archive-callout { background:rgba(0,3,0,.97); border-color:#3e5e22; }
.project-figure a { background:#000; }
.result-row:hover { background:#071101; }
.toggle { background:#172315; }
.settings-list input:checked + .toggle { background:var(--signal); box-shadow:0 0 12px #9dff0026; }
.settings-list input:checked + .toggle::after { background:#020700; }
#inspection-lines { stroke:var(--signal); filter:drop-shadow(0 0 3px #b6ff00aa) drop-shadow(0 0 9px #9dff0055); }
#inspection-point { fill:var(--signal); filter:drop-shadow(0 0 5px #b6ff0099); }
.loading-mark,.boot-logo,.welcome-logo { color:var(--signal); filter:drop-shadow(0 0 10px #a6ff0030); }
.scan > span { color:var(--signal); text-shadow:0 0 10px #a6ff0050; }
.viewer-index { color:#274018; }
''';f.write_text(s,encoding='utf-8')
f=p/'index.html';s=f.read_text(encoding='utf-8').replace('content="#080c09"','content="#000000"');f.write_text(s,encoding='utf-8')
print('Contrast and fluorescence updated; previous theme settings backed up locally.')
