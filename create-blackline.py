from pathlib import Path
import re,json
p=Path('.')
# Recolor CSS at the property level, retaining layout and every animation.
def recolor_value(prop,value):
 def hexmap(m):
  raw=m.group()[1:]; raw=''.join(c*2 for c in raw) if len(raw)==3 else raw
  rgb=raw[:6]; alpha=raw[6:]
  if len(rgb)!=6:return m.group()
  r,g,b=[int(rgb[i:i+2],16) for i in (0,2,4)]; light=(r+g+b)/3
  if prop in ['color','fill']:
   out='e6ede7' if light<105 or light>215 else '9aa89f'
  elif 'background' in prop:
   out='090d0b' if light>150 else '202922'
  elif prop in ['stroke']:
   out='b6f549' if light<130 else '485b4c'
  else:out='344438'
  return '#'+out+alpha
 value=re.sub(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b',hexmap,value)
 value=re.sub(r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*([\d.]+)\)',r'rgba(6, 11, 8, \1)',value)
 return value
for f in (p/'src').glob('*.css'):
 s=f.read_text(encoding='utf-8-sig')
 s=re.sub(r'([\w-]+)\s*:\s*([^;{}]+);',lambda m:m[1]+': '+recolor_value(m[1],m[2])+';',s)
 f.write_text(s,encoding='utf-8')
f=p/'src/main.ts';s=f.read_text(encoding='utf-8')
s=s.replace('import "./quality-settings.css";','import "./quality-settings.css";\nimport "./blackline.css";')
s=s.replace('space-field-saved','space-field-blackline-saved').replace('space-field-settings','space-field-blackline-settings')
s=s.replace('48 PROJECT STUDIES / 概念占位集','BLACKLINE / 02 · 48 PROJECT STUDIES').replace('PORTFOLIO / CONCEPT EDITION','BLACKLINE / LOCAL EDITION')
s=s.replace('stroke="#fff"','stroke="#8fbc52"').replace('stroke="#080a08"','stroke="#c0ff40"').replace('fill="#ed821b"','fill="#bcff3b"').replace('fill="#080a08"','fill="#bcff3b"')
s=s.replace('{ backgroundColor: "#67634c" }, { backgroundColor: "#252820" }','{ backgroundColor: "#425829" }, { backgroundColor: "#18221b" }')
f.write_text(s,encoding='utf-8')
f=p/'src/brand.ts';s=f.read_text(encoding='utf-8').replace('color="#171713"','color="#c0ff48"').replace('<b>SF</b>','<b>02</b>');f.write_text(s,encoding='utf-8')
f=p/'src/boot.ts';s=f.read_text(encoding='utf-8').replace('["#080a08", "#fff"]','["#bcff3b", "#27372a"]')
s=s.replace('`blur(${s.exitBlur}px) invert(${s.exit * 0.22}) sepia(${s.exit}) saturate(${1 + s.exit * 5}) hue-rotate(${s.exit * 115}deg)`','`blur(${s.exitBlur}px)`')
s=s.replace('`rgb(${255 * (1 - s.welcomeInk)} ${255 * (1 - s.welcomeInk)} ${255 * (1 - s.welcomeInk)})`','s.welcomeInk > 0.5 ? "#bcff3b" : "#eef5ec"')
f.write_text(s,encoding='utf-8')
# A single shared material palette also drives the independent model viewer.
(p/'src/blackline-materials.ts').write_text('''import * as THREE from "three";
export function blacklineMaterial(material: THREE.MeshPhysicalMaterial, name: string, array = false) {
  material.envMapIntensity = 1.15;
  material.emissive?.set("#000000");
  material.emissiveIntensity = 0;
  const steel = (color: string, roughness: number, metalness = .85) => {
    material.color.set(color); material.roughness = roughness;
    material.metalness = metalness; material.transmission = 0;
  };
  switch (name) {
    case "Frosted_Polymer":
      material.color.set(array ? "#454e49" : "#87918a");
      material.metalness = array ? .36 : .18;
      material.transmission = array ? .24 : .56;
      material.thickness = array ? .18 : .085;
      material.roughness = array ? .32 : .22;
      material.attenuationColor.set("#a7b8aa"); material.attenuationDistance = 2.8;
      material.clearcoat = .55; material.clearcoatRoughness = .22;
      break;
    case "Ivory_Edges": steel(array ? "#7e8881" : "#bcc6c0", .25, .9); break;
    case "Titanium_Fasteners": steel("#ccd4cf", .19, .98); break;
    case "Internal_Ceramic": steel("#171f1b", .55, .48); break;
    case "Optical_Diffuser": steel(array ? "#111814" : "#252e28", .48, .58); break;
    case "Subsurface_Optics": steel("#505e54", .32, .72); break;
    case "Optical_Edges": steel("#9caea1", .2, .88); break;
    case "Printed_Label": steel("#111a13", .65, .08); break;
    case "Champagne_Index": steel(array ? "#829361" : "#baff48", .36, .55); break;
    case "Amber_Lightguide":
      steel("#b7ff3b", .28, .22);
      material.emissive.set("#89e52b"); material.emissiveIntensity = .32;
      break;
    default: steel("#58665d", .36, .68);
  }
}
''',encoding='utf-8')
f=p/'src/scene.ts';s=f.read_text(encoding='utf-8')
s='import { blacklineMaterial } from "./blackline-materials";\n'+s
s=s.replace('"#eae5e1"','"#080c09"').replace('color: "#d8c9b9", roughness: 0.95','color: "#0b110d", roughness: 0.78, metalness: 0.3')
s=s.replace('      const selectedMesh = new THREE.Mesh(geom, mat);','      blacklineMaterial(mat, name);\n      const selectedMesh = new THREE.Mesh(geom, mat);')
s=s.replace('      this.appearance.register(name, mat, arrayMat);','      blacklineMaterial(arrayMat, name, true);\n      this.appearance.register(name, mat, arrayMat);')
s=s.replace('vec3(0.40, 0.30, 0.20), vec3(1.0, 0.98, 0.94)','vec3(0.32, 0.37, 0.34), vec3(0.91, 0.98, 0.94)')
s=s.replace('c.fillStyle = "#e6e2d9"','c.fillStyle = "#101812"').replace('c.fillStyle = "#171713"','c.fillStyle = "#d0dbd2"').replace('c.fillStyle = "#878476"','c.fillStyle = "#8a9b8c"').replace('c.fillStyle = "#eee9de"','c.fillStyle = "#131d13"')
s=s.replace('    c.font = "bold 130px MiSans";','    c.fillStyle = "#baff48";\n    c.font = "bold 130px MiSans";')
s=s.replace('c.fillText("S F / 0 1",','c.fillText("B L / 0 2",')
f.write_text(s,encoding='utf-8')
f=p/'src/appearance.ts';s=f.read_text(encoding='utf-8').replace('vec3(0.40, 0.30, 0.20), vec3(1.0, 0.98, 0.94)','vec3(0.32, 0.37, 0.34), vec3(0.91, 0.98, 0.94)');f.write_text(s,encoding='utf-8')
f=p/'src/model-viewer.ts';s=f.read_text(encoding='utf-8').replace('"#eae5e1"','"#080c09"');f.write_text(s,encoding='utf-8')
(p/'src/archive-lighting.ts').write_text('''import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
export type LightingLook = "baseline" | "refined";
// Neutral studio reflections reveal the black/silver shell. Green is a rim accent.
export function createArchiveLighting(renderer: THREE.WebGLRenderer, scene: THREE.Scene, _look: LightingLook = "baseline") {
  renderer.toneMappingExposure = 1.08;
  const pmrem = new THREE.PMREMGenerator(renderer);
  const room = new RoomEnvironment();
  scene.environment = pmrem.fromScene(room, .035).texture;
  room.dispose(); pmrem.dispose();
  scene.environmentIntensity = .72;
  scene.add(new THREE.HemisphereLight("#e4ece6", "#0a140d", .62));
  const key = new THREE.DirectionalLight("#eef5f1", 2.35);
  key.position.set(-6, 14, -5);
  const fill = new THREE.DirectionalLight("#c4d4cb", .85);
  fill.position.set(7, 8, -10);
  const rim = new THREE.DirectionalLight("#bcff48", .32);
  rim.position.set(8, 3, 7);
  scene.add(key, fill, rim);
  return key;
}
''',encoding='utf-8')
f=p/'index.html';s=f.read_text(encoding='utf-8').replace('#e8e5e1','#080c09').replace('<title>SPACE / FIELD · DESIGN ARCHIVE</title>','<title>SPACE / FIELD — BLACKLINE 02</title>');f.write_text(s,encoding='utf-8')
f=p/'public/favicon.svg';s=f.read_text(encoding='utf-8').replace('#e8e5e1','#080c09').replace('#171713','#baff48');f.write_text(s,encoding='utf-8')
f=p/'package.json';c=json.loads(f.read_text(encoding='utf-8'));c['name']='space-field-blackline';c['scripts']['dev']='vite --host 127.0.0.1 --port 5174 --strictPort';c['scripts']['preview']='vite preview --host 127.0.0.1 --port 4174 --strictPort';f.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=p/'package-lock.json';c=json.loads(f.read_text(encoding='utf-8'));c['name']='space-field-blackline';c['packages']['']['name']='space-field-blackline';f.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=p/'启动作品集.cmd';s=f.read_text(encoding='utf-8').replace('5173','5174');f.write_text(s,encoding='utf-8')
print('Blackline UI, shared material palette, lighting and independent local port configured.')
