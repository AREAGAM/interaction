import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
export type LightingLook = "baseline" | "refined";
// Neutral studio reflections reveal the black/silver shell. Green is a rim accent.
export function createArchiveLighting(renderer: THREE.WebGLRenderer, scene: THREE.Scene, _look: LightingLook = "baseline") {
  renderer.toneMappingExposure = 1.08;
  const pmrem = new THREE.PMREMGenerator(renderer);
  const room = new RoomEnvironment();
  scene.environment = pmrem.fromScene(room, .035).texture;
  room.dispose(); pmrem.dispose();
  scene.environmentIntensity = .28;
  scene.add(new THREE.HemisphereLight("#e4ece6", "#000000", .12));
  const key = new THREE.DirectionalLight("#f5fff6", 3.1);
  key.position.set(-6, 14, -5);
  const fill = new THREE.DirectionalLight("#c4d4cb", .18);
  fill.position.set(7, 8, -10);
  const rim = new THREE.DirectionalLight("#b6ff00", .38);
  rim.position.set(8, 3, 7);
  scene.add(key, fill, rim);
  return key;
}
